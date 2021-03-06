#!/bin/bash
#PBS -S /bin/bash
#PBS -r y
#PBS -q adis
#PBS -v PBS_O_SHELL=bash,PBS_ENVIRONMENT=PBS_BATCH
#PBS -N pipeline_control
#PBS -o /sternadi/home/volume3/omer/logs/
#PBS -l ncpus=1
#PBS -l mem=2gb
#PBS -J 0-31

id
date
hostname
module load python/python-anaconda3.2019.7

ref_ET86="/sternadi/home/volume1/shared/data/ref_genomes/HIV_C/Ref_C_ET86.fasta"

# original
declare -a SAMPLES_ARRAY=(100888_S14  130945_S2  504185_S29 504190_S34  504194_S38  504198_S42 504202_S46  504206_S50  504210_S54  504215_S59  504221_S65  504226_S70  504231_S75  79504_S23  83476_S27  84864_S47  TASPX100926_S26  X145364_S75  X83354_S92 105090_S50  504181_S25  504186_S30  504191_S35  504195_S39  504199_S43  504203_S47  504207_S51  504211_S55  504217_S61  504223_S67  504227_S71  504233_S77  81065_S64  84298_S2   87415_S75  TASPX119494_S74  X145656_S76  X84335_S20 105094_S45  504182_S26  504188_S32  504192_S36  504196_S40  504200_S44  504204_S48  504208_S52  504212_S56  504218_S62  504224_S68  504228_S72  504234_S78  83351_S15  84434_S32  TASPX100702_S59  X100748_S73  X160138_S81  X84434_S3 105257_S39  504184_S28  504189_S33  504193_S37  504197_S41  504201_S45  504205_S49  504209_S53  504214_S58  504220_S64  504225_S69  504230_S74  504235_S79  83456_S87 84785_S56  TASPX100711_S29  X145364-R_S95 X83322_S89   X84994_S90)

sample=${SAMPLES_ARRAY[$PBS_ARRAY_INDEX]}
input_dir="/sternadi/datasets/volume2/HIV_ravi_gupta_merged/$sample"

# low_qual run
ref_low="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta/runs/ET86_merged_low_qual/iter1/cons/$sample.fasta"
output_dir_low="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta/runs/ET86_merged_low_qual/iter2/$sample"
mkdir -p $output_dir_low
python /sternadi/home/volume1/shared/SternLab/pipeline_runner.py -i $input_dir -o $output_dir_low -r $ref_low  -NGS_or_Cirseq 1 -q 30 -rep 1 -b 40 -t z -ev 1e-2

# high_qual run
ref_high="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta/runs/ET86_merged_high_qual/iter1/cons/$sample.fasta"
output_dir_high="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta/runs/ET86_merged_high_qual/iter2/$sample"
mkdir -p $output_dir_high
python /sternadi/home/volume1/shared/SternLab/pipeline_runner.py -i $input_dir -o $output_dir_high -r $ref_high  -NGS_or_Cirseq 1 -q 30 -rep 2 -b 40 -t z -ev 1e-2


# first line
declare -a SAMPLES_ARRAY_FIRSTLINE=(78292_S1  X105350_S13  X108456_S11  X117807_S26  X122087_S18  X128277_S27  X135623_S20  X161610_S28  X165309_S33  X83744_S2  X96026_S5  X101530_S9  X105354_S14  X111406_S10  X122054_S15  X122107_S17  X130823_S22  X160392_S24  X165276_S32  X178870_S29  X87707_S25  X96051_S7  X102662_S8  X108262_S21  X111489_S12  X122061_S16  X122107_S27  X132700_S84  X160433_S25  X165290_S34  X83348_S4  X88469_S6)

sample=${SAMPLES_ARRAY_FIRSTLINE[$PBS_ARRAY_INDEX]}
input_dir="/sternadi/datasets/volume2/HIV_ravi_gupta_CONTROL_merged/1st_line_VF/$sample"
ref_low="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta_control/runs/ET86_low_qual/iter1/1st_line_VF/cons/$sample.fasta"
ref_high="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta_control/runs/ET86_high_qual/iter1/1st_line_VF/cons/$sample.fasta"
output_dir_low="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta_control/runs/ET86_low_qual/iter2/1st_line_VF/$sample"
output_dir_high="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta_control/runs/ET86_high_qual/iter2/1st_line_VF/$sample"

# low_qual run
mkdir -p $output_dir_low
python /sternadi/home/volume1/shared/SternLab/pipeline_runner.py -i $input_dir -o $output_dir_low -r $ref_low  -NGS_or_Cirseq 1 -q 30 -rep 1 -b 40 -t z -ev 1e-2
# high_qual run
mkdir -p $output_dir_high
python /sternadi/home/volume1/shared/SternLab/pipeline_runner.py -i $input_dir -o $output_dir_high -r $ref_high  -NGS_or_Cirseq 1 -q 30 -rep 2 -b 40 -t z -ev 1e-2

# baseline
declare -a SAMPLES_ARRAY_BASELINE=(78486_S9  79649_S49  81088_S63  X105130_S8   X105416_S169  X112003_S13  X117597_S55  X117659_S88  X119113_S320  X122207_S32  X160394_S25  X84355_S11   X84505_S40  X84772_S12   X88273_S273  X94731_S49  79578  81003_S48  X101706  X105289_S56  X105500_S302  X117547_S16  X117607_S11  X117890_S46  X121017_S309  X135606_S69  X83676_S242  X84469_S265  X84641_S47  X84990_S248  X88373_S267  X96465_S54)

sample=${SAMPLES_ARRAY_BASELINE[$PBS_ARRAY_INDEX]}
input_dir="/sternadi/datasets/volume2/HIV_ravi_gupta_CONTROL_merged/Baseline/$sample"
ref_low="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta_control/runs/ET86_low_qual/iter1/Baseline/cons/$sample.fasta"
ref_high="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta_control/runs/ET86_high_qual/iter1/Baseline/cons/$sample.fasta"
output_dir_low="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta_control/runs/ET86_low_qual/iter2/Baseline/$sample"
output_dir_high="/sternadi/home/volume1/shared/analysis/HIV_ravi_gupta_control/runs/ET86_high_qual/iter2/Baseline/$sample"

# low_qual run
mkdir -p $output_dir_low
python /sternadi/home/volume1/shared/SternLab/pipeline_runner.py -i $input_dir -o $output_dir_low -r $ref_low  -NGS_or_Cirseq 1 -q 30 -rep 1 -b 40 -t z -ev 1e-2
# high_qual run
mkdir -p $output_dir_high
python /sternadi/home/volume1/shared/SternLab/pipeline_runner.py -i $input_dir -o $output_dir_high -r $ref_high  -NGS_or_Cirseq 1 -q 30 -rep 2 -b 40 -t z -ev 1e-2


date