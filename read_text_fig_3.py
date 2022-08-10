import matplotlib.pyplot as plt

"""
This library is intended to read an idiosyncratically formatted type of file that I was generating as part of early-stage work in the paper.
It will likely be unnecessary on other configurations.

"""


with open("/work2/08710/pmberg/stampede2/fig_3_result_02.txt") as f:
    lines = f.readlines()
linecount =  len(lines)
processed_lines = []
line_inx = 0
while line_inx < linecount:
    line = lines[line_inx]
    if "[" in line:
        list_str = line
        while "]" not in line:
            line_inx += 1
            line = lines[line_inx]
            list_str += line
        processed_lines.append(list_str.strip("\n"))
    else:
        processed_lines.append(line.strip("\n"))
    line_inx += 1
#processed_lines is intended to remove newlines, and merge multi-line lists into single lines.


#Final desired data structure: a dictionary gal_dict, mapping galaxy names to dictionaries mapping species names to tuples of radii and axis ratios.

gal_dict =  {}
line_inx = 0
linecount =  len(processed_lines)

while line_inx < linecount:
    line = processed_lines[line_inx]
    if "Galaxy:" in line:
        gal_name = line.replace("Galaxy: ", "")
        spec_name = processed_lines[line_inx - 1].replace("Species: ", "")
        radius_list = processed_lines[line_inx + 3].split()
        #then go through, see if strings are brackets and delete them,
        for inx, item in enumerate(radius_list):
            if item ==  "[" or item == "]":
                radius_list.remove(item)
        for inx, item in enumerate(radius_list):
            radius_list[inx] = float(item.strip("[],"))
        ratio_list = processed_lines[line_inx + 5].split()
        for inx, item in enumerate(ratio_list):
            if item ==  "[" or item == "]":
                ratio_list.remove(item)
        for inx, item in enumerate(ratio_list):
            ratio_list[inx] = float(item.strip("[],"))
        #at this point, we have valid radius_list, ratio_list, gal_name, and spec_name.
        if gal_name in gal_dict:
            gal_dict[gal_name][spec_name] = (radius_list, ratio_list)
        else:
            gal_dict[gal_name] = {spec_name: (radius_list, ratio_list)}
    line_inx += 1


sims_dict = {"m10v_res250": "r", "m09_res30": "r", "m10q_res30": "g", "m10q_res250": "b", "m10v_res30": "c", "m10v_res250": "m"}
species_dict = {"dark": "--", "star": "-"}
# {"gas": ":"
#some preliminary  plot formatting
plt.clf()
#plt.title("Figure 3: Dark matter c/a ratios for dwarf galaxy simulations")
plt.xlabel("Radius [kpc]")
#x is in kpc
plt.ylabel("c/a ratio")
#y is in km/s
plt.xlim(0.5,20)
plt.ylim(0,1)
plt.xscale("log")

#loop through all galaxies and types of data
#this is the extent to which the data are subsampled. 1 = no subsampling, 100 = only 1/100 of data points are sampled, etc.

subsample_param = 1
for spec_name in species_dict:
    for gal_name in sims_dict:
        line_style = sims_dict[gal_name] + species_dict[spec_name]
        plt.plot(gal_dict[gal_name][spec_name][0], gal_dict[gal_name][spec_name][1], line_style, label = gal_name + " " + spec_name)
plt.legend(ncol = 2, prop={'size': 10})
plt.savefig("/work2/08710/pmberg/stampede2/fig_03_test_02.pdf")