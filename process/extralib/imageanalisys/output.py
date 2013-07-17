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


def plot(data):
    cmap = cm.Greys_r
    plt.imshow(data, cmap)
    plt.show()

#

def histogram(data, labels=None, outfile=None):
    if labels == None:
        labels = [''] * len(data)
    for i in range(0, len(data)):
        plt.hist(data[i], bins=255, alpha=0.5, label=labels[i])
    plt.xlabel('Intensity')
    plt.ylabel('Number of occurrencies')
    plt.xlim(0, 256)
    plt.legend()
    if outfile == None:
        plt.show()
    else:
        plt.savefig(outfile)

#

def boxplot(x, labels=None, outfile=None, xlab='', ylab=''):
    if labels == None:
        labels = [''] * len(x)
    r = plt.boxplot(x)
    plt.setp(r['medians'], color='black')
    plt.setp(r['boxes'], color='black')
    plt.setp(r['fliers'], color='gray')
    plt.setp(r['whiskers'], color='black', lw=2)
    plt.setp(r['caps'], color='black', lw=2)
    plt.xticks(range(1, len(x) + 1), labels)
    # y=range(0,256)
    # plt.yticks(y, y)
    plt.ylim(0, 256)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    if outfile == None:
        plt.show()
    else:
        plt.savefig(outfile)

#
