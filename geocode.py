import pandas as pd
import urllib.parse
import requests
import csv
import pickle

def get_location(query):
    response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=name,geometry&key=keyhere'.format(query))
    if response.status_code != 200:
        return None

    info = response.json()
    if len(info['candidates']) == 0:
        return None
    
    location_info = info['candidates'][0]['geometry']['location']
    return location_info

all_games = []
all_games.append(['Bowl', 'Date', 'Location', 'points1', 'points2', 'team1', 'team2', 'stadiumlat', 'stadiumlng', 'team1lat', 'team1lng', 'team2lat', 'team2lng'])
with open('games2.csv') as file:
    readCSV = csv.reader(file, delimiter=',')


    for row in readCSV:
        if row[0] == 'index':
            continue

        game = []

        for i in range(0,8):
            game.append(row[i])

        # get only the location, not the name of the bowl
        stadium = urllib.parse.quote(row[3].split(' - ')[-1:][0])
        stadium_loc = get_location(stadium)
        if stadium_loc == None:
            continue
        stadiumlat = stadium_loc['lat']
        stadiumlng = stadium_loc['lng']

        # Approximate names; even when the university names aren't completely correct, google places seems to pick it up
        team1 = urllib.parse.quote('University of ' + row[6].split('(')[0])
        team1_loc = get_location(team1)
        if team1_loc == None:
            continue
        team1_lat = team1_loc['lat']
        team1_lng = team1_loc['lng']
        
        team2 = urllib.parse.quote('University of ' + row[7].split('(')[0])
        team2_loc = get_location(team2)
        if team2_loc == None:
            continue
        team2_lat = team2_loc['lat']
        team2_lng = team2_loc['lng']


        game.append(stadiumlat)
        game.append(stadiumlng)
        game.append(team1_lat)
        game.append(team1_lng)
        game.append(team2_lat)
        game.append(team2_lng)

        all_games.append(game)

        
        print(game)

#backup incase the csv writing goes wrong
# I don't want to have to request google more than necessary
pickle.dump(all_games, open('all_games.p', 'wb'))

with open('geocoded.csv', mode='w') as outfile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for game in all_games:
        writer.writerow(game)



