from rvic.parameters import parameters
from rvic.convolution import convolution
from pathlib import Path
import sys
import logging
import time
import datetime

pour_txt = "lons,lats\n"
coordinate_dict = {
    1: "-120.8,56.2",
    10: "-117.6,55.6",
    50: "-121.4,56.1",
    140: "-120.3,56.0",
    282: "-121.7,56.4",
    360: "-121.6,56.3",
    486: "-120.9,56.1",
    631: "-120.5,56.2",
    1351: "-117.7,55.5",    
    1948: "-117.4,56.1",
    2867: "-122.0,56.0",        
    2868: "-121.9,56.0",    
    2900: "-121.8,56.1",  
    2925: "-121.7,56.1",
    3300: "-121.3,56.2",
    3921: "-120.5,56.1",
    3342: "-121.1,56.2",
    4558: "-120.3,56.1",
    4708: "-120.1,56.1",
    5104: "-118.9,56.1",
    5248: "-118.6,55.9",
    5256: "-118.5,55.9",
    5264: "-118.3,55.9",
    5266: "-118.2,55.9",
    5363: "-118.0,55.9",
    5387: "-117.8,56.0",
    5404: "-117.5,56.1",
    71: "-124.90625,57.21875",		# ARNT7,07EA007
    67: "-121.21875,56.65625", 		# BRBAC,07FC003
    623: "-120.71875,56.28125", 	# BRNFS,07FC001
    669: "-125.28125,57.15625", 	# FRAAR,07EA005
    84: "-122.34375,56.46875", 		# GRACC,07FA005
    83: "-117.03125,56.03125", 		# HERNN,07HA003
    155: "-122.34375,56.53125",		# HRAGR,07FA003
    361: "-121.59375,56.21875", 	# HRNFC,07FA006
    163: "-125.21875,56.71875",		# IRASR,07EA004
    128: "-120.53125,55.96875", 	# KIRNF,07FD001
    104: "-125.65625,57.46875", 	# KWRNW,07EA002
    433: "-117.15625,55.46875", 	# LSRNG,07GH002
    118: "-124.65625,56.21875", 	# MRAGC,07EC003
    90: "-121.03125,55.03125", 		# MRAWR,07FB006
    51: "-121.34375,56.09375", 		# MRNFS,07FB008
    204: "-121.21875,55.53125", 	# MRNTM,07FB002
    179: "-124.28125,55.21875", 	# NRNFS,07ED001
    271: "-123.59375,55.46875", 	# NRNTM,07ED003
    85: "-123.96875,56.53125", 		# ORAAC,07EB002
    222: "-124.59375,55.90625", 	# ORAOR,07EC002
    69: "-124.78125,56.09375", 		# ORNEL,07EC004
    119: "-120.03125,55.84375", 	# PCRBH,07FD007
    3910: "-120.65625,56.15625", 	# PERNT,07FD002
    2836: "-122.21875,56.03125", 	# PRABD,BCGMS
    444: "-121.21875,55.71875", 	# PRAEP,07FB001
    174: "-122.84375,55.03125", 	# PRAMR,07EE007
    149: "-123.03125,54.96875", 	# PRAOO,07EE010
    7484: "-117.28125,56.21875", 	# PRAPR,07HA001
    47: "-119.71875,55.09375", 		# RRNRG,07GD004
    1907: "-117.59375,55.78125", 	# SMRAW,07GJ001
    103: "-121.59375,55.53125", 	# SRNTM,07FB003
    417: "-118.78125,55.09375", 	# WRNGP,07GE001
    41: "-117.21875,54.71875", 		# WRNTM,07GG001

}   
case_id = sys.argv[-1]
today = datetime.datetime.now()
logging.critical("\n")
logging.critical(case_id + "\n")
with open("peace_parameters.config.cfg", "rt") as param_config:
    data = ""
    for line in param_config:
        if line.startswith("CASEID"):
            data += f"CASEID : {case_id}\n"
        else:
            data += line


with open("peace_parameters.config.cfg", "wt") as param_config:
    param_config.write(data)

with open("peace_convolve.config.cfg", "rt") as convolve_config:
    data = ""
    for line in convolve_config:
        if line.startswith("CASEID"):
            data += f"CASEID : {case_id}\n"

        elif "rvic.prm" in line:
            data += f"FILE_NAME: ./routing/{case_id}/params/{case_id}.rvic.prm.PEACE.{str(today.year)}0{str(today.month)+str(today.day)}.nc\n"

        elif line.startswith("DATL_FILE"):
            data += f"DATL_FILE: {case_id}/flux/peace_vicset2_1945to2100.nc\n"
       
        else:
            data += line
    
with open("peace_convolve.config.cfg", "wt") as convolve_config:
    convolve_config.write(data)

for k in sorted(coordinate_dict.keys()):        
     
    with open("pour.txt", "wt") as pf:
        pf.write(pour_txt+coordinate_dict[k])
    
    start_time = time.time() 
    parameters("peace_parameters.config.cfg")
    convolution("peace_convolve.config.cfg")
    
    elapsed_time = round(time.time() - start_time, 5)
    output_size = Path(f"/storage/home/sangwonl/rvic_run/routing/{case_id}/hist/{case_id}.rvic.h0a.2100-01-01.nc").stat().st_size
    
    logging.critical(f"total run time:{elapsed_time} sec")
    logging.critical(f"output file size:{output_size} byte")
    logging.critical("----------------------------------------------------------------------------------")

