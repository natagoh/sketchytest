"""Split the SIGNS dataset into train/val/test and resize images to 64x64.

The SIGNS dataset comes into the following format:
    train_signs/
        0_IMG_5864.jpg
        ...
    test_signs/
        0_IMG_5942.jpg
        ...

Original images have size (3024, 3024).
Resizing to (64, 64) reduces the dataset size from 1.16 GB to 4.7 MB, and loading smaller images
makes training faster.

We already have a test set created, so we only need to split "train_signs" into train and val sets.
Because we don't have a lot of images and we want that the statistics on the val set be as
representative as possible, we'll take 20% of "train_signs" as val set.
"""

import argparse
import random
import os
import platform

from PIL import Image
from tqdm import tqdm

SIZE = 64

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', default='data/SKETCHES', help="Directory with the SIGNS dataset")
parser.add_argument('--output_dir', default='data/64x64_SKETCHES', help="Where to write the new data")


def resize_and_save(filename, output_dir, new_name, size=SIZE):
    """Resize the image contained in `filename` and save it to the `output_dir`"""
    image = Image.open(filename)
    # Use bilinear interpolation instead of the default "nearest neighbor" method
    image = image.resize((size, size), Image.BILINEAR)
    image.save(os.path.join(output_dir, new_name))

# extract the classes from the data
# params: directory of data with separate folders for each class
# output: list of classes
def extract_classes(data_dir):
    classes = []
    for item in os.listdir(data_dir):
        if item != "filelist.txt":
            classes.append(item)

    return classes

# extracts images from individual folders and compiles into one folder
def compile_images(data_dir, classes, dst_dir):
    for clas in classes:
        curr_dir = os.path.join(data_dir, clas)
        for f in os.listdir(curr_dir):
            if (f.endswith('.png')):
                if platform.system() == 'Windows':
                    src = os.path.abspath(curr_dir) + '\\' + f
                else:
                    src = os.path.abspath(curr_dir) + '/' + f

                num = f.split(".")[0]
                new_name = clas + "_" + num + ".png"
                resize_and_save(src, dst_dir, new_name)
        print('done renaming imgs in class: ', clas)


if __name__ == '__main__':
    args = parser.parse_args()

    assert os.path.isdir(args.data_dir), "Couldn't find the dataset at {}".format(args.data_dir)
    # Define the data directories
    #train_data_dir = os.path.join(args.data_dir, 'train_signs')
    #test_data_dir = os.path.join(args.data_dir, 'test_signs')
    #print(train_data_dir)

    # extract list of classes
    classes = extract_classes(args.data_dir)

    # rename images (append classification to filename)
    par_dir = os.path.abspath(os.path.join(args.data_dir, os.pardir))
    dst_data_dir = os.path.join(par_dir, '64x64_SKETCHES')
    if not os.path.exists(dst_data_dir):
        os.makedirs(dst_data_dir)
    compile_images(args.data_dir, classes, os.path.abspath(dst_data_dir))

    '''

    # Get the filenames in each directory (train and test)
    filenames = os.listdir(train_data_dir)
    filenames = [os.path.join(train_data_dir, f) for f in filenames if f.endswith('.jpg')]

    test_filenames = os.listdir(test_data_dir)
    test_filenames = [os.path.join(test_data_dir, f) for f in test_filenames if f.endswith('.jpg')]

    # Split the images in 'train_signs' into 80% train and 20% val
    # Make sure to always shuffle with a fixed seed so that the split is reproducible
    random.seed(230)
    filenames.sort()
    random.shuffle(filenames)

    split = int(0.8 * len(filenames))
    train_filenames = filenames[:split]
    val_filenames = filenames[split:]

    filenames = {'train': train_filenames,
                 'val': val_filenames,
                 'test': test_filenames}

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    else:
        print("Warning: output dir {} already exists".format(args.output_dir))

    # Preprocess train, val and test
    for split in ['train', 'val', 'test']:
        output_dir_split = os.path.join(args.output_dir, '{}_signs'.format(split))
        if not os.path.exists(output_dir_split):
            os.mkdir(output_dir_split)
        else:
            print("Warning: dir {} already exists".format(output_dir_split))

        print("Processing {} data, saving preprocessed data to {}".format(split, output_dir_split))
        for filename in tqdm(filenames[split]):
            resize_and_save(filename, output_dir_split, size=SIZE)

    print("Done building dataset")
    '''
