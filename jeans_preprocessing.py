import numpy as np
import gizmo_read
import random
import gizmo_analysis as gizmo

def generate_jeans_samples(data_ending_list, sample_size=100, data_species="star"):
    """
    Parameters:
    data_ending_list: A list of strings containing directory names that, when appended to data_root
    (which may be changed by an end user depending on their directory structure), lead to galaxy simulatioons
    sample_size: the number of samples to be drawn from each galaxy
    data_species: the population within the simulation (either "star", "gas", or "dark") from which these samples will be drawn


    Returns: Nothing.
    Creates files containing samples of galaxies, formatted with the first line saying
    # x[kpc] y[kpc] z[kpc] vx[km/s] vy[km/s] vz[km/s]
    and subsequent lines containing those parameters, as floats, separated by spaces, with each line corresponding
    to a point sampled.
    """
    data_root = "/scratch/projects/xsede/GalaxiesOnFIRE/metal_diffusion/"
    for data_ending in data_ending_list:
        data_directory = data_root + data_ending
        snapshot = gizmo.io.Read.read_snapshots([data_species], 'redshift', 0, data_directory)

        #snapshot = gizmo_read.read.Read.read_snapshot(species=data_species, directory=data_directory)
        particle_positions_cartesian = snapshot[data_species].prop("host.distance")
        particle_radii = snapshot[data_species].prop("host.distance.total")
        particle_velocities_cartesian = snapshot[data_species].prop("host.velocity")
        local_indices = particle_radii < 20
        size_of_snapshot = len(particle_positions_cartesian[local_indices])
        print(size_of_snapshot)
        for num_str in ["01","02","03","04", "05", "06", "07", "08", "09", "10"]:
            sample_indices = random.sample(range(size_of_snapshot), sample_size)
            #these indices correspond to positions within local_indices
            #now draw the particle positions and velocities from the sample indices
            local_positions = particle_positions_cartesian[local_indices]
            local_velocities = particle_velocities_cartesian[local_indices]
            sample_positions = local_positions[sample_indices]
            sample_velocities = local_velocities[sample_indices]
            #now put them in a file
            file_name = "jeans_samples/" + data_ending + "_size_1000_sample_" + num_str + ".txt"
            output_file = open(file_name, 'w')
            output_file.write("# x[kpc] y[kpc] z[kpc] vx[km/s] vy[km/s] vz[km/s]\n")
            for position in range(sample_size):
                #this special slicing removes the brackets from the array to give pure values
                pos_str = str(sample_positions[position])[1:-1]
                vel_str = str(sample_velocities[position])[1:-1]
                line_str = pos_str + ' ' + vel_str +  '\n'
                output_file.write(line_str)
            output_file.close()

data_ending_list = ["m10q_res30", "m10q_res250","m10v_res250","m10v_res30"]
sample_size = 1000

generate_jeans_samples(data_ending_list, sample_size)