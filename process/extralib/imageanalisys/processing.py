import scipy.ndimage
import mahotas
import numpy as np
import scipy.stats
import loader
import output

# # # # # # # # # # # # 
#  Single image of pairs of images analysis
# # # # # # # # # # # # 

'''
Select pixel values applying a mask (0/>1 mask).
Mask must have the same size of image.
'''
def select_region(image, mask):
    selection = image[mask>0]
    return(selection)
#


'''
Identify ROIs by taking all pixels with value > 0
'''
def find_ROI(A, otsu=False, fill_holes=False):
    T = 0
    if otsu:
        T = mahotas.thresholding.otsu(A)
    C = A.copy()
    C[ C <= T ] = 0
    C[ C > T ] = 1
    filled = C
    if fill_holes:
        filled = scipy.ndimage.morphology.binary_fill_holes(C)
    filled = filled.astype(np.uint8)
    return(filled)
#


'''
Identify ROI and returns molecule intensity values of selected pixels
'''
def get_intensity(nucleus, litaf):
    nu = find_ROI(nucleus)
    regi = select_region(litaf, nu)
    return(regi)
#

def compare_distributions(dist1, dist2):
    return(scipy.stats.ranksums(dist1, dist2))
#

'''
Get molecular distribution from a deck of slices
For each slice evaluate:
- amount of molecule in pixels selected by mask
- amount of molecule in pixels from all the molecule image
- amount of molecule in pixels from all the molecule image but mask
'''
def get_molecule_distribution(dataset,
                              nucleus_index = 0, molecule_index = 1,
                              nucleus_channel = 1, molecule_channel = 0,
                              nucleus_fill_holes = True, nucleus_otsu = True,
                              molecule_fill_holes = False, molecule_otsu = True,
                              single_object_analysis = False
):

    slices = loader.load_slices(dataset)
    slices_gray = []
    for i in slices:
        slices_gray.append([])
        if not nucleus_channel == None:
            slices_gray[len(slices_gray)-1].append(loader.select_channel(i[nucleus_index], channel = nucleus_channel))
        else:
            slices_gray[len(slices_gray)-1].append(i[nucleus_index])
        if not molecule_channel == None:
            slices_gray[len(slices_gray)-1].append(loader.select_channel(i[molecule_index], channel = molecule_channel))
        else:
            slices_gray[len(slices_gray)-1].append(i[molecule_index])


    slices_mask = []
    for i in slices_gray:
        slices_mask.append([])
        slices_mask[len(slices_mask)-1].append(find_ROI(i[0], fill_holes=nucleus_fill_holes, otsu=nucleus_otsu))  # only nucleus
        slices_mask[len(slices_mask)-1].append(find_ROI(i[1], fill_holes=molecule_fill_holes, otsu=molecule_otsu))  # whole intensity

    for i in slices_mask:
        i.append(i[1]*(1.0-i[0])) # only cyto


    slices_intensity = []
    for i in range(0,len(slices_mask)):
        slices_intensity.append([])
        for j in slices_mask[i]:
            slices_intensity[len(slices_intensity)-1].append(select_region(slices_gray[i][1], j))


    merged_intensity = []
    for i in range(0,len(slices_intensity[0])):
        merged_intensity.append(np.array([]))
    for j in slices_intensity:
        for k in range(0,len(j)):
            merged_intensity[k] = np.concatenate([merged_intensity[k], j[k]])

    # slices_nuclear_intensity = slices_intensity[:][0]
    # slices_whole_intensity = slices_intensity[:][1]
    # slices_extranuclear_intensity = slices_intensity[:][2]
    # return((slices_nuclear_intensity, slices_whole_intensity, slices_extranuclear_intensity))

    data = {}
    data['slices'] = slices
    data['slices_gray'] = slices_gray
    data['slices_mask'] = slices_mask
    data['slices_intensity'] = slices_intensity
    data['merged_intensity'] = merged_intensity
    data['slices_dataset'] = dataset

    return(data)
#

# def compare_molecule_distribution(dataset,
# 		nucleus_index = 0, molecule_index = 1,
# 		nucleus_channel = 1, molecule_channel = 0,
# 		nucleus_fill_holes = True, nucleus_otsu = True,
# 		molecule_fill_holes = False, molecule_otsu = True
# 		):

def compare_molecule_distribution(datasets,
                                  nucleus_index = 0, molecule_index = 1,
                                  nucleus_channel = 1, molecule_channel = 0,
                                  nucleus_fill_holes = True, nucleus_otsu = True,
                                  molecule_fill_holes = False, molecule_otsu = True,
                                  single_object_analysis = False
):
    conditions = []
    for i in datasets:
        conditions.append(get_molecule_distribution(i,
                                                    nucleus_index = nucleus_index, molecule_index = molecule_index, nucleus_channel = nucleus_channel, molecule_channel = molecule_channel,
                                                    nucleus_fill_holes = nucleus_fill_holes, nucleus_otsu = nucleus_otsu, molecule_fill_holes = molecule_fill_holes, molecule_otsu = molecule_otsu,
                                                    single_object_analysis = single_object_analysis))
    return conditions
#

def get_molecule_pos(data):
    for i in range(0,len(data['slices_mask'])):
        temp = np.where(data['slices_mask'][i] == 1)
        XY = np.vstack((SC[0], SC[1], data['slices_mask'][i][temp]))
    return XY
#


def collect_statistics(conditions, output_folder=None):
# def compare(condition1, condition2, output_folder=None):

    nuclei_arrays = []
    for i in range(0, len(conditions)):
        nuclei_arrays.append(output.select_arrays([conditions[i]], merged = True, what = [0])[0])
    all_arrays = []
    for i in range(0, len(conditions)):
        all_arrays.append(output.select_arrays([conditions[i]], merged = True, what = [1])[0])
    diff_arrays = []
    for i in range(0, len(conditions)):
        diff_arrays.append(output.select_arrays([conditions[i]], merged = True, what = [2])[0])

    nuclei_arrays = []
    for i in range(0, len(conditions)):
        nuclei_arrays.append(output.select_arrays([conditions[i]], merged = False, what = [0])[0])
    all_arrays = []
    for i in range(0, len(conditions)):
        all_arrays.append(output.select_arrays([conditions[i]], merged = False, what = [1])[0])
    diff_arrays = []
    for i in range(0, len(conditions)):
        diff_arrays.append(output.select_arrays([conditions[i]], merged = False, what = [2])[0])


    nuclei_median = []
    nuclei_mean = []
    nuclei_var = []
    nuclei_sum = []
    for i in nuclei_arrays:
        temp = []
        for j in i:
            temp.append(np.median(j))
        nuclei_median.append(temp)
        temp = []
        for j in i:
            temp.append(np.mean(j))
        nuclei_mean.append(temp)
        temp = []
        for j in i:
            temp.append(np.sum(j))
        nuclei_sum.append(temp)
        temp = []
        for j in i:
            temp.append(np.var(j))
        nuclei_var.append(temp)

    all_median = []
    all_mean = []
    all_var = []
    all_sum = []
    for i in all_arrays:
        temp = []
        for j in i:
            temp.append(np.median(j))
        all_median.append(temp)
        temp = []
        for j in i:
            temp.append(np.mean(j))
        all_mean.append(temp)
        temp = []
        for j in i:
            temp.append(np.sum(j))
        all_sum.append(temp)
        temp = []
        for j in i:
            temp.append(np.var(j))
        all_var.append(temp)

    diff_median = []
    diff_mean = []
    diff_var = []
    diff_sum = []
    for i in diff_arrays:
        temp = []
        for j in i:
            temp.append(np.median(j))
        diff_median.append(temp)
        temp = []
        for j in i:
            temp.append(np.mean(j))
        diff_mean.append(temp)
        temp = []
        for j in i:
            temp.append(np.sum(j))
        diff_sum.append(temp)
        temp = []
        for j in i:
            temp.append(np.var(j))
        diff_var.append(temp)


    ratio_median = []
    ratio_mean = []
    ratio_sum = []
    for i in range(0, len(nuclei_arrays)):
        temp = []
        for j in range(0, len(nuclei_arrays[i])):
            temp.append(float(nuclei_median[i][j])/all_median[i][j])
        ratio_median.append(temp)
        temp = []
        for j in range(0, len(nuclei_arrays[i])):
            temp.append(float(nuclei_mean[i][j])/all_mean[i][j])
        ratio_mean.append(temp)
        temp = []
        for j in range(0, len(nuclei_arrays[i])):
            temp.append(float(nuclei_sum[i][j])/all_sum[i][j])
        ratio_sum.append(temp)

    results = {}
    results['median'] = [nuclei_median, all_median, diff_median]
    results['mean'] = [nuclei_mean, all_mean, diff_mean]
    results['sum'] = [nuclei_sum, all_sum, diff_sum]
    results['median_ratio'] = ratio_median
    results['mean_ratio'] = ratio_mean
    results['sum_ratio'] = ratio_sum

    return(results)
#

def compare_statistics(x):
    statistics = np.zeros((len(x['sum_ratio'])*(len(x['sum_ratio'])-1)/2 , 6))
    cup = 0
    for i in range(0, len(x['sum_ratio'])-1):
        for j in range(i+1, len(x['sum_ratio'])):
            print str(i) + '  ' + str(j)
            # print x['median'][0][i]
            # print x['median'][0][j]
            statistics[cup,:] = [
                scipy.stats.ranksums(x['median'][0][i], x['median'][0][j])[1]
                ,scipy.stats.ranksums(x['mean'][0][i], x['mean'][0][j])[1]
                ,scipy.stats.ranksums(x['sum'][0][i], x['sum'][0][j])[1]
                ,scipy.stats.ranksums(x['median_ratio'][i], x['median_ratio'][j])[1]
                ,scipy.stats.ranksums(x['mean_ratio'][i], x['mean_ratio'][j])[1]
                ,scipy.stats.ranksums(x['sum_ratio'][i], x['sum_ratio'][j])[1]
            ]
            cup += 1

    return(statistics)

def save_statistics(x, output_file, condition_labels):
    h = open(output_file, 'w')
    nr = 0
    for i in range(0, len(condition_labels)-1):
        for j in range(i+1, len(condition_labels)):
            rc = condition_labels[i] + "\t" + condition_labels[j]
            row = x[nr, :]
            for k in row:
                rc += "\t" + str(k)
            print rc
            h.write(rc + "\n")
            nr += 1
    h.close()
    #


    # def all_statistics(x, out_folder, condition_labels = None, obj_labels = None, channel_labels = None):
    # 	for i in range(0, len(x)-1):
    # 		for j in range(i+1, len(x)):
    # 			statistics = processing.compare(x[i], x[j])

    # 			print(condition_labels[i] + '\t' +
    # 			condition_labels[j] + '\t' +
    # 			str(statistics['rank_sum_median'][1]) + '\t' +
    # 			str(statistics['rank_sum_mean'][1]) + '\t' +
    # 			str(statistics['rank_sum_sum'][1]) + '\t' +
    # 			str(statistics['rank_sum_median_ratio'][1]) + '\t' +
    # 			str(statistics['rank_sum_mean_ratio'][1]) + '\t' +
    # 			str(statistics['rank_sum_sum_ratio'][1]) + '\n')

    # #