# created on 07.03.2021
# author Ingo Dietz von Bayer

import time
import pandas as pd
import statistics as st
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Would you like to explore the data for Chicago, New York City or Washington? \n ")).lower()
    while city not in ("new york city", "chicago", "washington"):
        city = str(input("City name not found! Please choose on of the following cities:Chicago, New York City or Washington. \n ")).lower()

    # get user input for month (all, january, february, ... , june)
    month = str(input("Would you like to Anaylse all Months or a specific month? Answer with all or specific month. \n")).lower()
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
        month = str(input("Month not in the dataset! Please choose on of the following months:january, february, march, april, may, june. \n")).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input("Would you like to Anaylse the whole week or only a specific week Day? Answer with all or the specific week Day.\n")).lower()
    while day not in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = str(input("This is not a weekday! Please choose a weekday! \n")).lower()

    # get user input for raw data
    raw_data = str(input("Would you like to See the raw Data? Answer with y or n. \n")).lower()
    while raw_data not in ['y','n']:
        raw_data = str(input("Please enter y or n! \n")).lower()

    number_of_Lines = 0  # initialise variable

    if raw_data == 'y':
        all_or_number = str(input("Would you like to specify how lines of Raw Data are outputed? Answer with y or n. \n")).lower()
        while all_or_number not in ['y','n']:
            all_or_number = str(input("Please enter y or n! \n")).lower()
        if all_or_number == 'y':
            number_of_Lines = int(input("How Many lines of Raw Data would you like to see? Answer with a whole number. \n"))
        else:
            number_of_Lines =300000 # set a large number so that all lines will be printed


    return city, month, day, number_of_Lines



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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df = df.dropna(0) # omnitt NA rows

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] =pd.DatetimeIndex(df['Start Time']).dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day= days.index(day)
        df= df[df['day_of_week']==day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is:  %s" % (calendar.month_name[st.mode(df["month"])]))
    # display the most common day of week
    print("The most common Day is:  %s" % (calendar.day_name[st.mode(df["day_of_week"])]))

    # display the most common start hour
    mode_hour= st.mode(pd.DatetimeIndex(df["Start Time"]).hour)
    print("The most common Start hour is the: ", mode_hour, "o'clock")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].value_counts().index.tolist()[0]
    print("The most common Start Station is: ",most_common_start_station)

    # display most commonly used end station

    most_common_end_station = df["End Station"].value_counts().index.tolist()[0]
    print("The most common End Station is: ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    df["Combination_start_end_station"]= df["Start Station"] + [" to "] + df["End Station"]
    most_frequent_combination = df["Combination_start_end_station"].value_counts().index.tolist()[0]
    print("The most common Combination of Start and End Station is: ",most_frequent_combination )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The Total Travel Time is: ",df["Trip Duration"].sum().round(0), "min")
    # display mean travel time
    print("The mean Travel Time is: ",df["Trip Duration"].mean().round(0), "min")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    count_user_type = df.groupby('User Type')['User Type'].count()
    print("User type Statistics \n")
    print("Count of",count_user_type )
    print('-'*40)

    # Display counts of gender
    print("Gender Statistics \n")
    if  city != "washington":
        count_gender = df.groupby('Gender')['Gender'].count()
        print("Count of",count_gender )

    print('-'*40)
    # Display earliest, most recent, and most common year of birth
    print("Demographic Statistics \n")
    if city != "washington":
        print("User Demographics:\n" )
        print("Earlies Birth year:",df["Birth Year"].min())
        print("Most recent Birth year:",df["Birth Year"].max().round(0))
        print("Most common Birth year: %s" % (st.mode(df["Birth Year"])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, number_of_Lines = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        print(" Here is a brief summary of the Data: \n", df.describe())
        print('-'*40, '\n')
        print(" Here is the Raw Data you asked for. \n", df.head(number_of_Lines))

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
