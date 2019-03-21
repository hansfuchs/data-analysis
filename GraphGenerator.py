import numpy as np
import matplotlib.pyplot as plt
from typing import List

from config import Constants
from utils import get_files_of_dir


class GraphGenerator:

    const: Constants = Constants()

    def __init__(self):
        self.files: List[str] = get_files_of_dir(self.const.DIR_MACHINE_CSVS)


if __name__ == "__main__":

    t = np.arange(0.0, 1.0 + 0.01, 0.01)
    s = np.cos(2 * 2 * np.pi * t)
    t[41:60] = np.nan

    # y = list of as many zeroes as x values exist

    plt.subplot(2, 1, 1)
    plt.plot(t, s, '-', lw=2)

    # set proper values for axes
    # xmin, xmax, ymin, ymax
    # plt.axis([0, 10, 0, 20])

    #plt.xlabel('time (s)')
    #plt.ylabel('voltage (mV)')
    #plt.title('A sine wave with a gap of NaNs between 0.4 and 0.6')
    #plt.grid(True)

    plt.subplot(2, 1, 2)
    t[0] = np.nan
    t[-1] = np.nan
    plt.plot(t, s, '-', lw=2)
    plt.title('Also with NaN in first and last point')

    plt.xlabel('time (s)')
    plt.ylabel('more nans')
    plt.grid(True)

    plt.show()
