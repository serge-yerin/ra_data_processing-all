'''
'''
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import pylab


def MultipleValueWithTimePlot(timeline, Ydat1, Label, xmin, xmax, ymin, ymax, x_auto, y_auto,
                        XLabel, YLabel, SupTitle, Title, FileName,
                        currentDate, currentTime, Software_version):
    '''
    Plots 2D plot of multiple datasets with date and time
    '''

    a, b = Ydat1.shape

    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (9, 5))
    ax1 = fig.add_subplot(111)
    for i in range (a):
        ax1.plot(Ydat1[i, :], linestyle = '-', linewidth = '1.00', label = Label[i])
    ax1.legend(loc = 'upper right', fontsize = 6)
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    if x_auto == 0: ax1.set_xlim([xmin, xmax])
    if y_auto == 0: ax1.set_ylim([ymin, ymax])
    ax1.set_ylabel(YLabel, fontsize=6, fontweight='bold')
    ax1.set_title(Title, fontsize = 6)
    ax1.set_xlabel(XLabel, fontsize=6, fontweight='bold')
    text = ax1.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = timeline[k]
    ax1.set_xticklabels(text, fontsize = 6, fontweight = 'bold')
    fig.subplots_adjust(top=0.92)
    fig.suptitle(SupTitle, fontsize = 8, fontweight='bold')
    fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(FileName, bbox_inches = 'tight', dpi = 160)
    plt.close('all')


    '''
    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(Ydat1, linestyle = '-', linewidth = '1.00', label = Label1)
    ax1.legend(loc = 'upper right', fontsize = 6)
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    if x_auto == 0: ax1.set_xlim([xmin, xmax])
    if y_auto == 0: ax1.set_ylim([ymin, ymax])
    ax1.set_ylabel(YLabel, fontsize=6, fontweight='bold')
    ax1.set_title(Title, fontsize = 6)
    ax1.set_xlabel(XLabel, fontsize=6, fontweight='bold')
    text = ax1.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = timeline[k]  # text[i] = timeline[i] ???
    ax1.set_xticklabels(text, fontsize = 6, fontweight = 'bold')
    fig.subplots_adjust(top=0.92)
    fig.suptitle(SupTitle, fontsize = 8, fontweight='bold')
    fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(FileName, bbox_inches = 'tight', dpi = 160)
    plt.close('all')
    return
    '''
