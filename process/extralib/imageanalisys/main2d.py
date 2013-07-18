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

def main_api(conditions, out_folder, condition_labels = None, slice_labels = None, channel_labels = None,
             mask_index = 0, molecule_index = 1, mask_channel = None, molecule_channel = None,
             mask_otsu = True, mask_fillholes = True, molecule_otsu = False, molecule_fillholes = False,
             single_object_analysis = False):

    # TODO: for debugging
    # print "condi: " + str(conditions)
    # print "out" + str(out_folder)
    # print "cond_labels" + str(condition_labels)
    # print "slice_labels " + str(type(slice_labels))
    # print "chan_labels" + str(channel_labels)
    # print "mask_idx" + str(mask_index)
    # print "mol_idx" + str(molecule_index)
    # print "mask_chan" + str(mask_channel)
    # print "mol_chan" + str(molecule_channel)
    # print "mask_otsu" + str(mask_otsu)
    # print "mask_fill" + str(mask_fillholes)
    # print "molecule_otsu" + str(molecule_otsu)
    # print "molecule_fill" + str(molecule_fillholes)
    # print "single_obj" + str(single_object_analysis)


    if not exists(out_folder):
        mkdir(out_folder)

    if str(channel_labels) == '':
        channel_labels = None
    if str(condition_labels) == '':
        condition_labels = None
    if str(slice_labels) == '':
        slice_labels = None
    if str(mask_channel) == '':
        mask_channel = None
    if str(molecule_channel) == '':
        molecule_channel = None

    proc = processing.compare_molecule_distribution(conditions,
            nucleus_index = mask_index, molecule_index = molecule_index,
            nucleus_channel = mask_channel, molecule_channel = molecule_channel,
            nucleus_fill_holes = mask_fillholes, nucleus_otsu = mask_otsu,
            molecule_fill_holes = molecule_fillholes, molecule_otsu = molecule_otsu,
            single_object_analysis=single_object_analysis)

    out = processing.collect_statistics(proc, out_folder)
    out = processing.compare_statistics(out)
    processing.save_statistics(out, out_folder + '/condition_comparison_pvalues.txt', condition_labels)
    out = output.plot_all(proc, conditions, out_folder,
                          condition_labels=condition_labels, obj_labels=slice_labels, channel_labels=channel_labels)

    return out_folder
