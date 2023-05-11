import pandas as pd
import numpy as np
import argparse, sys, os, re, math

def writeCSV(sketches_sm, sketches_spsp, results_spsp, results_sourmash, results_simka, benchs, out):
    data = {}
    read_bench(benchs, data)
    read_index_size(sketches_sm, sketches_spsp, data)
    compare_results(results_spsp, results_sourmash, results_simka, data)
    with open(out, 'w') as out_file:
        out_file.write("Error_containment,Error_jaccard,time,ram,disk,tool_name,sub_rate\n")
        for key in data:
            for name in data[key]:
                    out_file.write(str(data[key][name]['diff_containment']))
                    out_file.write(",")
                    out_file.write(str(data[key][name]['diff_jaccard']))
                    out_file.write(",")
                    out_file.write(str(data[key][name]['time']))
                    out_file.write(",")
                    out_file.write(str(data[key][name]['ram']))
                    out_file.write(",")
                    out_file.write(str(data[key][name]['disk']))
                    out_file.write(",")
                    out_file.write(name)
                    out_file.write(",")
                    out_file.write(key)
                    out_file.write("\n")

def read_bench(fof, data):
    with open(fof, 'r') as file_of_file:
        name = file_of_file.readline().strip()
        while name != "":
            tmp = name.split("/")[-1]
            key = [s for s in re.findall(r'\d+', tmp)][0]
            parts = name.split("_")
            with open(name, 'r') as bench:
                skip = bench.readline();
                values = bench.readline().strip().split("\t")
                if not math.isclose(float(values[-1]), 0.0):
                    time = values[-1]
                else:
                    time = values[0]
                ram = values[2]
                if "spsp" in parts:
                    tool = "SuperSampler_m"+parts[3]
                else:
                    tool = "Sourmash"
                if key in data:
                    if tool in data[key]:
                        data[key][tool]['ram'] = ram
                        data[key][tool]['time'] = time
                    else:
                        data[key][tool] = {}
                        data[key][tool]['ram'] = ram
                        data[key][tool]['time'] = time
                else:
                    data[key] = {}
                    data[key][tool] = {}
                    data[key][tool]['ram'] = ram
                    data[key][tool]['time'] = time
            name = file_of_file.readline().strip()
    print(data)

          

def read_index_size(sub_sourmash, sub_spsp, data):
    with open(sub_sourmash, 'r') as fof_sub_sourmash:
        line = fof_sub_sourmash.readline().strip()
        while line != "":
            tool = "Sourmash"
            #SAVING NAMES FOR DISPLAY IN FIGURE
            tmp = line.split("/")[-1]
            key = [s for s in re.findall(r'\d+', tmp)][0]
            if key in data:
                data[key][tool]['disk'] = os.stat(line).st_size/(1024*1024)
            else:
                data[key] = {}
                data[key][tool] = {}
                data[key][tool]['disk'] = os.stat(line).st_size/(1024*1024)
            line = fof_sub_sourmash.readline().strip()
    with open(sub_spsp, 'r') as fof_sub_spsp:
        f_name = fof_sub_spsp.readline().strip()
        while f_name != "":
            size = 0
            #SAVING NAMES FOR DISPLAY IN FIGURE
            tmp = f_name.split("/")[-1]
            tool = "SuperSampler_m" + [s for s in re.findall(r'\d+', tmp)][1]
            key = [s for s in re.findall(r'\d+', tmp)][0]
            if key in data:
                data[key][tool]['disk'] = os.stat(f_name).st_size/(1024*1024)
            else:
                data[key] = {}
                data[key][tool] = {}
                data[key][tool]['disk'] = os.stat(f_name).st_size/(1024*1024)
            f_name = fof_sub_spsp.readline().strip()

def populate_list(fof):
    file_list = []
    with open(fof, 'r') as fof_read:
        line = fof_read.readline().strip()
        while line != "":
            file_list.append(line)
            line = fof_read.readline().strip()
    return file_list

def get_diff(files_tool, simka, data, tool_name):
    if files_tool[0].find("containment") != -1:
        diff = "diff_containment"
    else:
        diff = "diff_jaccard"
    for i in range(len(files_tool)):
        df = pd.read_csv(files_tool[i], sep = ",", header = 0)
        df = df.to_numpy()
        ltri_simka = simka[np.tril_indices_from(simka, k = -1)]
        ltri_df = df[np.tril_indices_from(df, k = -1)]
        name = files_tool[i].split("/")[-1]
        key = [s for s in re.findall(r'\d+', name)][0]
        if tool_name == "SuperSampler_m":
            tool = tool_name + [s for s in re.findall(r'\d+', name)][1]
        else:
            tool = tool_name
        if key in data:
            if tool in data[key]:
                #MEAN DIFF
                #data[key][tool][diff] = np.mean(abs(simka - df)/simka)
                #SUM DIFF
                if diff == "diff_containment":
                    data[key][tool][diff] = abs(np.mean(simka) - np.mean(df))
                else:
                    #Using only half matrices as Jaccard is symetrical
                    print(diff)
                    data[key][tool][diff] = np.mean(abs(ltri_simka - ltri_df))
            else:
                print(f"should not happen, {tool} not in dict[{key}]")
        else:
            print(f"should not happen, {key} not in dict.")


def compare_results(res_spsp, res_sourmash, res_simka, data):
    #READING SIMKA
    simka = pd.read_csv(res_simka, sep = ";", header = 0)
    simka = simka.drop(simka.columns[[0]], axis = 1)
    simka =  simka.applymap(lambda x: 1-x)
    simka = simka.to_numpy()
    #ltri_simka = simka[np.tril_indices_from(simka, k = -1)]

    #GETTING EVERY CSV FILENAME
    files_spsp, files_sourmash = [], []
    files_spsp = populate_list(res_spsp)
    files_sourmash = populate_list(res_sourmash)

    #COMPUTING DIFFERENCES FOR SPSP + SAVING IN DICT
    get_diff(files_spsp, simka, data, "SuperSampler_m")
    get_diff(files_sourmash, simka, data, "Sourmash")

    if files_spsp[0].find("containment") != -1:
        for i in range(len(files_spsp)):
            files_spsp[i] = files_spsp[i].replace("containment", "jaccard")
    if files_sourmash[0].find("containment") != -1:
        for i in range(len(files_sourmash)):
            files_sourmash[i] = files_sourmash[i].replace("containment", "jaccard")
    get_diff(files_spsp, simka, data, "SuperSampler_m")
    get_diff(files_sourmash, simka, data, "Sourmash")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Stats comparing sourmash and SPSP')
    parser.add_argument('res_spsp', help='file of file of results for SuPerSamPler')
    parser.add_argument('res_sourmash', help='file of file of results for sourmash')
    parser.add_argument('res_simka', help='results for SimKa')
    parser.add_argument('sub_spsp', help='Subsampling file of file for SPSP (needed to output size)')
    parser.add_argument('sub_sm', help='Subsampling file for sourmash (needed to output size)')
    parser.add_argument('benchs', help="File of file for bench on comparisons (Needed for graph with ram and time).")
    parser.add_argument('out', help='Out filename')
    args = parser.parse_args(sys.argv[1:])
    writeCSV(args.sub_sm, args.sub_spsp, args.res_spsp, args.res_sourmash, args.res_simka, args.benchs, args.out)

#construct_variants(snakemake.input[0], snakemake.output[0], snakemake.output[1], snakemake.params["n"])
""""""
