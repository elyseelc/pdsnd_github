import time
import pandas as pd
import numpy as np
import calendar
import fnmatch

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # getting user input for city
    while True:
        city = input('\nEnter the city you would like to look at (Chicago, New York, or Washington): \n').lower().title()
        if city in CITY_DATA:
            break
        else:
            print('\nInvalid input. \nEnter one of "Chicago", "New York", or "Washington".')

    # getting user input for month
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'All']
    while True:
        month = input('\nEnter the month you would like to look at, (enter "All" to see all 6 months): \n').lower().title()
        if month in months:
            break
        else:
            print('\nInvalid input. \n Enter one of "Jan", "Feb", "Mar", "Apr", "May", "Jun", or "All"')
            

    # getting user input for day of week
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'All']
    while True:
        day = input('\nEnter the day of the week you would like to look at, (enter "All" to see data for all days): \n').lower().title()
        if day in days:
            break
        else:
            print('\nInvalid input. \nEnter one of "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "All"')

    print('-'*40)    # formatting
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # reading the data
    df = pd.read_csv(CITY_DATA[city])
    
    # converting (Start Time) column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month (if applicable)
    if month != 'All':
        # filter by month, creating new dataframe
        df = df[df['month'].str.startswith(month.title())]
        
    # filter by day (if applicable)
    if day != 'All':
        # filter by day, creating new dataframe
        df = df[df['day_of_week'].str.startswith(day.title())]
        
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # displaying the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('Most common month: ' + str(calendar.month_name[common_month]))

    # displaying the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    common_day = df['day'].mode()[0]
    print('Most common day: ' + str(common_day))

    # displaying the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common hour: ' + str(common_start_hour) + ' o\'clock.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)   # formatting


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displaying most commonly used start station
    print('The most common start station is ' + df['Start Station'].mode() + '.')

    # displaying most commonly used end station
    print('The most common end station is ' + df['End Station'].mode() + '.')

    # displaying most frequent combination of start station and end station trip
    comb = (df['Start Station'] + '; ' + df['End Station']).mode()
    print('The most common combination of start station and end station is ' + str(comb) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displaying total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time for your specifications was ' + str(total_travel_time) + ' seconds.')

    # displaying mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time for your specifications was ' + str(mean_travel_time) + ' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # displaying counts of user types
    user_type_counts = df['User Type'].value_counts()
    print(user_type_counts)

    # displaying counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    except:
        # washington doesn't have this data
        print('There is no gender data for your chosen city.')


    # displaying earliest, most recent, and most common year of birth
    try: 
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        mode_birth_year = df['Birth Year'].mode()
        print('The earliest birth year is ' + str(earliest) + '.')
        print('The most recent birth year is ' + str(most_recent) + '.')
        print('The most common birth year is ' + str(mode_birth_year) + '.')
    except:
        # washington doesn't have this data
        print('There is no birth year data for your chosen city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    # formatting


# asking if they want to see 5 lines of raw data    
def raw(df):
    raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()
    starting_loc = 0
    while raw_data == 'yes':
        print(df.iloc[0:5])    # this will print the 5 rows
        starting_loc += 5    # getting ready for the next round
        raw_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no?\n").lower()
        
    return df


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
