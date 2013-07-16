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
