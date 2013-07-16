import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from . import loader
from . import processing
from . import output

cmap = cm.Greys_r

def main():
    condition1_files = [
    ['LX-2/NT/01_nucleus.tif', 'LX-2/NT/01_LITAF.tif'],
    ['LX-2/NT/02_nucleus.tif', 'LX-2/NT/02_LITAF.tif'],
    ['LX-2/NT/03_nucleus.tif', 'LX-2/NT/03_LITAF.tif'],
    ['LX-2/NT/04_nucleus.tif', 'LX-2/NT/04_LITAF.tif']]
    
    condition2_files = [
    ['LX-2/2hLPS500/01_nucleus.tif', 'LX-2/2hLPS500/01_LITAF.tif'],
    ['LX-2/2hLPS500/02_nucleus.tif', 'LX-2/2hLPS500/02_LITAF.tif'],
    ['LX-2/2hLPS500/03_nucleus.tif', 'LX-2/2hLPS500/03_LITAF.tif'],
    ['LX-2/2hLPS500/04_nucleus.tif', 'LX-2/2hLPS500/04_LITAF.tif']]
    
    condition1 = processing.get_molecule_distribution(condition1_files)
    condition2 = processing.get_molecule_distribution(condition2_files)
    
    labels_1 = ['NT 01', 'NT 02', 'NT 03', 'NT 04']
    labels_2 = ['LPS500 01', 'LPS500 02', 'LPS500 03', 'LPS500 04']
    
    nuclei_intensity_c1 = []
    for i in condition1['slices_intensity']:
    	nuclei_intensity_c1.append(i[0])
    
    nuclei_intensity_c2 = []
    for i in condition2['slices_intensity']:
    	nuclei_intensity_c2.append(i[0])
    
    extranuclei_intensity_c1 = []
    for i in condition1['slices_intensity']:
    	extranuclei_intensity_c1.append(i[2])
    
    extranuclei_intensity_c2 = []
    for i in condition2['slices_intensity']:
    	extranuclei_intensity_c2.append(i[2])
    
    nuclei_intensity = nuclei_intensity_c1 +  nuclei_intensity_c2
    output.boxplot(nuclei_intensity, outfile='prova.png')

if __name__ == "__main__":
    main()

# plt.hist(merged_intensity[0], bins=255, color='r', alpha=0.5)
# plt.hist(merged_intensity[1], bins=255, color='g', alpha=0.5)
# plt.hist(merged_intensity[2], bins=255, color='b', alpha=0.5)
# plt.show()

# plt.hist(slices_1_intensity[0][0], bins=255, color='r', alpha=0.5)
# plt.hist(slices_1_intensity[0][1], bins=255, color='g', alpha=0.5)
# plt.hist(slices_1_intensity[0][2], bins=255, color='b', alpha=0.5)
# plt.show()

# scipy.stats.ranksums(LPS500res[0][0], NAres[2][0])






# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# cmap = cm.Greys_r

# import loader
# import processing
# import output

# # input:
# # input files (list of lists, condition1:[slice1:[img1, img2, ...], slice2:[img3, img4, ...]])
# # input params: condition1 files, condition2 files, roi channel index, molecule channel index
# # 

# '''
# Compares 2 conditions
# Assume slices are described by N images. nucleus/molecule concentration (or any molecule to be considered)
# '''

# slices1_data = load.load_slices(slices1)
# slices_1_gray = []
# 	for i in slices_1:
# 		slices_1_gray.append([])
# 		slices_1_gray[len(slices_1_gray)-1].append(load.select_channel(i[0], channel = 1))
# 		slices_1_gray[len(slices_1_gray)-1].append(load.select_channel(i[1], channel = 0))

# 	slices2_data = load.load_slices(slices2)
# 	slice1_distrib = []
# 	for i in slices1_data:
# 		slice1_distrib.append(analysis.get_intensity(i[0], i[1]))
# 	slice2_distrib = []
# 	for i in slices2_data:
# 		slice2_distrib.append(analysis.litafnucleus(i[0], i[1]))
# 	return(slice1_distrib, slice2_distrib)

# def analyze_slices(slices1, slices2):
# 	slices1_data = load.load_slices(slices1)
# 	slices_1_gray = []
# 	for i in slices_1:
# 		slices_1_gray.append([])
# 		slices_1_gray[len(slices_1_gray)-1].append(load.select_channel(i[0], channel = 1))
# 		slices_1_gray[len(slices_1_gray)-1].append(load.select_channel(i[1], channel = 0))

# 	slices2_data = load.load_slices(slices2)
# 	slice1_distrib = []
# 	for i in slices1_data:
# 		slice1_distrib.append(analysis.get_intensity(i[0], i[1]))
# 	slice2_distrib = []
# 	for i in slices2_data:
# 		slice2_distrib.append(analysis.litafnucleus(i[0], i[1]))
# 	return(slice1_distrib, slice2_distrib)
# #

# AC = [
# 	['data/AC_HSC_CTRL/01_nucleus.tif','data/AC_HSC_CTRL/01_LITAF.tif'],
# 	['data/AC_HSC_CTRL/02_nucleus.tif','data/AC_HSC_CTRL/02_LITAF.tif'],
# 	['data/AC_HSC_CTRL/03_nucleus.tif','data/AC_HSC_CTRL/03_LITAF.tif'],
# 	['data/AC_HSC_CTRL/04_nucleus.tif','data/AC_HSC_CTRL/04_LITAF.tif'],
# 	['data/AC_HSC_CTRL/05_nucleus.tif','data/AC_HSC_CTRL/05_LITAF.tif'],
# 	['data/AC_HSC_CTRL/06_nucleus.tif','data/AC_HSC_CTRL/06_LITAF.tif']
# 	]

# NA = [
# 	['data/NA_HSC_CTRL/01_nucleus.tif','data/NA_HSC_CTRL/01_LITAF.tif'],
# 	['data/NA_HSC_CTRL/02_nucleus.tif','data/NA_HSC_CTRL/02_LITAF.tif'],
# 	['data/NA_HSC_CTRL/03_nucleus.tif','data/NA_HSC_CTRL/03_LITAF.tif'],
# 	['data/NA_HSC_CTRL/04_nucleus.tif','data/NA_HSC_CTRL/04_LITAF.tif'],
# 	['data/NA_HSC_CTRL/05_nucleus.tif','data/NA_HSC_CTRL/05_LITAF.tif'],
# 	['data/NA_HSC_CTRL/06_nucleus.tif','data/NA_HSC_CTRL/06_LITAF.tif']
# 	]

# intensity = analyze_slices(AC, NA)

# plt.boxplot([intensity[0][0],intensity[1][0]])
# output_file = 'test.png'
# plt.savefig(output_file)

