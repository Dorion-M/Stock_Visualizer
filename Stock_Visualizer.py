#api key: NB0AK6IK339LRUMR
import requests
import json
import datetime

#function to check if a given date is within a specified range
def is_date_in_range(date_str, start_date, end_date):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    return start <= date <= end

#function to filter JSON data based on a specified date range
def filter_json_data(json_data, start_date, end_date):
    filtered_data = {}
    time_series_keys = [key for key in json_data.keys() if "Time Series" in key]
    
    if time_series_keys:
        time_series_key = time_series_keys[0]
        for date_str, data in json_data[time_series_key].items():
            if is_date_in_range(date_str, start_date, end_date):
                filtered_data[date_str] = data
    
    #Converts the filtered dictionary to a list of key-value pairs
    filtered_data_list = list(filtered_data.items())
    
    #Sorts the list based on the date in ascending order
    sorted_data_list = sorted(filtered_data_list, key=lambda x: datetime.datetime.strptime(x[0], "%Y-%m-%d"))
    
    #Converts the sorted list back to a dictionary
    sorted_filtered_data = dict(sorted_data_list)
    
    return sorted_filtered_data

#Function to get user input for stock symbol, chart type, time series function, start date, and end date
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
        params += f'&interval={interval}&outputsize=full'

    #makes sure output size is full for daily, so that the JSON data doesn't get cut off
    if function == 'TIME_SERIES_DAILY':
        params += f'&outputsize=full'

    response = requests.get(base_url + params)  #get the json data from querying the API
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    

#main loop to interact with the user and process stock data
while True:
    #get user input for stock symbol, chart type, time series function, start date, and end date
    stock_symbol, chart_type, time_series_function, start_date, end_date = get_user_input()
    
    #get the JSON data from the Alpha Vantage API based on user input
    json_data = construct_api_url(stock_symbol, time_series_function)
    
    if json_data:
        #filter the JSON data based on the given start_date and end_date
        filtered_data = filter_json_data(json_data, start_date, end_date)
        
        if filtered_data:
            #process the filtered data here. This is probably where we would generate and render the chart to the browser
            print(filtered_data)
            
        else:
            print("No data found within the specified date range.")
    
    #ask user if they want to view more stock data
    repeat_function = input("\nWould you like to view more stock data? (y/n)\n")
    if repeat_function == "n":
        break