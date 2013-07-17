# This file is part of nanothings.
#
#     nanothings is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero GPL as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     nanothings is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero GPL for more details.
#
#     You should have received a copy of the GNU Affero GPL
#     along with nanothings.  If not, see <http://www.gnu.org/licenses/>.

# import scipy.stats
# import matplotlib.pyplot as plt
import matplotlib.cm as cm
from os.path import join as j, exists
from os import mkdir
from . import loader
from . import processing
from . import output

cmap = cm.Greys_r


def test1(conditions, out_folder, conditions_labels=None, mask_label='mask', molecule_label='molecule'):
    if not exists(out_folder):
        mkdir(out_folder)

    # conditions_labels = ['NT', '2hLPS500']

    data = processing.compare_molecule_distribution(conditions,
        nucleus_index = 0, molecule_index = 1, nucleus_channel = 1, molecule_channel = 0,
        nucleus_fill_holes = True, nucleus_otsu = True, molecule_fill_holes = False, molecule_otsu = False)

# INTER CONDITION - masks - histo + boxplot - merged slices
    temp = output.select_arrays(data, merged = True, what = [0])
    labels = conditions_labels
    output.boxplot(temp, labels = labels, outfile = j(out_folder, 'mask_merged_boxplot.png'))
    output.histogram(temp, log=True, labels = labels, histtype='step', bins=128, color = None, outfile = j(out_folder, 'mask_merged_histogram.png'))

# SINGLE CONDITION - mask vs all - histo + boxplot - single slices
    for i in range(0, len(data)):
        temp = output.select_arrays([data[i]], merged = False, what=[0,1])
        labels = [conditions_labels[i] + '_nuclei' , conditions_labels[i] + '_all']
        output.histogram(temp, log=True, labels = labels, histtype='step', bins=128, color = ['green', 'red']*(len(temp)/2), outfile = j(out_folder, conditions_labels[i] + '_histogram.png'))
        output.boxplot(temp, labels=labels, outfile = j(out_folder, conditions_labels[i] + '_boxplot.png'))

# SINGLE CONDITION - mask vs all - histo + boxplot - merged slices
    for i in range(0, len(data)):
        temp = output.select_arrays([data[i]], merged = True, what = [0,1])
        labels = [ conditions_labels[i] + '_nuclei' , conditions_labels[i] + '_all']
        output.histogram(temp, log=True, labels = labels, histtype='step', bins=128, color = ['green', 'red']*(len(temp)/2), outfile = j(out_folder, conditions_labels[i] + '_merged_histogram.png'))
        output.boxplot(temp, labels = labels, outfile = j(out_folder, conditions_labels[i] + '_merged_boxplot.png'))

    return data
