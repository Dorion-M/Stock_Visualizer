import requests
import json
import datetime
import pygal
from lxml import etree
import webbrowser
import os

#Function to check if a given date is within a specified range
def is_date_in_range(date_str, start_date, end_date):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    return start <= date <= end

#Function to filter JSON data based on a specified date range
def filter_json_data(json_data, start_date, end_date):
    filtered_data = {}
    time_series_keys = [key for key in json_data.keys() if "Time Series" in key]
    
    if time_series_keys:
        time_series_key = time_series_keys[0]
        for date_str, data in json_data[time_series_key].items():   #iterate over the data for each date, check if its in the range
            if is_date_in_range(date_str, start_date, end_date):
                filtered_data[date_str] = data                      #if it is in the range, add the data
    
    #Convert the filtered dictionary to a list of key-value pairs
    filtered_data_list = list(filtered_data.items())
    
    #Sort the list based on the date in ascending order
    sorted_data_list = sorted(filtered_data_list, key=lambda x: datetime.datetime.strptime(x[0], "%Y-%m-%d"))
    
    #Convert the sorted list back to a dictionary
    sorted_filtered_data = dict(sorted_data_list)
    
    return sorted_filtered_data

#Gets user input for stock symbol, chart type, time series function, start date, and end date
def get_user_input():
    while True:
        stock_symbol = input("\nEnter the stock symbol you are looking for: ")
        if stock_symbol.strip():
            break
        print("Invalid input. Please try again.")

    while True:
        print("\nChart types \n ----------- \n 1. Bar \n 2. Line\n")
        chart_type = input("Enter the chart type (1, 2): ")
        if chart_type in ('1', '2'):
            break
        print("Invalid input. Please try again.")

    while True:
        print("\nSelect the time series of the chart you want to generate \n ------------------------------------- \n 1. Intraday \n 2. Daily\n 3. Weekly \n 4. Monthly")
        time_series_function = input("Enter the time series option (1, 2, 3, 4): ")
        if time_series_function.strip() in ('1', '2', '3', '4'):
            break
        print("Invalid input. Please try again.")

    while True:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        if len(start_date.strip()) == 10:
            break
        print("Invalid input. Please try again.")

    while True:
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        if len(end_date.strip()) == 10:
            break
        print("Invalid input. Please try again.")

    return stock_symbol, chart_type, time_series_function, start_date, end_date

#Function to construct the API URL based on user input
def construct_api_url(stock_symbol, time_series_function):
    base_url = 'https://www.alphavantage.co/query?' #base url
    function_map = {
        '1': 'TIME_SERIES_INTRADAY',
        '2': 'TIME_SERIES_DAILY',
        '3': 'TIME_SERIES_WEEKLY',
        '4': 'TIME_SERIES_MONTHLY'
    }

    function = function_map[time_series_function]
    api_key = 'NB0AK6IK339LRUMR'
    params = f'function={function}&symbol={stock_symbol}&apikey={api_key}'  #construct the parameters based on user input

    #add an interval if the user chose intraday
    if function == 'TIME_SERIES_INTRADAY':
        interval = '60min'
        params += f'&interval={interval}&outputsize=full'   #also increase the output size to full so the data doesn't cut off
    
    if function == 'TIME_SERIES_DAILY':
        params += f'&outputsize=full'                       #increase output size for daily as well, so that the data doesn't cut off

    response = requests.get(base_url + params)  #get the json data from querying the API. the query is the base url + parameters
    print(base_url + params)
    if response.status_code == 200:             #if status code is 200 (i.e. the query successfully went through)
        return response.json()                  #then return the json data from the API query
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None     #if it doesn't work, tell the user and return nothing
    


def generate_chart(filtered_data, chart_type, stock_symbol):
    #extract dates from the filtered data
    dates = list(filtered_data.keys())

    #extract open prices from the filtered data
    open_prices = [float(data['1. open']) for data in filtered_data.values()]

    #extract high prices from the filtered data
    high_prices = [float(data['2. high']) for data in filtered_data.values()]

    #extract low prices from the filtered data
    low_prices = [float(data['3. low']) for data in filtered_data.values()]

    #extract close prices from the filtered data
    close_prices = [float(data['4. close']) for data in filtered_data.values()]

    #create a bar chart if chart_type is '1', otherwise create a line chart
    if chart_type == '1':
        chart = pygal.Bar(x_label_rotation=45)
        chart.title = f'{stock_symbol} Stock Prices - Bar Chart'
    else:
        chart = pygal.Line(x_label_rotation=45)
        chart.title = f'{stock_symbol} Stock Prices - Line Chart'

    #set the x-labels of the chart to the dates
    chart.x_labels = dates

    #add the open prices to the chart
    chart.add('Open', open_prices)

    #add the high prices to the chart
    chart.add('High', high_prices)

    #add the low prices to the chart
    chart.add('Low', low_prices)

    #add the close prices to the chart
    chart.add('Close', close_prices)

    #return the generated chart object
    return chart

def render_chart_in_browser(chart):
    #define the file name for the chart HTML file
    chart_file = 'chart.html'

    #render the chart to the specified file
    chart.render_to_file(chart_file)

    #open the generated chart HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(chart_file))

