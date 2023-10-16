from pathlib import Path
import datetime as dt

# chrome driver path
chrome_driver = r'C:\Users\Sebastian\Desktop\chromedriver.exe'
# chrome_driver = r'C:\Users\sebas\OneDrive\Pulpit\chromedriver.exe'

# project directory
project_dir = str(Path(__file__).resolve().parents[1])

# ekstraklasa site with players links
election_results = 'https://wybory.gov.pl/sejmsenat2023/pl/obkw/1165194'

# ekstraklasa site with current match scores
ekstraclass_current_match_scores = 'https://ekstraklasa.org/rozgrywki/terminarz/ekstraklasa-4'

# time stamp
today = dt.date.today()
day = today.strftime("%d")
month = today.strftime("%m").upper()
year = today.strftime("%y")
time_stamp = year + "_" + month + "_" + day