import os 
import sys
import inspect 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2 
import io
import sqlalchemy 
import pprint
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Connect to database (Note: The package psychopg2 is required for Postgres to work with SQLAlchemy)
engine = sqlalchemy.create_engine("postgresql://postgres:Password@localhost/postgres")
con = engine.connect()

ids = [2544, 201939, 203081, 1629027, 203507]


from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

career0 = playergamelog.PlayerGameLog(player_id = ids[0],  season = SeasonAll.all)
career1 = playergamelog.PlayerGameLog(player_id = ids[1],  season = SeasonAll.all)
career2 = playergamelog.PlayerGameLog(player_id = ids[2],  season = SeasonAll.all)
career3 = playergamelog.PlayerGameLog(player_id = ids[3],  season = SeasonAll.all)
career4 = playergamelog.PlayerGameLog(player_id = ids[4],  season = SeasonAll.all)
x = career0.get_data_frames()[0]
y = career1.get_data_frames()[0]
z = career2.get_data_frames()[0]
aa = career3.get_data_frames()[0]
bb = career4.get_data_frames()[0]

result = pd.concat([x, y, z, aa, bb], axis=0)

result['GAME_DATE'] =pd.to_datetime(result.GAME_DATE)

result = result.sort_values(by = 'GAME_DATE', ascending=False)


result['Player_ID'] = result['Player_ID'].replace([2544, 201939, 203081, 1629027, 203507], ['lebron_james', 'stephen_curry', 'damian_lillard', 'trae_young', 'giannis_antetokounmpo'])


result.drop(['SEASON_ID', 'Game_ID', 'VIDEO_AVAILABLE'], axis=1, inplace=True)

xxx = result.copy()

xxx['FG_PCT'] = round(xxx['FG_PCT'] * 100,2)

xxx['FG3_PCT'] = round(xxx['FG3_PCT'] * 100,2)

xxx['FT_PCT'] = round(xxx['FT_PCT'] * 100,2)

xxx['GAME_DATE'] = pd.to_datetime(xxx['GAME_DATE'])

xxx = xxx.set_index("GAME_DATE")

# Add columns with year, month, and weekday name
xxx['YEAR'] = xxx.index.year
xxx['MONTH'] = xxx.index.month_name()
xxx['DAY'] = xxx.index.day
xxx['DAY_OF_WEEK'] = xxx.index.day_name()


xxx = xxx.reset_index()

stat_line = xxx[['Player_ID', 'GAME_DATE', 'MONTH', 'DAY', 'YEAR',
        'DAY_OF_WEEK', 'MATCHUP', 'WL', 'MIN', 'FGM', 
        'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 
        'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 
        'REB', 'AST', 'STL', 'BLK', 'TOV' 
        ,'PF', 'PTS', 'PLUS_MINUS']]


stat_line['GAME_DATE'] =pd.to_datetime(stat_line.GAME_DATE)

start_career = stat_line.sort_values(by = 'GAME_DATE')

start_career.index = np.arange(1, len(start_career) +1)

start_career['OPP'] = start_career['MATCHUP'].copy()

start_career['OPP'] = start_career['MATCHUP'].str[-3:]

atlantic = ['BKN', 'PHI', 'TOR', 'BOS', 'NYK', 'NJN']
southeast = ['MIA', 'CHA', 'WAS', 'ATL', 'ORL']
central = ['CHI', 'CLE', 'MIL', 'IND', 'DET']
pacific = ['PHX', 'GSW', 'LAL', 'LAC', 'SAC', 'GOS', 'PHO']
southwest = ['MEM', 'DAL', 'SAS', 'NOP', 'HOU', 'NOH', 'NOK']
northwest = ['UTA', 'DEN', 'MIN', 'POR', 'OKC', 'SEA']

western = [pacific, northwest, southwest]

eastern = [atlantic, southeast, central]

index = start_career.index

index.name = "GP"

def div_sort(a):
    if str(a) in (atlantic):
        return "ATLANTIC"
    elif str(a) in (southeast):
        return "SOUTHEAST"
    elif str(a) in (central):
        return "CENTRAL"
    elif str(a) in (pacific):
        return "PACIFIC"
    elif str(a) in (southwest):
        return "SOUTHWEST"
    else:
        return 'NORTHWEST'
    
def conf_sort(a):
    if str(a) in (atlantic):
        return "EASTERN"
    elif str(a) in (southeast):
        return "EASTERN"
    elif str(a) in (central):
        return "EASTERN"
    elif str(a) in (pacific):
        return "WESTERN"
    elif str(a) in (southwest):
        return "WESTERN"
    else:
        return 'WESTERN'
    
start_career['DIV'] = start_career['OPP'].apply(div_sort)
start_career['CONF'] = start_career['OPP'].apply(conf_sort)
start_career['LOCATION'] = start_career["MATCHUP"].map(lambda x: "HOME" if "vs." in x else "AWAY" if "@" in x else "")

start_career['G'] = start_career.index.copy()

start_career = start_career[['G', 'Player_ID', 'GAME_DATE', 'MONTH', 'DAY', 'YEAR',
        'DAY_OF_WEEK', 'MATCHUP', 'LOCATION', 'OPP', 'DIV', 'CONF', 'WL', 'MIN', 'FGM', 
        'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 
        'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 
        'REB', 'AST', 'STL', 'BLK', 'TOV' 
        ,'PF', 'PTS', 'PLUS_MINUS']]


#For loop used to created multiple dataframes from unique values of a given column
baller = start_career['Player_ID'].unique().tolist()
gbl = globals()
for i in baller:
    gbl[i] = start_career[start_career.Player_ID==i]
    
vcr = len(trae_young)
lbj = lebron_james.tail(vcr)
sc = stephen_curry.tail(vcr)
dolla = damian_lillard.tail(vcr)
ice = trae_young.tail(vcr)
greek_freak = giannis_antetokounmpo.tail(vcr)

ballers = [lbj, sc, dolla, ice, greek_freak]

nba_5 = pd.DataFrame()

for df in ballers:
    nba_5 = pd.concat([df, nba_5]) 
    
    
nba_5 = nba_5.sort_values(by='GAME_DATE', ascending=False)

lebron_james.to_sql(baller[0], con, if_exists='replace',index=False) 
stephen_curry.to_sql(baller[1], con, if_exists='replace',index=False) 
damian_lillard.to_sql(baller[2], con, if_exists='replace',index=False) 
trae_young.to_sql(baller[4], con, if_exists='replace',index=False) 
giannis_antetokounmpo.to_sql(baller[3], con, if_exists='replace',index=False) 
nba_5.to_sql('nba_5', con, if_exists='replace',index=False)

engine = create_engine('postgresql://postgres:Password@localhost/postgres')

conn = psycopg2.connect('postgresql://postgres:Password@localhost/postgres')
cur = conn.cursor()
con.close()

print('Finished update!')
