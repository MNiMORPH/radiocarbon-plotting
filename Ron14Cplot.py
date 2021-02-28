#! /usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

plt.ioff()

########
# DATA #
########

# Import sheet with empty cells as empty string instead of nan
data = pd.read_excel('/home/awickert/Downloads/Ron14Cpruned.xlsx', 
                     sheet_name='Ron Edited Main',
                     keep_default_na=False)

# DATA TO PLOT
index = data.index + 1
raw14C_years = 1950 - data['14C age']
xerr2s = np.array([raw14C_years - data['2sig low'], 
                   data['2sig hi'] - raw14C_years])
xerr1s = np.array([raw14C_years - data['1sig low'], 
                   data['1sig hi'] - raw14C_years])

# SITE NAMES & LABELS
ylabels = []
site_names = []
for i in range(len(data)):
    site_name = '%02d' %data['State'][i] + data['County'][i] \
                 + '%04d' %data['Number'][i]
    site_names.append(site_name)
    ylabels.append(site_name + ' F' + str(data['Feature'][i]) + ': ' 
                   + str(data['Depth'][i]) + data['Depth units'][i])


#############
# FULL PLOT #
#############

fig = plt.figure(figsize=(8,16))
ax = plt.subplot(1,1,1)
plt.plot(raw14C_years, index, 'ko')
plt.errorbar(raw14C_years, index, 
             xerr=xerr2s,
             elinewidth=2,
             ecolor='.4', fmt='none')
plt.errorbar(raw14C_years, index, 
             xerr=xerr1s,
             elinewidth=4,
             ecolor='.4', fmt='none')
plt.yticks(index, ylabels)
plt.xlabel('Year [AD/CE]', fontsize=16)
plt.tight_layout()
plt.ylim(index[0]-.5, index[-1]+.5)
ax.yaxis.set_ticks_position('both')
ax.invert_yaxis() # Reverse default order (bottom-up) into readable (top down)
plt.tight_layout()

plt.savefig('RonDatesTest03.pdf')

plt.close()


######################
# SITE-BY-SITE PLOTS #
######################

# Create a set of unique site names
sites = list(set(site_names))

# Then loop over this set
for site in sites:

    toplot = np.array(site_names) == site
    _index = np.arange(np.sum(toplot)) + 1

    # Estimate the required figure height.
    fig = plt.figure(figsize=(8,16*np.sum(toplot)/60.+1.))
    ax = plt.subplot(1,1,1)
    plt.plot(raw14C_years[toplot], _index, 'ko')
    plt.errorbar(np.array(raw14C_years[toplot]), _index, 
                 xerr=[xerr2s[0][toplot], xerr2s[1][toplot]],
                 elinewidth=2,
                 ecolor='.4', fmt='none')
    plt.errorbar(np.array(raw14C_years[toplot]), _index, 
                 xerr=[xerr1s[0][toplot], xerr1s[1][toplot]],
                 elinewidth=4,
                 ecolor='.4', fmt='none')
    plt.yticks(_index, np.array(ylabels)[toplot])
    plt.xlabel('Year [AD/CE]', fontsize=16)
    plt.tight_layout()
    plt.ylim(_index[0]-.5, _index[-1]+.5)
    ax.yaxis.set_ticks_position('both')
    ax.invert_yaxis() # Reverse default order (bottom-up) into readable (top down)
    plt.tight_layout()

    #plt.show()
    plt.savefig(site +'_14C.pdf')
    plt.close()


