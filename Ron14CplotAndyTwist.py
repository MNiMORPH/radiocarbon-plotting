#! /usr/bin/python3

import pandas as pd
import iosacal
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

plt.ioff()
matplotlib.use('tkagg') # iosacal sets this; need to unset for 
                        # any troubleshooting / plotting while coding

########
# DATA #
########

# Import sheet with empty cells as empty string instead of nan
data = pd.read_excel('/home/awickert/Downloads/Ron14Cpruned.xlsx', 
                     sheet_name='Ron Edited Main',
                     keep_default_na=False)
#data = data[:10]

# SITE NAMES & LABELS
ylabels = []
site_names = []
for i in range(len(data)):
    site_name = '%02d' %data['State'][i] + data['County'][i] \
                 + '%04d' %data['Number'][i]
    site_names.append(site_name)
    ylabels.append(site_name + ' F' + str(data['Feature'][i]) + ': ' 
                   + str(data['Depth'][i]) + data['Depth units'][i])

# MODIFIED VARIABLES
# Raw ages in standard solar calendar
raw14C_years_ADCE = 1950 - data['14C age']
# Index
index = data.index + 1

# 14C age probability distributions
raw_age_object_list = []
cal_age_pdf_list = []
for i in range(len(data)):
    raw_age_object_list.append( iosacal.R( date=data['14C age'][i],
                                           sigma=data['±'][i],
                                           id=data['Lab ID#'] ) )
    cal_age_pdf_list.append( raw_age_object_list[-1].calibrate('intcal13') )


#############
# FULL PLOT #
#############

fig = plt.figure(figsize=(12,16))
ax = plt.subplot(1,1,1)
# In long term, would be better to attach these objects to DataFrame.
# For now, I know that the matching numbers line up.
_index = 1
for pdf in cal_age_pdf_list:
    age_cal_ADCE = 1950 - pdf[:,0]
    pdf_mag_rescaled = pdf[:,1]/np.max(pdf[:,1]) * .4
    plt.fill_between( age_cal_ADCE, _index-pdf_mag_rescaled, 
                      _index+pdf_mag_rescaled, 
                      color='.5')
    _index += 1
plt.plot(raw14C_years_ADCE, index, 'ko')
plt.yticks(index, ylabels)
plt.xlabel('Year [AD/CE]', fontsize=16)
plt.tight_layout()
plt.ylim(index[0]-.5, index[-1]+.5)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.invert_yaxis() # Reverse default order (bottom-up) into readable (top down)
ax.set_xlim(800,1700)
plt.tight_layout()

plt.savefig('RonDatesTest05.pdf')
plt.close()


######################
# SITE-BY-SITE PLOTS #
######################

# UPDATE TO INCLUDE FULL PDFs (like above)

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


