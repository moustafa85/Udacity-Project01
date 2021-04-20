import time
import pandas as pd
from os import system, name

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
filter_DayMonth = ['Month', 'Days', 'Both', 'None']
filter_index = -1


# Done
def get_user_input(choices=days):
    """This is a generic function that provides a confirmation from user for any input data
       the procedure will be like the following:
            1.	choices are a list of available options; it will appear as numbered list
            2.	user have to select a value in a number way 1, 2, 3....
            3.	user then will confirm his/her choice
            4.	in case of invalid input, options will appear again to select one of them
            5.	it will return selection index from the input list

     """
    message = ""
    selection = -1
    # Add available options to appear as numbered list
    for counter in range(len(choices)):
        message += str(counter + 1) + "." + choices[counter].title() + "\n"
    # Start of the loop
    while True:
        print('Could you select from below options \n')
        # show available options in the list
        print(message)
        # start checking of any invalid input
        try:
            # user have to select one option only in a number
            selection = input('\tSelect a number from 1 to ' + str(len(choices)) + '\t')
            selection = int(selection)
            if len(choices) >= selection >= 1:
                # display the user selection to user
                print('\nYou select:\t' + str(choices[selection - 1].title()))
                try:
                    # ask user for a confirmation, he has to select y or yes to confirm
                    confirm = input('Are you sure? Please Type yes(y) / No(n):\t')
                except (ValueError, KeyboardInterrupt):
                    # in case of any valid values, go to the options again
                    continue
                # in case of valid option and user select y / yes
                if confirm.lower() == 'y' or confirm.lower() == 'yes':
                    # go out the selection loop
                    break
                else:
                    # for any other value other than yes, go again to the options
                    continue
        except (ValueError, KeyboardInterrupt):
            # for any invalid values, return to selection list again
            print('\nooh!!! You didn\'t select a number between available options :( \n')
            continue
        # user pass value outside the options, like select 4 for a list of 3 options
        print('\nooh!!! You didn\'t select a number between available options :( \n')
    # return user selection index
    return selection


# Done
def get_filters():
    global filter_index
    # clear screen
    clear_screen()
    print('\n' * 5)
    print('\t' * 5 + '\033[93m' + 'Hello! Let\'s explore some US bike share data!')
    time.sleep(1)
    print('\n' * 5)
    # get user input for city (chicago, new york city, washington).
    cityindex = get_user_input(list(CITY_DATA.keys()))
    # get the right value from city dictionary using index returned
    city = list(CITY_DATA.keys())[cityindex - 1]
    # by default All Months
    month = 6
    # by default All Days
    day = 7
    # display a list of ['Month', 'Days', 'Both', 'None'] to filter
    print('\n \033[96m Do you want to filter Months / Days')
    filter_index = get_user_input(filter_DayMonth) - 1
    # in case of filter_index = Both=2 / Day=1 / Month =0
    if filter_index == 0 or filter_index == 2:
        # get user input for month (all, january, february, ... , june)
        month = get_user_input(months) - 1
    if filter_index == 1 or filter_index == 2:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = get_user_input(days) - 1
    # return user selection from city, day and month filter

    return city, months[month], days[day]


# Done
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
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day Name'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # month = months.index(month)
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['Day Name'] == day.title()]
    return df


# Done
def user_stats(data_table_obj):
    print('\n Calculating Statistics')

    # User Type Section
    print('\nWhat is the breakdown of users')
    # record time of the beginning to process
    start_time = time.time()
    # Display counts of user types
    user_types = data_table_obj['User Type'].value_counts()
    print(user_types)
    # calculate time to execute the process
    processing_time(start_time)

    # Gender Section
    print('\nWhat is the breakdown of Gender')
    # record time of the beginning to process
    start_time = time.time()
    # Check for Gender column availability
    if 'Gender' in list(data_table_obj.columns):
        # Display counts of gender
        gender_info = data_table_obj['Gender'].value_counts()
        print(gender_info)
    else:
        # No information available
        print('\nNo gender data is available\n')
    # calculate time to execute the process
    processing_time(start_time)

    # Birth Year Section
    print('\nWhat is the breakdown of Birth Year')
    # record time of the beginning to process
    start_time = time.time()
    # Check for Birth Year column availability
    if 'Birth Year' in list(data_table_obj.columns):
        # calculating different statistics: Recent, Oldest and Popular year
        most_recent = int(data_table_obj['Birth Year'].max())
        print('most_recent:\t' + str(most_recent))
        oldest = int(data_table_obj['Birth Year'].min())
        print('Oldest :\t' + str(oldest))
        most_popular = int(data_table_obj['Birth Year'].mode()[0])
        print('Most Popular  :\t' + str(most_popular))
    else:
        # No information available
        print('\nNo Year Info is available\n')
    # calculate time to execute the process
    processing_time(start_time)


# Done
def time_stats(data_table_obj):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    # record time of the beginning to process
    start_time = time.time()

    data_table_obj['Hour'] = data_table_obj['Start Time'].dt.hour
    # display the most common month
    print('Most Common Month:\t' + data_table_obj['Month'].mode()[0])
    # display the most common day of week
    print('Most Common Day of Week: ' + data_table_obj['Day Name'].mode()[0])
    # display the most common start hour
    pop_hour = str(data_table_obj['Hour'].mode()[0])
    print('Most Common Start Hour: ' + pop_hour)
    # print(data_table_obj['Hour'].value_counts()[:1])
    # calculate time to execute the process
    processing_time(start_time)


# Done
def station_stats(data_table_obj):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    # record time of the beginning to process
    start_time = time.time()
    # display most commonly used start station
    print('Most Common Start Station:\t' + str(data_table_obj['Start Station'].value_counts()[:1]))
    # display most commonly used end station
    print('Most Common End Station: \t' + str(data_table_obj['End Station'].value_counts()[:1]))
    # concatenate start to end station to calculate frequest trips
    data_table_obj["Trip"] = data_table_obj["Start Station"] + " to " + data_table_obj["End Station"]
    # display most frequent combination of start station and end station trip
    print('Most Common trip: \t' + str(data_table_obj['Trip'].value_counts()[:1]))
    # print('Most Common trip: \t' + str(data_table_obj['Trip'].mode()[0]))
    # calculate time to execute the process
    processing_time(start_time)


# Done
def trip_duration_stats(data_table_obj):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    # record time of the beginning to process
    start_time = time.time()
    # display total travel time
    print('Total Duration:\t' + str(data_table_obj['Trip Duration'].sum()))
    # display mean travel time
    print('Average Duration :\t' + str(data_table_obj['Trip Duration'].mean()))
    # calculate time to execute the process
    print('Count of Trips :\t' + str(data_table_obj['Trip Duration'].shape[0]))
    # calculate time to execute the process
    processing_time(start_time)


# Done
def filter_message(day='all', month='all'):
    """Displays the filter for Day / Month."""
    # values in filter_DayMonth = ['Month', 'Days','Both', 'None']
    filter_msg = 'Filter by (' + filter_DayMonth[filter_index] + ')'
    # in case of filter_index = Both=2 / Day=1 / Month =0
    if filter_index == 2 or filter_index == 0:
        filter_msg += '  ' + month.title()
    if filter_index == 2 or filter_index == 1:
        filter_msg += '  ' + day.title()
    # show filter message
    print(filter_msg)


# Done
def processing_time(start_time):
    """Displays the processing time"""
    print("\nThis took %s seconds." % (time.time() - start_time))
    # print line with ***************************************************
    print('-' * 40)


def display_rawdata(city):
    # show notification to end user if (s)he want to see data of the files in blocks of 5 rows
    print('\nRaw data is available to check... \n')
    display_raw = input('Do you want to see 5 rows of data set? Press Yes / No:\t')
    while display_raw.lower() not in ('yes', 'no', 'y', 'n'):
        try:
            # in case of invalid input value
            print('Invalid option, Could you select proper option?')
            display_raw = input('Do you want to see 5 rows of data set? Press Yes / No:\t')
        except (ValueError,KeyboardInterrupt):
            continue
    # clear screen to start with only data
    clear_screen()
    # start reading separate blocks of data, each block has 5 rows
    while display_raw.lower() in ('yes', 'y'):
        try:
            for block5 in pd.read_csv(CITY_DATA[city], index_col=0, chunksize=5):
                print(block5)
                # ask user for another block to show
                display_raw = input('Press Yes(y) if you want to see another 5 rows?')
                # read till the user didn't accept
                if display_raw.lower() not in('y','yes'):
                    # go outside the loop
                    break
            break
        except KeyboardInterrupt:
            print('invalid selection')


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# Test
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        clear_screen()
        # coloring the curson
        print('\033[92m')
        filter_message(day, month)
        time_stats(df)
        time.sleep(2)
        filter_message(day, month)
        user_stats(df)
        time.sleep(2)
        filter_message(day, month)
        station_stats(df)
        time.sleep(2)
        filter_message(day, month)
        trip_duration_stats(df)
        time.sleep(2)
        # coloring the curson
        print('\033[36m')
        display_rawdata(city)
        try:
            restart = input('\nWould you like to restart? Yes(y) / No(n):  ')
            if restart.lower() not in ('y', 'yes'):
                break
        except (ValueError, KeyboardInterrupt):
            break

    clear_screen()
    print('\n Good Luck !!!')


if __name__ == "__main__":
    main()
