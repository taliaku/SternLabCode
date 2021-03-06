#! python/python-anaconda3.2019.7

import os
import sys
import glob
import time
from utils.logger import pipeline_logger
from utils.pbs_jobs import submit


def check_queue(queue):
	allowed_queues = ["inf", "hugemem", "pup-interactive", "parallel", "adis", "adis-long", 'adistzachi@power9']
	if queue not in allowed_queues:
		raise Exception(f"Sorry but queue must be one of {allowed_queues}, not '{queue}'")

def Sleep (alias, job_id, sleep_max=1200000, sleep_quantum=3, queue='adistzachi'):
	start_time = time.time()
	i = 0
	if job_id[-2:]=='[]': # grep doesn't like these..
		job_id = job_id[:-2]
	qstat_command = f"qstat @power9 | grep {job_id}" #TODO: do we really need to specify power9?
	qstat_result = os.popen(qstat_command).read()
	while len(qstat_result) > 0 and i <= sleep_max: 
		for second in range(0, sleep_quantum):
			elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
			sys.stdout.write("\r")
			sys.stdout.write(f'Elapsed time: {elapsed_time}')
			sys.stdout.flush()
			time.sleep(1)
		i += sleep_quantum
		qstat_result = os.popen(qstat_command).read()
	sys.stdout.write("\n")
	if len(qstat_result) > 0:
		raise Exception(alias + " stage was not completed. Max sleep time reached\n")
	return elapsed_time

def FindFilesInDir(dir_path, file_type):
	file_path = dir_path + "/*" + file_type
	list_of_files = sorted(glob.glob(file_path))
	num_of_files = len(list_of_files)
	if num_of_files > 0:
		for file in list_of_files:
			size = os.path.getsize(file)
			if size == 0:
				time.sleep(15)
				size = os.path.getsize(file)
			if size == 0:
				raise Exception("Unexpected error, some of the " + file_type + " files in " + dir_path + " are empty\n")
	
	return list_of_files
	
def create_array(files_list):
	array = '(' 
	for i in range(len(files_list)):
		array += files_list[i]
		if i != len(files_list)-1:
			array += " "
	array += ')'
	return array


def submit_wait_and_log(cmdfile, logger, job_name):
	job_id = submit(cmdfile) 	#TODO: give a meaningful error when this fails.
	logger.info(f"Started {job_name} with job id: {job_id}")
	elapsed_time = Sleep(job_name, job_id)
	time_suffix = _get_time_suffix(elapsed_time)
	logger.info(f"Done {job_name} in {elapsed_time} {time_suffix}")


def _get_time_suffix(elapsed_time):
	time_suffix = 'seconds'
	if int(elapsed_time[:2]) > 0:
		time_suffix = 'hours'
	elif int(elapsed_time[3:5]) > 0:
		time_suffix = 'minutes'
	return time_suffix