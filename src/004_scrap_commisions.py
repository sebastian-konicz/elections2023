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
    muni_links_path = r'\data\raw\003_municipality_links.csv'
    muni_links_path = r'\data\raw\003_municipality_links_short.csv'
    comm_links_path = r'\data\raw\004_commission_links.csv'

    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    links_df = pd.read_csv(path + muni_links_path, delimiter=',')

    # creating list with links
    muni_link = links_df["municipality_link"].tolist()
    muni_id = links_df["municipality_id"].tolist()

    muni = dict(zip(muni_id, muni_link))
    print(muni)

    comm_df_list = []

    for id, link in muni.items():
        print('okręg', id)
        url = link

        session = HTMLSession()
        response = session.get(url)

        # rendering html and waiting for site to load fully
        response.html.render(sleep=1)

        soup = BeautifulSoup(response.html.html, 'html.parser')

        print(soup)

        # comm_ul = soup.find_all('ul', class_="list")
        # comm_ul = comm_ul[0].find_all('ul')
        # comm_ul = comm_ul[0].find_all('ul')
        # comm_ul = comm_ul[0].find_all('ul')
        # comm_li = comm_ul[0].find_all('li')

        print(comm_li)
#         muni_id_list = []
#         comm_id_list = []
#         comm_name_list = []
#         comm_link_list = []
#
#         for comm in comm_li:
#             # getting a tag with const name and link
#             a = comm.find("a")
#             comm_name = a.text
#             # const id
#             comm_id = a['data-id']
#             # link to results
#             comm_link = 'https://wybory.gov.pl' + a['href']
#             # appending data
#             muni_id_list.append(id)
#             comm_id_list.append(comm_id)
#             comm_name_list.append(comm_name)
#             comm_link_list.append(comm_link)
#             print(id, comm_id, comm_name, comm_link)
#
#         # zipping lists
#         data_tuple = list(zip(muni_id_list, comm_id_list, comm_name_list, comm_link_list))
#
#         # creating dataframe
#         comm_link_df = pd.DataFrame(data_tuple, columns=["municipality_id", "commission_id", "commission_name", "commission_link"])
#
#         comm_df_list.append(comm_link_df)
    #
    # # concatenating dataframes
    # comm_link_data = pd.concat(comm_df_list, axis=0, sort=False)
    #
    # print(comm_link_data.head(5))
    # print('długość finalnego dataframu:', len(comm_link_data.index))
    #
    # # # saving dataframe
    # comm_link_data.to_csv(path + comm_links_path, index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()