import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
        Returns:
          city  -> string : The selected city.
          month -> string : The selected month.
          day   -> string : The selected day.

        purpose: allows the user to take a city, month, and day
                 to filter the bikeshare data.

      """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('What city are you looking for? chicago, '
                     'new york city, washington?: ').lower()
        if city in CITY_DATA:
            break;
        else:
            print('That\'s not a valid city!')

    months = ['all','january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    while True:
        month = input('What month are you looking for? january, february, march, ...., all: ').lower()
        if month in months:
            break;
        else:
            print('That\'s not a valid month!')

    days = ['all','saturday', 'sunday', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday']

    while True:
        day = input('which day are you looking for?: ')
        if day in days:
            break
        else:
            print('That\'s not a valid day!')
        print('-'*40)
    return city, month, day

def load_data(city, month, day):
   """
       accepts: city, month, day as a param.
       returns: data frame contains formatted dates:
            - start time as formatted date.
            - month.
            - day name.
   """
   df = pd.read_csv(CITY_DATA[city])
   df['Start Time'] = pd.to_datetime(df['Start Time'])
   df['month'] = df['Start Time'].dt.month
   df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

   if month != 'all':
      months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
                'august', 'sept', 'oct', 'november', 'december']
      month = months.index(month)+1
      df = df[df['month'] == month]

   if day != 'all':
       df = df[df['day_of_week'] == day]

   return df


def time_stats(df):

    """
        accepts: data frame.
        returns: nothing (void for calculations and printing only).
        purpose: calculates some interesting statistics such as most common month.

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if df.empty:
        print('No Data!')
        return;

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November',
              'December']

    most_common_mon = df['month'].mode()[0]
    most_common_mon_name = months[most_common_mon  - 1]
    print(f'most_common_mon: {most_common_mon_name}')

    days = ['Saturday', 'Sunday', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday']

    most_common_day = df['day_of_week'].mode()[0]
    print(f'most_common_day: {most_common_day}', )

    df['hour'] = df['Start Time'].dt.hour
    most_comm_strt_hour = df['hour'].mode()[0]
    print(f'most_comm_strt_hour: {most_comm_strt_hour} ')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def station_stats(df):

    """
        accepts: data frame.
        returns: nothing (void for calculations and printing).
        purpose: calculates some interesting statistics
                 such as the most commont start station.

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.empty:
        print('No Data!')
        return;

    most_cmn_strt_stn = df['Start Station'].mode()[0]
    print(f'most common start station: {most_cmn_strt_stn}')

    most_cmn_end_stn = df['End Station'].mode()[0]
    print(f'most common end station: {most_cmn_end_stn} ')

    most_cmn_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"most common trip: {most_cmn_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """"
            accpets: data frame.
            returns  nothing (void for calculations and printing)
            purpose: calculates total & mean trip durations.

    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if df.empty:
        print('No Data!')
        return;

    total_duration = df['Trip Duration'].sum()
    print("total trip duration: ", total_duration, ' seconds')

    mean_travle_time = df['Trip Duration'].mean()
    print("mean travel time: ", mean_travle_time, ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):

    """
           accepts: data frame.
            returns nothing (void for calculations and printing).
            purpose: generate some user statistics.
    """


    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if df.empty:
        print('No Data!')
        return;

    user_types = df['User Type'].value_counts()
    print("user types:")
    for index, value in user_types.items():
        print(f'{index}    {value}')



    if 'Gender' in user_types:
        gender_counts = df['Gender'].value_counts()
        print("gender counts: ", gender_counts)

    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_cmn_year = df['Birth Year'].mode()[0]
        print(f'earliest birth year: {earliest_birth_year}')
        print(f'most recent birth year: {most_recent_birth_year}')
        print(f'most common year {most_cmn_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data_rows(df):
    start = 0
    while True:
        ask_user = input("would you like to see 5 lines of raw data? ( enter yes OR no\n").lower()
        if ask_user != 'yes':
            break

        end = start + 5
        data = df.iloc[start:end]
        print(tabulate(data, headers='keys', tablefmt='fancy_grid', stralign='center'))
        start+= 5
        if start >=  len(df):
            print('End of data reached')
            break;





def main():
    """
        - calling the methods and produce the required results.
        - allows the user to restart the program as many times as needed.
    """

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
