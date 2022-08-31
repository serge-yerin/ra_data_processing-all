import matplotlib.pyplot as plt
import numpy as np
import pylab
from matplotlib import rc


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
