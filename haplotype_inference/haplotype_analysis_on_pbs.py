import argparse
import os
import sys
STERNLAB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(STERNLAB_PATH)
from utils.pbs_jobs import create_pbs_cmd
from utils.logger import pipeline_logger
from utils.runner_utils import submit_wait_and_log


def main(args):
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    input = args.input_dir
    num_of_jobs = args.number_of_bases
    log = pipeline_logger(logger_name='Haplotype-Analysis', log_folder=output_dir)
    log.info(f"Starting haplotype analysis on folder {input} and outputting to {output_dir}")
    mutations_path = os.path.join(input, 'mutations_all.txt')
    blast_path = os.path.join(input, 'joined.blast')
    freqs_path = os.path.join(input, 'joined.freqs')
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    variants_cmd = os.path.join(this_dir_path, 'variants_on_same_read.py')
    variants_folder = os.path.join(output_dir, 'variants')
    os.makedirs(variants_folder, exist_ok=True)
    cmd1 = f"python {variants_cmd} {blast_path} {mutations_path} $PBS_ARRAY_INDEX {freqs_path} > " \
           f"{variants_folder}/$PBS_ARRAY_INDEX.txt"
    cmd_path = os.path.join(output_dir, 'variants.cmd')
    alias = 'Haplotype-Analysis - Getting Variants'
    create_pbs_cmd(cmdfile=cmd_path, alias=alias, jnum=num_of_jobs, gmem=7, cmds=cmd1)
    submit_wait_and_log(cmdfile=cmd_path, logger=log, job_name=alias)
    linked_pairs_path = os.path.join(output_dir, "linked_pairs.txt")
    cmd2 = f"cat {variants_folder}/*.txt > {linked_pairs_path}"
    co_occurs_cmd = os.path.join(this_dir_path, 'co-occurs_to_stretches.py')
    stretches_path = os.path.join(output_dir, 'stretches.csv')
    cmd3 = f"python {co_occurs_cmd} {linked_pairs_path} -o {stretches_path}"
    graph_haplotypes_cmd = os.path.join(this_dir_path, 'graph_haplotypes.py')
    cmd4 = f"python {graph_haplotypes_cmd} -i {stretches_path} -o {output_dir}"
    cmds = cmd2 + "\n" + cmd3 + "\n" + cmd4
    cmd_path = os.path.join(output_dir, 'haplotype_analysis.cmd')
    alias = 'Haplotype-Analysis'
    create_pbs_cmd(cmdfile=cmd_path, alias='Haplotype-Analysis - Graphing', cmds=cmds)
    submit_wait_and_log(cmdfile=cmd_path, logger=log, job_name=alias)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_dir", help="Where all the files will go", required=True)
    parser.add_argument("-i", "--input_dir", help="Folder containing perl pipeline output", required=True)
    parser.add_argument("-n", "--number_of_bases", help="How many bases were sequenced?", default=3000) #TODO: do this automatically..
    args = parser.parse_args()
    main(args)
