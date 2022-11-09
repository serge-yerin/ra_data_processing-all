import matplotlib.pyplot as plt
import numpy as np
import pylab
from matplotlib import rc
import matplotlib.ticker as mticker   # <---- Added to suppress warning


def plot_pulse_profile_and_spectra(profile, data, frequency, profile_pic_min, profile_pic_max,
                                   spectrum_pic_min, spectrum_pic_max,  periods_per_fig, fig_suptitle, fig_title,
                                   pic_filename, current_date, current_time, software_version, custom_dpi,
                                   colormap, show=False, save=True):
    """Displays and/or saves picture with integrated profile and dynamic spectrum of average pulse"""
    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')

    ax1 = fig.add_subplot(211)
    ax1.plot(profile, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60',
             label='Pulses integrated time profile')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.axis([0, len(profile), profile_pic_min, profile_pic_max])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title(fig_title, fontsize=5, fontweight='bold')

    # Grid lines parameters
    major_ticks_top = np.linspace(0, len(profile), periods_per_fig+1)
    minor_ticks_top = np.linspace(0, len(profile), (4 * periods_per_fig+1))
    ax1.set_xticks([])
    ax1.yaxis.grid(visible=True, which='major', color='silver', linewidth='0.30', linestyle='--')  # Major y
    ax1.yaxis.grid(visible=True, which='minor', color='silver', linewidth='0.30', linestyle='--')  # Minor all

    ax1up = ax1.twiny()
    ax1up.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax1up.set_xticks(major_ticks_top)
    ax1up.set_xticks(minor_ticks_top, minor=True)

    ax1up.xaxis.grid(visible=True, which='major', color='gray', linewidth='0.50', linestyle='-')  # Major x
    ax1up.xaxis.grid(visible=True, which='minor', color='silver', linewidth='0.30', linestyle='--')  # Minor all

    ax2 = fig.add_subplot(212)
    ax2.imshow(np.flipud(data), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max,
               extent=[0, periods_per_fig, frequency[0], frequency[-1]])
    ax2.set_xlabel('Pulsar period phase', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')

    major_ticks_bottom = np.linspace(0, periods_per_fig, 4 * periods_per_fig+1)
    ax2.set_xticks(major_ticks_bottom)

    fig.subplots_adjust(hspace=0.05, top=0.86)
    fig.suptitle(fig_suptitle, fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    if save:
        pylab.savefig(pic_filename, bbox_inches='tight', dpi=custom_dpi)
    if show:
        plt.show()
    plt.close('all')
    return 0


def plot_pulsar_pulses_evolution(data, fig_suptitle, fig_title, timeline, scale_factor,
                                 pic_filename, custom_dpi, software_version, current_date, current_time,
                                 show=False, save=True):
    """
    Plots pulsar pulse evolution with time, i.e. each line is a pulse period
    data - 2D numpy array (float)
    fig_title - title pf the plot (text)
    v_min - min value of colormap
    v_max - max value of colormap
    timeline - timeline as read from txt file to use for the figure
    scale_factor
    pic_filename
    custom_dpi
    software_version
    current_date - just current date (text)
    current_time - just current time (text)
    show - to display figure on the screen or not (bool)
    save - to save the figure to the file or not (bool)
    """
    fig = plt.figure(figsize=(8.0, 6.0))
    rc('font', size=6, weight='bold')
    ax0 = fig.add_subplot(111)
    ax0.imshow(data, cmap='Greys', aspect='auto')  # vmin=v_min, vmax=v_max
    ax0.set_title(fig_title, fontsize=5, fontweight='bold')

    major_ticks_bottom = np.linspace(0, data.shape[1], 4 + 1)

    ax0.axis([0, 1, data.shape[0] - 1, 0])
    ax0.set_xticks(major_ticks_bottom)

    ax0.set_xlabel('Number of sample in pulsar period', fontsize=6, fontweight='bold')
    ax0.set_ylabel('Number of pulsar period', fontsize=6, fontweight='bold')

    ax1 = ax0.twinx()
    ax1.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False)

    ax1.axis([0, 1, data.shape[0] - 1, 0])
    ax1.set_xticks(major_ticks_bottom)
    text = ax0.get_yticks().tolist()
    for i in range(len(text) - 1):
        k = int(text[i])
        text[i] = timeline[k * int(data.shape[1] / scale_factor)][11:23]

    ticks_loc = ax1.get_yticks().tolist()                           # <---- Added to suppress warning
    ax1.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))    # <---- Added to suppress warning
    ax1.set_yticklabels(text, fontsize=6, fontweight='bold')

    fig.subplots_adjust(hspace=0.05, top=0.92)
    fig.suptitle(fig_suptitle, fontsize=7, fontweight='bold')

    fig.text(0.922, 0.935, 'UTC time', fontsize=6, transform=plt.gcf().transFigure)
    fig.text(0.82, 0.060, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.060, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)

    if save:
        pylab.savefig(pic_filename, bbox_inches='tight', dpi=custom_dpi)
    if show:
        plt.show()
    plt.close('all')
    return 0


def plot_pulsar_ridgeline_profiles(data, pic_filename, custom_dpi, overlap=0.0, fill=True, labels=None,
                                   show=False, save=True):
    """
    Creates a ridgeline plot of pulsar profiles.

    data - 2D numpy array.
    overlap -  overlap between distributions. 1 - max overlap, 0 - no overlap.
    fill - fill the distributions.
    labels - values to place on the y axis to describe the distributions.
    """
    if overlap > 1.0 or overlap < 0.0:
        raise ValueError('overlap must be in [0 1]')
    xx = np.linspace(0, 1, num=data.shape[1])
    ys = []
    fig, ax0 = plt.subplots(1, 1, figsize=(4, 8))
    for k in range(data.shape[0]):
        y = k * (1.0 - overlap)
        ys.append(y)
        curve = data[k, :]
        if fill:
            ax0.fill_between(xx, np.ones(data.shape[1]) * y, curve + y,
                             zorder=data.shape[0] - k + 1, color='royalblue')
        ax0.plot(xx, curve + y, color='royalblue', zorder=data.shape[0] - k + 1, linewidth=0.2)
        ax0.axis('off')
    if labels:
        ax0.yticks(ys, labels)
    if save:
        pylab.savefig(pic_filename, bbox_inches='tight', dpi=custom_dpi)
    if show:
        plt.show()
    plt.close('all')


def plot_average_profiles(a_data_array, data_type, filename, result_path, custom_dpi):
    """

    Args:
        a_data_array:
        data_type:
        filename:
        result_path:
        custom_dpi:

    Returns:

    """

    n = '1' if data_type == 'Raw' else '2'

    integr_profile_0 = np.sum(a_data_array, axis=0)
    integr_profile_1 = np.sum(a_data_array, axis=1)

    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=None, right=None, top=0.86, wspace=None, hspace=0.3)
    plt.subplot(2, 1, 1)
    plt.title(data_type + ' data integrated over time and over frequency \n File: ' + filename,
              fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.plot(integr_profile_0)
    plt.xlabel('Samples in time', fontsize=8, fontweight='bold')
    plt.ylabel('Dummy values', fontsize=8, fontweight='bold')
    plt.xticks(fontsize=6, fontweight='bold')
    plt.yticks(fontsize=6, fontweight='bold')
    plt.subplot(2, 1, 2)
    plt.plot(integr_profile_1)
    plt.xlabel('Frequency points', fontsize=8, fontweight='bold')
    plt.ylabel('Dummy values', fontsize=8, fontweight='bold')
    plt.xticks(fontsize=6, fontweight='bold')
    plt.yticks(fontsize=6, fontweight='bold')
    pylab.savefig(result_path + '/02.' + n + ' - ' + data_type + ' data integrated over time and over frequency.png',
                  bbox_inches='tight', dpi=custom_dpi)  # 250
    plt.close('all')

    del integr_profile_0, integr_profile_1

    return 0
