from API_Functions import api_call

from Graphing_functions import filter_json_data, generate_chart, render_chart_in_browser, parse_date_string
import datetime

#Gets user input for stock symbol, chart type, time series function, start date, and end date
def get_user_input():
    start_date = None
    end_date = None

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

    while not start_date:
        start_input = input("Enter the start date (YYYY-MM-DD): ")
        start_date = parse_date_string(start_input)

    while not end_date:
        end_input = input("Enter the end date (YYYY-MM-DD): ")

        if(parse_date_string(end_input) is None):
            continue
        
        if (start_date < parse_date_string(end_input)):
            end_date = parse_date_string(end_input)
            if end_date is not None:
                break

        print("Start date cannot be later than the end date. Enter the dates again.\n")


    return stock_symbol, chart_type, time_series_function, start_date, end_date


while True: 
    #get user input for stock symbol, chart type, time series function, start date, and end date
    stock_symbol, chart_type, time_series_function, start_date, end_date = get_user_input()
    
    #get the JSON data from the Alpha Vantage API based on user input
    json_data = api_call(stock_symbol, time_series_function, start_date)
    
    if json_data:
        #filter the JSON data based on the given start_date and end_date
        filtered_data = filter_json_data(json_data, start_date, end_date)
        
        if filtered_data:
            chart = generate_chart(filtered_data, chart_type, stock_symbol, start_date, end_date)
            render_chart_in_browser(chart)
            #print(filtered_data)
        else:
            print("No data found within the specified date range.")
    
    #ask user if they want to view more stock data
    repeat_function = input("\nWould you like to view more stock data? (y/n)\n")
    if repeat_function == "n":
        break