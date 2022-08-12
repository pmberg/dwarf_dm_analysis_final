import numpy as np
import gizmo_read
import random
import gizmo_analysis as gizmo
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors

#these first two values depend on your directory configuration, and the desired results.
#this code will make three subplots, from left to right: xy, xz, yz.
#bounded at 100 kpc on all sides
data_species = "star"
#note that this depends on your system configuration
data_root = "/scratch/projects/xsede/GalaxiesOnFIRE/metal_diffusion/"

def make_gal_hexbin(gal_dir, species, bounds = 100): 
    """
    Parameters:
    gal_dir: the directory from  which the galactic snapshots will be red
    species: the species of data to be plotted, as a string ("star", "dark", or "gas")
    bounds: the coordinate out to which the graph will be extended in a square of 2 * bounds centered on the origin.

    Returns: None
    Plots a three-panel hexbin plot, showing a hexagonal histogram of density projected onto xy, xz, and yz planes.
    """
    plt.clf()
    #then make a figure with three plots
    fig, axs = plt.subplots(1, 3, figsize = (12,3))
    snapshot = gizmo.io.Read.read_snapshots([species], 'redshift', 0, gal_dir)
    particle_positions_cartesian = snapshot[species].prop("host.distance")
    ax0_coords_original = particle_positions_cartesian[:,0]
    ax1_coords_original = particle_positions_cartesian[:,1]
    ax2_coords_original = particle_positions_cartesian[:,2]
    gridsize = 100
    vmin = 1
    vmax = 1000
    norm = colors.LogNorm(vmin=vmin, vmax=vmax)
    #plot the three panes
    hb1 = axs[0].hexbin(ax0_coords_original, ax1_coords_original, extent = (-bounds,bounds,-bounds,bounds), gridsize=gridsize, mincnt=1, norm=norm)    
    axs[0].set_xlabel("x (kpc)")
    axs[0].set_ylabel("y (kpc)")
    hb2 = axs[1].hexbin(ax0_coords_original, ax2_coords_original, extent = (-bounds,bounds,-bounds,bounds), gridsize=gridsize, mincnt=1, norm=norm)
    axs[1].set_xlabel("x (kpc)")
    axs[1].set_ylabel("z (kpc)")
    hb3 = axs[2].hexbin(ax1_coords_original, ax2_coords_original, extent = (-bounds,bounds,-bounds,bounds), gridsize=gridsize, mincnt=1, norm=norm)
    axs[2].set_xlabel("y (kpc)")
    axs[2].set_ylabel("z (kpc)")
    #adjust the spacing
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=1.0, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

    
    #create a color bar
    plt.tight_layout()
    cbar = plt.colorbar(hb3, ax=axs.ravel().tolist(), aspect = 10)
    cbar.set_label(r'Count', fontsize = 18)
    plt.savefig("fig_01_test_02.png")





for galaxy_name in ["m10q_res30"]:
    
    
    data_directory = data_root + galaxy_name
    make_gal_hexbin(data_directory, data_species, 100)