import src.variables as var
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
from requests_html import HTMLSession

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # variables
    # season = '2021_2022'
    # round = 'test'
    #
    # # output files
    # # players_links_path = r'\data\raw\ekstraclass\01_players_links_{date}.csv'.format(date=var.time_stamp)
    # players_links_path = r'\data\raw\01_players_links_{s}_round_{r}.csv'.format(s=season, r=round)

    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    url = "https://wybory.gov.pl/sejmsenat2023/pl/obkw/1165194"

    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)

    print(response.html)

    soup = BeautifulSoup(response.html.html, 'html.parser')

    body = soup.find_all('div', class_="col-xs-12 col-xl-6 table-responsive")
    for div in body:
        print(div)
        list = div.find('a')
        print(list.text)
        tbody = div.find('tbody')
        print(tbody)
    #
    # print(soup)
    # body = soup.find_all('div', class_="col-xs-12")
    # site = BeautifulSoup(page, 'html.parser')
    # print(site)

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver.get(var.election_results)
    #
    # html = driver.page_source
    # # print(html)
    # site = BeautifulSoup(html, 'html.parser')
    # # print(site)
    #
    # body = site.find_all('div', class_="col-xs-12")
    # # body = site.find_all('h5')
    # print(body)
    #
    # for div in body:
    #     print(div)

    ite_list =[]
    # # looping throug pagination (only 33 sites)
    # for i in range(34):
    #     # getting the site
    #     html = driver.page_source
    #     site = BeautifulSoup(html, 'html.parser')
    #     # adding site to site_list
    #     site_list.append(site)
    #     # getting the button for the next site
    #     next_button = driver.find_element_by_link_text('Następny')
    #     # going to the next site
    #     next_button.click()
    #
    # # empty lists for values
    # players_list = []
    # links_list = []
    #
    # # looping thgrou sites
    # for site in site_list:
    #     # getting rows form table
    #     table_body = site.find_all('td', class_="sorting_1")
    #     for td in table_body:
    #         # getting a tag with player's name and link
    #         a = td.find("a")
    #         # player name
    #         player = a.text
    #         # link to player's stats
    #         link = 'https://fantasy.ekstraklasa.org' + a['href']
    #         # appending lists
    #         players_list.append(player)
    #         links_list.append(link)
    #
    # # zipping lists
    # data_tuples = list(zip(players_list, links_list))
    #
    # # creating dataframe
    # players_links_df = pd.DataFrame(data_tuples, columns=['player', 'link'])
    #
    # # saving dataframe
    # players_links_df.to_csv(path + players_links_path, index=False, encoding='UTF-8')

    # # shutting down selenium driver
    # driver.quit()

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


