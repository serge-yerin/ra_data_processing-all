'''
'''
import matplotlib.pyplot as plt
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
