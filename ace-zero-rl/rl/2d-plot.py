import matplotlib.pyplot as plt
import numpy as np
import csv

# Plots 2D blue vs. red
blue_x = []
blue_y = []
red_x = []
red_y = []

with open("../rl_results/eligibility_traces_cql_2d2.json/00030000-0050/test-result-00-024900.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    line_no = 1
    for row in reader:
        line_no += 1
        if line_no > 9: #and line_no < 1000:
            if len(row) == 0:
                break
            blue_x.append(float(row[1]))
            blue_y.append(float(row[2]))
            red_x.append(float(row[4]))
            red_y.append(float(row[5]))

# print len(blue_x)
# plt.plot(blue_x, blue_y, 'b')
# plt.plot(red_x, red_y, 'r')
# #plt.axis([0, 6, 0, 20])
# plt.show()
# raw_input("hi")
# plt.show()

import matplotlib.pyplot as plt
import numpy as np


def plot_figures(figures, nrows = 1, ncols=1):
    """Plot a dictionary of figures.

    Parameters
    ----------
    figures : <title, figure> dictionary
    ncols : number of columns of subplots wanted in the display
    nrows : number of rows of subplots wanted in the figure
    """

    fig, axeslist = plt.subplots(ncols=ncols, nrows=nrows)
    for ind,title in enumerate(figures):
        axeslist.ravel()[ind].imshow(figures[title], cmap=plt.gray())
        axeslist.ravel()[ind].set_title(title)
        axeslist.ravel()[ind].set_axis_off()
    plt.tight_layout() # optional
    plt.show()
# generation of a dictionary of (title, images)
number_of_im = 10
figures = {'im'+str(i): np.random.randn(100, 100) for i in list(range(number_of_im))}

# plot of the images in a figure, with 2 rows and 3 columns
plot_figures(figures, 2, 5)
