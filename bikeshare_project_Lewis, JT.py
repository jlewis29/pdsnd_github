import time
import pandas as pd
import numpy as np

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
    flag1 = True
    while flag1:
        city_input = input('Enter a city name to analyze: \n')
        try:
            # try this code; test lowercase version of input city name against available optoins
            csv = CITY_DATA[city_input.lower()]
            # if this works, exit loop
            flag1 = False
            city = city_input.lower()
        except:
            # this will execute if city_input is not in the dictionary
            # prompt user again until an appropriate city is chosen
            print('Error; invalid city input. Please try again.\n')
            flag1 = True           

    # get user input for month (all, january, february, ... , june)
    flag2 = True
    while flag2:
        month_input = input('Enter a month to filter by, from January to June, or "all" to apply no month filter: \n')
        valid_months = ['all','january','february','march','april','may','june']
        if month_input.lower() in valid_months:
            month = month_input.lower()
            flag2 = False
        else:
            print('Error; invalid month input. Please try again.')
            flag2 = True

    # get user input for day of week (all, monday, tuesday, ... sunday)
    flag3 = True
    while flag3:
        day_input = input('Enter a day of week to filter by, or "all" to apply no day filter: \n')
        valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if day_input.lower() in valid_days:
            day = day_input.lower()
            flag3 = False
        else:
            print('Error; invalid day input. Please try again.\n')
            flag3 = True

    #print('City, Month, Day = '+city+', '+month+', '+day)
    print('-'*40)
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
    #NOTE: this function is assuming good inputs are provided via get_filters() function
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # add month and day of week columns 
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[ df['Month'] == month ]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['Day of Week'] == day.title() ]
    # return the filtered dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # caluclate mode of month series
    month_mode = df['Month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most common month for riding: '+months[month_mode-1].title())

    # display the most common day of week
    # calculate mode of day of week
    day_mode = df['Day of Week'].mode()[0]
    print('Most common day of week for riding: '+str(day_mode))
    
    # display the most common start hour
    # add a column iwht the start hour to dataFrame
    df['Hour'] = df['Start Time'].dt.hour
    # calculate mode for hour
    hour_mode = df['Hour'].mode()[0]
    print('Most common hour to start riding: '+str(hour_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nMost commonly used starting station:'+str( df['Start Station'].mode()[0] ) )

    # display most commonly used end station
    print('\nMost commonly used ending station:'+str( df['End Station'].mode()[0] ) )

    # display most frequent combination of start station and end station trip\
    # combine start & end station into a variable
    df['Trip Endpoints'] = df['Start Station']+'_'+df['End Station']
    # get mode for that new variable
    trip_mode = df['Trip Endpoints'].mode()[0]
    trip_mode = trip_mode.split('_')
    print('\nMost common start-end trip stations: %s to %s' %(trip_mode[0], trip_mode[1]) )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time for bikeshare database = '+str(df['Trip Duration'].sum() ) )

    # display mean travel time
    print('Average travel time for bikeshare database = '+str(df['Trip Duration'].mean() ) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of different bikeshare user types:\n')
    print( df['User Type'].value_counts() )

    #NOTE: gender data not available for D.C., so catch exceptions
    print('\nCounts of different bikeshare user genders:\n')
    try:
        # Display counts of gender
        print( df['Gender'].value_counts() )
    except:
        print('\nWarning: Gender data not available for selected city. Continuing to next issue.')
        
    # similar for birth year, only available for some cities
    print('\nStatistics for bikeshare user age distributions:')
    try:
        # Display earliest, most recent, and most common year of birth
        print('\nEarliest year of birth for bikeshare users: '+str(df['Birth Year'].min()) )
        print('\nMost recent year of birth for bikeshare users: '+str(df['Birth Year'].max()) )
        print('\nMost common year of birth for bikeshare users: '+str(df['Birth Year'].mode()[0]) )
    except:
        print('\nWarning: Birth Year data not available for selected city. Continuing to next issue.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """ Upon user request, prints raw data from filtered input file for a query."""
    
    request = input('Would you like to print 5 lines of raw data from filtered table? Enter Y or N: ')
    if request.lower() in ['yes', 'y']:
        # allows slight variations of the yes input
        # all non-yes inputs will be translated as "NO"
        row_count = 0
        nrows, ncols = df.shape
        while row_count<nrows:
            # prevent array overrun
            n_iter = min(nrows-row_count,5)
            sub_df = df.iloc[row_count:row_count+n_iter,1:7]
            print(sub_df)
            row_count += n_iter
            stay = input('Continue with printing the next 5 lines of data? Enter Y or N: ')
            if stay not in ['yes', 'y']:
                break
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter Y or N: ')
        if restart.lower() not in  ['yes','y']:
            break


if __name__ == "__main__":
	print('\nExecuting main code!\n')
    main()
