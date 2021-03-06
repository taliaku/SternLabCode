
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
import os.path
import pathlib
from file_utilities import *
from optparse import OptionParser
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
sns.set_context("talk")




def main():
    # for Cluster
    # parser = OptionParser("usage: %prog [options]")
    # parser.add_option("-f", "--freqs_file_path", dest="freqs_file_path", help="path of the freqs file")
    # parser.add_option("-v", "--virus", dest="virus", help="Virus name: CVB3 for CV; RVB14 for RV; PV for PV")
    # (options, args) = parser.parse_args()
    #
    # freqs_file = options.freqs_file_path
    # virus = options.virus
    #
    # freqs_file = check_filename(freqs_file)

    #for Local
    source1 = "RV-p11"
    suffix1 = "%s.with.mutation.type.freqs" % source1
    freqs_file1 = "/Volumes/STERNADILABHOME$/volume3/okushnir/AccuNGS/180503_OST_FINAL_03052018/merged/%s/q30_3UTR_new/%s" % \
                 (source1, suffix1)

    source2 = "RV-p12"
    suffix2 = "%s.with.mutation.type.freqs" % source2
    freqs_file2 = "/Volumes/STERNADILABHOME$/volume3/okushnir/AccuNGS/180503_OST_FINAL_03052018/merged/%s/q30_3UTR_new/%s" % \
                 (source2, suffix2)
    source3 = "RV-IVT"
    suffix3 = "%s.with.mutation.type.freqs" % source3
    freqs_file3 = "/Volumes/STERNADILABHOME$/volume3/okushnir/AccuNGS/180503_OST_FINAL_03052018/merged/%s/q30_3UTR_new/%s" % \
                 (source3, suffix3)
    virus = "RVB14"
    seq_meth = "AccuNGS"
    freqs_list = [freqs_file1, freqs_file2, freqs_file3]


    # 1. Get freqs file and CirSeq running directory.
    path = freqs_file1.split('/')[0:-1]
    out_dir = '' #the freqs directory
    for i in path:
        out_dir += str(i + '/')
    tmp_cirseq_dir = out_dir + 'tmp/'
    pathlib.Path(out_dir + 'plots/').mkdir(parents=True, exist_ok=True)
    out_plots_dir = out_dir + 'plots/'

    if virus == "CVB3":
        ncbi_id ="M16572"
    if virus == "RVB14":
        ncbi_id = "NC_001490"
    if virus == "PV":
        ncbi_id ="V01149"


    """ 3. Adding mutation types to the freqs file"""
    # for i in freqs_list:
    #     if not os.path.isfile(i[0:-5] + "with.mutation.type.freqs"):
    #          append_mutation = find_mutation_type(i, ncbi_id)
    #     freqs_file_mutations = i[0:-5] + "with.mutation.type.freqs"

    fig2 = plt.figure()
    # gs = gridspec.GridSpec(2, 2)
    ax0 = plt.subplot()

    # gs.tight_layout(fig2)
    # ax = plt.subplot()

    make_boxplot_sample_control(freqs_list, ax0)

    plt.savefig(out_plots_dir + suffix1.split(sep='.')[0] + '_Transitions_Report_Control_sample.png', dpi=300)
    plt.close("all")
    print("The Transition Plot is ready in the folder")

"""Graphs"""

def arrange_freqs_file(freqs_file):
    """
    Plots the mutation frequencies boxplot
    :param freqs_file: pandas DataFrame after find_mutation_type function
    :param ax: ax location
    :return:
    """
    data = pd.read_table(freqs_file)
    data.reset_index(drop=True, inplace=True)
    flag = '-' in data.Base.values
    if flag is True:
        data = data[data.Ref != '-']
        data = data[data.Base != '-']
        data.reset_index(drop=True, inplace=True)
        # data['abs_counts'] = data['Freq'] * data["Read_count"]  # .apply(lambda x: abs(math.log(x,10))/3.45)
        # data['Frequency'] = data['abs_counts'].apply(lambda x: 1 if x == 0 else x) / data["Read_count"]
        # raise Exception("This script does not support freqs file with deletions, for support please contact Maoz ;)"
    data['Base'].replace('T', 'U', inplace=True)
    data['Ref'].replace('T', 'U', inplace=True)
    min_read_count = 100000
    data = data[data['Pos'] == np.round(data['Pos'])]  # remove insertions
    data['Pos'] = data[['Pos']].apply(pd.to_numeric)
    data = data[data['Read_count'] > min_read_count]
    data['mutation_type'] = data['Ref'] + data['Base']
    data = data[data['Ref'] != data['Base']]
    data = data[data["Base"] != "-"]
    data['abs_counts'] = data['Freq'] * data["Read_count"]  # .apply(lambda x: abs(math.log(x,10))/3.45)
    data['Frequency'] = data['abs_counts'].apply(lambda x: 1 if x == 0 else x) / data["Read_count"]
    data["Mutation"] = data["Ref"] + "->" + data["Base"]
    data["Source"] = freqs_file.split('/')[-1].split('.')[0]
    return data


def make_boxplot_sample_control(freqs_list, ax):
    data = pd.DataFrame()
    for k, i in enumerate(freqs_list):
        data_freqs = arrange_freqs_file(i)
        data = pd.concat([data_freqs, data], axis=0)
    #
    data.to_csv("/Volumes/STERNADILABHOME$/volume3/okushnir/AccuNGS/180503_OST_FINAL_03052018/merged/RV-p11/q30_3UTR_new/data.csv", sep=',', encoding='utf-8')

    g1 = sns.factorplot(x="Mutation Type", y="Frequency", data=data, col="Mutation", hue="Source", order=["Synonymous",
                        "Non-Synonymous", "Premature Stop Codon"], col_order=["C->U", "U->C", "G->A", "A->G"], kind="box", col_wrap=2)

    g1.set_xticklabels(["Synonymous", "Non\nSynonymous", "Premature\nStop Codon"], fontsize=10)
    g1.set(yscale="log", ylim=(0.00001, 0.01))
    g1.set_xlabels('')

    sns.set_palette(sns.color_palette("Paired", 12))
    # for a in g1.axes.flat:
    #     a.axhline(y=2.07E-04, color='r', linestyle='--')
    #Synonymous mutations
    data_AG_syn = data[data['Mutation'] == 'A->G']
    data_AG_syn = data_AG_syn[data_AG_syn['Mutation Type'] == 'Synonymous']
    data_UC_syn = data[data['Mutation'] == 'U->C']
    data_UC_syn = data_UC_syn[data_UC_syn['Mutation Type'] == 'Synonymous']
    data_AG_syn.to_csv(
        "/Volumes/STERNADILABHOME$/volume3/okushnir/AccuNGS/180503_OST_FINAL_03052018/merged/RV-p11/q30_3UTR_new/data_AG_syn.csv",
        sep=',', encoding='utf-8')
    cat1 = data_AG_syn[data_AG_syn['Source'] == 'RV-IVT']
    cat2 = data_AG_syn[data_AG_syn['Source'] == 'RV-p12']
    print("A->G Synonymous", ttest_ind(cat1['Frequency'], cat2['Frequency']))
    cat3 = data_UC_syn[data_UC_syn['Source'] == 'RV-IVT']
    cat4 = data_UC_syn[data_UC_syn['Source'] == 'RV-p12']
    print("U->C Synonymous", ttest_ind(cat3['Frequency'], cat4['Frequency']))
    # Non-Synonymous mutations
    data_AG_nonsyn = data[data['Mutation'] == 'A->G']
    data_AG_nonsyn = data_AG_nonsyn[data_AG_nonsyn['Mutation Type'] == 'Non-Synonymous']
    data_UC_nonsyn = data[data['Mutation'] == 'U->C']
    data_UC_nonsyn = data_UC_nonsyn[data_UC_nonsyn['Mutation Type'] == 'Non-Synonymous']
    data_AG_nonsyn.to_csv(
        "/Volumes/STERNADILABHOME$/volume3/okushnir/AccuNGS/180503_OST_FINAL_03052018/merged/RV-p11/q30_3UTR_new/data_AG_nonsyn.csv",
        sep=',', encoding='utf-8')
    cat1 = data_AG_nonsyn[data_AG_nonsyn['Source'] == 'RV-IVT']
    cat2 = data_AG_nonsyn[data_AG_nonsyn['Source'] == 'RV-p12']
    print("A->G Non-Synonymous", ttest_ind(cat1['Frequency'], cat2['Frequency']))
    cat3 = data_UC_nonsyn[data_UC_nonsyn['Source'] == 'RV-IVT']
    cat4 = data_UC_nonsyn[data_UC_nonsyn['Source'] == 'RV-p12']
    print("U->C Non-Synonymous", ttest_ind(cat3['Frequency'], cat4['Frequency']))

if __name__ == "__main__":
    main()
