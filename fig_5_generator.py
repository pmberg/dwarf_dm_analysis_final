import sys
sys.path

import gizmo_analysis as gizmo
import numpy as np
import matplotlib.pyplot as plt
import bilby
import utilities as ut

#make a series of bins
bins = np.logspace(-2,2,40)
sample_size = 100
#these values are all dependent on your filestructure
gal_name_list = ("m09_res30", "m10q_res30", "m10q_res250", "m10v_res30", "m10v_res250")
root_name = "/work2/08710/pmberg/stampede2/jeans_results/"
sim_root = "/scratch/projects/xsede/GalaxiesOnFIRE/metal_diffusion/"

fig, axs = plt.subplots(1,5, figsize = (40, 10))


def get_shell_density(rarr, marr, r_start, r_end):
    """
    Parameters:
    rarr: the array of particle distances from the center
    marr: the array of particle masses, corresponding to the same indices as rarr
    r_start: the radius where the shell starts
    r_end: the radius where the shell ends
    
    Returns:
    shell_density: the density (mass/volume) of particles within the shell
    """
    valid_particle_indices = np.intersect1d(np.nonzero(rarr < r_end), np.nonzero(rarr >= r_start))
    valid_masses = np.take(marr, valid_particle_indices)
    total_mass = np.sum(valid_masses)
    total_volume = (4/3) * np.pi * (r_end**3 - r_start**3)
    shell_density = total_mass/total_volume
    return shell_density


def take_density_table(directory, data_species, min_rad_power, max_rad_power, rad_count):
    """
    Parameters:
    directory: a string representing the path to the particle (e.g. "m12f/")
    data_species: a string representing the type of particle to be examined (e.g. "dark", "star", "gas")
    min_rad_power: the logarithm base ten of the lowest radius for which a density must be calculated
    max_rad_power: the logarithm base ten of the highest radius for which a density must be calculated
    rad_count: the number of radial bins used in the table

    Returns:
    trial_rad_arr: The list of radii used to compute the densities.
    density_arr: The list of densities derived from the radii in question.
    """
    #early data processing stage
    raw_data = gizmo.io.Read.read_snapshots([data_species], 'redshift', 0, directory)
    radius_arr = raw_data[data_species].prop('host.distance.total')
    mass_arr = raw_data[data_species]["mass"]
    trial_rad_arr = np.logspace(min_rad_power, max_rad_power, rad_count)
    density_arr = np.zeros(rad_count)
    for rinx, rad in enumerate(trial_rad_arr):
        if rad > trial_rad_arr[rinx - 1]:
            density_arr[rinx] = get_shell_density(radius_arr, mass_arr, trial_rad_arr[rinx - 1], rad)
        else:
            density_arr[rinx] = get_shell_density(radius_arr, mass_arr, 0, rad)
    return trial_rad_arr, density_arr

#then for each radius:
#calculate rho(r) at that radius, based on 50th percentile MCMC for each of ten realizations
#calculate the 16th and 84th percentiles of rho based on that distribution
#repeat for all radius bins

def nfw_density(r, gamma, rho_0, r_s):
    """
    Parameters:
    r: The radius at which the density is calculated.
    gamma: The characteristic exponent of the NFW equation.
    rho_0: The density scaling factor for the NFW equation.
    r_s: The characteristic radius of the NFW equation.
    """
    return rho_0 * (r/r_s)**(-gamma) * (1+r/r_s)**(gamma - 3)

for gal_name_inx, gal in enumerate(gal_name_list):
    p16_radius = []
    p50_radius = []
    p84_radius = []
    median_r_dm = []
    median_gamma = []
    median_rho_0 = []
    median_L = []
    median_r_star = []
    #go through all ten realizations
    for gal_inx in [str(x).zfill(2) for x in range(1,11)]:
        #this argument is based on the naming scheme used on a researcher's system; change for your own machine
        gal_dir = root_name + gal + "_size" + str(sample_size) + "_" + gal_inx + "/jeans_result.json"
        #read in this file using the utility for reading in these files
        bil_result = bilby.core.result.read_in_result(filename = gal_dir)
        samples = bil_result.samples
        median_r_dm.append(np.percentile(samples[:,0], 50))
        median_gamma.append(np.percentile(samples[:,1], 50))
        median_rho_0.append(np.percentile(samples[:,2], 50))
        median_L.append(np.percentile(samples[:,3], 50))
        median_r_star.append(np.percentile(samples[:,4], 50))
    #now we have a whole bunch of parameters here.     

    for radius in bins:
        #calculate the values at the radii
        all_radii_list = []
        for equation_inx in range(10):
            all_radii_list.append(nfw_density(radius, median_gamma[equation_inx], median_rho_0[equation_inx], median_r_dm[equation_inx]))
        p16_radius.append(np.percentile(all_radii_list, 16))
        p50_radius.append(np.percentile(all_radii_list, 50))
        p84_radius.append(np.percentile(all_radii_list, 84))

    axs[gal_name_inx].plot(bins, p50_radius, label = "Median estimate")  
    axs[gal_name_inx].fill_between(bins, p16_radius, p84_radius, alpha=0.7, label = "1σ CI")
    axs[gal_name_inx].set_xlabel("r(kpc)")
    axs[gal_name_inx].set_ylabel("$ρ(r)(M_☉/kpc^3)")
    axs[gal_name_inx].set_xscale("log")
    axs[gal_name_inx].set_yscale("log")
    axs[gal_name_inx].set_title(gal)
    sim_dir = sim_root + gal
    dir_radius_arr, dir_density_arr = take_density_table(sim_dir, "dark", -2, 2, 100)
    print("Galaxy: " + gal)
    print("Sample size: " + str(sample_size))
    print("Estimate radii: " + str(bins))
    print("16th percentile results: " + str(p16_radius))
    print("50th percentile results: " + str(p50_radius))
    print("84th percentile results: " + str(p84_radius))
    print("True density radii: " + str(dir_radius_arr))
    print("True densities: " + str(dir_density_arr))


    axs[gal_name_inx].plot(dir_radius_arr, dir_density_arr, label = "True density")
    axs[gal_name_inx].legend()
    title_str = "Figure 5: Estimated versus actual density profile for " + gal + " galaxy"
fig.suptitle(title_str)
fig.savefig("fig_5_v2.png", dpi = 300)


#save the figure
