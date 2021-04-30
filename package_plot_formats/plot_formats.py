"""
Library of standard plots for radio astronomy data
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker   # <---- Added to suppress warning
import numpy as np
import pylab

from matplotlib import rc


def plot1D(data, fig_name, Label, Title, x_label, y_label, customDPI):
    """
    Plots 1D plots of variable
    """
    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(data, label=Label)
    plt.title(Title, fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.legend(loc = 'upper right', fontsize=10)
    plt.ylabel(x_label, fontsize=10, fontweight='bold')
    plt.xlabel(y_label, fontsize=10, fontweight='bold')
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xticks(fontsize=8, fontweight='bold')
    pylab.savefig(fig_name, bbox_inches='tight', dpi=customDPI)
    plt.close('all')


def plot2D(data, fig_name, frequency_list, colormap, Title, customDPI):
    """
    Plots 2D plots of variable with automatic limits
    """
    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    ImA = plt.imshow(np.flipud(data), aspect='auto', vmin=np.min(data), vmax=np.max(data),
                     extent=[0, 1, frequency_list[0], frequency_list[-1]], cmap=colormap)
    plt.title(Title, fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.ylabel('Frequency, MHz', fontsize=10, fontweight='bold')
    plt.xlabel('Phase of pulsar period', fontsize=10, fontweight='bold')
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xticks(fontsize=8, fontweight='bold')
    plt.colorbar()
    pylab.savefig(fig_name, bbox_inches='tight', dpi=customDPI)
    plt.close('all')


def plot2Da(data, fig_name, frequency_list, min_limit, max_limit, colormap, Title, customDPI):
    """
    Plots 2D plots of variable with manually predefined limits
    """

    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    ImA = plt.imshow(np.flipud(data), aspect='auto', vmin=min_limit, vmax=max_limit, cmap=colormap)  #,extent=[0,1,frequency_list[0],frequency_list[len(frequency_list)-1]]
    plt.title(Title, fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.ylabel('Frequency, MHz', fontsize=10, fontweight='bold')
    plt.xlabel('Phase of pulsar period', fontsize=10, fontweight='bold')
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xticks(fontsize=8, fontweight='bold')
    plt.colorbar()
    pylab.savefig(fig_name, bbox_inches='tight', dpi=customDPI)
    plt.close('all')


# *** Plot 2D plot with one data set ***
def OneImmedSpecterPlot(Xax, Ydat, Label, xmin, xmax, ymin, ymax, XLab, YLab,
                        SupTitle, Title, FileName, currentDate, currentTime, Software_version):
    """
    Plots 2D plot of immediate specter
    """

    plt.figure()
    rc('font', size=8, weight='normal')
    plt.plot(Xax, Ydat, color='b', linestyle='-', linewidth='1.00', label=Label)
    plt.axis([xmin, xmax, ymin, ymax])
    plt.xlabel(XLab)
    plt.ylabel(YLab)
    plt.suptitle(SupTitle, fontsize=9, fontweight='bold')
    plt.title(Title, fontsize=7, x=0.46, y=1.005)
    plt.grid(b=True, which='both', color='0.00', linestyle='--')
    plt.legend(loc='upper right', fontsize=8)
    plt.text(0.7,  0.03, 'Processed ' + currentDate + ' at ' + currentTime,
             fontsize=5, transform=plt.gcf().transFigure)
    plt.text(0.03, 0.03, 'Software version: ' + Software_version + ' yerin.serge@gmail.com, IRA NASU',
             fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(FileName, bbox_inches='tight', dpi=160)
    plt.close('all')
    return


# *** Plot 2D plot with two data sets ***

def TwoImmedSpectraPlot(Xax, Ydat1, Ydat2, Label1, Label2, xmin, xmax, ymin, ymax,
                        XLab, YLab, SupTitle, Title, FileName, currentDate, currentTime, Software_version):
    """
    Plots 2D plot of two immediate scpectra
    """
    plt.figure()
    rc('font', size=8, weight='normal')
    plt.plot(Xax, Ydat1, color='r', linestyle='-', linewidth='1.00', label=Label1)
    plt.plot(Xax, Ydat2, color='b', linestyle='-', linewidth='1.00', label=Label2)
    plt.axis([xmin, xmax, ymin, ymax])
    plt.xlabel(XLab)
    plt.ylabel(YLab)
    plt.suptitle(SupTitle, fontsize=9, fontweight='bold')
    plt.title(Title, fontsize=7, x=0.46, y=1.005)
    plt.grid(b=True, which='both', color='0.00', linestyle='--')
    plt.legend(loc='upper right', fontsize=8)
    plt.text(0.7,  0.03, 'Processed ' + currentDate + ' at ' + currentTime,
             fontsize=5, transform=plt.gcf().transFigure)
    plt.text(0.03, 0.03, 'Software version: ' + Software_version + ' yerin.serge@gmail.com, IRA NASU',
             fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(FileName, bbox_inches='tight', dpi=160)
    plt.close('all')
    return 0


# *** Plot 2D plot with two data sets ***
def TwoOrOneValuePlot(no_of_sets, Xax, Ydat1, Ydat2, Label1, Label2,
                        xmin, xmax, ymin_1, ymax_1, ymin_2, ymax_2,
                        XLab, YLab_1, YLab_2, SupTitle, Title, FileName,
                        currentDate, currentTime, Software_version):
    """
    Plots 2D plot of one or two immediate scpectra - univrsal plot for immediate spectra
    """

    rc('font', size=6, weight='bold')
    if no_of_sets == 1:
        fig = plt.figure(figsize=(9, 5))
        ax1 = fig.add_subplot(111)
    elif no_of_sets == 2:
        fig = plt.figure(figsize=(9, 9))
        ax1 = fig.add_subplot(211)
    else:
        print(' ERROR !!!')
    if no_of_sets == 2:
        ax1.plot(Xax, Ydat2, color=u'#ff7f0e', linestyle='-', alpha=0.4, linewidth='1.00')
    ax1.plot(Xax, Ydat1, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='1.00', label=Label1)
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    ax1.axis([xmin, xmax, ymin_1, ymax_1])
    ax1.set_ylabel(YLab_1, fontsize=6, fontweight='bold')
    ax1.set_title(Title, fontsize=6)
    if no_of_sets == 2:
        ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        ax2 = fig.add_subplot(212)
        if no_of_sets == 2:
            ax2.plot(Xax, Ydat1, color=u'#1f77b4', linestyle='-', alpha=0.4, linewidth='1.00')
        ax2.plot(Xax, Ydat2, color=u'#ff7f0e', linestyle='-', alpha=1.0, linewidth='1.00', label=Label2)
        ax2.legend(loc='upper right', fontsize=6)
        ax2.grid(b=True, which='both', color='silver', linestyle='-')
        ax2.axis([xmin, xmax, ymin_2, ymax_2])
        ax2.set_xlabel(XLab, fontsize=6, fontweight='bold')
        ax2.set_ylabel(YLab_2, fontsize=6, fontweight='bold')
        fig.subplots_adjust(hspace=0.05, top=0.94)
    elif no_of_sets == 1:
        ax1.set_xlabel(XLab, fontsize=6, fontweight='bold')
        fig.subplots_adjust(top=0.92)
    else:
        print(' ERROR !!!')
    fig.suptitle(SupTitle, fontsize = 8, fontweight='bold')
    if no_of_sets == 2:
        fig.text(0.73, 0.06, 'Processed ' + currentDate + ' at ' + currentTime,
                 fontsize=4, transform=plt.gcf().transFigure)
        fig.text(0.09, 0.06, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
                 fontsize=4, transform=plt.gcf().transFigure)
    elif no_of_sets == 1:
        fig.text(0.73, 0.03, 'Processed ' + currentDate + ' at '+currentTime,
                 fontsize=4, transform=plt.gcf().transFigure)
        fig.text(0.09, 0.03, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
                 fontsize=4, transform=plt.gcf().transFigure)
    else:
        print(' ERROR !!!')
    pylab.savefig(FileName, bbox_inches='tight', dpi=160)
    plt.close('all')
    return


def OneValueWithTimePlot(timeline, Ydat1, Label1, xmin, xmax, ymin, ymax, x_auto, y_auto,
                        XLabel, YLabel, SupTitle, Title, FileName,
                        currentDate, currentTime, Software_version):
    """
    Plots 2D plot of one dataset with time
    """

    rc('font', size=6, weight='bold')
    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(Ydat1, linestyle='-', linewidth='1.00', label=Label1)
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    if x_auto == 0: ax1.set_xlim([xmin, xmax])
    if y_auto == 0: ax1.set_ylim([ymin, ymax])
    ax1.set_ylabel(YLabel, fontsize=6, fontweight='bold')
    ax1.set_title(Title, fontsize=6)
    ax1.set_xlabel(XLabel, fontsize=6, fontweight='bold')
    text = ax1.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = timeline[k]  # text[i] = timeline[i] ???
    ax1.set_xticklabels(text, fontsize=6, fontweight='bold')
    fig.subplots_adjust(top=0.92)
    fig.suptitle(SupTitle, fontsize=8, fontweight='bold')
    fig.text(0.79, 0.03, 'Processed ' + currentDate + ' at ' + currentTime,
             fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.03, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(FileName, bbox_inches='tight', dpi=160)
    plt.close('all')
    return


#   *** Plot dynamic spectra of one data set ***
def OneDynSpectraPlot(Data, Vmin, Vmax, Suptitle, CBarLabel, no_of_spectra, TimeScale,
                        frequency, FreqPointsNum, colormap, Xlabel, fig_file_name,
                        currentDate, currentTime, Software_version, customDPI):
    """
    One dynamic spectra plot
    """

    fig, axarr = plt.subplots(1, 1, figsize=(16.0, 7.0))
    im0 = axarr.imshow(np.flipud(Data), aspect='auto', vmin=Vmin, vmax=Vmax,
                       extent=[0, no_of_spectra, frequency[0], frequency[FreqPointsNum-1]], cmap=colormap)
    rc('font', size=8, weight='bold')
    axarr.set_ylabel('Frequency, MHz', fontweight='bold', fontsize=10)
    fig.suptitle(Suptitle, fontsize=10, fontweight='bold', x=0.46, y=0.96)

    ticks_loc = axarr.get_yticks().tolist()                               # <---- Added to suppress warning
    axarr.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))        # <---- Added to suppress warning

    axarr.set_yticklabels(axarr.get_yticks(), fontsize=8, fontweight='bold')
    cbar = fig.colorbar(im0, ax=axarr, pad=0.005)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label(CBarLabel, fontsize=9, fontweight='bold')
    text = axarr.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = TimeScale[k]

    ticks_loc = axarr.get_xticks().tolist()                              # <---- Added to suppress warning
    axarr.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))       # <---- Added to suppress warning

    axarr.set_xticklabels(text, fontsize=8, fontweight='bold')
    axarr.set_yticklabels(axarr.get_yticks(), fontsize=8, fontweight='bold')
    axarr.set_xlabel(Xlabel, fontsize=10, fontweight='bold')
    fig.text(0.72, 0.04, 'Processed ' + currentDate + ' at ' + currentTime,
             fontsize=6, fontweight='bold', transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=6, fontweight='bold', transform=plt.gcf().transFigure)
    pylab.savefig(fig_file_name, bbox_inches='tight', dpi=customDPI)
    plt.close('all')
    return


#   *** Plot dynamic spectra of one data set in format for PhD thesis ***
def OneDynSpectraPlotPhD(Data, Vmin, Vmax, Suptitle, CBarLabel, no_of_spectra, TimeScale,
                        frequency, FreqPointsNum, colormap, Xlabel, fig_file_name,
                        currentDate, currentTime, Software_version, customDPI):
    """
    One dynamic spectra plot of PhD style
    """

    fig, axarr = plt.subplots(1, 1, figsize=(16.0, 7.0))
    im0 = axarr.imshow(np.flipud(Data), aspect='auto', vmin=Vmin, vmax=Vmax,
                       extent=[0, no_of_spectra, frequency[0], frequency[-1]], cmap=colormap)
    rc('font', size=14, weight='bold')
    axarr.set_ylabel('Частота, МГц', fontweight='bold', fontsize=14)
    #fig.suptitle(Suptitle, fontsize = 10, fontweight = 'bold', x = 0.46, y = 0.96)
    ticks_loc = axarr.get_yticks().tolist()                               # <---- Added to suppress warning
    axarr.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))        # <---- Added to suppress warning
    axarr.set_yticklabels(axarr.get_yticks(), fontsize=14, fontweight='bold')
    cbar = fig.colorbar(im0, ax=axarr, pad=0.005)
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label(CBarLabel, fontsize=14, fontweight='bold')
    text = axarr.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = TimeScale[k]
        # text[i] = TimeScale[k][0:20]

    ticks_loc = axarr.get_xticks().tolist()                               # <---- Added to suppress warning
    axarr.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))        # <---- Added to suppress warning
    ticks_loc = axarr.get_yticks().tolist()                               # <---- Added to suppress warning
    axarr.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))        # <---- Added to suppress warning
    axarr.set_xticklabels(text, fontsize=12, fontweight='bold')
    axarr.set_yticklabels(axarr.get_yticks(), fontsize=12, fontweight='bold')
    axarr.set_xlabel(Xlabel, fontsize=14, fontweight='bold')
    pylab.savefig(fig_file_name, bbox_inches='tight', dpi=customDPI)
    plt.close('all')
    return


#   *** Plot dynamic spectra of two data sets ***
def TwoDynSpectraPlot(Data_Ch_A, Data_Ch_B, VminA, VmaxA, VminB, VmaxB, Suptitle,
                        CBarLabelA, CBarLabelB, no_of_spectra,
                        TimeFigureScale, TimeScale, frequency,
                        FreqPointsNum, colormap, TitleA, TitleB, fig_file_name,
                        currentDate, currentTime, Software_version, customDPI):
    """
    Two dynamic spectra plot
    """
    fig, axarr = plt.subplots(2, 1, figsize=(16.0, 9.0))
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.08)
    im0 = axarr[0].imshow(np.flipud(Data_Ch_A), aspect='auto', vmin=VminA, vmax=VmaxA,
                          extent=[0,no_of_spectra, frequency[0], frequency[FreqPointsNum-1]], cmap=colormap)
    rc('font', size=8, weight='bold')

    ticks_loc = axarr[0].get_yticks().tolist()                              # <---- Added to suppress warning
    axarr[0].yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))       # <---- Added to suppress warning

    axarr[0].set_ylabel('Frequency, MHz', fontweight='bold', fontsize=10)
    axarr[0].set_yticklabels(axarr[0].get_yticks(), fontsize=8, fontweight='bold')
    cbar = fig.colorbar(im0, ax=axarr[0], pad=0.005)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label(CBarLabelA, fontsize=9, fontweight='bold')
    text = axarr[0].get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = ' '

    ticks_loc = axarr[0].get_xticks().tolist()                              # <---- Added to suppress warning
    axarr[0].xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))       # <---- Added to suppress warning

    axarr[0].set_xticklabels(text)
    axis_copy = axarr[0].twiny()
    axis_copy.set_xlim(0, no_of_spectra)
    text = axis_copy.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = TimeFigureScale[k]

    ticks_loc = axis_copy.get_xticks().tolist()                              # <---- Added to suppress warning
    axis_copy.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))       # <---- Added to suppress warning

    axis_copy.set_xticklabels(text, fontsize=8, fontweight='bold')
    axarr[0].set_title(TitleA, fontsize=10, fontweight='bold', style='italic', y=1.05)
    im1 = axarr[1].imshow(np.flipud(Data_Ch_B), aspect='auto', vmin=VminB, vmax=VmaxB,
                          extent=[0, no_of_spectra, frequency[0], frequency[-1]], cmap=colormap)
    # frequency[FreqPointsNum-1]

    ticks_loc = axarr[1].get_xticks().tolist()                              # <---- Added to suppress warning
    axarr[1].xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))       # <---- Added to suppress warning

    ticks_loc = axarr[1].get_yticks().tolist()                              # <---- Added to suppress warning
    axarr[1].yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))       # <---- Added to suppress warning

    axarr[1].set_xlabel('UTC Time, HH:MM:SS.msec', fontsize=10, fontweight='bold')
    axarr[1].set_ylabel('Frequency, MHz', fontsize=10, fontweight='bold')
    cbar = fig.colorbar(im1, ax=axarr[1], pad=0.005)
    cbar.set_label(CBarLabelB, fontsize=9, fontweight='bold')
    cbar.ax.tick_params(labelsize=8)
    text = axarr[1].get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = TimeScale[k]
    axarr[1].set_xticklabels(text, fontsize=8, fontweight='bold')
    axarr[1].set_yticklabels(axarr[1].get_yticks(), fontsize=8, fontweight='bold')
    axarr[1].set_title(TitleB, fontsize=10, fontweight='bold', style='italic', y=1.00)
    fig.suptitle(Suptitle, fontsize=10, fontweight='bold', x=0.46, y=1.01)
    fig.subplots_adjust(top=0.91)
    fig.text(0.72, 0.065, 'Processed ' + currentDate + ' at ' + currentTime,
             fontsize=6, transform=plt.gcf().transFigure)
    fig.text(0.1,  0.065, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=6, transform=plt.gcf().transFigure)
    pylab.savefig(fig_file_name, bbox_inches='tight', dpi=customDPI)
    plt.close('all')
    return 0
