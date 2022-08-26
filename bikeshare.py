import time

import pandas as pd
import numpy as np

CITY_DATA = {'Chicago': 'chicago.csv',
             'Newyork': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global month, day, flag
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:

        city = input('Would you like to see data for Chicago, New York or Washington?\n')
        city = city.replace(' ', '')
        city = city.capitalize()
        if city == 'Chicago' or city == 'Newyork' or city == 'Washington':
            break
        else:
            print('Your input is wrong, please re-enter it.\n')
            continue
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        flag = 0
        filter_by = input(
            'Would you like to filter the data by month, day, both or none? Type "none" for no time filter.\n ')
        filter_by = filter_by.replace(' ', '')
        filter_by = filter_by.lower()
        if filter_by in ['month', 'day', 'both', 'none']:
            while filter_by == 'month':
                day = 'All'
                month = input('Which month? all, January, February, March, April, May or June?\n')
                month = month.replace(' ', '')
                month = month.capitalize()
                if month not in ['All', 'January', 'February', 'March', 'April', 'May', 'June']:
                    print('Your input is wrong, please re-enter it:\n')
                    continue
                else:
                    flag = True
                    break
            # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
            while filter_by == 'day':
                month = 'All'
                day = input(
                    'Which day? Please type your response(e.g: Sunday)or type "all" to get the data for the whole week.\n')
                day = day.replace(' ', '')
                day = day.title()
                if day in ['Monday', 'Tuesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']:
                    flag = True
                    break
                else:
                    print('Please enter an integer or "all" :\n')
                    continue

            while filter_by == 'both':
                month = input('Which month? all, January, February, March, April, May or June?\n')
                month = month.replace(' ', '')
                month = month.capitalize()
                if month not in ['All', 'January', 'February', 'March', 'April', 'May', 'June']:
                    print('Your input is wrong, please re-enter it:\n')
                    continue
                day = input(
                    'Which day? Please type your response(e.g: Sunday).\n')
                day = day.replace(' ', '')
                day = day.title()
                if day in ['Monday', 'Tuesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']:
                    flag = True
                    break
                else:
                    print('Please enter an integer or "all" :\n')
                    continue
            while filter_by == 'none':
                month = 'All'
                day = 'All'
                flag = True
                break
        else:
            print('Your input is wrong, please re-enter it:\n')
            continue
        if flag:
            break
    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    a = df.month.value_counts()
    b = a.idxmax()
    count = a.max()
    print('Most common month: {0}, Count: {1}\n'.format(b, count))
    # TO DO: display the most common day of week
    a = df.day_of_week.value_counts()
    b = a.idxmax()
    count = a.max()
    print('Most common day of week: {0}, Count: {1}\n'.format(b, count))
    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    a = df.start_hour.value_counts()
    b = a.idxmax()
    count = a.max()
    print('Most popular hour: {0}, Count: {1}\n'.format(b, count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    a = df.loc[:,'Start Station'].value_counts()
    b = a.idxmax()
    count = a.max()
    print('Start Station: {0}, Count: {1}'.format(b, count))
    # TO DO: display most commonly used end station
    a = df.loc[:, 'End Station'].value_counts()
    b = a.idxmax()
    count = a.max()
    print('End Station: {0}, Count: {1}'.format(b, count))
    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'].map(str) + '_' + df['End Station'].map(str)
    a = df.loc[:,'combination'].value_counts()
    b = a.idxmax()
    count = a.max()
    split = b.split('_')
    start = split[0]
    end = split[1]
    print("Most popular trip:(\'{0}\', \'{1}\')".format(start, end), 'Count:{0}'.format(count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['diff_time'] = (df['End Time'] - df['Start Time']).dt.seconds
    total = df['diff_time'].sum()
    count = df.shape[0]
    # TO DO: display mean travel time
    mean_time = total / count
    print('Total travel time: {0}, Count: {1}, Avg time: {2}'.format(total, count, mean_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    a = df['User Type'].value_counts()
    print('Users Types: \n{0}'.format(a))
    # TO DO: Display counts of gender
    if 'Gender' in df:
        a = df['Gender'].value_counts()
        print('Users Gender: \n{0}'.format(a))
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        a = df['Birth Year'].value_counts()
        common = a.idxmax()
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        print('Earliest year of birth: {0}, Most recent year of birth: {1}, Most common year of birth: {2}'
              .format(earliest, recent, common))
    else:
        print('Birth Year stats cannot be calculated because Gender does not appear in the dataframe')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        df = pd.read_csv(CITY_DATA[city])
        for i in range(df.shape[0]+1):
            if i % 5 == 0:
                view = input('Would you like to view individual trip data? Type "yes" or "no".\n')
                view.replace(' ','')
                if view.lower() != 'yes':
                    break
                if view.lower() == 'yes':
                    df5 = df.iloc[i]
                    print(df5,'\n')
            else:
                df5 = df.iloc[i]
                print(df5,'\n')


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        restart.replace(' ','')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
