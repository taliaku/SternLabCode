

# from OU_model_constructor import *
from selection_model_analysis import *
import argparse

def main(args):


    # run the MC simulation and wrute results to log.

    # super_folder = r'/Volumes/STERNADILABHOME$/volume1/daniellem1/Entropy/data/Phylogeny/family'
    # features = ['k5']
    # out= r'/Volumes/STERNADILABHOME$/volume1/daniellem1/Entropy/data/OU_model/MonteCarlo'

    #BM_OU_runner(super_folder, features, out, MC=True, log=False)

    # run the analysis of the families that are ou significant
    fasta = r'/sternadi/home/volume1/daniellem1/Entropy/data/Phylogeny/family/Caliciviridae/Caliciviridae.fasta'
    # out = r'/Users/daniellemiller/Google Drive/Msc Bioinformatics/Projects/entropy/most_updated/OU_significant/k5'
    out = r'/sternadi/home/volume1/daniellem1/Entropy/data/profile'
    # out = r'/sternadi/home//volume1/daniellem1/Entropy/data/ecoli'


    df = pd.read_csv(r'/sternadi/home/volume1/daniellem1/Entropy/data/OU_model/simulations_significance_bm_k5.csv')
    #df = pd.read_csv(r'/Volumes/STERNADILABHOME$/volume1/daniellem1/Entropy/data/OU_model/simulations_significance_bm_k5.csv')
    families = df['family'].values
    family = families[args.index -1]
    # print(family)
    fasta = r'/sternadi/home/volume1/daniellem1/Entropy/data/Phylogeny/family/{}/{}.fasta'.format(family, family)
    # # get_kmers_distribution(fasta, 1, out)
    get_entropy_profile(fasta, 200, out)
    deltaG_profile(fasta, 200, out)

    # sns.set_style('white')
    # # run the kmers test for all families regardless their model significance
    # families = df['family'].values
    # for family in tqdm(families):
    #     fasta = r'/Volumes/STERNADILABHOME$/volume1/daniellem1/Entropy/data/Phylogeny/family/{}/{}.fasta'.format(family, family)
    #     get_kmers_distribution(fasta, 5, out)

    # description_2_seq = []
    # for rec in SeqIO.parse("/sternadi/home/volume1/daniellem1/Entropy/data/ecoli/sequence.gb", "genbank"):
    #     description_2_seq.append((rec.description, str(rec.seq)))
    #
    # idx = args.index
    #
    # description = description_2_seq[idx][0]
    # seq = description_2_seq[idx][1]
    #
    # get_entropy_profile_per_sequence(seq, 10000, description, out=out)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--index", type=int, help="array index")

    args = parser.parse_args()

    main(args)
