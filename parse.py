import pandas as pd
import geopy.distance
import plotly.graph_objects as go

df = pd.read_csv('geocoded.csv')

def find_distance1(x):
    return geopy.distance.distance((x['stadiumlat'], x['stadiumlng']), (x['team1lat'], x['team1lng'])).miles

def find_distance2(x):
    return geopy.distance.distance((x['stadiumlat'], x['stadiumlng']), (x['team2lat'], x['team2lng'])).miles

# the winning team is always listed as team1
def find_winner(x):
    if x['points1'] == x['points2']:
        return 'tie'
    elif x['dist1'] > x['dist2']:
        return 'further'
    return 'closer'

def find_significant_advantage(x):
    if x['dist1'] < 100 and x['dist2'] > 200:
        return 'winner'
    elif x['dist2'] < 100 and x['dist1'] > 200:
        return 'loser'
    return 'n/s'

df['dist1'] = df.apply(find_distance1, axis=1)
df['dist2'] = df.apply(find_distance2, axis=1)
df['winner'] = df.apply(find_winner, axis=1)
df['significant'] = df.apply(find_significant_advantage, axis=1)
print(df)
print(df['significant'].value_counts())

labels = ['Closer Team Victory', 'Farther Team Victory']
values = [df['winner'].value_counts().to_dict()['closer'], df['winner'].value_counts().to_dict()['further']]

fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.2)])
fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=['lightgreen', 'darkorange'], line=dict(color='#000000', width=2)))
fig1.show()

labels = ['Significant Home Advantage Win', 'Significant Home Advantage Loss']
values = [df['significant'].value_counts().to_dict()['winner'], df['significant'].value_counts().to_dict()['loser']]

fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.2)])
fig2.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=['mediumturquoise', 'gold'], line=dict(color='#000000', width=2)))
fig2.show()

df.to_csv('final.csv')

