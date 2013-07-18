import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from PIL import Image
from scipy.stats import gaussian_kde

def plot(data, outfile = None):
    fig = plt.figure(figsize=(15.0, 15.0))
    cmap = cm.Greys_r
    plt.imshow(data, cmap)
    if outfile == None:
        plt.show()
    else:
        plt.savefig(outfile, dpi=100)
#

def histogram(data, labels = None, outfile = None, log=False, histtype='stepfilled', bins=255, color = None, freq = False, density = False):
    fig = plt.figure(figsize=(15.0, 10.0))
    if labels == None:
        labels = [''] * len(data)
    if len(labels) < len(data):
        labels = labels * int(math.ceil(float(len(data))/ len(labels)))

    plt.clf()

    if density:

        minim = 0
        maxim = 0
        xminim = 0
        xmaxim = 256

        for i in range(0,len(data)):
            temp = plt.hist(data[i], normed = True, bins=bins, alpha=0.5, label = labels[i], log=log, histtype=histtype)
            if maxim < temp[0].max():
                maxim = temp[0].max()
            if xmaxim < temp[1].max():
                xmaxim = math.ceil(temp[1].max())
        plt.clf()
        for i in range(0,len(data)):
            if color == None:
                try:
                    dataf = data[i].astype(np.float32)
                    density = gaussian_kde(dataf)
                    xs = np.linspace(xminim,xmaxim,bins)
                    density.covariance_factor = lambda : .25
                    density._compute_covariance()
                    plt.plot(xs,density(xs), label = labels[i])
                except Exception:
                    pass
            # plt.hist(data[i], bins=bins, alpha=0.5, label = labels[i], log=log, histtype=histtype)
            else:
                try:
                    dataf = data[i].astype(np.float32)
                    density = gaussian_kde(dataf)
                    xs = np.linspace(xminim,xmaxim,bins)
                    density.covariance_factor = lambda : .25
                    density._compute_covariance()
                    plt.plot(xs,density(xs), label = labels[i], color = color[i])
                except Exception:
                    pass
        plt.xlabel('Intensity')
        plt.ylabel('Number of occurrences')
        plt.xlim(0, xmaxim)
        # plt.ylim(minim, maxim)
        plt.legend()

    elif freq:
        minim = 0
        maxim = 0
        xminim = 0
        xmaxim = 256

        for i in range(0,len(data)):
            temp = plt.hist(data[i], normed = True, bins=bins, alpha=0.5, label = labels[i], log=log, histtype=histtype)
            if maxim < temp[0].max():
                maxim = temp[0].max()
            if xmaxim < temp[1].max():
                xmaxim = math.ceil(temp[1].max())

        plt.clf()
        for i in range(0,len(data)):
            if color == None:
                plt.hist(data[i], normed = True, bins=bins, alpha=0.5, label = labels[i], log=log, histtype=histtype)
            else:
                plt.hist(data[i], normed = True, bins=bins, alpha=0.5, label = labels[i], log=log, histtype=histtype, color = color[i])

        plt.xlabel('Intensity')
        plt.ylabel('Number of occurrences')
        plt.xlim(0, xmaxim)
        plt.ylim(minim, maxim)
        plt.legend()
    else:
        minim = 1
        maxim = 0
        xminim = 0
        xmaxim = 256
        for i in range(0,len(data)):
            temp = plt.hist(data[i], bins=bins, alpha=0.5, label = labels[i], log=log, histtype=histtype)
            if maxim < temp[0].max():
                maxim = temp[0].max()
            if xmaxim < temp[1].max():
                xmaxim = math.ceil(temp[1].max())

        plt.clf()
        for i in range(0,len(data)):
            if color == None:
                plt.hist(data[i], bins=bins, alpha=0.5, label = labels[i], log=log, histtype=histtype)
            else:
                plt.hist(data[i], bins=bins, alpha=0.5, label = labels[i], log=log, histtype=histtype, color = color[i])

        plt.xlabel('Intensity')
        plt.ylabel('Number of occurrences')
        plt.xlim(0, xmaxim)
        plt.ylim(minim, maxim)
        plt.legend()

    if outfile == None:
        plt.show()
    else:
        plt.savefig(outfile, dpi=150)
#

def boxplot(x, labels = None, outfile = None, xlab = '', ylab = '', ylim = 256, xrotation=0):
    fig = plt.figure(figsize=(23.5, 13.0))
    if labels == None:
        labels = [''] * len(x)
    if len(labels) < len(x):
        labels = labels * int(math.ceil(float(len(x))/ len(labels)))
    r = plt.boxplot(x)
    plt.setp(r['medians'], color='black')
    plt.setp(r['boxes'], color='black')
    plt.setp(r['fliers'], color='gray')
    plt.setp(r['whiskers'], color='black', lw=2)
    plt.setp(r['caps'], color='black', lw=2)
    plt.xticks(range(1,len(x)+1), labels, rotation=xrotation)
    # y=range(0,256)
    # plt.yticks(y, y)

    # plt.ylim(0, ylim)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    if outfile == None:
        plt.show()
    else:
        plt.savefig(outfile, dpi=150)
#

def select_images(conditions, name = 'slices_mask', what=[0]):
    data = []
    for i in conditions:
        for j in i[name]:
            for k in what:
                data.append(j[k])
    # version with dict first and list after
    return(data)
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
    return(data)
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

'''
Build a flat list of images from data.
Input parameters:
- x: list of condition/dataset datastructures
- name: the set to consider. Can be 'slices_mask', 'slices_gray', 'objs_mask', 'objs_gray', 
- what: the subset to consider. List comprising 0 (only mask), 1 (all), or 2 (all - mask)
- condition_labels: optional list of condition labels for labeling output data
- obj_labels: optional list of slice/object labels for labeling output data
- channel_labels: optional list of channel labels for labeling output data (i.e. nucleus, all, all - nucleus)

The flat list is ordered by [condition][[slice/object]][[[channel]]].
'''

def select_images(x, name = 'slices_mask', what=[0],  condition_labels = None, obj_labels = None, channel_labels = None):
    data = []
    labels = []
    for i in range(0, len(x)):
        if not condition_labels == None:
            temp = condition_labels[i]
        else:
            temp = 'condition ' + str(i)
        for j in range(0, len(x[i][name])):
            if not obj_labels == None:
                temp2 = temp + ' - ' + obj_labels[i][j]
            else:
                temp2 = temp + ' - ' + 'sample ' + str(j)
            for k in what:
                data.append(x[i][name][j][k])
                if not channel_labels == None:
                    labels.append(temp2 + ' - ' + channel_labels[k])
                else:
                    labels.append(temp2 + ' - ' + 'ch. ' + str(k))

    # version with dict first and list after
    return(data, labels)
#

'''
Build a flat list of arrays from data.
Input parameters:
- x: list of condition/dataset datastructures
- name: the set to consider. Can be 'slices_intensity', 'objs_intensity'
- merged: whether merged data should be considered
- what: the subset to consider. List comprising 0 (only mask), 1 (all), or 2 (all - mask)
- condition_labels: optional list of condition labels for labeling output data
- obj_labels: optional list of slice labels for labeling output data
- channel_labels: optional list of channel labels for labeling output data (i.e. nucleus, all, all - nucleus)

The flat list is ordered by [condition][[slice]][[[channel]]].
'''

def select_arrays(x, name = 'slices_intensity', merged=False, what=[0], condition_labels = None, obj_labels = None, channel_labels = None):
    data = []
    labels = []
    if merged:
        tos = 'merged_intensity'
        for i in range(0, len(x)):
            if not condition_labels == None:
                temp1 = condition_labels[i]
            else:
                temp1 = 'condition ' + str(i)
            j = x[i][tos]
            temp2 = 'merged'
            for k in what:
                data.append(j[k])
                if not channel_labels == None:
                    labels.append(temp1 + ' - ' + temp2 + ' - ' + channel_labels[k])
                else:
                    labels.append(temp1 + ' - ' + temp2 + ' - ' + 'ch. ' + str(k))
    else:
        tos = name
        for i in range(0, len(x)):
            if not condition_labels == None:
                temp1 = condition_labels[i]
            else:
                temp1 = 'condition ' + str(i)
            for j in range(0, len(x[i][tos])):
                if not obj_labels == None:
                    temp2 = obj_labels[i][j]
                else:
                    temp2 = 'obj_' + str(j)
                for k in what:
                    data.append(x[i][tos][j][k])
                    if not channel_labels == None:
                        labels.append(temp1 + ' - ' + temp2 + ' - ' + channel_labels[k])
                    else:
                        labels.append(temp1 + ' - ' + temp2 + ' - ' + 'ch. ' + str(k))
    return(data, labels)
#

def plot_all(data, conditions, out_folder = '.', condition_labels = None, obj_labels = None, channel_labels = None):

# SINGLE CONDITION - mask vs all - histo + boxplot - merged slices
    for i in range(0,len(data)):
        temp = select_arrays([data[i]],
                             name = 'slices_intensity', merged = True, what = [0,1],
                             condition_labels = [condition_labels[i]], obj_labels = obj_labels, channel_labels = channel_labels)
        color = ['green', 'red']*(len(temp[0])/2)
        histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = color, outfile = out_folder + '/' + condition_labels[i] + '_merged_histogram.png')
        histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = color, outfile = out_folder + '/' + condition_labels[i] + '_merged_histogram_density.png', density=True)
        boxplot(temp[0], labels = temp[1], outfile = out_folder + '/' + condition_labels[i] + '_merged_boxplot.png', xrotation = 45)

    # SINGLE CONDITION - mask vs all - histo + boxplot - single slices
    for i in range(0,len(data)):
        temp = select_arrays([data[i]],
                             name = 'slices_intensity', merged = False, what = [0,1],
                             condition_labels = [condition_labels[i]], obj_labels = obj_labels, channel_labels = channel_labels)
        color = ['green', 'red']*(len(temp[0])/2)
        histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = color, outfile = out_folder + '/' + condition_labels[i] + '_histogram.png')
        histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = color, outfile = out_folder + '/' + condition_labels[i] + '_histogram_density.png', density=True)
        boxplot(temp[0], labels = temp[1], outfile = out_folder + '/' + condition_labels[i] + '_boxplot.png', xrotation = 45)

    # INTER CONDITION - masks - histo + boxplot - merged slices
    temp = select_arrays(data,
                         name = 'slices_intensity', merged = True, what = [0],
                         condition_labels = condition_labels, obj_labels = obj_labels, channel_labels = channel_labels)

    boxplot(temp[0], labels = temp[1], outfile = out_folder + '/' + 'merged_boxplots.png', xrotation = 45)
    histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = None, outfile = out_folder + '/' + 'merged_histograms.png')
    histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = None, outfile = out_folder + '/' + 'merged_histograms_density.png', density=True)

    # PAIRWISE INTER CONDITION - masks - histo + boxplot - single slices
    for i in range(0,len(data)-1):
        for j in range(i+1,len(data)):
            temp = select_arrays([data[i], data[j]],
                                 name = 'slices_intensity', merged = False, what = [0],
                                 condition_labels = [condition_labels[i],condition_labels[j]], obj_labels = obj_labels, channel_labels = channel_labels)

            color1 = ['red'] *len(conditions[i])
            color2 = ['green'] * len(conditions[j])
            color = color1 + color2

            histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = color,
                      outfile = out_folder + '/' + condition_labels[i] + '-' + condition_labels[j] + '_histogram.png')
            histogram(temp[0], log=True, labels = temp[1], histtype='stepfilled', bins=128, color = color,
                      outfile = out_folder + '/' + condition_labels[i] + '-' + condition_labels[j] + '_histogram_filled.png')
            histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = color,
                      outfile = out_folder + '/' + condition_labels[i] + '-' + condition_labels[j] + '_histogram_freq.png', freq=True)

            histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = color,
                      outfile = out_folder + '/' + condition_labels[i] + '-' + condition_labels[j] + '_histogram_density.png', density=True)
            histogram(temp[0], log=True, labels = temp[1], histtype='stepfilled', bins=128, color = color,
                      outfile = out_folder + '/' + condition_labels[i] + '-' + condition_labels[j] + '_histogram_filled_density.png', density=True)
            histogram(temp[0], log=True, labels = temp[1], histtype='step', bins=128, color = color,
                      outfile = out_folder + '/' + condition_labels[i] + '-' + condition_labels[j] + '_histogram_density_density.png', density=True)


            boxplot(temp[0], labels = temp[1], outfile = out_folder + '/' + condition_labels[i]  + '-' + condition_labels[j] + '_boxplot.png', xrotation = 45)


        # SINGLE SLICE - masks and molecule masks - BWplots - single slices

    for j in range(0,len(data)):
        mask = select_images([data[j]], name = 'slices_mask', what = [0],
                             condition_labels = [condition_labels[j]], obj_labels = obj_labels, channel_labels = channel_labels)
        molecule = select_images([data[j]], name = 'slices_mask', what = [1],
                                 condition_labels = [condition_labels[j]], obj_labels = obj_labels, channel_labels = channel_labels)
        for i in range(0, len(mask[0])):
            A = mask[0][i].copy()
            plot(A, out_folder + '/' + mask[1][i] + '_mask.tif')
            A = molecule[0][i].copy()
            plot(A, out_folder + '/' + molecule[1][i] + '_mask.tif')

        # SINGLE SLICE - masks and molecule gray - BWplots - single slices

    for j in range(0,len(data)):
        mask = select_images([data[j]], name = 'slices_gray', what = [0],
                             condition_labels = [condition_labels[j]], obj_labels = obj_labels, channel_labels = channel_labels)
        molecule = select_images([data[j]], name = 'slices_gray', what = [1],
                                 condition_labels = [condition_labels[j]], obj_labels = obj_labels, channel_labels = channel_labels)
        for i in range(0, len(mask[0])):
            A = mask[0][i].copy()
            plot(A, out_folder + '/' + mask[1][i] + '_gray.tif')
            A = molecule[0][i].copy()
            plot(A, out_folder + '/' + molecule[1][i] + '_gray.tif')
            #