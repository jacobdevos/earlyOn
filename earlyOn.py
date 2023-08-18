import webbrowser
import requests
from tabulate import tabulate
import datetime
from pretty_html_table import build_table
from bs4 import BeautifulSoup


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


# The API endpoint
url = "https://www.keyon.ca/en/Events/GetEvents?id=501&startDate=2023-07-30T04%3A00%3A00.000Z&endDate=2023-09-10T04%3A00%3A00.000Z"

# A GET request to the API
response = requests.get(url)

# Print the response
response_json = response.json()

table = [['Start Time', 'End Time', 'Name']]


def get_from_utc_time(epoch_time):
    date = datetime.datetime.fromtimestamp(epoch_time)
    return date


def get_epoch_time_from_earlyon_format(time_str):
    return int(time_str[6:][:-2])/1000


def make_tables_pretty(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all table elements in the HTML
    tables = soup.find_all('table')

    # Apply styling to each table
    for table in tables:
        # Apply styles to the <table> element
        table['style'] = 'border-collapse: collapse; width: 100%;'

        # Apply styles to <th> (table header) elements
        table_headers = table.find_all('th')
        for th in table_headers:
            th['style'] = 'background-color: #f2f2f2; padding: 10px; text-align: left;'

        # Apply styles to <td> (table data) elements
        table_data = table.find_all('td')
        for td in table_data:
            td['style'] = 'padding: 10px; text-align: left;'

    return soup.prettify()


for item in response_json:
    start = get_epoch_time_from_earlyon_format(item['start'])
    end = get_epoch_time_from_earlyon_format(item['end'])
    table.append([str(get_from_utc_time(start)), str(
        get_from_utc_time(end)), item['title']])

with open('earlyOn.html', 'w') as html_file:
    table = tabulate(table, tablefmt='html', headers='firstrow')
    pretty_table = make_tables_pretty(table)
    html_file.writelines(pretty_table)

webbrowser.open('earlyOn.html', new=2)
