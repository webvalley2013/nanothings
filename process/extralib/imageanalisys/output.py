# This file is part of nanothings.
#
#     nanothings is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero GPL as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero GPL for more details.
#
#     You should have received a copy of the GNU Affero GPL
#     along with nanothings.  If not, see <http://www.gnu.org/licenses/>.
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math


def plot(data):
    plt.clf()
    cmap = cm.Greys_r
    plt.imshow(data, cmap)
    plt.show()

#

def histogram(data, labels=None, outfile=None, log=False, histtype='stepfilled', bins=255, color=None):
    fig = plt.figure(figsize=(23.5, 13.0))
    if labels == None:
        labels = [''] * len(data)
    if len(labels) < len(data):
        labels = labels * int(math.ceil(float(len(data)) / len(labels)))
    plt.clf()
    minim = 1
    maxim = 0
    for i in range(0, len(data)):
        temp = plt.hist(data[i], bins=bins, alpha=0.5, label=labels[i], log=log, histtype=histtype)
        if maxim < temp[0].max():
            maxim = temp[0].max()

    plt.clf()
    for i in range(0, len(data)):
        if color == None:
            plt.hist(data[i], bins=bins, alpha=0.5, label=labels[i], log=log, histtype=histtype)
        else:
            plt.hist(data[i], bins=bins, alpha=0.5, label=labels[i], log=log, histtype=histtype, color=color[i])

    plt.xlabel('Intensity')
    plt.ylabel('Number of occurrences')
    plt.xlim(0, 256)
    plt.ylim(minim, maxim)
    plt.legend()
    if outfile == None:
        plt.show()
    else:
        plt.savefig(outfile, dpi=72)

#

def boxplot(x, labels=None, outfile=None, xlab='', ylab='', xrot=0):
    fig = plt.figure(figsize=(23.5, 13.0))
    # plt.clf()
    if labels == None:
        labels = [''] * len(x)
    if len(labels) < len(x):
        labels = labels * int(math.ceil(float(len(x)) / len(labels)))
    r = plt.boxplot(x)
    plt.setp(r['medians'], color='black')
    plt.setp(r['boxes'], color='black')
    plt.setp(r['fliers'], color='gray')
    plt.setp(r['whiskers'], color='black', lw=2)
    plt.setp(r['caps'], color='black', lw=2)
    plt.xticks(range(1, len(x) + 1), labels, rotation=xrot)
    # y=range(0,256)
    # plt.yticks(y, y)
    plt.ylim(0, 256)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    if outfile == None:
        plt.show()
    else:
        plt.savefig(outfile, dpi=72)

#

def select_images(conditions, name='slices_mask', what=[0]):
    data = []
    for i in conditions:
        for j in i[name]:
            for k in what:
                data.append(j[k])
    # version with dict first and list after
    return (data)

#

def select_arrays(conditions, merged=False, what=[0]):
    data = []
    if merged:
        tos = 'merged_intensity'
        for i in conditions:
            j = i[tos]
            for k in what:
                data.append(j[k])
    else:
        tos = 'slices_intensity'
        for i in conditions:
            for j in i[tos]:
                for k in what:
                    data.append(j[k])
    # version with dict first and list after
    return (data)

#

# def print_single_histograms(data, folder = '.'):

# 	fna = folder + "/slice_"
# 	data['slices']
# 	data['slices_gray'] = slices_gray
# 	data['slices_mask'] = slices_mask
# 	data['slices_dataset'] = dataset

# 	fna = folder + "/intensity_"

# 	boxplot()
# 	for i in data['slices_intensity']:
# 		histogram


# 	data['merged_intensity'] = merged_intensity



# #
