import matplotlib.pylab as plt
import numpy as np
import sys

def formater(file_name, line):
    if file_name.endswith(".RVIC"):
        date = line.split(":")[1].split(" ")[1]
        flow = float(line.split(":")[4].split()[0])
        if line.split(":")[-1].split()[0] == "streamflow":
            is_flow = True
        else:
            is_flow = False
    else:
        date = line.split(",")[0]
        flow = float(line.split(",")[1])
        is_flow = True

    return date, flow, is_flow

def build_dict(file_name):
    with open(file_name, "r") as f:
        daily_list_dict = {}
        for line in f:
            try:
                date, flow, is_flow = formater(file_name, line)
            except:
                continue

            if is_flow:
                try:
                    daily_list_dict[int(date.split("-")[1] + date.split("-")[2])].append(flow)
                except:
                    daily_list_dict[int(date.split("-")[1] + date.split("-")[2])] = [flow]
        
        daily_mean_dict = {}
        daily_max_dict = {}
        daily_min_dict = {}
        i = 0 
        for k in daily_list_dict.keys():
            daily_mean_dict[i] = sum(daily_list_dict[k]) / len(daily_list_dict[k])
            daily_max_dict[i] = max(daily_list_dict[k])
            daily_min_dict[i] = min(daily_list_dict[k])
            i += 1

    return daily_mean_dict

def plot(title, dict1, dict2):
    lists = sorted(dict1.items()) 
    x, y = zip(*lists)
    plt.plot(x, y, label="After modification")

    lists = sorted(dict2.items()) 
    x, y = zip(*lists)
    plt.plot(x, y, label="Before modification")

    plt.title(f"RVIC verification ({title})")
    plt.legend(loc="upper right")
    
    plt.show()


comparand = sys.argv[1]
comparator = sys.argv[2]
RVIC_daily_mean_dict = build_dict(comparand)
PNWNAMET_daily_mean_dict = build_dict(comparator)

plot(comparand.split(".")[0], RVIC_daily_mean_dict, PNWNAMET_daily_mean_dict)
