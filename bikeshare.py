import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

snake_string = """
Welcome to Python3!

             ____
            / . .\\
            \  ---<
             \  /
   __________/ /
-=:___________/

<3, Juno
"""
def get_filters():
    """Asks user to specify a city, month, and day to analyze. Returns:(str) city - name of the city to analyze (str) month - name of the month to filter by, or "all" to apply no month filter (str) day - name of the day of week to filter by, or "all" to apply no day filter"""
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ['chicago','new york city','washington']
    months = ['january','february','march','april','may','june','all']
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you like to explore: Chicago, New York city, Washington:\n").lower()

    while (city not in cities):
        city = input("Please type your answer again: Chicago, New York city or Washington, or all:").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to explore? (Januray, Februrary, March, April, May, June, or all)\n").lower()

    while (month not in months):
        month = input("Please type your answer again:\n").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which month would you like to explore? (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or all)\n").lower()
    while (day not in days):
        day = input("Please type your answer again:\n").lower()
    else:
        print('-'*50)
        print(city, month, day)

    return city, month, day

def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable. Args:(str) city - name of the city to analyze(str) month - name of the month to filter by, or "all" to apply no month filter (str) day - name of the day of week to filter by, or "all" to apply no day filter Returns: df - Pandas DataFrame containing city data filtered by month and day"""
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1


        # filter by month to create the new dataframe
        df = df[df['month'] == month]
      # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_num = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6}
        df = df[df['day_of_week'] == day_num[day]]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # display the most common month
    month_number = {1:'January', 2:"February", 3:'March', 4:'April', 5:'May', 6:'June'}
    df['month_num'] = pd.to_datetime(df['Start Time']).dt.month
    popular_month = month_number[df['month_num'].value_counts().idxmax()]
    print("{} is the most popular month.".format(popular_month))

    # display the most common day of week
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.day_name()
    popular_week_day = df['day_of_week'].value_counts().idxmax()
    print("{} is the most populat day of the week.".format(popular_week_day))

    # display the most common start hour
    popular_hour = pd.to_datetime(df['Start Time']).dt.hour.mode()[0]
    print("{} is the most common hour.".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].value_counts()
    print('The most popular start station is {}.'.format(popular_start_station.idxmax()))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].value_counts()
    print('The most popular end station is {}.'.format(popular_end_station.idxmax()))

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end_route'] = df['Start Station'] + " to " +df['End Station']
    popular_route = df['start_end_route'].value_counts()
    print('The most popular route is {}.'.format(popular_route.idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print("The total minutes of bike sharing is {}.".format(total_travel_time))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean trip duration in is {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if df.get('Gender') is not None:
      gender = df['Gender'].dropna().value_counts()
      print(gender)
    else:
      print("No gender information recorded.")

    # Display earliest, most recent, and most common year of birth
    if df.get('Birth Year') is not None:
      birth_year_time = df['Birth Year'].dropna().sort_values()
      num_birth_year = df['Birth Year'].value_counts()
      print("The oldest user was born in {}.".format(int(birth_year_time.iloc[0])))
      print("The youngest user was born in {}".format(int(birth_year_time.iloc[-1])))
      print("People born in {} use our service most often.".format(int(num_birth_year.idxmax())))
    else:
      print("No birth year information recorded.")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Ask users whether they want to see the raw data. If yes, prompt the first five rows and ask whether additional five rows are needed in the subsequent questions."""
    i = 5
    raw = input("Would you like to see the raw data? 'yes' or 'no'\n").lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.head(i)) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("Would you like to see more of the raw data? 'yes' or 'no'\n").lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        station_stats(df)
        time_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
		print(snake_string)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
