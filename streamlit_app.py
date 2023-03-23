import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
import numpy as np
import math
from scipy import stats
from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle, Arc

import matplotlib as mpl
mpl.rcParams["axes.spines.right"] = True
mpl.rcParams["axes.spines.top"] = True
mpl.rcParams["axes.spines.left"] = True
mpl.rcParams["axes.spines.bottom"] = True

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

font_dirs = ["//Users//sissigarduno//Downloads"]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

plt.rcParams['font.family'] = "Poppins"
plt.rcParams['font.size'] = '10.6'

image = Image.open("Logos/EUROCUP.png")
st.sidebar.image(image)


#Web scraping of data
df = pd.read_csv("Data Eurocup - Stats.csv")
df_shots = pd.read_csv("Data Eurocup - Shots.csv")
df_round = pd.read_csv("Data Eurocup - Shots.csv")

#Filters
st.sidebar.header('Filters')
st.sidebar.write("Select a range of rounds :")
begin = st.sidebar.slider('First game :', 1, 18, 1)
end = st.sidebar.slider('Last game :', 1, 18, 18)
location = st.sidebar.selectbox('Home / Away :', ('All', 'Home', 'Away'))

#Filtering data
df = df[df['Round'].between(begin, end)]
df['Pace_home'] = df["FieldGoalsAttempted2_home"] + df["FieldGoalsAttempted3_home"] + 0.44*df["FreeThrowsAttempted_home"] - df["OffensiveRebounds_home"] + df["Turnovers_home"]
df['Pace_away'] = df["FieldGoalsAttempted2_away"] + df["FieldGoalsAttempted3_away"] + 0.44*df["FreeThrowsAttempted_away"] - df["OffensiveRebounds_away"] + df["Turnovers_away"]

#Data treatment
home = df.groupby('Team_home').agg({'Game_id':'count','Points_home':'sum','Pace_home':'sum','FieldGoalsMade2_home':'sum','FieldGoalsAttempted2_home':'sum',
                                      'FieldGoalsMade3_home':'sum','FieldGoalsAttempted3_home':'sum','FreeThrowsMade_home':'sum',
                                      'FreeThrowsAttempted_home':'sum','OffensiveRebounds_home':'sum','DefensiveRebounds_home':'sum',
                                      'TotalRebounds_home':'sum','Assistances_home':'sum','Steals_home':'sum','Turnovers_home':'sum',
                                      'BlocksFavour_home':'sum','BlocksAgainst_home':'sum','FoulsCommited_home':'sum',
                                      'FoulsReceived_home':'sum','Valuation_home':'sum','Points_away':'sum','Pace_away':'sum','FieldGoalsMade2_away':'sum',
                                      'FieldGoalsAttempted2_away':'sum','FieldGoalsMade3_away':'sum','FieldGoalsAttempted3_away':'sum',
                                      'FreeThrowsMade_away':'sum','FreeThrowsAttempted_away':'sum','OffensiveRebounds_away':'sum',
                                      'DefensiveRebounds_away':'sum','TotalRebounds_away':'sum','Assistances_away':'sum',
                                      'Steals_away':'sum','Turnovers_away':'sum','BlocksFavour_away':'sum','BlocksAgainst_away':'sum',
                                      'FoulsCommited_away':'sum','FoulsReceived_away':'sum','Valuation_away':'sum'}).reset_index().rename(columns={'Game_id':'Nb_games',
                    'Points_home': 'Points_team', 'Pace_home': 'Pace_team', 'FieldGoalsMade2_home': 'FieldGoalsMade2_team', 'FieldGoalsAttempted2_home': 'FieldGoalsAttempted2_team', 
                     'FieldGoalsMade3_home': 'FieldGoalsMade3_team', 'FieldGoalsAttempted3_home': 'FieldGoalsAttempted3_team', 
                     'FreeThrowsMade_home': 'FreeThrowsMade_team', 'FreeThrowsAttempted_home': 'FreeThrowsAttempted_team', 
                     'OffensiveRebounds_home': 'OffensiveRebounds_team', 'DefensiveRebounds_home': 'DefensiveRebounds_team', 
                     'TotalRebounds_home': 'TotalRebounds_team', 'Assistances_home': 'Assistances_team', 'Steals_home': 'Steals_team', 
                     'Turnovers_home': 'Turnovers_team', 'BlocksFavour_home': 'BlocksFavour_team', 'BlocksAgainst_home': 'BlocksAgainst_team', 
                     'FoulsCommited_home': 'FoulsCommited_team', 'FoulsReceived_home': 'FoulsReceived_team', 'Valuation_home': 'Valuation_team', 
                     'Points_away': 'Points_opp', 'Pace_away': 'Pace_opp', 'FieldGoalsMade2_away': 'FieldGoalsMade2_opp', 'FieldGoalsAttempted2_away': 'FieldGoalsAttempted2_opp', 
                     'FieldGoalsMade3_away': 'FieldGoalsMade3_opp', 'FieldGoalsAttempted3_away': 'FieldGoalsAttempted3_opp', 
                     'FreeThrowsMade_away': 'FreeThrowsMade_opp', 'FreeThrowsAttempted_away': 'FreeThrowsAttempted_opp', 
                     'OffensiveRebounds_away': 'OffensiveRebounds_opp', 'DefensiveRebounds_away': 'DefensiveRebounds_opp', 
                     'TotalRebounds_away': 'TotalRebounds_opp', 'Assistances_away': 'Assistances_opp', 'Steals_away': 'Steals_opp', 
                     'Turnovers_away': 'Turnovers_opp', 'BlocksFavour_away': 'BlocksFavour_opp', 'BlocksAgainst_away': 'BlocksAgainst_opp', 
                     'FoulsCommited_away': 'FoulsCommited_opp', 'FoulsReceived_away': 'FoulsReceived_opp', 
                     'Valuation_away': 'Valuation_opp'})
home.rename(columns={'Team_home': 'Team_name'}, inplace=True)

away = df.groupby('Team_away').agg({'Game_id':'count','Points_home':'sum','Pace_home':'sum','FieldGoalsMade2_home':'sum','FieldGoalsAttempted2_home':'sum',
                                      'FieldGoalsMade3_home':'sum','FieldGoalsAttempted3_home':'sum','FreeThrowsMade_home':'sum',
                                      'FreeThrowsAttempted_home':'sum','OffensiveRebounds_home':'sum','DefensiveRebounds_home':'sum',
                                      'TotalRebounds_home':'sum','Assistances_home':'sum','Steals_home':'sum','Turnovers_home':'sum',
                                      'BlocksFavour_home':'sum','BlocksAgainst_home':'sum','FoulsCommited_home':'sum',
                                      'FoulsReceived_home':'sum','Valuation_home':'sum','Points_away':'sum','Pace_away':'sum','FieldGoalsMade2_away':'sum',
                                      'FieldGoalsAttempted2_away':'sum','FieldGoalsMade3_away':'sum','FieldGoalsAttempted3_away':'sum',
                                      'FreeThrowsMade_away':'sum','FreeThrowsAttempted_away':'sum','OffensiveRebounds_away':'sum',
                                      'DefensiveRebounds_away':'sum','TotalRebounds_away':'sum','Assistances_away':'sum',
                                      'Steals_away':'sum','Turnovers_away':'sum','BlocksFavour_away':'sum','BlocksAgainst_away':'sum',
                                      'FoulsCommited_away':'sum','FoulsReceived_away':'sum','Valuation_away':'sum'}).reset_index().rename(columns={'Game_id':'Nb_games',
                    'Points_home': 'Points_opp', 'Pace_home': 'Pace_opp', 'FieldGoalsMade2_home': 'FieldGoalsMade2_opp', 'FieldGoalsAttempted2_home': 'FieldGoalsAttempted2_opp', 
                     'FieldGoalsMade3_home': 'FieldGoalsMade3_opp', 'FieldGoalsAttempted3_home': 'FieldGoalsAttempted3_opp', 
                     'FreeThrowsMade_home': 'FreeThrowsMade_opp', 'FreeThrowsAttempted_home': 'FreeThrowsAttempted_opp', 
                     'OffensiveRebounds_home': 'OffensiveRebounds_opp', 'DefensiveRebounds_home': 'DefensiveRebounds_opp', 
                     'TotalRebounds_home': 'TotalRebounds_opp', 'Assistances_home': 'Assistances_opp', 'Steals_home': 'Steals_opp', 
                     'Turnovers_home': 'Turnovers_opp', 'BlocksFavour_home': 'BlocksFavour_opp', 'BlocksAgainst_home': 'BlocksAgainst_opp', 
                     'FoulsCommited_home': 'FoulsCommited_opp', 'FoulsReceived_home': 'FoulsReceived_opp', 'Valuation_home': 'Valuation_opp', 
                     'Points_away': 'Points_team', 'Pace_away': 'Pace_team', 'FieldGoalsMade2_away': 'FieldGoalsMade2_team', 'FieldGoalsAttempted2_away': 'FieldGoalsAttempted2_team', 
                     'FieldGoalsMade3_away': 'FieldGoalsMade3_team', 'FieldGoalsAttempted3_away': 'FieldGoalsAttempted3_team', 
                     'FreeThrowsMade_away': 'FreeThrowsMade_team', 'FreeThrowsAttempted_away': 'FreeThrowsAttempted_team', 
                     'OffensiveRebounds_away': 'OffensiveRebounds_team', 'DefensiveRebounds_away': 'DefensiveRebounds_team', 
                     'TotalRebounds_away': 'TotalRebounds_team', 'Assistances_away': 'Assistances_team', 'Steals_away': 'Steals_team', 
                     'Turnovers_away': 'Turnovers_team', 'BlocksFavour_away': 'BlocksFavour_team', 'BlocksAgainst_away': 'BlocksAgainst_team', 
                     'FoulsCommited_away': 'FoulsCommited_team', 'FoulsReceived_away': 'FoulsReceived_team', 
                     'Valuation_away': 'Valuation_team'})
away.rename(columns={'Team_away': 'Team_name'}, inplace=True)

if location == "Home":
    result = home
elif location == "Away":
    result = away
else:
    result = pd.concat([home, away])

result = result.groupby(['Team_name']).agg({'Nb_games':'sum', 'Points_team':'sum','Pace_team':'sum','FieldGoalsMade2_team':'sum','FieldGoalsAttempted2_team':'sum',
                                             'FieldGoalsMade3_team':'sum','FieldGoalsAttempted3_team':'sum','FreeThrowsMade_team':'sum',
                                             'FreeThrowsAttempted_team':'sum','OffensiveRebounds_team':'sum','DefensiveRebounds_team':'sum',
                                             'TotalRebounds_team':'sum','Assistances_team':'sum','Steals_team':'sum',
                                             'Turnovers_team':'sum','BlocksFavour_team':'sum','BlocksAgainst_team':'sum',
                                             'FoulsCommited_team':'sum','FoulsReceived_team':'sum','Valuation_team':'sum',
                                             'Points_opp':'sum','Pace_opp':'sum','FieldGoalsMade2_opp':'sum','FieldGoalsAttempted2_opp':'sum',
                                             'FieldGoalsMade3_opp':'sum','FieldGoalsAttempted3_opp':'sum','FreeThrowsMade_opp':'sum',
                                             'FreeThrowsAttempted_opp':'sum','OffensiveRebounds_opp':'sum','DefensiveRebounds_opp':'sum',
                                             'TotalRebounds_opp':'sum','Assistances_opp':'sum','Steals_opp':'sum','Turnovers_opp':'sum',
                                             'BlocksFavour_opp':'sum','BlocksAgainst_opp':'sum','FoulsCommited_opp':'sum',
                                             'FoulsReceived_opp':'sum','Valuation_opp':'sum'})
result = result.rename_axis('Team_name').reset_index()

#Creation of Data
result['ORTG'] = result['Points_team'] / result['Pace_team'] * 100
result['DRTG'] = result['Points_opp'] / result['Pace_opp'] * 100
result['NetRTG'] = result['ORTG'] - result['DRTG']
result['eFG%'] = ((result['FieldGoalsMade2_team'] + result['FieldGoalsMade3_team']*1.5) / (result['FieldGoalsAttempted2_team'] + result['FieldGoalsAttempted3_team'])) * 100
result['eFG% opp'] = ((result['FieldGoalsMade2_opp'] + result['FieldGoalsMade3_opp']*1.5) / (result['FieldGoalsAttempted2_opp'] + result['FieldGoalsAttempted3_opp'])) * 100
result['TS%'] = (result['Points_team'] / (2*((result['FieldGoalsAttempted2_team'] + result['FieldGoalsAttempted3_team']) + 0.44*result['FreeThrowsAttempted_team']))) * 100
result['TS% opp'] = (result['Points_opp'] / (2*((result['FieldGoalsAttempted2_opp'] + result['FieldGoalsAttempted3_opp']) + 0.44*result['FreeThrowsAttempted_opp']))) * 100
result['AST/TO'] = result['Assistances_team'] / result['Turnovers_team']
result['AST/TO opp'] = result['Assistances_opp'] / result['Turnovers_opp']
result['TOV%'] = (result['Turnovers_team'] / result['Pace_team']) * 100
result['TOV% opp'] = (result['Turnovers_opp'] / result['Pace_opp']) * 100
result['OREB%'] = (result['OffensiveRebounds_team'] / (result['OffensiveRebounds_team'] + result['DefensiveRebounds_opp'])) * 100
result['OREB% opp'] = (result['OffensiveRebounds_opp'] / (result['OffensiveRebounds_opp'] + result['DefensiveRebounds_team'])) * 100
result['DREB%'] = (result['DefensiveRebounds_team'] / (result['DefensiveRebounds_team'] + result['OffensiveRebounds_opp'])) * 100
result['DREB% opp'] = (result['DefensiveRebounds_opp'] / (result['DefensiveRebounds_opp'] + result['OffensiveRebounds_team'])) * 100
result['BLK%'] = (result['BlocksFavour_team'] / result['FieldGoalsAttempted2_opp']) * 100
result['BLK% opp'] = (result['BlocksFavour_opp'] / result['FieldGoalsAttempted2_team']) * 100
result['STL%'] = (result['Steals_team'] / result['Pace_opp']) * 100
result['STL% opp'] = (result['Steals_opp'] / result['Pace_team']) * 100
result['Poss/G'] = result['Pace_team'] / result['Nb_games']
result['Poss/G opp'] = result['Pace_opp'] / result['Nb_games']
result['FTAr'] = (result['FreeThrowsAttempted_team'] / (result['FieldGoalsAttempted2_team'] + result['FieldGoalsAttempted3_team'])) * 100
result['FTAr opp'] = (result['FreeThrowsAttempted_opp'] / (result['FieldGoalsAttempted2_opp'] + result['FieldGoalsAttempted3_opp'])) * 100
result['2P%'] = (result['FieldGoalsMade2_team'] / result['FieldGoalsAttempted2_team'])*100
result['2P% opp'] = (result['FieldGoalsMade2_opp'] / result['FieldGoalsAttempted2_opp'])*100
result['3P%'] = (result['FieldGoalsMade3_team'] / result['FieldGoalsAttempted3_team'])*100
result['3P% opp'] = (result['FieldGoalsMade3_opp'] / result['FieldGoalsAttempted3_opp'])*100
result['FT%'] = (result['FreeThrowsMade_team'] / result['FreeThrowsAttempted_team'])*100
result['FT% opp'] = (result['FreeThrowsMade_opp'] / result['FreeThrowsAttempted_opp'])*100
result["FGA% 2PT"] = (result["FieldGoalsAttempted2_team"] / (result["FieldGoalsAttempted2_team"] + result["FieldGoalsAttempted3_team"])) * 100
result["FGA% 3PT"] = (result["FieldGoalsAttempted3_team"] / (result["FieldGoalsAttempted2_team"] + result["FieldGoalsAttempted3_team"])) * 100
result["PTS% 2PT"] = (result["FieldGoalsMade2_team"]*2 / (result["FieldGoalsMade2_team"]*2 + result["FieldGoalsMade3_team"]*3 + result["FreeThrowsMade_team"])) * 100
result["PTS% 3PT"] = (result["FieldGoalsMade3_team"]*3 / (result["FieldGoalsMade2_team"]*2 + result["FieldGoalsMade3_team"]*3 + result["FreeThrowsMade_team"])) * 100
result["PTS% FT"] = (result["FreeThrowsMade_team"] / (result["FieldGoalsMade2_team"]*2 + result["FieldGoalsMade3_team"]*3 + result["FreeThrowsMade_team"])) * 100
result["FGM% AST"] = (result["Assistances_team"] / (result["FieldGoalsMade2_team"] + result["FieldGoalsMade3_team"])) * 100
result["FGM% UAST"] = (1-(result["Assistances_team"] / (result["FieldGoalsMade2_team"] + result["FieldGoalsMade3_team"]))) * 100
result["FGA% 2PT opp"] = (result["FieldGoalsAttempted2_opp"] / (result["FieldGoalsAttempted2_opp"] + result["FieldGoalsAttempted3_opp"])) * 100
result["FGA% 3PT opp"] = (result["FieldGoalsAttempted3_opp"] / (result["FieldGoalsAttempted2_opp"] + result["FieldGoalsAttempted3_opp"])) * 100
result["PTS% 2PT opp"] = (result["FieldGoalsMade2_opp"]*2 / (result["FieldGoalsMade2_opp"]*2 + result["FieldGoalsMade3_opp"]*3 + result["FreeThrowsMade_opp"])) * 100
result["PTS% 3PT opp"] = (result["FieldGoalsMade3_opp"]*3 / (result["FieldGoalsMade2_opp"]*2 + result["FieldGoalsMade3_opp"]*3 + result["FreeThrowsMade_opp"])) * 100
result["PTS% FT opp"] = (result["FreeThrowsMade_opp"] / (result["FieldGoalsMade2_opp"]*2 + result["FieldGoalsMade3_opp"]*3 + result["FreeThrowsMade_opp"])) * 100
result["FGM% AST opp"] = (result["Assistances_opp"] / (result["FieldGoalsMade2_opp"] + result["FieldGoalsMade3_opp"])) * 100
result["FGM% UAST opp"] = (1-(result["Assistances_opp"] / (result["FieldGoalsMade2_opp"] + result["FieldGoalsMade3_opp"]))) * 100
result['PTS/G'] = result['Points_team'] / result['Nb_games']
result['2PM/G'] = result['FieldGoalsMade2_team'] / result['Nb_games']
result['2PA/G'] = result['FieldGoalsAttempted2_team'] / result['Nb_games']
result['3PM/G'] = result['FieldGoalsMade3_team'] / result['Nb_games']
result['3PA/G'] = result['FieldGoalsAttempted3_team'] / result['Nb_games']
result['FTM/G'] = result['FreeThrowsMade_team'] / result['Nb_games']
result['FTA/G'] = result['FreeThrowsAttempted_team'] / result['Nb_games']
result['OREB/G'] = result['OffensiveRebounds_team'] / result['Nb_games']
result['DREB/G'] = result['DefensiveRebounds_team'] / result['Nb_games']
result['TREB/G'] = result['TotalRebounds_team'] / result['Nb_games']
result['AST/G'] = result['Assistances_team'] / result['Nb_games']
result['STL/G'] = result['Steals_team'] / result['Nb_games']
result['TOV/G'] = result['Turnovers_team'] / result['Nb_games']
result['BLK/G'] = result['BlocksFavour_team'] / result['Nb_games']
result['BLKA/G'] = result['BlocksAgainst_team'] / result['Nb_games']
result['PF/G'] = result['FoulsCommited_team'] / result['Nb_games']
result['PFD/G'] = result['FoulsReceived_team'] / result['Nb_games']
result['EVAL/G'] = result['Valuation_team'] / result['Nb_games']
result['PTS/G opp'] = result['Points_opp'] / result['Nb_games']
result['2PM/G opp'] = result['FieldGoalsMade2_opp'] / result['Nb_games']
result['2PA/G opp'] = result['FieldGoalsAttempted2_opp'] / result['Nb_games']
result['3PM/G opp'] = result['FieldGoalsMade3_opp'] / result['Nb_games']
result['3PA/G opp'] = result['FieldGoalsAttempted3_opp'] / result['Nb_games']
result['FTM/G opp'] = result['FreeThrowsMade_opp'] / result['Nb_games']
result['FTA/G opp'] = result['FreeThrowsAttempted_opp'] / result['Nb_games']
result['OREB/G opp'] = result['OffensiveRebounds_opp'] / result['Nb_games']
result['DREB/G opp'] = result['DefensiveRebounds_opp'] / result['Nb_games']
result['TREB/G opp'] = result['TotalRebounds_opp'] / result['Nb_games']
result['AST/G opp'] = result['Assistances_opp'] / result['Nb_games']
result['STL/G opp'] = result['Steals_opp'] / result['Nb_games']
result['TOV/G opp'] = result['Turnovers_opp'] / result['Nb_games']
result['BLK/G opp'] = result['BlocksFavour_opp'] / result['Nb_games']
result['BLKA/G opp'] = result['BlocksAgainst_opp'] / result['Nb_games']
result['PF/G opp'] = result['FoulsCommited_opp'] / result['Nb_games']
result['PFD/G opp'] = result['FoulsReceived_opp'] / result['Nb_games']
result['EVAL/G opp'] = result['Valuation_opp'] / result['Nb_games']

#Team Filter
st.sidebar.write("Select a team : ")
teamname = result['Team_name']
teamselection = st.sidebar.selectbox('Team :',(teamname), label_visibility="collapsed")
st.sidebar.write("##")
st.sidebar.write('*Rounds available : from ',df_round['Round'].min(),' to ', df_round['Round'].max())

#VIZ 1
#Graph
result.sort_index()
def getImage(path, zoom=1):
    return OffsetImage(plt.imread(path), zoom=0.225)

paths = [
    'Logos/7BET-LIETKABELIS PANEVEZYS.png',
    'Logos/BUDUCNOST VOLI PODGORICA.png',
    'Logos/CEDEVITA OLIMPIJA LJUBLJANA.png',
    'Logos/DOLOMITI ENERGIA TRENTO.png',
    'Logos/FRUTTI EXTRA BURSASPOR.png',
    'Logos/GERMANI BRESCIA.png',
    'Logos/GRAN CANARIA.png',
    'Logos/HAPOEL TEL AVIV.png',
    'Logos/JOVENTUT BADALONA.png',
    'Logos/LONDON LIONS.png',
    'Logos/MINCIDELICE JL BOURG EN BRESSE.png',
    'Logos/PARIS BASKETBALL.png',
    'Logos/PROMETEY SLOBOZHANSKE.png',
    'Logos/PROMITHEAS PATRAS.png',
    'Logos/RATIOPHARM ULM.png',
    'Logos/SLASK WROCLAW.png',
    'Logos/TURK TELEKOM ANKARA.png',
    'Logos/U-BT CLUJ-NAPOCA.png',
    'Logos/UMANA REYER VENICE.png',
    'Logos/VEOLIA TOWERS HAMBURG.png'
]
    
x = result['ORTG']
y = result['DRTG']

fig, ax = plt.subplots()
ax.scatter(x, y, c="white") 
# Move left y-axis and bottom x-axis to centre, passing through (0,0)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Others
ax.invert_yaxis()
ax.tick_params(axis='both', which='major', labelsize=8)
ax.text(105.5, 120, 'Defensive Rating', rotation = 'vertical', fontsize = 'xx-small')
ax.text(90, 104.5, 'Offensive Rating', rotation = 'horizontal', fontsize = 'xx-small')
ax.text(90.5, 93.3, 'Positive Teams', rotation = -35, fontsize = 'xx-small', c="lightgrey", weight='bold')
ax.text(90, 94.4, 'Negative Teams', rotation = -35, fontsize = 'xx-small', c="lightgrey", weight='bold')
ax.text(96, 92, 'Net +5', rotation = -35, fontsize = 'xx-small', c="lightgrey")
ax.text(100.8, 92, 'Net +10', rotation = -35, fontsize = 'xx-small', c="lightgrey")
ax.text(105.8, 92, 'Net +15', rotation = -35, fontsize = 'xx-small', c="lightgrey")
ax.text(90, 95.8, 'Net -5', rotation = -35, fontsize = 'xx-small', c="lightgrey")
ax.text(90, 101, 'Net -10', rotation = -35, fontsize = 'xx-small', c="lightgrey")
ax.text(91, 107, 'Net -15', rotation = -35, fontsize = 'xx-small', c="lightgrey")
ax.plot([85, 130], [85, 130], ls="--", c="lightgrey", linewidth=1)
ax.plot([85, 125], [90, 130], ls="--", c="lightgrey", linewidth=0.5)
ax.plot([85, 120], [95, 130], ls="--", c="lightgrey", linewidth=0.5)
ax.plot([85, 115], [100, 130], ls="--", c="lightgrey", linewidth=0.5)
ax.plot([90, 130], [85, 125], ls="--", c="lightgrey", linewidth=0.5)
ax.plot([95, 130], [85, 120], ls="--", c="lightgrey", linewidth=0.5)
ax.plot([100, 130], [85, 115], ls="--", c="lightgrey", linewidth=0.5)
ax.set(xlim=(90, 120), ylim=(120, 90))

for x0, y0, path in zip(x, y,paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
    ax.add_artist(ab)
    
# VIZ 2
params = ['ORTG', 'eFG%', 'TS%', 'AST/TO', 'TOV%', 'OREB%', 'DRTG', 'DREB%', 'BLK%', 'STL%', 'NetRTG', 'Poss/G', 'FTAr', 'EVAL/G']

pizza = (result[['Team_name', 'ORTG', 'eFG%', 'TS%', 'AST/TO', 'TOV%', 'OREB%', 'DRTG', 'DREB%', 'BLK%', 'STL%', 'NetRTG', 'Poss/G', 'FTAr', 'EVAL/G']])
pizza = pizza.fillna(0)

team = pizza.loc[pizza['Team_name'] == teamselection].reset_index()
team = list(team.loc[0])
team = team[2:]

values = []
for x in range(len(params)):
    values.append(math.floor(stats.percentileofscore(pizza[params[x]], team[x])))
    
values[4] = 100 - values[4]
values[6] = 100 - values[6]

    
 # color for the slices and text
slice_colors = ["#1A78CF"] * 3 + ["#FF9300"] * 3 + ["#D70232"] * 4 + ["grey"] * 4
box_colors = ["white"] * 14
box_font_colors = ["#252528"] * 14
text_colors = ["black"] * 14

# instantiate PyPizza class
baker = PyPizza(
    params=params,  # list of parameters
    background_color="#FFFFFF",  # background color
    straight_line_color="white",  # color for straight lines
    straight_line_lw=1,  # linewidth for straight lines
    last_circle_lw=0,  # linewidth of last circle
    other_circle_lw=0,  # linewidth for other circles
    inner_circle_size=0  # size of inner circle
)

# plot pizza
fig1, ax = baker.make_pizza(
    values,  # list of values
    figsize=(8, 8.5),  # adjust figsize according to your need
    color_blank_space="same",  # use same color to fill blank space
    slice_colors=slice_colors,  # color for individual slices
    value_colors=box_colors,  # color for the value-text
    value_bck_colors=box_font_colors,  # color for the blank spaces
    blank_alpha=0.4,# alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#212124", zorder=2, linewidth=1
    ),  # values to be used when plotting slices
    kwargs_params=dict(
        color="black", fontsize=11,
        va="center"
    ),  # values to be used when adding parameter
    kwargs_values=dict(
        color="black", fontsize=11,
        zorder=3,
        bbox=dict(
            edgecolor="black", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )  # values to be used when adding parameter-values
)

#Legend
# add text
fig1.text(0.5, 0.97, teamselection, size=20, color="#000000", ha="center")
fig1.text(
    0.1, 0.925, "Attacking", size=10, color="#000000"
)
fig1.text(
    0.1, 0.900, "Possession", size=10, color="#000000"
)
fig1.text(
    0.1, 0.875, "Defending", size=10, color="#000000"
)
fig1.text(
    0.1, 0.850, "Other", size=10, color="#000000"
)

# add rectangles
fig1.patches.extend([
    plt.Rectangle(
        (0.06, 0.922), 0.025, 0.021, fill=True, color="#1a78cf",
        transform=fig1.transFigure, figure=fig1
    ),
    plt.Rectangle(
        (0.06, 0.897), 0.025, 0.021, fill=True, color="#ff9300",
        transform=fig1.transFigure, figure=fig1
    ),
    plt.Rectangle(
        (0.06, 0.872), 0.025, 0.021, fill=True, color="#d70232",
        transform=fig1.transFigure, figure=fig1
    ),
    plt.Rectangle(
        (0.06, 0.847), 0.025, 0.021, fill=True, color="grey",
        transform=fig1.transFigure, figure=fig1
    ),
])

# VIZ 4
def draw_court(ax=None, color='black', lw=1, outer_lines=True):
    """
    FIBA basketball court dimensions:
    https://www.msfsports.com.au/basketball-court-dimensions/
    It seems like the Euroleauge API returns the shooting positions
    in resolution of 1cm x 1cm.
    """
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 45.72cm so it has a radius 45.72/2 cms
    hoop = Circle((0, 0), radius=45.72 / 2, linewidth=lw, color=color,
                  fill=False)

    # Create backboard
    backboard = Rectangle((-90, -157.5 + 120), 180, -1, linewidth=lw,
                          color=color)

    # The paint
    # Create the outer box of the paint
    outer_box = Rectangle((-490 / 2, -157.5), 490, 580, linewidth=lw,
                          color=color, fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-360 / 2, -157.5), 360, 580, linewidth=lw,
                          color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 580 - 157.5), 360, 360, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 580 - 157.5), 360, 360, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 2 * 125, 2 * 125, theta1=0, theta2=180,
                     linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines
    corner_three_a = Rectangle((-750 + 90, -157.5), 0, 305, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((750 - 90, -157.5), 0, 305, linewidth=lw,
                               color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 2 * 675, 2 * 675, theta1=12, theta2=167.5,
                    linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box,
                      restricted, top_free_throw, bottom_free_throw,
                      corner_three_a, corner_three_b, three_arc]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def plot_scatter(made, miss, title=None):
    """
    Scatter plot of made and missed shots
    """
    plt.figure()
    draw_court()
    plt.plot(miss['COORD_X'], miss['COORD_Y'], 'o', color='red', label='Missed', alpha=0.6, markeredgecolor='black', markersize=4)
    plt.plot(made['COORD_X'], made['COORD_Y'], 'o', label='Made', color='green', alpha=0.6, markeredgecolor='black', markersize=4)
    plt.legend(fontsize="x-small", frameon=False)
    plt.xlim([-800, 800])
    plt.ylim([-155, 1300])
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    plt.show()
    return

# split the home and away teams, their made and missed shots
df_shots = df_shots[df_shots['Round'].between(begin, end)]
df_shots['TEAM'] = df_shots['TEAM'].str.strip()  # team id contains trailing white space
df_shots['ID_PLAYER'] = df_shots['ID_PLAYER'].str.strip()  # player id contains trailing white space
home_df = df_shots[df_shots['TEAM'] == teamselection]
fg_made_home_df = home_df[home_df['ID_ACTION'].isin(['2FGM', '3FGM'])]
fg_miss_home_df = home_df[home_df['ID_ACTION'].isin(['2FGA', '3FGA'])]

# scatter shot chart of PAOs
fig2 = plot_scatter(fg_made_home_df, fg_miss_home_df, title=teamselection)

#Differents dataframes
statsavancees = (result[['Team_name', 'ORTG', 'DRTG', 'NetRTG', 'eFG%', 'TS%', 'AST/TO', 'OREB%', 'DREB%', 'TOV%', 'BLK%', 'STL%', 'FTAr', 'Poss/G', 'EVAL/G']])
statsavancees = statsavancees.set_index('Team_name')

statsavanceesopp = (result[['Team_name', 'eFG% opp', 'TS% opp', 'AST/TO opp', 'OREB% opp', 'DREB% opp', 'TOV% opp', 'BLK% opp', 'STL% opp', 'FTAr opp', 'Poss/G opp', 'EVAL/G opp']])
statsavanceesopp = statsavanceesopp.set_index('Team_name')

fourfactors = (result[['Team_name', 'eFG%', 'TOV%', 'OREB%', 'FTAr']])
fourfactors = fourfactors.set_index('Team_name')

fourfactorsopp = (result[['Team_name', 'eFG% opp', 'TOV% opp', 'OREB% opp', 'FTAr opp']])
fourfactorsopp = fourfactorsopp.set_index('Team_name')

traditionaltotal = (result[['Team_name', 'Points_team', 'FieldGoalsMade2_team', 'FieldGoalsAttempted2_team', '2P%', 'FieldGoalsMade3_team', 'FieldGoalsAttempted3_team', '3P%', 'FreeThrowsMade_team', 'FreeThrowsAttempted_team', 'FT%', 'OffensiveRebounds_team', 'DefensiveRebounds_team', 'TotalRebounds_team', 'Assistances_team', 'Steals_team', 'Turnovers_team', 'BlocksFavour_team', 'BlocksAgainst_team', 'FoulsCommited_team' ,'FoulsReceived_team' ,'Valuation_team']])
traditionaltotal = traditionaltotal.set_index('Team_name')
traditionaltotal = traditionaltotal.rename(columns={"Points_team": "PTS", "FieldGoalsMade2_team": "2PM", "FieldGoalsAttempted2_team": "2PA", "FieldGoalsMade3_team": "3PM", "FieldGoalsAttempted3_team": "3PA", "FreeThrowsMade_team": "FTM", "FreeThrowsAttempted_team": "FTA", "OffensiveRebounds_team": "OREB", "DefensiveRebounds_team": "DREB", "TotalRebounds_team": "TREB", "Assistances_team": "AST", "Steals_team": "STL", "Turnovers_team": "TOV", "BlocksFavour_team": "BLK", "BlocksAgainst_team": "BLKA", "FoulsCommited_team": "PF", "FoulsReceived_team": "PFD", "Valuation_team": "EVAL"})

traditionaltotalopp = (result[['Team_name', 'Points_opp', 'FieldGoalsMade2_opp', 'FieldGoalsAttempted2_opp', '2P% opp', 'FieldGoalsMade3_opp', 'FieldGoalsAttempted3_opp', '3P% opp', 'FreeThrowsMade_opp', 'FreeThrowsAttempted_opp', 'FT% opp', 'OffensiveRebounds_opp', 'DefensiveRebounds_opp', 'TotalRebounds_opp', 'Assistances_opp', 'Steals_opp', 'Turnovers_opp', 'BlocksFavour_opp', 'BlocksAgainst_opp', 'FoulsCommited_opp' ,'FoulsReceived_opp' ,'Valuation_opp']])
traditionaltotalopp = traditionaltotalopp.set_index('Team_name')
traditionaltotalopp = traditionaltotalopp.rename(columns={"Points_opp": "PTS opp", "FieldGoalsMade2_opp": "2PM opp", "FieldGoalsAttempted2_opp": "2PA opp", "FieldGoalsMade3_opp": "3PM opp", "FieldGoalsAttempted3_opp": "3PA opp", "FreeThrowsMade_opp": "FTM opp", "FreeThrowsAttempted_opp": "FTA opp", "OffensiveRebounds_opp": "OREB opp", "DefensiveRebounds_opp": "DREB opp", "TotalRebounds_opp": "TREB opp", "Assistances_opp": "AST opp", "Steals_opp": "STL opp", "Turnovers_opp": "TOV opp", "BlocksFavour_opp": "BLK opp", "BlocksAgainst_opp": "BLKA opp", "FoulsCommited_opp": "PF opp", "FoulsReceived_opp": "PFD opp", "Valuation_opp": "EVAL opp"})

traditionalavg = (result[['Team_name', 'PTS/G', '2PM/G', '2PA/G', '2P%', '3PM/G', '3PA/G', '3P%', 'FTM/G', 'FTA/G', 'FT%', 'OREB/G', 'DREB/G', 'TREB/G', 'AST/G', 'STL/G', 'TOV/G', 'BLK/G', 'BLKA/G', 'PF/G', 'PFD/G', 'EVAL/G']])
traditionalavg = traditionalavg.set_index('Team_name')

traditionalavgopp = (result[['Team_name', 'PTS/G opp', '2PM/G opp', '2PA/G opp', '2P% opp', '3PM/G opp', '3PA/G opp', '3P% opp', 'FTM/G opp', 'FTA/G opp', 'FT% opp', 'OREB/G opp', 'DREB/G opp', 'TREB/G opp', 'AST/G opp', 'STL/G opp', 'TOV/G opp', 'BLK/G opp', 'BLKA/G opp', 'PF/G opp', 'PFD/G opp', 'EVAL/G opp']])
traditionalavgopp = traditionalavgopp.set_index('Team_name')

scoring = (result[['Team_name', 'FGA% 2PT', 'FGA% 3PT', 'PTS% 2PT', 'PTS% 3PT', 'PTS% FT', 'FGM% AST', 'FGM% UAST']])
scoring = scoring.set_index('Team_name')

scoringopp = (result[['Team_name', 'FGA% 2PT opp', 'FGA% 3PT opp', 'PTS% 2PT opp', 'PTS% 3PT opp', 'PTS% FT opp', 'FGM% AST opp', 'FGM% UAST opp']])
scoringopp = scoringopp.set_index('Team_name')

#Display
row1_col1, row1_col2 = st.columns(2)
    
with row1_col1:
    st.header('Efficiency Landscape')
    st.pyplot(fig)
    st.header('Percentiles')
    st.pyplot(fig1)
    
with row1_col2:
    st.header('Statistics')
    stats = st.selectbox("",('Traditional Total', 'Traditional Average', 'Advanced Stats', 'Four Factors', 'Scoring'), label_visibility="collapsed")
    offdef = st.selectbox("",('Offense', 'Defense'), label_visibility="collapsed")
    if stats == "Four Factors" and offdef == "Offense":
        statsdf = fourfactors
    elif stats == "Traditional Total" and offdef == "Offense":
        statsdf = traditionaltotal
    elif stats == "Traditional Average" and offdef == "Offense":
        statsdf = traditionalavg
    elif stats == "Scoring" and offdef == "Offense":
        statsdf = scoring
    elif stats == "Advanced Stats" and offdef == "Offense":
        statsdf = statsavancees
    elif stats == "Four Factors" and offdef == "Defense":
        statsdf = fourfactorsopp
    elif stats == "Advanced Stats" and offdef == "Defense":
        statsdf = statsavanceesopp
    elif stats == "Scoring" and offdef == "Defense":
        statsdf = scoringopp
    elif stats == "Traditional Total" and offdef == "Defense":
        statsdf = traditionaltotalopp
    elif stats == "Traditional Average" and offdef == "Defense":
        statsdf = traditionalavgopp
    else:
        statsdf = df
    st.dataframe(statsdf.style.format("{:.0f}"))
    st.markdown("")
    st.header('Shot Chart')
    st.pyplot(fig2)
    
st.write("GLOSSARY :")
st.write("ORTG : Offensive Rating / DRTG : Defensive Rating / NetRTG : Net Rating / eFG% : Effective Field Goal / TS% : True Shooting / FTAr : Free Throw rate")
st.write("FGA% 2PT : Percent of Field Goals Attempted (2 Pointers) / FGA% 3PT : Percent of Field Goals Attempted (3 Pointers) / PTS% 2PT : Percent of Points (2 Pointers) / PTS% 3PT : Percent of Points (3 Pointers) / PTS% FT : Percent of Points (Free Throws)")
st.write("FGM% AST : Percent of Point Field Goals Made Assisted / FGM% UAST : Percent of Point Field Goals Made Unassisted")