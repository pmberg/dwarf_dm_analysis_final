import matplotlib.pyplot as plt

"""
This library is intended to read an idiosyncratically formatted type of file that I was generating as part of early-stage work in the paper.
It will likely be unnecessary on other configurations.

"""


with open("/work2/08710/pmberg/stampede2/fig_5_result_02.txt") as f:
    lines = f.readlines()
linecount =  len(lines)
processed_lines = []
line_inx = 0
while line_inx < linecount:
    line = lines[line_inx]
    if "[" in line:
        list_str = line.strip("\n")
        while "]" not in line:
            line_inx += 1
            line = lines[line_inx]
            list_str += line.strip("\n")
        processed_lines.append(list_str)
    else:
        processed_lines.append(line.strip("\n"))
    line_inx += 1

#processed_lines is intended to remove newlines, and merge multi-line lists into single lines.

#Final desired data structure: a dictionary gal_dict, mapping galaxy names to dictionaries mapping sample size, estimate radii, 16th percentile, 50th percentile, 84th percentile, density radii, and densities to associated lists

gal_dict =  {}
line_inx = 0
linecount =  len(processed_lines)
while line_inx < linecount:
    line = processed_lines[line_inx]
    if "Galaxy:" in line:
        gal_name = line.replace("Galaxy: ", "")
        sample_size = int(processed_lines[line_inx + 1].replace("Sample size: ", ""))
        estimate_radii = processed_lines[line_inx + 2].replace("Estimate radii: ", "").split()

        percent_16 = processed_lines[line_inx + 3].replace("16th percentile results: ", "").split()
        percent_50 = processed_lines[line_inx + 4].replace("50th percentile results: ", "").split()
        percent_84 = processed_lines[line_inx + 5].replace("84th percentile results: ", "").split()
        density_radii = processed_lines[line_inx + 6].replace("True density radii: ", "").split()
        densities = processed_lines[line_inx + 7].replace("True densities: ", "").split()
        #then go through, see if strings are brackets and delete them,
        for ilist in (estimate_radii, percent_16, percent_50, percent_84, density_radii, densities):
            for inx, item in enumerate(ilist):
                if item ==  "[" or item == "]":
                    ilist.remove(item)
            for inx, item in enumerate(ilist):
                ilist[inx] = float(item.strip("[],"))
        #at this point, we have valid lists
        gal_dict[gal_name] = {"sample_size": sample_size, 
            "estimate_radii": estimate_radii, 
            "percent_16": percent_16,
            "percent_50": percent_50,
            "percent_84": percent_84,
            "density_radii": density_radii,
            "densities": densities}
    line_inx += 1
#print(gal_dict)




fig, axs = plt.subplots(1,5, figsize = (15, 4))
gal_name_list = ("m09_res30", "m10q_res30", "m10q_res250", "m10v_res30", "m10v_res250")
for gal_name_inx, gal in enumerate(gal_name_list):


    axs[gal_name_inx].plot(gal_dict[gal]["estimate_radii"], gal_dict[gal]["percent_50"], label = "Median estimate")  
    axs[gal_name_inx].fill_between(gal_dict[gal]["estimate_radii"], gal_dict[gal]["percent_16"], gal_dict[gal]["percent_84"], alpha=0.7, label = "1σ CI")
    axs[gal_name_inx].set_xlabel("r(kpc)")
    axs[gal_name_inx].set_ylabel("$ρ(r)(M_☉/kpc^3)$")
    axs[gal_name_inx].set_xscale("log")
    axs[gal_name_inx].set_yscale("log")
    axs[gal_name_inx].set_title(gal)
    axs[gal_name_inx].plot(gal_dict[gal]["density_radii"], gal_dict[gal]["densities"], label = "True density")
    axs[gal_name_inx].legend()
    #title_str = "Figure 5: Estimated versus actual density profile for " + gal + " galaxy"
#fig.suptitle(title_str)
fig.tight_layout()
fig.savefig("fig_5_v3.pdf", dpi = 300)


