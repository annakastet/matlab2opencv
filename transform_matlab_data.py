import re
import os
import numpy as np
from shutil import copyfile

MATLAB_LABELS_DIRECTORY = 'matlabLabels/'
FRAMES_DIRECTORY = 'frames/'
VIDEO_DIRECTORY = 'videos/'
DATASET_DIRECTORY = 'dataset/'
DATASET_IMAGES_DIRECTORY = 'images/'


def change_format(line):
    splitLine = re.split(',\s*', line)
    # get last part of path as MatLab outputs the absolute one
    splitLine[0] = os.path.basename(os.path.normpath(splitLine[0]))
    for i in range(1, len(splitLine)):
        # cut off line when there are no longer rectangles
        if not splitLine[i]:
            return splitLine[:i]
    return splitLine


def read_file(filePath):
    lines = []
    with open(filePath) as file:
        firstLine = True
        for line in file:
            if firstLine:
                # Ignore the first line
                firstLine = False
                continue
            lines.append(change_format(line))
    return lines


def get_number_of_rectangles(line):
    return (len(line) - 1) / 4


def write_to_new_format(csvFileName, lines):
    datasetFileName = csvFileName.split('.')[0]  # remove .csv

    # create DATASET_DIRECTORY
    if not os.path.exists(DATASET_DIRECTORY):
        os.makedirs(DATASET_DIRECTORY)

    # CREATE DATASET_IMAGES_DIRECTORY in DATASET_DIRECTORY
    if not os.path.exists(os.path.join(os.path.join(
        DATASET_DIRECTORY,
        DATASET_IMAGES_DIRECTORY
    ))):
            os.makedirs(os.path.join(os.path.join(
                DATASET_DIRECTORY,
                DATASET_IMAGES_DIRECTORY
            )))

    with open(os.path.join(DATASET_DIRECTORY, datasetFileName), 'w') as file:
        for line in lines:

            # Write to new text file in DATASET_DIRECTORY
            imagePath = os.path.join(
                DATASET_IMAGES_DIRECTORY,
                line[0]
            )
            writeLine = imagePath + ' ' + \
                str(get_number_of_rectangles(line)) + ' '
            rectangles = line[1:]
            # reshape the rectangle matrix from MatLab
            if get_number_of_rectangles(line) > 1:
                rectangles = np.array(rectangles).reshape(
                    4,
                    get_number_of_rectangles(line)) \
                    .transpose().flatten().tolist()
            writeLine += ' '.join(str(e) for e in rectangles) + '\n'

            file.write(writeLine)

            # Copy relevant frames to DATASET_DIRECTORY
            copyfile(
                os.path.join(FRAMES_DIRECTORY, line[0]),
                os.path.join(
                    DATASET_DIRECTORY,
                    imagePath)
            )


for filename in os.listdir(MATLAB_LABELS_DIRECTORY):
    if filename.endswith(".csv"):
        lines = read_file(os.path.join(MATLAB_LABELS_DIRECTORY, filename))
        write_to_new_format(filename, lines)
