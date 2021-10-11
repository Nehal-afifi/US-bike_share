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
    print("Welcome to bikeshare data! \n")

    # Taksk0.1: Users choose a city, create a list with length=CITY_DATA , 
    #in future, it other cities are added codes will updated automatically
    all_cities=list(CITY_DATA)
    for i in range(len(all_cities)):
         message = ("For the city of {} ,The code is {}\n".format(all_cities[i],i+1))
         print(message)
    ##output of the for loop will code each city with a number, according to it's (position+1) in the dictionary 
    ## position is from 0 to 2, city codes are from 1 to 3, no manual recoding for city names
    ## user chooses a city "user input" by entering 1,2,3
     
    print("***choose a city to start\n***")
    city_code=input()
    
    ## check if user choice is valid, if enter a number out of range code restarts until a correct city chosen
    ## decode the user input number into city name
    ## print a confirmation message to the user with his choice
    while int(city_code) >  (len(all_cities)):
        print("Sorry, City choice invalid")
        city_code = input ("Please choose a number from 1 to 3\n")
        city_code=int(city_code)
    else:
        city= all_cities[int(city_code)-1]   
    print("Nice! you will get statistics for**",city.title())

    # Task0.2: get user input for month (all, january, february, ... , june)
    ##user enter month number from 1 to 6 representing january to June or all for all month
    print("Choose a month from January to June\n")   
    month = input ("Please type (all) to see all months   \nor select a number from 1 to 6 : January is 1 \n---------------------------\n\n")
    ## if user chooses all month, no filtering, if month choice greater than 6  print warning and loop, until a correct choice
    if month != "all":
        month=int(month)
        while month > 6:
             print('**Warning**  OUT OF RANGE!only months from 1 to 6 available')
             month = input ("Please choose a number from 1 to 6\n\n")
             month=int(month)
        else:
             month==month
             print("\n Month chosen is ***" ,month, "***")
    else:
         print("No Month filter applied")
   
    print("-"*40)


    #task0.3: TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    ##create a list matching week days short names to their full name, write the list in title for "first letter capital"
    days_dict = {"Su": "Sunday",
                 "Mo": "Monday",
                 "Tu": "Tuesday",
                 "We": "Wednesday", 
                 "Th": "Thursday",
                 "Fr": "Friday",
                 "Sa": "Saturday"}
    ## ask user to choose a day name by giving at least the first 2 letters of the day
    ## conver user input to title format NOTE!! dont trim now as user may choose "all" days
    ## if user choose all days, no warnings
    ## if user enters a day name, trim only the first 2 letters to avoid Typos, look up if the letters correspond to day name
    ## by consulting the dictionay, then return the day full name
    print("Choose a day? ")   
    day= input ("Please type (all) for no filtering \nor choose a weeek day  \n ")
    day=day.title()
      
    if day != "All":
        day=(day[0:2]).title() 
        while day not in days_dict:
            print('**Warning**  not a valid day')
            day = input ("please enter at least first 2 characters of the day \n\n")
            day=(day[0:2]).title()
        else:
           day=days_dict[day]
           print("\n Day chosen is ***" ,day, "***")
        
    else:
         print("No day filter applied")  
     
    print('-'*40)
    ## end of first function to gather user choices
    ## return values for city name, month and day selction or all
    ## saved as 3 inputs city,month,day
    ##print a confirmation method to the user with his choices! city,month and day
    print("you will see data for ** {}** city, for month *{}* and day * {}*".format(city,month,day))
    print("-"*40)
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
    ##task0.4 now the user choices are all ready and saved, start preparing your data 
    ## first, load the data of the selected city using the pd.read_csv command for the user specified city 
    df = pd.read_csv(CITY_DATA[city])
     ## read the column start time as a date, to start extracting information from it
    df['Start Time']=pd.to_datetime(df['Start Time'])
     ##define a new column"month" as a function from start time, which reads the month from the date
    df['month'] = df['Start Time'].dt.month
      ## extract the day name from the start time, append a new column"day_of_week" to the dataframe 
    df['day_of_week'] = df['Start Time'].dt.day_name()
     ## extract the hour of the start time and save to a new variable"hour"   
    df['hour'] = df['Start Time'].dt.hour
        
     ## now, the panel data is complete with variables of interest created
     ## time to consider user filters on month and day!!
     ## for the month, if user choice is all, no changes to dataset
     ## if user specifies a month,filter the dataset column"month" with the selected value
    if month !="all":
       df=(df[df['month']==int(month)])
    
      ## for the day column, if user doesnt choose a specific day and select"all", no change to df
      ## if the user chooses a day, filter the "day_of_week" column for the specified day
    if day !="All":
       df=(df[df['day_of_week']==day])
            
      ## print the first five rows of data to confirm filters are applied
     ## return the data frame to start calculating statistics
    #print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print("if you selcted a specific month, it will be the most frequent")
    print("Choose all month for most frequent month data")
    start_time = time.time()
    #Task1.1: TO DO: display the most common month
     ## most common month is the mode of month
     ## if user selects only one month, it will be the mode
     ## if user selects all month, this will calculate most frequent month#
    common_month=df["month"].mode()[0]
    common_month_percentage = df["month"].value_counts(normalize=True)*100
    common_month_count = df["month"].value_counts()
    common_month_stat=pd.concat([common_month_count,common_month_percentage],axis=1,join="inner")
    common_month_stat = common_month_stat.reset_index()
    common_month_stat.columns = ["Month",'No. of trips', '% Trips']
    print("="* 25)
    print("The dataset includes only {} month,from  the month {} to the month {}".format(len(common_month_count),min(df["month"]),max(df["month"])))
    print("The month with highest travel count is: {} with {:.2f} % share of trips".format(common_month,max(common_month_percentage)))
    print("="* 25)
    print("The number of trips each month and their share percentage is:")
    print(common_month_stat.round(2))
    
   #task1.2: The most popular hour
 ## summarize the start hour and get the mode/most frequect hour
    ## get the counts of travel per hour and the percentage
    ##print the count of travel and the percentage as a table
    print("When is it most busy? Let's have a look")
    common_hour=df["hour"].mode()[0]
    common_hour_percentage = df["hour"].value_counts(normalize=True)*100
    common_hour_count = df["hour"].value_counts()
    common_hour_stat=pd.concat([common_hour_count,common_hour_percentage],axis=1,join="inner")
    common_hour_stat = common_hour_stat.reset_index()
    common_hour_stat.columns = ["Hour",'No. of trips', '% Trips']

    print("="* 25)
    print("The dataset includes information on 24 hours bike rental")
    print("The Hour with highest travel count /\nMost popular is: **{}** with **{:.2f}** % shre of trips".format(common_hour,max(common_hour_percentage)))
    print("="* 25)
    print("The number of trips each hour and their share percentage is:")
    print(common_hour_stat.round(2).head())
    start_time = time.time()

    # Task 1.3: most busy day of the week TO DO: display the most common day of week
    ##calculate the most commen day, and the count and percentage of each day in the df
    ## group counts and frequencies
    print("Now, guess the busiest day of the weeek!\nif you applied a day filter ofcourse it will be the only day in database!\n select all for days statistics")
    common_day=df["day_of_week"].mode()[0]
    common_day_percentage = df["day_of_week"].value_counts(normalize=True)*100
    common_day_count = df["day_of_week"].value_counts()
    common_day_stat=pd.concat([common_day_count,common_day_percentage],axis=1,join="inner")
    common_day_stat = common_day_stat.reset_index()
    common_day_stat.columns = ["Day",'No. of trips', '% Trips']

    print("="* 25)
    print("The dataset includes information on the 7 days of the week")
    print("The Day with highest travel count is: {} with {:.2f} % shre of trips".format(common_day,max(common_day_percentage)))
    print("="* 25)
    print("The number of trips each day and their share percentage is:")
    print(common_day_stat.round(2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
     ###Tsk 2:popular stations and trips
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
   ##task2.1:start_station: most popular start station is the mode
   ## calculate the count and percentage of trips from each station
    ## present counts and percentage in a table
    ##calculate total number of start stations in database filtered
    popular_start_station=df["Start Station"].mode()[0]
    popular_start_station_percentage = df['Start Station'].value_counts(normalize=True)*100
    popular_start_station_count = df['Start Station'].value_counts()
    start_station_stat=pd.concat([popular_start_station_count,popular_start_station_percentage],axis=1,join="inner")
    start_station_stat.columns=['start_Count', 'Start_Frequency%'] 

    print("\n  out of * {} * stations and * {} * trips".format(len(popular_start_station_count),sum(popular_start_station_count)))
    print("\n  The Most popular start point is:*** ",popular_start_station,"***")
    print("="* 40)
    print("The 5 most common starting stations counts &  Frequency are :")
    print("="* 40)
    print(start_station_stat.head().round(2))
    print("="* 40)

    ##task 2.2: end station statistics
    ## calculate count and percentage of number of trips at each end station
    ## display the table of counts and percentages
    popular_end_station=df["End Station"].mode()[0]
    popular_end_station_percentage = df['End Station'].value_counts(normalize=True)*100
    popular_end_station_count = df['End Station'].value_counts()
    end_station_stat=pd.concat([popular_end_station_count,popular_end_station_percentage],axis=1,join="inner")
    end_station_stat.columns=['End_Count', 'End_Frequency%'] 
    print("\n   out of * {} * stations and * {}* trips ".format(len(popular_end_station_count),sum(popular_end_station_count)))
    print("\n  The Most popular end point is:***",popular_end_station,"***")
    print("="* 40)
    print(" Top 5 most common end stations counts & their Frequency are :")
    print("="* 40)
    print(end_station_stat.head().round(2))


    ##task 2.3: traval routes  defined by merging start station +:+ end station
    ## create a new column in the data and name it travel route
    ## calculate count of trips for each route and the percentage from the total trips as  per data filtration
    ## it is very common in the data that the route start and end in the same station, in all of thee 3 cities
    df["travel_route"]=df["Start Station"] +" to :"+df["End Station"].mode()[0]
    popular_travel_route=df["travel_route"].mode()[0]
    popular_route_percentage = df['travel_route'].value_counts(normalize=True)*100
    popular_route_count = df['travel_route'].value_counts()
    (len(popular_route_percentage))
    (len(popular_route_count))
    route_stat=pd.concat([popular_route_count,popular_route_percentage],axis=1,join="inner")
    route_stat.columns=['Route_Count', 'Route_Frequency %'] 

    print("="* 40)
    print("\n out of {} routes ,the Most popular route is:\n *** {} *** ".format(len(popular_route_count),popular_travel_route))
    print("="* 40)
    print(" Number of trips for the 5 most common routes & their percentage are :")
    print("="* 40)
    print(route_stat.head().round(2))
    print("="* 40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    ##task3 Trip duration: total and average travel time
    ## time of each trip is given in seconds, it is converted into minutes and hours
    ##Task3.1 & 3.2 the total and average trip time, rounded to 2 decimal places are displayed in a table
    ##The shortest trip in the database is displayed in seconds
    ##The longest trip is displayed in seconds and in days
    total_travel_time=df['Trip Duration'].sum()
    average_travel_time=df['Trip Duration'].mean()
    travel_time={"total":pd.Series([total_travel_time,total_travel_time/60,total_travel_time/3600], index = ['Seconds', 'Minutes', 'Hours']),
             "Average":pd.Series([average_travel_time,average_travel_time/60,average_travel_time/3600], index = ['Seconds', 'Minutes', 'Hours'])}
    travel_time_data = pd.DataFrame(travel_time)
    shortest_time=df['Trip Duration'].min()
    longest_time=df['Trip Duration'].max()
    
    print("The shortest trip was",shortest_time," seconds")
    print("the longest trip was",longest_time.round(2),"seconds, almost in days",(longest_time/(60*60*24)).round(2))
    print("="* 25)
    print('\nThe total travel time in seconds, minutes and hours is given by: \n', travel_time_data["total"].to_frame())
    print("="* 25)
    print("\nThe average travel time in seconds, minutes and hours is given by:\n",travel_time_data["Average"].round(2).to_frame())
    print("="* 25)
   
    start_time = time.time()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    ##task4: user info\type\gender&birth year if available for the city
    ##user type data is avalable for all cities
    ## count of each type, frequency is printed in a table "only i New York city 3 types!
     # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts().to_frame()
    user_percentage = df['User Type'].value_counts(normalize=True)*100
    user_count_stat=pd.concat([user_counts,user_percentage],axis=1,join="inner")
    user_count_stat.columns=['User_Count', 'User_Frequency%'] 
    print("There are {} types of users :  ".format(len(user_counts)))
    for i in range (len(user_counts)):
        print(user_counts.index.values[i])
    print("\n\n","*"* 40)
    print("The count and percentage of each type is:")
    print("*"* 40)
    print(user_count_stat.round(2))
    print("*"* 40)

    #Task 4.2: TO DO: Display counts of gender
    ##functions to calculate gender distriburion"only for NY and washington"
    ## start with if statement to check if the data is in dataseries
    ## if data is apended in the future no need to change the code
     ## display gender count and frequency in every dataset
    if 'Gender' in df.columns :
        print("\n Gender data is available for this city")
        user_gender = df['Gender'].value_counts()
        user_gender_percentage = df['Gender'].value_counts(normalize=True)*100
        gender_stat=pd.concat([user_gender,user_gender_percentage],axis=1,join="inner")
        gender_stat.columns=['Gender_Count', 'Gender_Frequency%']
        print("The Number of users from each Gender and their percentage is given by")
        print("#"* 40)
        print(gender_stat.round(2))
        print("#"* 40)
 
    else :
         print("\n Gender data is not available for this city")

 # task 4.2: TO DO: Display earliest, most recent, and most common year of birth
    ## functions to calculate year of birth statistics
    ## condition to check if data is available for the current city
    # calculate the most common city, earliest and latest
    if 'Birth Year' in df.columns :
       print("\n Birth Year data is available for this city")
       birth_year = df['Birth Year']
       popular_year =df['Birth Year'].mode()[0]
       print("Some statistics related to year of birth")
       print("-"* 40)
       print("The earliest year of birth is : ****"+"{:.0f}".format(min(birth_year)),"***");
       print("The latest year of birth is : *** "+"{:.0f}".format(max(birth_year)),"***");
       print("The most common year of birth is : ***"+"{:.0f}".format(popular_year),"***");
     
    else :
        print("\n Birth Year data is not available for this city")
    start_time = time.time()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def data_view(df):
    
    ##this functions asks whether the user wants to see how the raw data looks
    ## if the answer is yes , moe 5 rows are displayed everytime
    print('\nHave a look at raw data?\n')
    start_loc = 0
    while True:
        view_data = input('to view data in raws of 5 , enter : yes or no \n').lower()
        if view_data not in ['yes', 'no']:
            print('please enter either *yes* or *no* ')

        elif view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc+=5

        elif view_data == 'no':
            print('\nThank you for using Bike share !')
            break
            
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_view(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
