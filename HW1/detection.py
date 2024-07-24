import os
from unittest import result
import cv2
import utils
import numpy as np
import matplotlib.pyplot as plt
import adaboost


def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:A
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
    explain part 4 code
    Open the .txt file in datapath and split it into a string list `line_list`.
    In the .txt file, the first line of each image is the file name and the number of face, `n_face`.
    In the following `n_face` lines, each line has four numbers represent the face's x, y, width, hight.
    Go through these faces and use `clf` to detect them.
    If `clf` says that this is a face, then draw a green box on it.
    Otherwise, draw a red box on it.
    """
    # raise NotImplementedError("To be implemented")
    
    # read file
    with open(dataPath, "r") as file:
        line_list = [line.rstrip() for line in file]

    line_idx = 0
    while line_idx < len(line_list):
        # read first line in each image and load image in grayscale
        img_name = line_list[line_idx].split()[0]
        n_face = int(line_list[line_idx].split()[1])
        img = cv2.imread(os.path.join("data/detect", img_name))
        img_gray = cv2.imread(os.path.join("data/detect", img_name), cv2.IMREAD_GRAYSCALE)
        line_idx+=1
        # go through each face
        for i in range(n_face):
            # read information of each face
            cur_line = line_idx+i
            coord = [int(float(j)) for j in line_list[cur_line].split()]
            left_top = (coord[0], coord[1])
            sz = coord[2]

            # resize and convert it to 19*19 gray scale
            img_crop = img_gray[left_top[1]:left_top[1]+sz, left_top[0]:left_top[0]+sz].copy()
            img_resize = cv2.resize(img_crop, (19, 19))

            # detect face
            if clf.classify(img_resize):
                # is face, draw green box
                cv2.rectangle(img, (coord[0], coord[1]), (coord[0]+sz, coord[1]+sz), (0, 255, 0), thickness=3)

            else:
                # non face, draw red box
                cv2.rectangle(img, (coord[0], coord[1]), (coord[0]+sz, coord[1]+sz), (0, 0, 255), thickness=3)
        
        img_result = img_name.split('.')[0] + "_result.jpg"
        cv2.imwrite(os.path.join("data/detect", img_result), img)
        # cv2.imshow("Image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()        
        line_idx+=n_face

        
    # End your code (Part 4)
