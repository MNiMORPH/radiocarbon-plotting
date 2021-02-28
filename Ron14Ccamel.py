#! /usr/bin/python3

import pandas as pd
import iosacal
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

plt.ioff()
matplotlib.use('tkagg') # iosacal sets this; need to unset for 
                        # any troubleshooting / plotting while coding

########
# DATA #
########

# Import sheet with empty cells as empty string instead of nan
data = pd.read_excel('/home/awickert/Downloads/Ron14Cpruned.xlsx', 
                     sheet_name='Ron Edited Pottery',
                     keep_default_na=False)

raw_age_object_list = []
cal_age_pdf_list = []
for i in range(len(data)):
    raw_age_object_list.append( iosacal.R( date=data['14C age'][i],
                                           sigma=data['±'][i],
                                           id=data['Lab ID#'] ) )
    cal_age_pdf_list.append( raw_age_object_list[-1].calibrate('intcal13') )

def get_age_range( _cal_age_pdf_list ):
    min_list = []
    max_list = []
    for _pdf in _cal_age_pdf_list:
        min_list.append( np.min(_pdf[:,0]) )
        max_list.append( np.max(_pdf[:,0]) )
    _min = np.min(min_list)
    _max = np.max(max_list)
    return [_min, _max]

age_lim = get_age_range( cal_age_pdf_list )
ages = np.arange(age_lim[0], age_lim[-1]+1, dtype=int)
ages_cal_ADCE = 1950 - ages

# All age PDFS on same age limits: can then sum appropriately
cal_pdf_list__full_range = []
for pdf in cal_age_pdf_list:
    f = interp1d(pdf[:,0], pdf[:,1], bounds_error=False, fill_value=0.)
    cal_pdf_list__full_range.append(f(ages))

#############
# FULL PLOT #
#############

fig = plt.figure(figsize=(8,4))
ax = plt.subplot(1,1,1)
for pdf in cal_age_pdf_list:
    age_cal_ADCE = 1950 - pdf[:,0]
    pdf_mag = pdf[:,1]
    plt.plot( age_cal_ADCE, pdf_mag, color='0.', alpha=.2 )
    plt.fill_between( age_cal_ADCE, 0, pdf_mag, color='0.', alpha=.01)
plt.plot( ages_cal_ADCE, np.sum(cal_pdf_list__full_range, axis=0) / 3,
          color='0.', linewidth=2)
plt.close()

##################
# MULTIPLE PLOTS #
##################

potteryPhases = ['Silvernale', 'Link', 'Bartron']
ppColors = ['blue', 'orange', 'purple']

fig = plt.figure(figsize=(8,4))
ax = plt.subplot(1,1,1)
# All ages
plt.plot( ages_cal_ADCE, np.sum(cal_pdf_list__full_range, axis=0) / len(data),
          color='0.', linewidth=7, label='All' )

for i in range(len(potteryPhases)):
    pp = potteryPhases[i]
    col = ppColors[i]
    sub = np.array(data['Pottery Phase'] == pp)
    plt.plot( ages_cal_ADCE, 
              np.sum(np.array(cal_pdf_list__full_range)[sub], axis=0) 
                       / np.sum(sub), # / len(data),
              color=col, linewidth=4, alpha=.6,label=pp )
plt.legend(fontsize=14)
plt.ylabel('Probability density', fontsize=16)
plt.xlabel('Year [AD/CE]', fontsize=16)
plt.xlim(950,1450)
plt.tight_layout()

plt.savefig('PotteryPeriodPDF.pdf')
plt.close()



potteryPhases = ['Silvernale, Link', 'Silvernale, Bartron', 
                 'Link, Bartron', 'Silvernale, Link, Bartron']
ppColors = ['violet', 'indigo', 'red', 'brown']

fig = plt.figure(figsize=(8,4))
ax = plt.subplot(1,1,1)
# All ages
plt.plot( ages_cal_ADCE, np.sum(cal_pdf_list__full_range, axis=0) / len(data),
          color='0.', linewidth=7, label='All' )

for i in range(len(potteryPhases)):
    pp = potteryPhases[i]
    col = ppColors[i]
    sub = np.array(data['Pottery Phase'] == pp)
    plt.plot( ages_cal_ADCE, 
              np.sum(np.array(cal_pdf_list__full_range)[sub], axis=0) 
                       / np.sum(sub), # / len(data),
              color=col, linewidth=4, alpha=.6,label=pp )
plt.legend(fontsize=14)
plt.ylabel('Probability density', fontsize=16)
plt.xlabel('Year [AD/CE]', fontsize=16)
plt.xlim(950,1450)
plt.tight_layout()

plt.savefig('PotteryPeriodMixPDF.pdf')
plt.close()


################
# ALL TOGETHER #
################

potteryPhases = ['Silvernale, Link', 'Silvernale, Bartron', 
                 'Link, Bartron', 'Silvernale, Link, Bartron']
ppColors = ['violet', 'indigo', 'red', 'brown']

fig = plt.figure(figsize=(8,4))
ax = plt.subplot(1,1,1)
# All ages
plt.plot( ages_cal_ADCE, np.sum(cal_pdf_list__full_range, axis=0) / len(data),
          color='0.', linewidth=7, label='All' )

for i in range(len(potteryPhases)):
    pp = potteryPhases[i]
    col = ppColors[i]
    sub = np.array(data['Pottery Phase'] == pp)
    plt.plot( ages_cal_ADCE, 
              np.sum(np.array(cal_pdf_list__full_range)[sub], axis=0) 
                       / np.sum(sub), # / len(data),
              color=col, linewidth=2, alpha=.6,label=pp )

potteryPhases = ['Silvernale', 'Link', 'Bartron']
ppColors = ['blue', 'orange', 'purple']

for i in range(len(potteryPhases)):
    pp = potteryPhases[i]
    col = ppColors[i]
    sub = np.array(data['Pottery Phase'] == pp)
    plt.plot( ages_cal_ADCE, 
              np.sum(np.array(cal_pdf_list__full_range)[sub], axis=0) 
                       / np.sum(sub), # / len(data),
              color=col, linewidth=4, alpha=.6,label=pp )

plt.legend(fontsize=10)
plt.ylabel('Probability density', fontsize=16)
plt.xlabel('Year [AD/CE]', fontsize=16)
plt.xlim(950,1450)
plt.tight_layout()

plt.savefig('PotteryPeriodAllPDF.pdf')
plt.close()

