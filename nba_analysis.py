
import pandas as pd
import numpy as np
import scipy.stats as stats
import pylab as pl
import seaborn as sns
from matplotlib import pyplot

data = pd.read_csv('all_data.csv')

por = data[data['team'] == 'POR']

def average(data, time):
    clocks = pd.DataFrame(data[time].value_counts())
    clocks = clocks.sort_index(ascending = True)
    clocks['gain'] = 0
    for value in clocks.index:
        clocks.loc[value, 'gain'] = (data[data[time] == value]['diff_gain']).mean()
    return clocks
    
def seaborn_matrix(data, group, group2):
    table = pd.DataFrame(data[group].value_counts()).sort_index()
    crimes = list(table.index.values)
    for crime in crimes:
        crime2 = pd.DataFrame(data[data[group] == crime][group2].value_counts()).sort_index(ascending = False)
        headers = list(crime2.index.values)
        for head in headers:
            if head not in list(table.column):
                table[head] = 0
            table.loc[crime, head] = int(100 * (data[(data[group] == crime) & (data[group2] == head)]['diff_gain']).mean())
    return table


###
foul = data[data.type == 'foul']
no_foul = data[data.type != 'foul']
lebron = data[data['player'] == 'L. James']
(lebron.diff_gain).mean()

###
clocks = average(data, 'clock')
clocks['gain'].plot(ylim = [0,1], figsize=(18, 14))
shot_clock = average(data, 'shot_clock')
plot = shot_clock['gain'].plot(ylim = [0,1.75], figsize=(15,10))
plot.set_xlabel('Shot Clock in Seconds')
plot.set_ylabel('Gain in Points at the End of the Quarter')


urgent = data[data.clock + (24 - data['shot_clock']) < 35]
check_urgent = urgent[(urgent.quarter != 'End of 4th quarter') & (urgent['shot_clock'] < 19)]

wins = data[data.diff_score > 0]
third = data[data.quarter == 'End of 3rd quarter']
thirdAndclose = third[abs(third.diff_q_score) < 10]
gaining = thirdAndclose[thirdAndclose.diff_shot_score > thirdAndclose.diff_score]

''' players analysis'''
players = data[data.type != 'foul']
players['player'].value_counts()
harden = players[players.player == 'J. Harden']
hou = players[players.team == 'HOU']
lac = players[players.team == 'LAC']
dist_bins = np.linspace(0, 30, 31)
pyplot.hist(list(hou.distance), dist_bins, label='HOU')
pyplot.hist(list(lac.distance), dist_bins, label='LAC')
pyplot.legend(loc='upper right')



