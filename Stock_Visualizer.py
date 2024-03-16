#api key: NB0AK6IK339LRUMR
import requests
import json

def get_user_input():
    
    while True:
        stock_symbol = input("\nEnter the stock symbol you are looking for: ")
        if stock_symbol.strip():  # Check if the input is not empty
            break
        print("Invalid input. Please try again.")

    while True:
        print("\nChart types \n ----------- \n 1. Bar \n 2. Line\n")
        chart_type = input("Enter the chart type (1, 2): ")
        if chart_type in ('1', '2'):  # Check if the input is either '1' or '2'
            break
        print("Invalid input. Please try again.")

    while True:
        print("\nSelect the time series of the chart you want to generate \n ------------------------------------- \n 1. Intraday \n 2. Daily\n 3. Weekly \n 4. Monthly")
        time_series_function = input("Enter the time series option (1, 2, 3, 4): ")
        if time_series_function.strip() in ('1', '2', '3', '4'):  # Check if the input is one of the valid options
            break
        print("Invalid input. Please try again.")  

    while True:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        if len(start_date.strip()) == 10:  # Check if the input has the correct length
            break
        print("Invalid input. Please try again.")

    while True:
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        if len(end_date.strip()) == 10:  # Check if the input has the correct length
            break
        print("Invalid input. Please try again.")
    return stock_symbol, chart_type, time_series_function, start_date, end_date


#def construct_api_url(stock_symbol, time_series_function, start_date, end_date):
def construct_api_url(stock_symbol, time_series_function):
    base_url = 'https://www.alphavantage.co/query?' #base query URL
    function_map = {                                #function map for the time_series_function choice
        '1': 'TIME_SERIES_INTRADAY',
        '2': 'TIME_SERIES_DAILY',
        '3': 'TIME_SERIES_WEEKLY',
        '4': 'TIME_SERIES_MONTHLY'
    }
    
    function = function_map[time_series_function]   #"function" will equal the mapped value of the number choice that the user input
    api_key = 'NB0AK6IK339LRUMR'                  
    
    params = f'function={function}&symbol={stock_symbol}&apikey={api_key}'  #constructs the parameters for the query URL

    if function == 'TIME_SERIES_INTRADAY':  #if you chose the intraday time series, then we will also need an interval parameter
        interval = '60min'  #this value can be either 1min, 5min, 15min, 30min, or 60min
        params += f'&interval={interval}'   #adds interval to parameters

    
    #else:
    #    if start_date and end_date:
    #        params += f'&start_date={start_date}&end_date={end_date}'
    #    elif start_date:
    #        params += f'&start_date={start_date}'
    #    elif end_date:
    #        params += f'&end_date={end_date}'

    
    return base_url + params #returns the API URL, which is the base URL plus the parameters the user chose



while True:
    stock_symbol, chart_type, time_series_function, start_date, end_date = get_user_input() #get the user input and store it in these variables
    #api_url = construct_api_url(stock_symbol, time_series_function, start_date, end_date)
    api_url = construct_api_url(stock_symbol, time_series_function)                #store the constructed URL into api_url

    print(api_url)          #print the API URL that you can paste into a browser


    repeat_function = input("\nWould you like to view more stock data? (y/n)\n")
    if repeat_function == "n":
        break