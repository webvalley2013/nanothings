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

'''
Load single image
Input: filename
Output: ndarray
'''


def load_image(filename):
    temp = plt.imread(filename)
    return (temp)

#

'''
Load a set of images for the same slice.
Input: list of image filenames
Output: list of ndarrayas (in the same order as input data)
'''


def load_slice(filenames, togray=False):
    temp = []
    for i in filenames:
        ndarr = load_image(i)
        if togray:
            ndarr = select_channel(ndarr, 0) # move outside
        temp.append(ndarr)
    return (temp)

#

'''
Load several slices.
Input: list of lists of image filenames
Output: list of lists of ndarrayas (in the same order as input data)
'''


def load_slices(slices, togray=False):
    slices_data = []
    for i in slices:
        slices_data.append(load_slice(i, togray))
    return (slices_data)

#

# Select different channels 

'''
Select only 1 channel from multichannel images
Input: ndarray (more than 2 dimensions)
Output: ndarray (2 dimensions)
'''


def select_channel(ndarr, channel=0):
    temp = ndarr[:, :, channel]
    return (temp)

#

# '''
# Load stack of slices (multiple images per slice supported)
# Input: list of lists of image filenames
# Output: list of lists of ndarrayas (in the same order as input data)
# '''
# # def loadstack(filenames):
# 	temp = []
# 	for i in filenames:
# 		temp.append(loadslice[i])
# 	return(temp)
#
