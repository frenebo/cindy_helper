import argparse
import os
from PIL import Image
import numpy as np

from .snakeutils.logger import PrintLogger
from .snakeutils.tifimage import get_single_tiff_info

def readable_dir(dirpath):
    if not os.path.isdir(dirpath):
        raise argparse.ArgumentTypeError("{} is not a directory".format(dirpath))

    return dirpath

def tiff_file_or_dir(target_path):
    try:
        dir_path = readable_dir(target_path)
        dir_contents = os.listdir(dir_path)
        tiff_filenames = [filename for filename in dir_contents if filename.endswith(".tif")]
        tiff_filepaths = [os.path.join(target_path,tiff_fn) for tiff_fn in tiff_filenames]
        return tiff_filepaths
    # bad idea why did i do it this way
    except argparse.ArgumentTypeError:
        if not target_path.endswith(".tif"):
            raise argparse.ArgumentTypeError("{} is not a directory or tiff file".format(target_path))

        if not os.path.exists(target_path):
            raise argparse.ArgumentTypeError("{} does not exist".format(target_path))

        return [target_path]

def readable_dir(dirpath):
    if not os.path.isdir(dirpath):
        raise argparse.ArgumentTypeError("{} is not a directory".format(dirpath))

    return dirpath

def tiff_info(tiff_paths,logger=PrintLogger):
    for tiff_path in tiff_paths:
        data = Image.open(tiff_path)
        shape = data.size
        stack_height = getattr(data, "n_frames", 1)
        arr = np.array(data)
        dtype = str(arr.dtype)
        min_val = arr.min()
        max_val = arr.max()
        avg = np.average(arr)

        logger.log("{}:".format(tiff_path))
        logger.success("   DIMENSIONS: XY shape: {}, Number of tiff n_frames (Z): {}".format(shape,stack_height))
        logger.success("   TIFF INFO: pixel dtype: {}, with min: {} and max: {}. Image average value is: {}".format(dtype, min_val, max_val, avg))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get info from tiff file or directory of tiff files')
    parser.add_argument('target',type=tiff_file_or_dir,help="TIFF file or directory of tiff files")

    args = parser.parse_args()

    tiff_info(args.target)