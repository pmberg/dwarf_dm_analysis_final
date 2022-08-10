from re import sub
import morphokinematicsdiagnostics
import gizmo_analysis as gizmo
import numpy as np
import matplotlib.pyplot as plt
import random

#points to a section on my system containing galaxy simulations. Change for your own system.
sim_dir = "/scratch/projects/xsede/GalaxiesOnFIRE/metal_diffusion/"
#Links between data and styles
sims_dict = {"m10v_res250": "c"}
#"m09_res30": "r", "m10q_res30": "g", "m10q_res250": "b", "m10v_res30": "c", "m10v_res250": "m"
species_dict = {"star": "-"}
#"star": "-", 
#some preliminary  plot formatting
plt.clf()
plt.title("Figure 3: Dark and stellar matter c/a ratios for dwarf galaxy simulations")
plt.xlabel("Radius [kpc]")
#x is in kpc
plt.ylabel("c/a ratio")
#y is in km/s
plt.xlim(1,20)
plt.ylim(0,1)
plt.xscale("log")
rs = np.exp(np.arange(np.log(0.5), np.log(20), 0.15))

#loop through all galaxies and types of data
#this is the extent to which the data are subsampled. 1 = no subsampling, 100 = only 1/100 of data points are sampled, etc.

subsample_param = 1
for sims_name in sims_dict:
    part = gizmo.io.Read.read_snapshots(
            ["star", "dark", "gas"], "redshift", 0, sim_dir + sims_name, assign_hosts_rotation=True
        )
    for species in species_dict:
        df = {"ellipticity": [], "triaxiality": [], "Transform": [], "abc":[]}
        if species == "star":
            subsample_param = 1
            species_positions = part[species].prop("host.distance")
            species_masses = part[species]["mass"]
            vel_species = part[species].prop("host.velocity")
        else:
            if len(part[species].prop("host.distance")) > 100000:
                subsample_param = 1
            else:
                subsample_param = 1
            raw_positions = part[species].prop("host.distance")
            raw_masses = part[species]["mass"]
            raw_vel = part[species].prop("host.velocity")
            raw_distances = part[species].prop("host.distance.total")
            part_count = len(raw_positions)
            sample_indices = random.sample(range(part_count), part_count//subsample_param)
            species_positions = raw_positions[sample_indices]
            species_masses = raw_masses[sample_indices]
            vel_species = raw_vel[sample_indices]
        print("Positions: " + str(species_positions))
        print("Velocities: " + str(vel_species))
        print("Masses: " + str(species_masses))
        try:
            for r_i in rs:
                print("Calculating triaxiality at: ", r_i)
                #call to morphokinematicsdiagnostics code by Adrien Thob
                r_ellip, r_triax, r_transform, r_abc = morphokinematicsdiagnostics.morphological_diagnostics(
                    species_positions, species_masses, vel_species, r_i)
                df["ellipticity"].append(r_ellip)
                df["triaxiality"].append(r_triax)
                df["Transform"].append(r_transform)
                df["abc"].append(r_abc)
        except ValueError:
            df["ellipticity"] = []
            df["triaxiality"] = []
            df["Transform"] = []
            df["abc"] = []
            rs = np.exp(np.arange(np.log(1), np.log(20), 0.15))
            for r_i in rs:
                print("Calculating triaxiality at: ", r_i)
                #call to morphokinematicsdiagnostics code by Adrien Thob
                r_ellip, r_triax, r_transform, r_abc = morphokinematicsdiagnostics.morphological_diagnostics(
                    species_positions, species_masses, vel_species, r_i)
                df["ellipticity"].append(r_ellip)
                df["triaxiality"].append(r_triax)
                df["Transform"].append(r_transform)
                df["abc"].append(r_abc)
        #this line turns the 1-c/a value of "ellipticity" into c/a
        s_list = [1-x for x in df["ellipticity"]]
        print("Species: " + species)
        print("Galaxy: " + sims_name)
        print("Subsample factor: " + str(subsample_param))
        print("Radii")
        print(rs)
        print("Axis ratios")
        print(s_list)
        line_style = sims_dict[sims_name] + species_dict[species]
        plt.plot(rs, s_list, line_style, label = sims_name + " " + species)
plt.legend(ncol = 2, prop={'size': 6})
plt.savefig("/work2/08710/pmberg/stampede2/figure_3_dm_paper.png", dpi=300)


