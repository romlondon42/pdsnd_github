import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

"""Asks user to specify a city, month, and day to analyze."""

def get_filters():
    city_choice = ['chicago', 'new york' , 'washington']
    while True:
        city = str(input('Enter a city: chicago, washington or new york').lower())
        if city in city_choice:
            print ("Good choice")
            break
        else:
            print('Please enter a different city')

    month_choice = ['all','january', 'february', 'march' ,'april' ,'may', 'june']
    while True:
        month = str(input('Enter a month: all, or any month from january to june').lower())
        if month in month_choice:
            print ("Good choice")
            break
        else:
            print('Please enter a valid month')

    day_choice = ['all','monday', 'tuesday', 'wednesday' ,'thursday' ,'friday', 'saturday' , 'sunday']
    
    while True:
        day = str(input('Enter a day: all, or any day of the week').lower())
        if day in day_choice:
            print ("Good choice")
            break
        else:
            print('Please enter a valid day')

    print('Hello! Let\'s now explore some US bikeshare data!')

    return city, month, day

def load_data(city, month, day):
    " Load the choosen city in dataframe"
    df = pd.read_csv(CITY_DATA[city])

    "Convert the start time to datime"
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    "Create month/day/hour column "
    df['month'] = df['Start Time'].dt.month
    df['days'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january','february', 'march', 'april', 'may', 'june']
        correct_month = months.index(month)+1
        df = df[df['month'] == correct_month]

    "filter the day from user input"
    if day != 'all':
        df =df[df['days'].str.lower() == day]
    return df

" Ask the user if he wants to see the first 5 rows of data"
def display_data(df):
    first_row = 5
    count=0
    while True:
        if count==0:
         display_data = str(input('Do you want to see the first 5 lines of the data, yes or no').lower())
         count+=1
        else:
            display_data = str(input('Do you want to see the next 5 lines of the data, yes or no').lower())
        if display_data == 'yes':
            print(df.head(first_row))
            first_row +=5 
        else:
            break

"""Displays statistics on the most frequent times of travel."""

def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most popular month of rental:', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['days'].mode()[0]
    print('Most popular day of rental:', popular_day)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour of rental:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Displays statistics on the most popular stations and trip."""

def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_startstation = df['Start Station'].mode()[0]
    print('Most popular start Station of rental:', popular_startstation)

    popular_endstation = df['End Station'].mode()[0]
    print('Most popular end Station of rental:', popular_endstation)

    "Create a column with Start and End Station concatenation"
    df['Trip'] = df['Start Station'] + "-->" + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most popular trip: ', popular_trip)

  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Maximun travel time for your choice', df['Trip Duration'].max())
    print('Mean travel time for your choice', df['Trip Duration'].mean())
    print('Minimum travel time for your choice', df['Trip Duration'].min())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)
    
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print(gender_types)

        print('Please bear in mind:', df['Gender'].isnull().sum(), ' users have no gender specified')
    else:
        print('The city you selected has no data available for Gender')

    if 'Birth Year' in df.columns:
        print('Easliest user date of birth', int(df['Birth Year'].min()))
        print('Most common user date of birth', int(df['Birth Year'].mode()[0]))
        print('Most recent user date of birth', int(df['Birth Year'].max()))
    else:
        print('The city you selected has no data available for Date of Birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def split_and_calculate_avg_trip_duration(df):
    " We want to see the average trip duration between users who have fill their gender info and the ones who did not."
    if 'Gender' in df.columns:
        with_gender = df[df['Gender'].notna()]
        no_gender = df[df['Gender'].isna()] 
    
        avg_trip_duration_with_gender = with_gender['Trip Duration'].mean()
        avg_trip_duration_withno_gender = no_gender['Trip Duration'].mean()
        print('The average trip duration for a user with gender info available is:', avg_trip_duration_with_gender, 'min' )
        print('The average trip duration for a user with gender info available is:', avg_trip_duration_withno_gender, 'min' )
    else:
        print('The city you selected has no data available for Gender')



def plot_avg_trip_duration_per_month(df):
    """Displays a graph: average trip duration per month."""
    avg_trip_duration_per_month = df.groupby('month')['Trip Duration'].mean()
    months = ['January', 'February', 'March', 'April', 'May', 'June'] 
    plt.figure(figsize=(10, 10))
    plt.plot(months, avg_trip_duration_per_month, marker='o')
    plt.title('Average Trip Duration per Month')
    plt.xlabel('Month')
    plt.ylabel('Average Trip Duration (seconds)')
    plt.grid(True)
    plt.show()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        split_and_calculate_avg_trip_duration(df)
    
        if month == 'all':    
            plot_avg_trip_duration_per_month(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()