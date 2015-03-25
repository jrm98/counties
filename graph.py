# Data Analytics for Counties in the US
# Jake Martinez (jrm98)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg 
from matplotlib import cm


df = pd.read_csv('counties.csv')

fig = plt.figure()

def df_filter(val):
    if val == 'all':
        return df
    else:
        return df[df['State'] == val]

# global variables
state = 'all'
annotation = None

states = ['all'] + df['State'].unique().tolist()

# displays current state
ax = fig.add_axes( (0.8, 0.1, 0.1, 0.05) )
t = b = wdg.Button(ax, 'all')

# creates state slider
ax = fig.add_axes( (0.1, 0.1, 0.6, 0.05) )
s = wdg.Slider(ax, 'State', 0, 51 , valinit=0)
def update(val):
    global g,state,annotation
    state = states[int(val)]

    t.label.set_text(state) # change label

    # change scatterplot data
    data = df_filter(state)
    if g != None:
        g.remove()
    g = ax.scatter(data['PercentCollegeGrad'],
                   data['IncomePerCapita'],
                   picker=True,
                   c=data['MedianRent'],
                   cmap=cm.Blues)

    # remove annotation label
    if annotation != None:
        annotation.remove()
        annotation = None
    fig.canvas.draw_idle()

s.on_changed(update)

# creates reset button
ax = fig.add_axes( (0.1, 0.2, 0.1, 0.05) )  
b = wdg.Button(ax, 'Reset')
def onpress(event):
    s.set_val(0)
    global annotation
    if annotation != None:
        annotation.remove()
        annotation = None
    fig.canvas.draw_idle()
b.on_clicked(onpress)


def onpick(event):
    global annotation
    xy = event.artist.get_offsets()

    # remove old annotation, if exists
    if annotation != None:
        annotation.remove()

    # makes sure all annotations are from the correct state
    if state == 'all':
        text = df['Name'][event.ind[0]] + ", " + df['State'][event.ind[0]]
    else:
        # filter df for prec. grads then by state
        data = df[df['PercentCollegeGrad'] == xy[event.ind][0][0]]
        data = data[data['State'] == state]

        # gets county name then state
        text = data.iloc[0,0] + ", " + data.iloc[0,1]

    # creates annotation and saves the reference to global variable
    annotation = ax.annotate(text, 
        xy=(xy[event.ind][0][0], xy[event.ind][0][1]),
        color='black',
        xycoords='data',
        xytext=(0,0),
        textcoords='offset points')
    fig.canvas.draw_idle()


ax = fig.add_axes( (0.15, 0.3, 0.8, 0.65) )
g = ax.scatter(df['PercentCollegeGrad'],
               df['IncomePerCapita'],
               picker=True,
               c=df['MedianRent'],
               cmap=cm.Blues)
plt.xlabel('Percent College Grad')
plt.ylabel('Income Per Capita')
PCM=ax.get_children()[2] #get the mappable, the 1st and the 2nd are the x and y axes
plt.colorbar(PCM, ax=ax).set_label('Median Rent')


fig.canvas.mpl_connect('pick_event', onpick) # connect pick event handler

plt.show()


