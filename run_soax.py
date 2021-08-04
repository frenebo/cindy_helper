import argparse
from snakeutils.files import readable_dir
import os
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import subprocess
import tqdm
from ctypes import c_int32
import time
from snakeutils.logger import PrintLogger, Colors

def run_soax(soax_args):
    batch_soax = soax_args["batch_soax"]
    tif_dir = soax_args["tif_dir"]
    params_name = soax_args["params_name"]
    param_fp = soax_args["param_fp"]
    snakes_output_dir = soax_args["snakes_output_dir"]
    logger = soax_args["logger"]
    stdout_fp = soax_args["stdout_fp"]
    errors_fp = soax_args["errors_fp"]

    # error_fp = os.path.join(logging_dir,"error_" + params_name + ".txt")

    # stdout_fp = os.path.join(logging_dir,"stdout_" + params_name + ".txt")

    with open(error_fp,"w") as error_file, open(stdout_fp,"w") as stdout_file:
        command = "{batch_soax} --image {tif_dir} --parameter {param_fp} --snake {snakes_output_dir}".format(
            batch_soax = batch_soax,
            tif_dir=tif_dir,
            param_fp=param_fp,
            snakes_output_dir=snakes_output_dir,
        )

        logger.log("Executing '{}'".format(command))
        try:
            code = subprocess.run(command,shell=True,stdout=stdout_file,stderr=error_file,check=True).returncode
            logger.success("Completed {}".format(command))
        except subprocess.CalledProcessError as e:
            logger.error("ERROR: ")
            logger.error("Failed to run {}. return code {}".format(command,e.returncode))
            logger.error("STDERR saved in {}".format(error_fp))
            logger.error("STDOUT saved in {}".format(stdout_fp))

def run_soax(
    batch_soax,
    tif_dir,
    params_dir,
    output_dir,
    logging_dir,
    use_subdirs,
    workers_num,
    logger=PrintLogger):
    param_files = [filename for filename in os.listdir(params_dir) if filename.endswith(".txt")]
    param_files.sort()

    logger.log("WORKERS: {}".format(workers_num))

    soax_args = []

    # If recursive subdirs, we have
    # {tif_dir} -> subdir0 -> tif,tif,tif,tif
    #                 subdir1 -> tif,tif,tif,tif,
    #                    ........
    #                 subdir123 -> tif,tif,tif,tif,
    # So we need to run soax on each subdir with parameter
    if use_subdirs:
        tif_dir_contents = os.listdir(tif_dir)
        subdir_names = [name for name in tif_dir_contents if os.path.isdir(os.path.join(tif_dir,name))]
        subdir_names.sort()

        for params_filename in param_files:
            param_fp = os.path.join(params_dir,params_filename)
            params_name = params_filename[:-len(".txt")]

            sublogging_dir = os.path.join(logging_dir, params_name)
            if not os.path.isdir(sublogging_dir):
                if os.path.exists(sublogging_dir):
                    logger.FAIL("Logging dir {} exists but is not directory. Cannot log output there".format(sublogging_dir))
                else:
                    os.makedirs(sublogging_dir)

            for subdir_name in subdir_names:
                subdir_path = os.path.join(tif_dir,subdir_name)
                snakes_output_dir = os.path.join(output_dir, params_name, subdir_name)

                stdout_fp = os.path.join(sublogging_dir, subdir_name + "_stdout.txt")
                errors_fp = os.path.join(sublogging_dir, subdir_name + "_errors.txt")

                if not os.path.isdir(snakes_output_dir):
                    if os.path.exists(snakes_output_dir):
                        logger.FAIL("Snakes dir {} exists but is not a directory. Cannot output snakes here".format(snakes_output_dir))
                    else:
                        os.makedirs(snakes_output_dir)

                soax_args.append({
                    "batch_soax": batch_soax,
                    "tif_dir": subdir_path,
                    "param_fp": param_fp,
                    "params_name": params_name,
                    "snakes_output_dir": snakes_output_dir,
                    "stdout_fp": stdout_fp,
                    "errors_fp" errors_fp,
                    "logger": logger,
                })
    # If no subdirs, we have
    # {tif_dir} -> tif,tif,tif,tif
    # so we only need to run soax once with each param on the same directory
    else:
        for params_filename in param_files:
            param_fp = os.path.join(params_dir,params_filename)
            params_name = params_filename[:-len(".txt")]
            soxa_args.append({
                "batch_soax": batch_soax,
                "tif_dir": tif_dir,
                "param_fp": param_fp,
                "params_name": params_name,
                "snakes_output_dir": output_dir,
                "stdout_fp": os.path.join(logging_dir, "stdout.txt"),
                "errors_fp" os.path.join(logging_dir, "errors.txt"),
                "logger": logger,
            })

    # logger.log("Creating snake output directories inside {}".format(output_dir))
    # for soax_arg in soax_args:
    #     params_output_dir = soax_arg["params_output_dir"]
    #     logger.log("Directory '{}' created".format(params_output_dir))

    with ThreadPool(workers_num) as pool:
        logger.log("Making future")
        future = pool.map(run_soax, soax_args)
        logger.log("Future finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Try some parameters for snakes')
    parser.add_argument('batch_soax',help="Path to batch_soax executable")
    parser.add_argument('tif_dir',type=readable_dir,help='Directory with tif files to run in soax')
    parser.add_argument('params_dir',type=readable_dir,help='Directory with soax param text files')
    parser.add_argument('output_dir',type=readable_dir,help='Directory to put')
    parser.add_argument('logging_dir', type=readable_dir,help='Directory to write error messages')
    parser.add_argument('--subdirs', default=False, action='store_true',help='If tif_dir has subdirectories of image')
    parser.add_argument('--workers', default=5, type=int, help='Number of batch_soax processes to have running at once')

    args = parser.parse_args()

    run_soax(
        args.batch_soax,
        args.tif_dir,
        args.params_dir,
        args.output_dir,
        args.logging_dir,
        args.subdirs,
        args.workers_num,
    )