import cv2
import argparse
import os
from collections import Counter

def predict_age(face):
    '''
    Function to predict age from a face image.
    
    Args:
        face: Image to predict age from.

    Returns:
        age: Predicted age group index.
    '''
    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    ageNet.setInput(blob)
    agePreds = ageNet.forward()
    age = agePreds[0].argmax()
    return age

def count_and_print_age(folder_path):
    '''
    Function to count and print the most common age group from images in a folder.
    
    Args:
        folder_path: Path to the folder containing images.
    '''
    age_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            frame = cv2.imread(image_path)
            if frame is not None:
                age = predict_age(frame)
                age_list.append(age)

    if age_list:
        most_common_age = Counter(age_list).most_common(1)[0][0]
        print("Most common age group:", ageList[most_common_age])
    else:
        print("No images detected in the folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', required=True, help='Path to the folder containing images.')
    args = parser.parse_args()

    ageProto = "weights/age_deploy.prototxt"
    ageModel = "weights/age_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

    ageNet = cv2.dnn.readNet(ageModel, ageProto)

    count_and_print_age(args.folder)
