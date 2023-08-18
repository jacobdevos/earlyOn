import webbrowser
import requests
from tabulate import tabulate
import datetime
from bs4 import BeautifulSoup


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def get_from_utc_time(epoch_time):
    date = datetime.datetime.fromtimestamp(epoch_time)
    date_str = date.strftime("%B %d, %Y")
    time_str = date.strftime("%I:%M%p")
    return date_str, time_str


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


today = datetime.datetime.now()
thirty_days_from_today = today + datetime.timedelta(30)

# The API endpoint
url_time_format = "%Y-%m-%d"
url = "https://www.keyon.ca/en/Events/GetEvents?id=501&startDate={start_date}T04%3A00%3A00.000Z&endDate={end_date}T04%3A00%3A00.000Z".format(
    start_date=today.strftime(url_time_format), end_date=thirty_days_from_today.strftime(url_time_format))

print(url)
# A GET request to the API
response = requests.get(url)

# Print the response
response_json = response.json()

filtered_response_json = [
    item for item in response_json if item['IsActive'] is True]

sorted_response_json = sorted(filtered_response_json, key=lambda x: x['start'])
table = [['Date', 'Start Time', 'End Time', 'Name', 'Description']]


def get_description(item):
    soup = BeautifulSoup(item['description'], features='html.parser')
    return soup.getText()


for item in sorted_response_json:
    start = get_epoch_time_from_earlyon_format(item['start'])
    end = get_epoch_time_from_earlyon_format(item['end'])
    start_date, start_time = get_from_utc_time(start)
    _, end_time = get_from_utc_time(end)
    description = get_description(item)
    table.append([start_date, start_time, end_time,
                 item['title'], description])

with open('earlyOn.html', 'w') as html_file:
    table = tabulate(table, tablefmt='html', headers='firstrow')
    pretty_table = make_tables_pretty(table)
    html_file.writelines(pretty_table)

webbrowser.open('earlyOn.html', new=2)
