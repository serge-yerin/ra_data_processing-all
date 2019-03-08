'''
'''
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import pylab

def plot1D(data, fig_name, Label, Title, x_label, y_label, customDPI):
    '''
    Plots 1D plots of variable
    '''
    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(data, label = Label)
    plt.title(Title, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.legend(loc = 'upper right', fontsize = 10) 
    plt.ylabel(x_label, fontsize = 10, fontweight='bold')
    plt.xlabel(y_label, fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig(fig_name, bbox_inches='tight', dpi = customDPI)
    plt.close('all')
    
    
    
def plot2D(data, fig_name, frequency_list, colormap, Title, customDPI):
    '''
    Plots 2D plots of variable
    '''
    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    ImA = plt.imshow(np.flipud(data), aspect='auto', vmin=np.min(data), vmax=np.max(data),extent=[0,1,frequency_list[0],frequency_list[len(frequency_list)-1]], cmap=colormap) 
    plt.title(Title, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.ylabel('Frequency, MHz', fontsize = 10, fontweight='bold')
    plt.xlabel('Phase of pulsar period', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig(fig_name, bbox_inches='tight', dpi = customDPI)
    plt.close('all')
    
    
# *** Plot 2D plot with one data set ***
def OneImmedSpecterPlot(Xax, Ydat, Label, xmin, xmax, ymin, ymax, XLab, YLab, 
                        SupTitle, Title, FileName, currentDate, currentTime, Software_version):
    '''
    Plots 2D plot of immediate specter
    '''
    
    plt.figure()
    rc('font', size = 8, weight = 'normal')
    plt.plot(Xax, Ydat, color = 'b', linestyle = '-', linewidth = '1.00', label = Label)
    plt.axis([xmin, xmax, ymin, ymax])   
    plt.xlabel(XLab)
    plt.ylabel(YLab)
    plt.suptitle(SupTitle, fontsize = 9, fontweight='bold')
    plt.title(Title, fontsize = 7, x = 0.46, y = 1.005)
    plt.grid(b = True, which = 'both', color = '0.00',linestyle = '--')
    plt.legend(loc = 'upper right', fontsize = 8)
    plt.text(0.7,  0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=5, transform=plt.gcf().transFigure)
    plt.text(0.03, 0.03, 'Software version: '+Software_version+' yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(FileName, bbox_inches = 'tight', dpi = 160)
    plt.close('all')
    return

# *** Plot 2D plot with two data sets ***
def TwoImmedSpectraPlot(Xax, Ydat1, Ydat2, Label1, Label2, xmin, xmax, ymin, ymax, 
                        XLab, YLab, SupTitle, Title, FileName, currentDate, currentTime, Software_version):
    '''
    Plots 2D plot of two immediate scpectra
    '''
    plt.figure()
    rc('font', size = 8, weight='normal')
    plt.plot(Xax, Ydat1, color = 'r', linestyle = '-', linewidth = '1.00', label = Label1)
    plt.plot(Xax, Ydat2, color = 'b', linestyle = '-', linewidth = '1.00', label = Label2)
    plt.axis([xmin, xmax, ymin, ymax])   
    plt.xlabel(XLab)
    plt.ylabel(YLab)
    plt.suptitle(SupTitle, fontsize = 9, fontweight='bold')
    plt.title(Title, fontsize = 7, x = 0.46, y = 1.005)
    plt.grid(b = True, which = 'both', color = '0.00',linestyle = '--')
    plt.legend(loc = 'upper right', fontsize = 8)
    plt.text(0.7,  0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=5, transform=plt.gcf().transFigure)
    plt.text(0.03, 0.03, 'Software version: '+Software_version+' yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(FileName, bbox_inches = 'tight', dpi = 160)
    plt.close('all')
    return

#   *** Plot dynamic spectra of two data sets ***
def TwoDynSpectraPlot(Data_Ch_A, Data_Ch_B, VminA, VmaxA, VminB, VmaxB, Suptitle, figID, figMAX, 
                        TimeRes, df, sumDifMode, df_system_name, df_obs_place, df_filename, 
                        df_description, CBarLabelA, CBarLabelB, Nim, SpInFrame, FrameInChunk, 
                        ReceiverMode, TimeFigureScale, TimeScale, SpectrNum, frequency, 
                        FreqPointsNum, colormap, TitleA, TitleB, path, FigFileName, 
                        currentDate, currentTime, Software_version, customDPI):
    
    '''
    Plots two plots of two dynamic scpectra
    '''
    
    fig, axarr = plt.subplots(2, 1, figsize=(16.0, 9.0))
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.08)
    im0 = axarr[0].imshow(np.flipud(Data_Ch_A.transpose()), aspect='auto', vmin=VminA, vmax=VmaxA, extent=[0,SpectrNum,frequency[0],frequency[FreqPointsNum-1]], cmap=colormap) 
    rc('font', size=8, weight='bold')
    axarr[0].set_ylabel('Frequency, MHz', fontweight='bold', fontsize=10)
    fig.suptitle(Suptitle+str(df_filename[0:18])+
                            ' - Fig. '+str(figID+1)+ ' of '+str(figMAX)+
                            '\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+
                            ' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+
                            ' Receiver: '+str(df_system_name)+
                            ', Place: '+str(df_obs_place) +
                            '\n'+ReceiverMode+', Description: '+str(df_description),
                            fontsize=10, fontweight='bold', x = 0.46, y = 1.01)
    axarr[0].set_yticklabels(axarr[0].get_yticks(), fontsize=8, fontweight='bold')  
    cbar = fig.colorbar(im0, ax = axarr[0], pad=0.005)
    cbar.ax.tick_params(labelsize=8) 
    cbar.set_label(CBarLabelA, fontsize=9, fontweight='bold')
    text = axarr[0].get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = ' ' 
    axarr[0].set_xticklabels(text)  
    axis_copy = axarr[0].twiny()
    axis_copy.set_xlim(0, Nim*SpInFrame*FrameInChunk)
    text = axis_copy.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])                
        text[i] = TimeFigureScale[k][0:11]
    axis_copy.set_xticklabels(text, fontsize=8, fontweight='bold')
    axarr[0].set_title(TitleA, fontsize=10, fontweight='bold', style='italic', y=1.05)
    im1 = axarr[1].imshow(np.flipud(Data_Ch_B.transpose()), aspect='auto', vmin=VminB, vmax=VmaxB, extent=[0,SpectrNum,frequency[0],frequency[FreqPointsNum-1]], cmap=colormap) #
    axarr[1].set_xlabel('UTC Time, HH:MM:SS.msec', fontsize=10, fontweight='bold') 
    axarr[1].set_ylabel('Frequency, MHz', fontsize=10, fontweight='bold') 
    cbar = fig.colorbar(im1, ax = axarr[1], pad=0.005)
    cbar.set_label(CBarLabelB, fontsize=9, fontweight='bold')
    cbar.ax.tick_params(labelsize=8) 
    text = axarr[1].get_xticks().tolist()    
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = TimeScale[k][11:23]
    axarr[1].set_xticklabels(text, fontsize=8, fontweight='bold')
    axarr[1].set_yticklabels(axarr[1].get_yticks(), fontsize=8, fontweight='bold')  
    axarr[1].set_title(TitleB, fontsize=10, fontweight='bold', style='italic', y=1.00)
    fig.subplots_adjust(top=0.91)
    fig.text(0.72, 0.065, 'Processed '+currentDate+ ' at '+currentTime, fontsize=6, transform=plt.gcf().transFigure)
    fig.text(0.1,  0.065, 'Software version: '+Software_version+' yerin.serge@gmail.com, IRA NASU', fontsize=6, transform=plt.gcf().transFigure)
    pylab.savefig(path + df_filename[0:14] + FigFileName + str(figID+1) + '.png', bbox_inches='tight', dpi = customDPI)   
    plt.close('all') 
    return    
    
