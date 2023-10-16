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

    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    url = "https://wybory.gov.pl/sejmsenat2023/pl/sejm/wynik/pl"

    session = HTMLSession()
    response = session.get(url)

    # rendering html and waiting for site to load fully
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, 'html.parser')

    consts_ul = soup.find_all('ul', class_="columns3")
    consts_li = consts_ul[0].find_all('li')

    const_id_list = []
    const_name_list = []
    const_link_list = []


    for const in consts_li:
        print(const)
        # getting a tag with const name and link
        a = const.find("a")
        const_name = a.text
        # const id
        const_id = a['data-id']
        # link to results
        const_link = 'https://wybory.gov.pl' + a['href']
        # appending data
        const_id_list.append(const_id)
        const_name_list.append(const_name)
        const_link_list.append(const_link)

    # zipping lists
    data_tuple = list(zip(const_id_list, const_name_list, const_link_list))

    # creating dataframe
    const_link_data = pd.DataFrame(data_tuple, columns=["const_id", "const_name", "const_link"])

    print(const_link_data)

    # saving dataframe
    const_link_data.to_csv(path + consts_links_path, index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()
