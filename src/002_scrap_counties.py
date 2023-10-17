import src.variables    as var
import pandas           as pd
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def main():
    # variables

    # # output files
    consts_links_path = r'\data\raw\001_const_links.csv'
    county_links_path = r'\data\raw\002_county_links.csv'

    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    url = "https://wybory.gov.pl/sejmsenat2023/pl/sejm/wynik/pl"


    links_df = pd.read_csv(path + consts_links_path, delimiter=',')

    # creating list with links
    const_link = links_df["const_link"].tolist()
    const_id = links_df["const_id"].tolist()

    const = dict(zip(const_id, const_link))

    county_df_list =[]

    for id, link in const.items():
        print('okręg', id)
        if id != 19:
            url = link

            session = HTMLSession()
            response = session.get(url)

            # rendering html and waiting for site to load fully
            response.html.render(sleep=1)

            soup = BeautifulSoup(response.html.html, 'html.parser')

            county_ul = soup.find_all('ul', class_="list")
            county_ul = county_ul[0].find_all('ul')
            county_ul = county_ul[0].find_all('ul')
            county_li = county_ul[0].find_all('li')

            const_id_list = []
            county_id_list = []
            county_name_list = []
            county_link_list = []

            for county in county_li:
                # getting a tag with const name and link
                a = county.find("a")
                county_name = a.text
                # const id
                county_id = a['data-id']
                # link to results
                county_link = 'https://wybory.gov.pl' + a['href']
                # appending data
                const_id_list.append(id)
                county_id_list.append(county_id)
                county_name_list.append(county_name)
                county_link_list.append(county_link)
                print(id, county_id, county_name, county_link)

            # zipping lists
            data_tuple = list(zip(const_id_list, county_id_list, county_name_list, county_link_list))

            # creating dataframe
            county_link_df = pd.DataFrame(data_tuple, columns=["const_id", "county_id", "county_name", "county_link"])

            county_df_list.append(county_link_df)
        else:
            pass

    # concatenating dataframes
    county_link_data = pd.concat(county_df_list, axis=0, sort=False)

    print('długość finalnego dataframu:', len(county_link_data.index))

    # # saving dataframe
    county_link_data.to_csv(path + county_links_path, index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()