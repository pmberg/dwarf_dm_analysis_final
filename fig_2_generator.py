import bilby
import numpy as np
import matplotlib.pyplot as plt
import corner

def make_corner_plot(file_dir_name, final_title, final_photo_name):
    """
    Parameters:

    file_dir_name: The name of a directory from which a bilby-compatible JSON file can be read off.
    final_title: The final title that is desired for the matplotlib figure.
    final_photo_name: The final name that is desired for the resulting PNG file.
    
    Returns:
    Nothing.
    Creates a file containing a corner plot of the five parameters derived in a Jeans analysis result.
    """
    
    plt.clf()
    bil_result = bilby.core.result.read_in_result(filename = file_dir_name)
    samples = bil_result.samples
    ndim = 5
    for x in range(ndim):
        if x != 1:
            samples[:,x] = np.log10(samples[:,x])
    labels = bil_result.parameter_labels
    for x in range(ndim):
        if x != 1:
            labels[x] = "log " + labels[x]
    labels[0] = "$\mathrm{log}(r_{dm})\; \mathrm{(kpc)}$"
    labels[1] = "$\gamma\; \mathrm{(unitless)}$"
    labels[2] = "$\mathrm{log}(ρ_0)\;(M_☉/kpc^3)$"
    labels[3] = "$\mathrm{log}(L) \;(L_☉)$"
    labels[4] = "$\mathrm{log}(r_{*})\; \mathrm{(kpc)}$"
    fig1 = corner.corner(samples, labels=labels)
    print(samples)
    print(labels)
    axes = np.array(fig1.axes).reshape((5,5))
    #plt.suptitle(final_title, fontsize = 16)
    plt.savefig(final_photo_name)
    #Gamma is in position 1 along the y-axis, and position 1 along the x-axis.

file_dir_list = []
final_photo_name_list = []
final_title_list = []


galsize = 1000
gal_name = "m10q_res30"
gal_count = "01"
file_dir = "jeans_results/" + gal_name + "_size" + str(galsize) + "_" + gal_count + "/jeans_result.json"
final_photo_name = "fig_02_v3.png"
final_title = "Figure 2"
make_corner_plot(file_dir, final_title, final_photo_name)

"""
for galsize in [20,100,1000]:
    for gal_name in ["m10q_res30", "m10q_res250", "m10v_res30", "m10v_res250"]:
        for gal_count in [str(realization + 1).zfill(2) for realization in range(10)]:
            if gal_name == "m09_res30":
                file_dir_list.append("jeans_results/Jeans_results_" + gal_name + "_size" + str(galsize) + "_" + gal_count + "/jeans_result.json")
            else:
                file_dir_list.append("jeans_results/" + gal_name + "_size" + str(galsize) + "_" + gal_count + "/jeans_result.json")
            final_photo_name_list.append("jeans_corner_plots/" + gal_name + "_size" + str(galsize) + "_" + gal_count + ".png")
            title_name = "Figure 2: Corner plot of " + gal_name + " galaxy instance " + gal_count + " at sample size " + str(galsize)
            final_title_list.append(title_name)

for  dir_name, title, photo_name in zip(file_dir_list, final_title_list, final_photo_name_list):
    make_corner_plot(dir_name, title, photo_name)
"""

"""
    try:
        make_corner_plot(dir_name, title, photo_name)
    except:
        print("Had a slight mishap, with galaxy " + dir_name)
"""