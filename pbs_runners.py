#! /usr/local/python_anaconda/bin/python3.4
#! /usr/local/python_anaconda/bin/python3.4

import pbs_jobs
import os
from os import path
from file_utilities import check_filename, check_dirname
from seqFileTools import convert_fasta_to_phylip

def baseml_runner(ctl, alias = "bml"):
    """
    run baseml program from PAML on cluster
    :param ctl: ctl file path
    :param alias: job name (default: bml)
    :return: job id
    """
    ctl = check_filename(ctl)
    cmdfile = "baseml_cmd.txt"; tnum = 1; gmem = 2
    cmds = "echo %s \n/sternadi/home/volume1/taliakustin/software/paml4.8/bin/baseml %s" %(ctl, ctl)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def codeml_runner(ctl, alias = "cml"):
    """
    run baseml program from PAML on cluster
    :param ctl: ctl file path
    :param alias: job name (default: bml)
    :return: job id
    """
    ctl = check_filename(ctl)
    base = os.path.split(ctl)[0]
    cmdfile = "codeml.txt"; tnum = 1; gmem = 2
    cmds = "cd %s\necho %s \n/sternadi/home/volume1/taliakustin/software/paml4.8/bin/codeml %s" %(base, ctl, ctl)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id

def script_runner(cmds, alias = "script"):
    """
    run script on cluster
    :param cmds: script running line
    :param alias: job name (default: script)
    :return: job id
    """
    cmdfile = "script"; tnum=1; gmem=1
    print(cmdfile, alias, tnum, gmem, cmds)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id

def phyml_runner(alignment, alias = "phyml", phylip=True):
    """
    run phyml on cluster (converts tpo phylip if the flag phylip==False)
    :param alignment: alignment file path
    :param alias: job name (default: phyml)
    :param phylip: True if phylip file, False if fasta file
    :return: job id
    """
    alignment = check_filename(alignment)
    if phylip == False:
        alignment = convert_fasta_to_phylip(alignment)
    cmdfile = "phyml"; tnum = 1; gmem = 2
    cmds = "/sternadi/home/volume1/shared/tools/PhyML/PhyML_3.0_linux64 -i %s -b 0 -o n" % alignment
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def phyml_aa_runner(alignment, alias = "phyml", phylip=True):
    """
    run phyml on aa alignment on cluster
    :param alignment: alignment file path
    :param alias: job name (default: phyml)
    :param phylip: True if phylip file, False if fasta file
    :return: job id
    """
    alignment = check_filename(alignment)
    if phylip == False:
        alignment = convert_fasta_to_phylip(alignment)
    cmdfile = "phyml"; tnum = 1; gmem = 2
    cmds = "/sternadi/home/volume1/shared/tools/PhyML/PhyML_3.0_linux64 -i %s -d aa -q -b 0" % alignment
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def fastml_runner(alignment, tree, alias = "fastml", outdir = None):
    """
    run fastml from phylogenyCode on cluster
    :param alignment: alignment file path
    :param tree: tree file path
    :param alias: job name (default: fastml)
    :param outdir: output directory for results (default: None - saves in the alignment's dir)
    :return: job id
    """
    alignment = check_filename(alignment)
    tree = check_filename(tree)
    if outdir == None:
        outdir = os.path.dirname(alignment)
    else:
        out_dir = check_dirname(outdir)
    basename = os.path.basename(alignment).split(".")[0].split("_aln")[0]
    newick_tree = outdir + "/" + basename + ".tree.newick.txt"
    ancestor_tree = outdir + "/" + basename + ".tree.ancestor.txt"
    joint_seqs = outdir + "/" + basename + ".seq.joint.txt"
    marginal_seqs = outdir + "/" + basename + ".seq.marginal.txt"
    joint_prob = outdir + "/" + basename + ".prob.joint.txt"
    marginal_prob = outdir + "/" + basename + ".prob.marginal.txt"
    cmdfile = "fastml"; tnum = 1; gmem = 1
    cmds = "/sternadi/home/volume1/shared/tools/phylogenyCode/programs/fastml/fastml -s %s -t %s -mn -x %s " \
           "-y %s -j %s -k %s -d %s -e %s -qf" % (alignment, tree, newick_tree, ancestor_tree, joint_seqs,
                                                 marginal_seqs, joint_prob, marginal_prob)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def mafft_runner(sequence, alignment = None, alias = "mafft"):
    """
    run mafft on cluster
    :param sequence: sequence file (fasta format)
    :param alignment: alignment output file (default: None)
    :param alias: job name (default: mafft)
    :return: job id
    """
    sequence = check_filename(sequence)
    if alignment == None:
        alignment = sequence.split(".fasta")[0] + ".aln"
    alignment = check_filename(alignment, Truefile=False)
    cmds = "/sternadi/home/volume1/taliakustin/software/mafft-7.300-with-extensions/scripts/mafft %s > %s"\
           % (sequence, alignment)
    cmdfile = "mafft"; tnum = 1; gmem = 1
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def prank_runner(sequence, alignment=None, alias = "prank"):
    """
    run prank on cluster
    :param sequence: sequence file path (fasta format)
    :param alignment: alignment output file (default: None)
    :param alias: job name (default: prank)
    :return: job id
    """
    if alignment == None:
        alignment = sequence.split(".fasta")[0] + ".aln"
    sequence = check_filename(sequence)
    alignment = check_filename(alignment, Truefile=False)
    cmds = "/powerapps/share/bin/prank -d=%s -o=%s -F" % (sequence, alignment)
    cmdfile = "prank_alignment"; tnum=1; gmem=7
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id



def prank_codon_runner(sequence, alignment=None, alias = "prank"):
    """
    run prank codon on cluster
    :param sequence: sequence file path (fasta format)
    :param alignment: alignment output file (default: None)
    :param alias: job name (default: prank)
    :return: job id
    """
    if alignment == None:
        alignment = sequence.split(".fasta")[0] + ".codon_aln"
    sequence = check_filename(sequence)
    alignment = check_filename(alignment, Truefile=False)
    cmds = "/powerapps/share/bin/prank -d=%s -o=%s -F -codon" % (sequence, alignment)
    cmdfile = "prank_alignment"; tnum=1; gmem=5
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def prank_codon_runner(sequence, alignment=None, alias = "prank"):
    """
    run phyml on cluster
    :param sequence: sequence file path (fasta format)
    :param alignment: alignment output file (default: None)
    :param alias: job name (default: prank)
    :return: job id
    """
    if alignment == None:
        alignment = sequence.split(".fasta")[0] + ".aln"
    sequence = check_filename(sequence)
    alignment = check_filename(alignment, Truefile=False)
    cmds = "/powerapps/share/bin/prank -d=%s -o=%s -F -codon" % (sequence, alignment)
    cmdfile = "prank_alignment"; tnum=1; gmem=5
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id



def prank_runner_with_tree(sequence, tree, alignment=None, alias = "prank"):
    """
    run prank with tree on cluster
    :param sequence: sequence file path (fasta format)
    :param tree: tree file path
    :param alignment: alignment output file (default: None)
    :param alias: job name (default: prank)
    :return: job id
    """
    if alignment == None:
        alignment = sequence.split(".fasta")[0] + ".aln"
    sequence = check_filename(sequence)
    tree = check_filename(tree)
    alignment = check_filename(alignment, Truefile=False)
    cmds = "/powerapps/share/bin/prank -d=%s -t=%s -o=%s -F" % (sequence, tree, alignment)
    cmdfile = "prank_alignment_with_tree"; tnum=1; gmem=5
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def njTree_runner(alignment, tree=None, alias = "njTree"):
    """
    run neighbors-joining tree on cluster
    :param alignment: alignment file path
    :param tree: output tree path (default: None)
    :param alias: job name (default: njTree)
    :return: job id
    """
    if tree == None:
        tree = alignment.split(".")[0] + ".tree"
    alignment = check_filename(alignment)
    tree = check_filename(tree, Truefile=False)
    cmdfile = "njTree"; tnum=1; gmem=2
    cmds = "/sternadi/home/volume1/shared/tools/phylogenyCode/programs/treeUtil/njTreeJCdist -i %s -o %s -an"\
           % (alignment, tree)
    dir = "/sternadi/home/volume1/shared/tools/phylogenyCode/programs/treeUtil/"
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def sampling_runner(alignment, amount, sampled_file=None, alias = "sampling"):
    """
    run sampling on cluster (doesn't sample random seqs)
    :param alignment: alignment file path
    :param amount: amount of sequences to sample
    :param sampled_file: output file (default: None)
    :param alias: job name (default: sampling)
    :return: job id
    """
    alignment = check_filename(alignment)
    if sampled_file == None:
        sampled_file = alignment.split(".")[0] + "_sampled.aln"
    output_file = check_filename(sampled_file, Truefile=False)
    cmdfile = "njTree"; tnum=1; gmem=2
    cmds = "/sternadi/home/volume1/shared/tools/phylogenyCode/programs/sampling/sampling -i %s -n %s -o %s"\
           % (alignment, amount, sampled_file)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def gzip_runner(file, alias = "gzip"):
    """
    run gzip on cluster
    :param file: input file path
    :param alias: job name (default: gzip)
    :return: job id
    """
    file = check_filename(file)
    cmdfile = "gzip"; tnum=1; gmem=2
    cmds = "gzip %s" % file
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def cp_runner(file, dest_file, alias = "cp"):
    """
    run cp on cluster
    :param file: input file path
    :param dest_file: output file path
    :param alias: job name (default: cp)
    :return: job id
    """
    if not "*" in file:
        file = check_filename(file)
        dest_file = check_filename(dest_file, Truefile=False)
    cmdfile = "cp"; tnum=1; gmem=2
    cmds = "cp %s %s" % (file, dest_file)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def baliphy_runner(sequence, alias = "baliphy"):
    """
    run baliphy on cluster
    :param sequence: input sequence file path
    :param alias: job name (default: baliphy)
    :return: job id
    """
    sequence = check_filename(sequence)
    cmdfile = "baliphy_M8_cmd.txt"; tnum = 1; gmem = 2
    cmds = "/sternadi/home/volume1/taliakustin/software/bali-phy-2.3.7/bin/bali-phy"\
                                                            + " " + sequence\
                                                            + " -V "
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id



def pear_runner(forward, reverse, output, alias = "pear"):
    """
    run pear (pair-ended merger) on cluster
    :param forward: forward file path
    :param reverse: reverse file path
    :param output: output file path
    :param alias: job name (default pear)
    :return: job id
    """
    forward = check_filename(forward)
    reverse = check_filename(reverse)
    output = check_filename(output, Truefile=False)
    cmdfile = "pear"; tnum = 1; gmem = 2
    cmds = "/usr/local/bin/pear -f %s -r %s -o %s" % (forward, reverse, output)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def ufilter_runner(fastq, output, alias = "ufilter"):
    """
    run ufilter on cluster
    :param fastq: fastq file path
    :param output: output file path
    :param alias: job name (default: ufilter)
    :return: job id
    """
    fastq = check_filename(fastq)
    output = check_filename(output, Truefile=False)
    cmdfile = "ufilter"; tnum = 1; gmem = 2
    cmds = "/usr/local/bin/usearch -fastq_stripleft 5 -fastq_filter %s -fastqout %s" % (fastq, output)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def umerge_runner(forward_fastq, output, alias = "umerge"):
    """
    run umerge on cluster
    :param forward_fastq: forward fastq file path
    :param output: ouput file path
    :param alias: job name (default: umerge)
    :return: job id
    """
    forward_fastq = check_filename(forward_fastq)
    output = check_filename(output, Truefile=False)
    cmdfile = "umerge"; tnum = 1; gmem = 2
    cmds = "/usr/local/bin/usearch" \
           " -fastq_qmaxout 80 -fastq_qmax 80 -fastq_mergepairs %s -fastqout %s -report %s.report"\
           % (forward_fastq, output, output)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def blast_runner(seqfile, dbfile="/sternadi/home/volume1/shared/data/nt/nt", outfile=None, alias="blast", hitlist_size=50000):
    """
    run blast on cluster
    :param seqfile: sequence file path
    :param dbfile: db file (default: /sternadi/home/volume1/shared/data/nt/nt)
    :param outfile: output file path (default: None)
    :param alias: job name (blast)
    :return: job id
    """
    seqfile = check_filename(seqfile)
    if outfile != None:
        outfile = check_filename(outfile, Truefile=False)
    else:
        outfile = path.split(seqfile)[0] + "/blast_results.txt"
    cmdfile = "blast_cmd"; tnum = 1; gmem = 2
    cmds = "/sternadi/home/volume1/shared/tools/ncbi-blast-2.2.30+/bin/blastn"\
                + " -query %s -out %s -db %s -outfmt 5 -max_target_seqs %i" % (seqfile, outfile, dbfile, hitlist_size)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def blast_output6_runner(seqfile, dbfile, outfile, alias = "blast"):
    """
    run blast on cluster - output as pipeline - format 6
    :param seqfile: sequence file path
    :param dbfile: db file
    :param outfile: output file path
    :param alias: job name (blast)
    :return: job id
    """
    seqfile = check_filename(seqfile)
    if outfile != None:
        outfile = check_filename(outfile, Truefile=False)
    cmdfile = "blast_cmd"; tnum = 1; gmem = 2
    cmds = "/sternadi/home/volume1/shared/tools/ncbi-blast-2.2.30+/bin/blastn"\
                + " -query %s -task megablast -out %s -db %s -outfmt '6 sseqid qseqid qstart qend qstrand sstart send sstrand length btop' " \
                  "-num_alignments 100 -dust no -soft_masking F -perc_identity 85 -evalue 1e-7"\
                  % (seqfile, outfile, dbfile)

    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id

def blastx_output6_runner(seqfile, outfile, dbfile="/sternadi/home/volume1/shared/data/nr/nr", alias = "blast"):
    """
    run blast on cluster - output as pipeline - format 6
    :param seqfile: sequence file path
    :param dbfile: db file
    :param outfile: output file path
    :param alias: job name (blast)
    :return: job id
    """
    seqfile = check_filename(seqfile)
    if outfile != None:
        outfile = check_filename(outfile, Truefile=False)
    cmdfile = "blast_cmd"; tnum = 1; gmem = 2
    cmds = "/sternadi/home/volume1/shared/tools/ncbi-blast-2.2.30+/bin/blastx"\
                + " -query %s -out %s -db %s -outfmt 6" % (seqfile, outfile, dbfile)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id

def bowtie2_runner(bowtie_index_path, fastq_file, sam_output, alias="bowtie2"):
    """
    run bowtie2 - very fast local flag is on
    :param bowtie_index_path: bowtie index file path (output of bowtie2-build)
    :param fastq_file: fastq file path
    :param sam_output: output file for sam file
    :param alias: job name (bowtie2)
    :return: job id
    """
    bowtie_index_path = check_filename(bowtie_index_path, Truefile=False)
    fastq_file = check_filename(fastq_file)
    sam_output = check_filename(sam_output, Truefile=False)
    cmdfile = "bowtie2"; tnum = 1; gmem = 2
    cmds = "/usr/local/bin/bowtie2"\
           + " --very-fast-local -x  %s %s -S %s" % (bowtie_index_path, fastq_file, sam_output)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id

def tophat2_runner(output_dir, bowtie_reference, fastq, alias="tophat2"):
    """
    tophat2 runner
    :param output_dir: output directory
    :param bowtie_reference: bowtie reference path
    :param fastq: fastq path
    :param alias: job name (tophat2)
    :return: job id
    """
    output_dir = check_dirname(output_dir, Truedir=False)
    bowtie_reference = check_filename(bowtie_reference, Truefile=False)
    fastq = check_filename(fastq)

    cmdfile = "tophat2"; tnum = 1; gmem = 2
    cmds = "/sternadi/home/volume1/taliakustin/software/tophat-2.1.1.Linux_x86_64/tophat2"\
           + " -o %s %s %s" % (output_dir, bowtie_reference, fastq)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds,load_python=False)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id



def r4s_runner(tree_file, seq_file, outfile, dirname, tree_outfile=None, unormelized_outfile=None, log_outfile=None,\
               alias = "r4s"):
    """
    run r4site on cluster
    :param tree_file: input tree file path
    :param seq_file: input sequence file path
    :param outfile: outfile path
    :param dirname: dirname for ouput files
    :param tree_outfile: output tree file path (default: None)
    :param unormelized_outfile: unormelized rated output file (default: None)
    :param log_outfile: output log file (default: None)
    :param alias: job name (default: r4s)
    :return: job id
    """
    tree_file = check_filename(tree_file)
    seq_file = check_filename(seq_file)
    dirname = check_dirname(dirname)

    if tree_outfile != None:
        tree_outfile = check_filename(tree_outfile, Truefile=False)
    else:
        tree_outfile = dirname + "/" + "out-tree"
    if unormelized_outfile != None:
        unormelized_outfile = check_filename(unormelized_outfile, Truefile=False)
    else:
        unormelized_outfile = dirname + "/out-unormelized"
    if log_outfile != None:
        log_outfile = check_filename(log_outfile, Truefile=False)
    else:
        log_outfile = dirname + "/out-log"


    cmdfile = "r4s_cmd.txt"; tnum = 1; gmem = 2
    if tree_file !=None:
        cmds = "/sternadi/home/volume1/shared/tools/rate4site"\
                                                            + " -t " + tree_file\
                                                            + " -s " + seq_file\
                                                            + " -o " + outfile\
                                                            + " -x " + tree_outfile\
                                                            + " -y " + unormelized_outfile\
                                                            + " -V 10"\
                                                            + " -l " + log_outfile\
                                                            + " -Mh -k 4"
    else:
        cmds = "/sternadi/home/volume1/shared/tools/rate4site"\
                                                            + " -s " + seq_file\
                                                            + " -o " + outfile\
                                                            + " -x " + tree_outfile\
                                                            + " -y " + unormelized_outfile\
                                                            + " -V 10"\
                                                            + " -l " + log_outfile\
                                                            + " -Mh -k 4"
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id


def codeml_united_runner(clt1, clt2, rst1_name, rst2_name, alias ="cml"):
    """
    run codeml program from PAML on cluster - (runs both alternative and null model in one job).
    :param ctl1: ctl file path for null model
    :param ctl2: ctl file path for alternative model
    :param rst1_name: result file name for null model
    :param rst2_name: result file alternative for null model
    :param alias: job name (default: bml)
    :return: job id
    """

    clt1 = file_utilities.check_filename(clt1)
    clt2 = file_utilities.check_filename(clt2)
    base = os.path.split(clt1)[0]
    cmdfile = "codeml.txt"; tnum = 1; gmem = 2
    cmds = "cd %s\n" \
           "/sternadi/home/volume1/taliakustin/software/paml4.8/bin/codeml %s\n" \
           "mv rst %s\n" \
           "/sternadi/home/volume1/taliakustin/software/paml4.8/bin/codeml %s\n" \
           "mv rst %s\n" % (base, clt1, rst1_name, clt2, rst2_name)
    pbs_jobs.create_pbs_cmd(cmdfile=cmdfile, alias=alias, jnum=tnum, gmem=gmem, cmds=cmds)
    job_id = pbs_jobs.submit(cmdfile)
    return job_id
