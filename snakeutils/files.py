import sys
import os
import numpy as np

def readable_dir(dirpath):
    if not os.path.isdir(dirpath):
        raise argparse.ArgumentTypeError("{} is not a directory".format(dirpath))

    return dirpath

def extract_snakes(snake_file):
    # get past starting params
    count = 0
    while count < 30:
        snake_file.readline()
        count += 1

    snake_dict = {}
    done = False
    lines = [line.strip().split() for line in snake_file]

    line_idx = 0
    snake_name = None
    snake_points = None
    while True:
        # if snake name is none, last iteration just finished a snake
        if snake_name is None:
            line = lines[line_idx]
            #reached junction point section
            if len(line) == 3:
                break

            snake_name = line[0]
            snake_points = []

        line = lines[line_idx]
        # if reached a new label for snake or reached junction section of file
        if len(line) == 1 or len(line) == 3:
            snake_dict[snake_name] = np.array(snake_points)
            snake_name = None
            snake_points = None

            #reached junction section
            if len(line) == 3:
                break
            #reached end of file
            if line_idx >= len(lines):
                break
            if len(line) == 1:
                # skip open/closed #1 #0 line
                line_idx += 1

            continue
        else:
            x= float(line[2])
            y= float(line[3])
            snake_points.append([x,y])

            line_idx += 1
            continue

    snake_arr = []

    # turn dict into array of snakes starting at index zero
    for key in sorted(snake_dict.keys()):
        snake = snake_dict[key]
        snake_arr.append(snake)

    return snake_arr


