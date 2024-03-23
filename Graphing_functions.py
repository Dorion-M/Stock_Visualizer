import datetime
import pygal
from lxml import etree
import webbrowser
import os

def parse_date_string(date_str):
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date entered. Please re-enter the date string and try again.")
            return None
    except TypeError:
        print("Invalid date entered. Please re-enter the date string and try again.")
        return None

    return date

#Function to check if a given date is within a specified range
def is_date_in_range(date_str, start, end):
    date = parse_date_string(date_str)
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
    try:
        sorted_data_list = sorted(filtered_data_list, key=lambda x: datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"))
    except:
        sorted_data_list = sorted(filtered_data_list, key=lambda x: datetime.datetime.strptime(x[0], "%Y-%m-%d"))

    
    #Convert the sorted list back to a dictionary
    sorted_filtered_data = dict(sorted_data_list)
    
    return sorted_filtered_data


def generate_chart(filtered_data, chart_type, stock_symbol, start_date, end_date):
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
        
    else:
        chart = pygal.Line(x_label_rotation=45)

    chart.title = f'Stock Data for {stock_symbol.upper()}: {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'

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
    chart_file = 'chart.svg'

    #render the chart to the specified file
    chart.render_to_file(chart_file)

    #open the generated chart HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(chart_file))