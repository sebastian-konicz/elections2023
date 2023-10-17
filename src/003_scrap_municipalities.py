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
    county_links_path = r'\data\raw\002_county_links.csv'
    # county_links_path = r'\data\raw\002_county_links_short.csv'
    muni_links_path = r'\data\raw\003_municipality_links.csv'
    county_cities_path = r'\data\raw\003_county_cities_links.csv'

    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    links_df = pd.read_csv(path + county_links_path, delimiter=',')

    # creating list with links
    county_link = links_df["county_link"].tolist()
    county_id = links_df["county_id"].tolist()

    county = dict(zip(county_id, county_link))

    muni_df_list = []
    county_cities_id_list = []

    for id, link in county.items():
        print('powiat', id)
        url = link

        session = HTMLSession()
        response = session.get(url)

        # rendering html and waiting for site to load fully
        response.html.render(sleep=1)

        soup = BeautifulSoup(response.html.html, 'html.parser')

        poland_ul = soup.find_all('ul', class_="list")
        consts_ul = poland_ul[0].find_all('ul')
        county_ul = consts_ul[0].find_all('ul')
        muni_ul = county_ul[0].find_all('ul')
        if len(muni_ul) != 0:
            muni_li = muni_ul[0].find_all('li')

            county_id_list = []
            muni_id_list = []
            muni_name_list = []
            muni_link_list = []

            for muni in muni_li:
                # getting a tag with const name and link
                a = muni.find("a")
                muni_name = a.text
                # const id
                muni_id = a['data-id']
                # link to results
                muni_link = 'https://wybory.gov.pl' + a['href']
                # appending data
                county_id_list.append(id)
                muni_id_list.append(muni_id)
                muni_name_list.append(muni_name)
                muni_link_list.append(muni_link)
                # print(id, muni_id, muni_name, muni_link)

            # zipping lists
            data_tuple = list(zip(county_id_list, muni_id_list, muni_name_list, muni_link_list))

            # creating dataframe
            muni_link_df = pd.DataFrame(data_tuple, columns=["county_id", "municipality_id", "municipality_name", "municipality_link"])

            muni_df_list.append(muni_link_df)

        else:
            county_cities_id_list.append(id)

    # concatenating dataframes
    muni_link_data = pd.concat(muni_df_list, axis=0, sort=False)

    print(muni_link_data.head(5))
    print('długość finalnego dataframu - municipalities:', len(muni_link_data.index))

    county_cities = links_df[links_df.county_id.isin(county_cities_id_list)]

    print(county_cities.head(5))
    print('długość finalnego dataframu - county cities:', len(county_cities.index))

    # # saving dataframes
    muni_link_data.to_csv(path + muni_links_path, index=False, encoding='UTF-8')
    county_cities.to_csv(path + county_cities_path, index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()