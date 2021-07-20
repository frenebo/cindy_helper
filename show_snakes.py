import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from snakeutils.files import extract_snakes, readable_dir
import argparse

def make_snake_images_and_save(dir_name,image_dir_name,image_width,image_height,colorful):
    filenames = os.listdir(dir_name)
    snake_filenames = [filename for filename in filenames if filename.endswith(".txt")]
    snake_filenames.sort()
    for snake_filename in snake_filenames:
        fp = os.path.join(dir_name,snake_filename)

        with open(fp, "r") as snake_file:
            print("Showing snakes for {}".format(fp))
            snakes = extract_snakes(snake_file)
            for snake_idx, snake_pts in enumerate(snakes):
                snake_pts = np.array(snake_pts)

                x,y = snake_pts.T[:2]

                if colorful:
                    plt.plot(x,y)
                else:
                    plt.plot(x,y,'b')

            # some_snakefile.tif => some_snakefile.jpg
            save_img_filename = "".join(snake_filename.split(".")[:-1]) + ".png"
            save_img_fp = os.path.join(image_dir_name,save_img_filename)

            plt.axes().set_aspect('equal', adjustable='box')
            # invert y axis
            plt.axis([0,image_width,image_height,0])
            plt.xlabel("x")
            plt.ylabel("y")
            plt.savefig(save_img_fp)
            # clear figure so we can do the next plot
            plt.clf()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Try some parameters for snakes')
    parser.add_argument('width',type=int,help="Width dimension of frame")
    parser.add_argument('height',type=int,help="Width dimension of frame")
    parser.add_argument('--subdirs', default=False, action='store_true',help='If we should make snakes for subdirectories in snake_dir and output in subdirectories in image_dir')
    parser.add_argument('--subsubdirs', defaul=False, action='store_true',help='If subdirectories in snake_dir are two levels deep')
    parser.add_argument('snake_dir',type=readable_dir,help="Source directory where snake text files are")
    parser.add_argument('image_dir',type=readable_dir,help="Target directory to save graphed snakes")
    parser.add_argument('-c','--colorful', action='store_true',help="Use different colors for each snake")

    args = parser.parse_args()

    dir_name = args.snake_dir
    image_dir = args.image_dir
    image_width = args.width
    image_height = args.height
    colorful = args.colorful

    snake_dirs = []
    image_dirs = []

    if args.subsubdirs:
        subs = [name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name,name))]
        for sub in subs:
            subsubs = [name for name in os.listdir(sub) if os.path.isdir(os.path.join(dir_name,sub,name))]
            image_subdir_path = os.path.join(image_dir,sub)
            os.mkdir(image_subdir_path)
            for subsub in subs:
                snake_subsubdir_path = os.path.join(dir_name,sub,subsub)
                image_subsubdir_path = os.path.join(image_dir,sub,subsub)
                os.mkdir(image_subsubdir_path)
                snake_dirs.append(snake_subsubdir_path)
                image_dirs.append(image_subsubdir_path)
    elif args.subdirs:
        subs = [name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name,name))]
        for sub in subs:
            snake_subdir_path = os.path.join(dir_name,sub)
            image_subdir_path = os.path.join(image_dir,sub)
            os.mkdir(image_subdir_path)
            snake_dirs.append(snake_subdir_path)
            image_dirs.append(image_subdir_path)
    else:
        snake_dirs.append(dir_name)
        image_dirs.append(image_dir)

    for i in len(snake_dirs):
        print("Making snakes for {}, saving in {}".format(snake_dirs[i],image_dirs[i]))
        make_snake_images_and_save(snake_dirs[i],image_dirs[i],image_width,image_height,colorful)
        # make_snake_images_and_save(snake_subdir_path,image_subdir_path,image_width,image_height,colorful)

    # if args.subdirs:
    #     subdir_names = [name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name,name))]

    #     print("Making snakes for snake subdirectories {}".format(subdir_names))

    #     for subdir_name in subdir_names:
    #         snake_subdir_path = os.path.join(dir_name,subdir_name)
    #         image_subdir_path = os.path.join(image_dir,subdir_name)
    #         os.mkdir(image_subdir_path)
    #         make_snake_images_and_save(snake_subdir_path,image_subdir_path,image_width,image_height,colorful)
    # else:
    #     make_snake_images_and_save(dir_name,image_dir,image_width,image_height,colorful)