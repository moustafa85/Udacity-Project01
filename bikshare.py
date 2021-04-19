import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']


def get_user_input(choices=days):
    message = ""
    selection = -1
    for counter in range(len(choices)):
        message += str(counter + 1) + "." + choices[counter].title() + "\n"
    while True:
        # print('*' * 20)
        print('Could you select a number from options you want filter:')
        print(message)
        # print('1. Chicago \n2. New York\n3. Washington')
        try:
            selection = input('\tSelect from 1 to ' + str(len(choices)) + ' \t')
            selection = int(selection)
            if len(choices) >= selection >= 1:
                # print('You select: \t' + list(CITY_DATA.keys())[city - 1])
                print('You select: \t' + str(choices[selection - 1].title()))
                try:
                    confirm = input('Are you sure? Y / N ')
                except KeyboardInterrupt:
                    continue
                if confirm.lower() == 'y':
                    break
                else:
                    continue
        except ValueError:
            print('\nooh!!! You didn\'t select a number between 1--> 3 :( \n')
            continue
        print('\nooh!!! You didn\'t select a number between available options :( \n')
    return selection


def get_filters():
    print('\nHello! Let\'s explore some US bike share data!\n')
    time.sleep(2)
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cityindex = get_user_input(list(CITY_DATA.keys()))
    city = list(CITY_DATA.keys())[cityindex-1]
    month = 6
    day = 7
    print('\nDo you want to filter Months / Days')
    filter_DayMonth = get_user_input(['Month', 'Days', 'Both', 'None']) - 1

    if filter_DayMonth == 0 or filter_DayMonth == 2:
        # get user input for month (all, january, february, ... , june)
        month = get_user_input(months) - 1
    if filter_DayMonth == 1 or filter_DayMonth == 2:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = get_user_input(days) - 1
    return city, months[month], days[day]


print(get_filters())


def load_data(city, month, day):
    """
       Loads data for the specified city and filters by month and day if applicable.

       Args:
           (str) city - name of the city to analyze
           (str) month - name of the month to filter by, or "all" to apply no month filter
           (str) day - name of the day of week to filter by, or "all" to apply no day filter
       Returns:
           df - pandas DataFrame containing city data filtered by month and day
   """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == (month + 1)]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        # days = ['saturday', 'sunday', 'monday', 'tuesday', 'wendsday', 'thrusday','friday']
        # selectedday = days.index(day)
        df = df[df['day_of_week'] == day.title()]
        print([day.title()])
    return df
