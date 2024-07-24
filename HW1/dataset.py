import os
import cv2
import glob
import numpy as np


def load_data_small():
    """
        This function loads images form the path: 'data/data_small' and return the training
        and testing dataset. The dataset is a list of tuples where the first element is the 
        numpy array of shape (m, n) representing the image the second element is its 
        classification (1 or 0).

        Parameters:
            None

        Returns:
            dataset: The first and second element represents the training and testing dataset respectively
    """

    # Begin your code (Part 1-1)
    """
    explain part 1-1 code
    For each folder, create a variable `path` to store the directory.
    Use a for loop to go through every file in the folder. (`for file in os.listdir(path)`)
    For each file in the folder, use `cv2.imread` to create the numpy array for the image
    and add it to the dataset list.
    """
    # raise NotImplementedError("To be implemented")
    dataset = []
    trainData  = []
    testData = []
    
    # create list for test/face
    path = "data/data_small/test/face"
    for file in os.listdir(path):
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            temp = (img, 1)
            testData.append(temp)

    # create list for test/non-face
    path = "data/data_small/test/non-face"
    for file in os.listdir(path):
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            temp = (img, 0)
            testData.append(temp)

    # create list for train/face
    path = "data/data_small/train/face"
    for file in os.listdir(path):
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            temp = (img, 1)
            trainData.append(temp)

    # create list for train/non-face
    path = "data/data_small/train/non-face"
    for file in os.listdir(path):
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            temp = (img, 0)
            trainData.append(temp)
    dataset = [trainData, testData]
    # End your code (Part 1-1)
    
    return dataset


def load_data_FDDB(data_idx="01"):
    """
        This function generates the training and testing dataset  form the path: 'data/data_small'.
        The dataset is a list of tuples where the first element is the numpy array of shape (m, n)
        representing the image the second element is its classification (1 or 0).
        
        In the following, there are 4 main steps:
        1. Read the .txt file
        2. Crop the faces using the ground truth label in the .txt file
        3. Random crop the non-faces region
        4. Split the dataset into training dataset and testing dataset
        
        Parameters:
            data_idx: the data index string of the .txt file

        Returns:
            train_dataset: the training dataset
            test_dataset: the testing dataset
    """

    with open("data/data_FDDB/FDDB-folds/FDDB-fold-{}-ellipseList.txt".format(data_idx)) as file:
        line_list = [line.rstrip() for line in file]

    # Set random seed for reproducing same image croping results
    np.random.seed(0)

    face_dataset, nonface_dataset = [], []
    line_idx = 0

    # Iterate through the .txt file
    # The detail .txt file structure can be seen in the README at https://vis-www.cs.umass.edu/fddb/
    while line_idx < len(line_list):
        img_gray = cv2.imread(os.path.join("data/data_FDDB", line_list[line_idx] + ".jpg"), cv2.IMREAD_GRAYSCALE)
        num_faces = int(line_list[line_idx + 1])

        # Crop face region using the ground truth label
        face_box_list = []
        for i in range(num_faces):
            # Here, each face is denoted by:
            # <major_axis_radius minor_axis_radius angle center_x center_y 1>.
            coord = [int(float(j)) for j in line_list[line_idx + 2 + i].split()]
            x, y = coord[3] - coord[1], coord[4] - coord[0]            
            w, h = 2 * coord[1], 2 * coord[0]

            left_top = (max(x, 0), max(y, 0))
            right_bottom = (min(x + w, img_gray.shape[1]), min(y + h, img_gray.shape[0]))
            face_box_list.append([left_top, right_bottom])
            # cv2.rectangle(img_gray, left_top, right_bottom, (0, 255, 0), 2)

            img_crop = img_gray[left_top[1]:right_bottom[1], left_top[0]:right_bottom[0]].copy()
            face_dataset.append((cv2.resize(img_crop, (19, 19)), 1))

        line_idx += num_faces + 2

        # Random crop N non-face region
        # Here we set N equal to the number of faces to generate a balanced dataset
        # Note that we have alreadly save the bounding box of faces into `face_box_list`, you can utilize it for non-face region cropping
        for i in range(num_faces):
            # Begin your code (Part 1-2)
            """
            explain part 1-2 code
            `img_gray.shape` return the height and width of the image.
            To random crop non-face region, we use `np.random.randint` to generate random number as x1 and y1's coordinate.
            x1+19 and y1+19 become the coordinat of x2 and y2.
            But we don't know whether the region contains face in it, so we use a for loop to go through all faces in `face_box_list`
            to check whether there is face in the region we create. If yes, we don't use this region and create another one.
            Otherwise, the region is valid and we can break the while loop to generate the next non-face region.
            """
            # raise NotImplementedError("To be implemented")
            h, w = img_gray.shape
            while True:
                # coordinate for non face box
                x1 = np.random.randint(0, w-19)
                y1 = np.random.randint(0, h-19)
                x2 = x1+19
                y2 = y1+19

                # check if the box includes face
                valid = True
                for left_top, right_bottom in face_box_list:
                    # the box includes face, break, find another box
                    if(x1<right_bottom[0] and x2>left_top[0] and y1<right_bottom[1] and y2>left_top[1]):
                        valid = False
                        break
                if valid:
                    break
            
            img_crop = img_gray[y1:y2, x1:x2].copy()
            
            # End your code (Part 1-2)

            nonface_dataset.append((cv2.resize(img_crop, (19, 19)), 0))

        # cv2.imshow("windows", img_gray)
        # cv2.waitKey(0)

    # train test split
    num_face_data, num_nonface_data = len(face_dataset), len(nonface_dataset)
    SPLIT_RATIO = 0.7

    train_dataset = face_dataset[:int(SPLIT_RATIO * num_face_data)] + nonface_dataset[:int(SPLIT_RATIO * num_nonface_data)]
    test_dataset = face_dataset[int(SPLIT_RATIO * num_face_data):] + nonface_dataset[int(SPLIT_RATIO * num_nonface_data):]

    return train_dataset, test_dataset


def create_dataset(data_type):
    if data_type == "small":
        return load_data_small()
    else:
        return load_data_FDDB()
