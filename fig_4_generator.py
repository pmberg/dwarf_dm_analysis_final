import gizmo_analysis as gizmo
import numpy as np
import matplotlib.pyplot as plt
import bilby


gal_names = ("m09_res30", "m10q_res30", "m10q_res250", "m10v_res30", "m10v_res250")
root_name = "/work2/08710/pmberg/stampede2/jeans_results/"
sample_sizes = (20,100)

fig, axs = plt.subplots(5,2, figsize=(8, 16))
#here, the second index indicates whether it uses sample size 20 or 100. The first index indicates the galaxy used here.

#this code is intended to theoretically plot multiple galaxies

#iterate through enumerated gal_names and sample_sizes

for gal_name_inx, gal in enumerate(gal_names):
    for sample_inx, sample_size in enumerate(sample_sizes):
        min_gamma_list = []
        max_gamma_list = []
        for gal_inx in [str(x).zfill(2) for x in range(1,11)]:
            gal_dir = root_name + gal + "_size" + str(sample_size) + "_" + gal_inx + "/jeans_result.json"
            #then read in this file using the utility for reading in these files
            bil_result = bilby.core.result.read_in_result(filename = gal_dir)
            samples = bil_result.samples
            samples_gamma = samples[:,1]
            min_gamma_list.append(min(samples_gamma))
            max_gamma_list.append(max(samples_gamma))
        min_gamma = min(min_gamma_list)
        max_gamma = max(max_gamma_list)
        hist_arr = np.zeros((40,10))
        bins = np.linspace(min_gamma,max_gamma,41)
        #go through all ten realizations
        for gal_inx in [str(x).zfill(2) for x in range(1,11)]:
            gal_dir = root_name + gal + "_size" + str(sample_size) + "_" + gal_inx + "/jeans_result.json"
            #then read in this file using the utility for reading in these files
            bil_result = bilby.core.result.read_in_result(filename = gal_dir)
            samples = bil_result.samples
            samples_gamma = samples[:,1]
            histogram_heights, bin_edges = np.histogram(samples_gamma, bins=bins, density=True)
            #save each set of histogram heights as a column in the array
            int_inx = int(gal_inx) -1
            hist_arr[:,int_inx] = histogram_heights

        #use broadcasted numpy operations to get bin_means and bin standard devs
        bin_means = np.mean(hist_arr, axis=1)
        bin_standard_deviations = np.std(hist_arr, axis=1)
        #plot and add fill commands
        fin_bins = bins[1:]
        #FIXME: Here, don't interface using plt: use the axs interface, and fig.suptitle, etc.
        #print(gal_name_inx)
        #print(sample_inx)
        axs[gal_name_inx, sample_inx].plot(fin_bins, bin_means, label = "Median value")  
        #TODO: Use an axes set_title, and a suptitle to indicate Figure 4 in the main plot
        axs[gal_name_inx, sample_inx].fill_between(fin_bins, bin_means - bin_standard_deviations, bin_means + bin_standard_deviations, alpha=0.7, label = "1σ CI")
        axs[gal_name_inx, sample_inx].set_xlabel("gamma")
        #fig.suptitle("Figure 4: Likelihood distribution of gamma for multiple galaxies")
        #TODO: Have some way to indicate a legend for the whole figure, since the colors are the same across the board
        axs[gal_name_inx, sample_inx].set_title(gal + ", sample size = " + str(sample_size))
        axs[gal_name_inx, sample_inx].set_xlim((-1,5))
        axs[gal_name_inx, sample_inx].set_ylim((0,1.5))
        axs[gal_name_inx, sample_inx].legend()
        axs[gal_name_inx, sample_inx].set_ylabel("Relative likelihoood (arbitrary)")
        fig.tight_layout()
fig.savefig("fig_4_07.pdf", dpi = 300)