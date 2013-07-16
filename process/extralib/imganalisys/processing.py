import scipy.ndimage
import mahotas
import numpy as np
import scipy.stats
from . import loader

# # # # # # # # # # # # 
#  Single image of pairs of images analysis
# # # # # # # # # # # # 

'''
Select pixel values applying a mask (0/>1 mask).
Mask must have the same size of image.
'''


def select_region(image, mask):
    selection = image[mask > 0]
    return (selection)

#


'''
Identify ROIs by taking all pixels with value > 0
'''


def find_ROI(A, otsu=False, fill_holes=False):
    T = 0
    if otsu:
        T = mahotas.thresholding.otsu(A)
    C = A.copy()
    C[C <= T] = 0
    C[C > T] = 1
    filled = C
    if fill_holes:
        filled = scipy.ndimage.morphology.binary_fill_holes(C)
    filled = filled.astype(np.uint8)
    return (filled)

#


'''
Identify ROI and returns molecule intensity values of selected pixels
'''


def get_intensity(nucleus, litaf):
    nu = find_ROI(nucleus)
    regi = select_region(litaf, nu)
    return (regi)

#

def compare_distributions(dist1, dist2):
    return (scipy.stats.ranksums(dist1, dist2))

#

'''
Get molecular distribution from a deck of slices
'''


def get_molecule_distribution(dataset,
                              nucleus_index=0, molecule_index=1,
                              nucleus_channel=1, molecule_channel=0,
                              nucleus_fill_holes=True, nucleus_otsu=True,
                              molecule_fill_holes=False, molecule_otsu=True
):
    slices = loader.load_slices(dataset)
    slices_gray = []
    for i in slices:
        slices_gray.append([])
        if not nucleus_channel == None:
            slices_gray[len(slices_gray) - 1].append(loader.select_channel(i[nucleus_index], channel=nucleus_channel))
        else:
            slices_gray[len(slices_gray) - 1].append(i[nucleus_index])
        if not molecule_channel == None:
            slices_gray[len(slices_gray) - 1].append(loader.select_channel(i[molecule_index], channel=molecule_channel))
        else:
            slices_gray[len(slices_gray) - 1].append(i[molecule_index])

    slices_mask = []
    for i in slices_gray:
        slices_mask.append([])
        slices_mask[len(slices_mask) - 1].append(
            find_ROI(i[0], fill_holes=nucleus_fill_holes, otsu=nucleus_otsu))  # only nucleus
        slices_mask[len(slices_mask) - 1].append(
            find_ROI(i[1], fill_holes=molecule_fill_holes, otsu=molecule_otsu))  # whole cell

    for i in slices_mask:
        i.append(i[1] * (1.0 - i[0])) # only cyto

    slices_intensity = []
    for i in range(0, len(slices_mask)):
        slices_intensity.append([])
        for j in slices_mask[i]:
            slices_intensity[len(slices_intensity) - 1].append(select_region(slices_gray[i][1], j))

    merged_intensity = []
    for i in range(0, len(slices_intensity[0])):
        merged_intensity.append(np.array([]))
    for j in slices_intensity:
        for k in range(0, len(j)):
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

    return (data)
    #

    # def compare_molecule_distribution(dataset,
    # 		nucleus_index = 0, molecule_index = 1,
    # 		nucleus_channel = 1, molecule_channel = 0,
    # 		nucleus_fill_holes = True, nucleus_otsu = True,
    # 		molecule_fill_holes = False, molecule_otsu = True
    # 		):