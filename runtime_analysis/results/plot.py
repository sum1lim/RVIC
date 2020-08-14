import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

scenario = None
plot_total_runtime = {}
plot_parameters_init = {}
plot_parameters_run = {}
plot_catchment_loop={}
plot_uh_loop={}
plot_uh_river_loop={}
plot_grid_uh_loop={}
plot_parameters_loop = {}
plot_parameters_final = {}
plot_convolution_init = {}
plot_convolution_run = {}
plot_convolution_loop = {}
plot_convolution_final = {}
plot_output_size = {}

def scatter_plot(plot_dict, title, yaxis):
    lists = sorted(plot_dict.items()) 
    x, y = zip(*lists)

    r_value = pearsonr(x, y)[0]
    p_value = pearsonr(x, y)[1]
    print("{}: {:.5f}, {:.5f}".format(title, r_value, p_value))

    plt.scatter(x, y)

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")

    plt.title(title)
    plt.xlabel("Number of upstream grid cells")
    plt.ylabel(yaxis)
    plt.show()

def init_dicts():
    return {}, {}, {}, {}, {}, {}, {}, {}

def plot_all(scenario):
    scatter_plot(plot_total_runtime, f"Total runtime: {scenario}", "Runtime (sec)")

    # scatter_plot(plot_parameters_init, f"parameters_init runtime: {scenario}", "Runtime (sec)")
    
    scatter_plot(plot_parameters_run, f"parameters_run runtime: {scenario}", "Runtime (sec)")
    scatter_plot(plot_catchment_loop, f"catchment loop runtime: {scenario}", "Runtime (sec)")
    scatter_plot(plot_uh_loop, f"uh loop runtime: {scenario}", "Runtime (sec)")
    scatter_plot(plot_uh_river_loop, f"uh river loop runtime: {scenario}", "Runtime (sec)")
    scatter_plot(plot_grid_uh_loop, f"grid_uh loop runtime: {scenario}", "Runtime (sec)")
    scatter_plot(plot_parameters_loop, f"Parameters main loops runtime: {scenario}", "Runtime (sec)")
    
    # scatter_plot(plot_parameters_final, f"parameters_final runtime: {scenario}", "Runtime (sec)")
    
    # scatter_plot(plot_convolution_init, f"convolution_init runtime: {scenario}", "Runtime (sec)")
    
    scatter_plot(plot_convolution_run, f"convolution_run runtime: {scenario}", "Runtime (sec)")
    scatter_plot(plot_convolution_loop, f"Convolution main loop runtime: {scenario}", "Runtime (sec)")
    
    # scatter_plot(plot_convolution_final, f"convolution_final runtime: {scenario}", "Runtime (sec)")
    
    # scatter_plot(plot_output_size, f"Output filesize: {scenario}", "Output size (byte)")

with open("rvic_run.e89690", "rt") as f:

    for line in f:
        if line.startswith("CRITICAL:root:"):
            root =  line.split("CRITICAL:root:")[1]
            if "rcp" in root:
                if scenario:
                    plot_all(scenario)
                    (
                        plot_total_runtime, 
                        plot_parameters_init, 
                        plot_parameters_run,
                        plot_parameters_final,
                        plot_convolution_init,
                        plot_convolution_run,
                        plot_convolution_final,
                        plot_output_size,
                    ) = init_dicts()
                scenario = root.split(":")[-1].split("\n")[0]

            elif "total run time" in root:
                total_run_time = float(root.split(":")[1].split()[0])
            elif "output file size"  in root:
                output_size = int(root.split(":")[1].split()[0])
                
                
        elif line.startswith("CRITICAL:parameters>>"):
            if "init" in line:
                param_init_runtime = float(line.split(": ")[-1].split()[0])
            if "run" in line:
                param_run_runtime = float(line.split(": ")[-1].split()[0])
            if "final" in line:
                param_final_runtime = float(line.split(": ")[-1].split()[0])
                
        elif line.startswith("CRITICAL:gen_uh_run>>"):
            if "catchment runtime: " in line:
                catchment_runtime = float(line.split(": ")[-1])
            if "uh runtime: " in line:
                uh_runtime = float(line.split(": ")[-1])
            if "uh_river runtime: " in line:
                uh_river_runtime = float(line.split(": ")[-1])
            if "grid_uh runtime: " in line:
                grid_uh_runtime = float(line.split(": ")[-1])

        elif line.startswith("CRITICAL:convolution>>"):
            if "init" in line:
                convolve_init_runtime = float(line.split(": ")[-1].split()[0])
            if "run" in line:
                convolve_run_runtime = float(line.split(": ")[-1].split()[0])
            if "final" in line:
                convolve_final_runtime = float(line.split(": ")[-1].split()[0])

        if line.startswith("CRITICAL:convolution_run>>"):
            if "upstreams cells" in line:
                num_cells = int(line.split(": ")[1])
            if "outlet cells" in line:
                outlet_cells = int(line.split(": ")[1])
            if "subset length" in line:
                subset_length = int(line.split(": ")[1])
            if "timesteps" in line:
                timesteps = int(line.split(": ")[1])
            if "average convolve loop runtime" in line:
                convolve_loop_runtime = float(line.split(": ")[1])

        elif "-------------------------------------------------------" in line:
            parameters_loops_runtime = catchment_runtime + uh_runtime + uh_river_runtime + grid_uh_runtime
            plot_total_runtime[num_cells*subset_length] = total_run_time
            
            plot_output_size[num_cells*subset_length] = output_size
            
            plot_parameters_init[num_cells*subset_length] = param_init_runtime
            
            plot_parameters_run[num_cells*subset_length] = param_run_runtime
            plot_catchment_loop[num_cells*subset_length] = catchment_runtime
            plot_uh_loop[num_cells*subset_length] = uh_runtime
            plot_uh_river_loop[num_cells*subset_length] = uh_river_runtime
            plot_grid_uh_loop[num_cells*subset_length] = grid_uh_runtime
            plot_parameters_loop[num_cells*subset_length] = parameters_loops_runtime
            
            plot_parameters_final[num_cells*subset_length] = param_final_runtime
            
            plot_convolution_init[num_cells*subset_length] = convolve_init_runtime
            
            plot_convolution_run[num_cells*subset_length] = convolve_run_runtime
            plot_convolution_loop[num_cells*subset_length] = convolve_loop_runtime
            
            plot_convolution_final[num_cells*subset_length] = convolve_final_runtime

plot_all(scenario)


