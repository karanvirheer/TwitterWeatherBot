import tweepy
import requests
from datetime import datetime
import schedule
import time
from pprint import pprint

# TWITTER API -------------------------------------------------------------

spacing = "\n"
dashes = "-----------------------------------------------"

# You can find multiple Youtube videos and blog's that talk about how to acquire these things.
consumer_key = 'FILL IN WITH YOUR OWN'
consumer_secret = 'FILL IN WITH YOUR OWN'
access_token = 'FILL IN WITH YOUR OWN'
access_token_secret = 'FILL IN WITH YOUR OWN'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Constructs the API instance
api = tweepy.API(auth)

# Prints out the name of the twitter account
user = api.me()
print(spacing + "Successfully connected to: " + user.name)

# WEATHER API -------------------------------------------------------------

# If two cities with same name:
# Ex. [city, country initial] -> [London, GB] or [London, CA]
# Otherwise just put city name as is
# Ex. [Toronto]
city = 'INSERT CITY NAME - without brackets!'

# Get the API KEY from the OpenWeatherMaps website: https://home.openweathermap.org/api_keys
# You have to create an account to get the API key
weather_maps_api_key = 'Paste API Key Here'

url = 'http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units=metric'.format(
    city, weather_maps_api_key)

res = requests.get(url)

data = res.json()

# Uncomment the print statement below to see the weather data in the console
# pprint(data)

temp = data['main']['temp']
wind_speed = data['wind']['speed']

description = data['weather'][0]['description']

print_temp = 'Temperature: {}°C'.format(int(temp))
print_wind_speed = 'Wind Speed: {} m/s'.format(wind_speed)
print_weather_cond = 'Weather Conditions: {}'.format(description.capitalize())


def get_date_time():
    now = datetime.now()
    return now.strftime("%H:%M")


def print_weather_status():
    status = 'Latest Update @ ' + get_date_time() + ' EST'
    print('STATUS HAS BEEN UPDATED')

    api.update_status(status + '\n\n' + print_temp + '\n' + print_wind_speed + '\n' + print_weather_cond)


if __name__ == '__main__':
    # MAIN METHOD
    try:
        # You can change the '.hours' portion of the code to any other time interval you desire
        # Ex. seconds, minutes, days, weeks etc
        schedule.every(1).hours.do(print_weather_status)
        while 1:
            schedule.run_pending()
            time.sleep(1)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            # Do something special
            print('duplicate message')
        else:
            raise error
