import numpy as np
import glob
import re
import pandas as pd
import sys

#This file is for reading the files, finding the loss function and write to file
k = float(sys.argv[1])
R0 = float(sys.argv[2])


def read_coordinates():
    # adding delatom files
    alkaneC_files = './cnt.bond.0802/dump.alkaneC1epo.*'
    bondedO_files = './cnt.bond.0802/dump.bondedO1epo.*'
    bondedCNT_files = './cnt.bond.0802/dump.bondedCNT1epo.*'

    alkane_files = sorted(glob.glob(alkaneC_files), key=key_func)[0]
    fun_file = sorted(glob.glob(bondedO_files), key=key_func)[0]
    bondedcnt_file = sorted(glob.glob(bondedCNT_files), key=key_func)[0]

    d_cnt0, d_R0 = readfiles(alkane_files=alkane_files, fun_file=fun_file, bondedcnt_file=bondedcnt_file)

    alkane_files = sorted(glob.glob(alkaneC_files), key=key_func)[1]
    fun_file = sorted(glob.glob(bondedO_files), key=key_func)[1]
    bondedcnt_file = sorted(glob.glob(bondedCNT_files), key=key_func)[1]

    d_cnt1, d_R1 = readfiles(alkane_files=alkane_files, fun_file=fun_file, bondedcnt_file=bondedcnt_file)



    return d_cnt0, d_R0, d_cnt1, d_R1




def readfiles(alkane_files, fun_file, bondedcnt_file):

    with open(fun_file) as f:
        text = f.readlines()

        for line in text:
            if line.startswith('ITEM: ATOMS'):
                header_choose = line.strip()
                header_choose = header_choose.split()
                header_choose = header_choose[2:]  # getting rid off the first two items, as it is ITEM: ATOMS


    df_R = pd.read_table(alkane_files, delim_whitespace=True, header=None, skiprows=9)
    df_O = pd.read_table(fun_file, delim_whitespace=True, header=None, skiprows=9)
    df_cnt = pd.read_table(bondedcnt_file, delim_whitespace=True, header=None, skiprows=9)



    df_O.columns = header_choose
    df_R.columns = header_choose
    df_cnt.columns = header_choose

    #computing distances


    p_O = df_O.loc[:, ['x', 'y', 'z']].as_matrix()
    p_R = df_R.loc[:, ['x', 'y', 'z']].as_matrix()
    p_CNT = df_cnt.loc[:, ['x', 'y', 'z']].as_matrix()

    d_cnt_O = compute_distance(p_O, p_CNT).flatten()[0]
    d_R_O = compute_distance(p_O, p_R).flatten()[-1]


    return d_cnt_O, d_R_O




#keyfunction to sort filesa
def key_func(x):
    nondigits= re.compile("\D")

    return int(nondigits.sub("", x))



def compute_distance(cnt_array, cnt_other_array):

    dist_list = []
    points = cnt_array


    for j in range(0, len(cnt_other_array)):

        single_point = cnt_other_array[j, :]

        dist = np.sum(((points - single_point)**2), axis=1)
        dist = np.sqrt(dist)
        dist_list.append(dist)


    return np.asarray(dist_list)



def save_data(file_name, k, R0, d_cnt0, d_R0, d_cnt1, d_R1):

    Z = np.array([k, R0, d_cnt0, d_R0, d_cnt1, d_R1])
    Z = Z[None, :]

    with open(file_name, 'ab') as f:
        np.savetxt(f, Z)



    return None


d1, d2, d3, d4 = read_coordinates()

save_data('eqb_distance.txt', k=k, R0=R0, d_cnt0=d1, d_R0=d2, d_cnt1=d3, d_R1=d4)
