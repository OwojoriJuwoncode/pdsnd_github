import time
import pandas as pd

CITY_DATA = {
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'
}

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')

    # Get user input for the city
    while True:
        city = input("\nWhich city would you like to filter by? New York City, Chicago, or Washington?\n").title()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter a valid city name.")

    # Get user input for the month
    while True:
        month = input("\nWhich month would you like to filter by? January, February, March, April, May, June, or type 'all' for no filter.\n").title()
        if month in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            break
        else:
            print("Invalid input. Please enter a valid month name.")

    # Get user input for the day of the week
    while True:
        day = input("\nAre you looking for a particular day? If so, kindly enter the day (e.g., Sunday, Monday, Tuesday, etc.), or type 'all' for no filter.\n").title()
        if day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']:
            break
        else:
            print("Invalid input. Please enter a valid day of the week.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')

    # Filter by month if applicable
    if month != 'All':
        df = df[df['month'] == month]

    # Filter by day of the week if applicable
    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    # Display the most common day of the week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.strftime('%H')
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)

    # Display most frequent combination of start station and end station trip
    combination_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Frequent Combination of Start Station and End Station Trip:', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in days
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time // 86400, 'Days')

    # Display mean travel time in minutes
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time // 60, 'Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender if available
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_counts)
    else:
        print('\nGender Types:\nNo data available for this month.')

    # Display earliest, most recent, and most common year of birth if available
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]

        print('\nEarliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', most_recent_birth_year)
        print('Most Common Birth Year:', most_common_birth_year)
    else:
        print('\nBirth Year Information:\nNo data available for this month.')

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
