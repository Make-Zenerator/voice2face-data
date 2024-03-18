import cv2
import math
import argparse
import os

def highlightFace(net, frame, conf_threshold=0.7):
    '''
    Function to detect faces in a frame using a pre-trained deep learning model.
    
    Args:
        net: Pre-trained deep learning model.
        frame: Input frame.
        conf_threshold: Confidence threshold for face detection.

    Returns:
        frameOpencvDnn: Copy of the input frame with face rectangles drawn.
        faceInfo: List containing information about detected faces (bbox, center, width, height).
    '''
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceInfo = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            w = x2 - x1
            h = y2 - y1
            faceInfo.append({'bbox': (x1, y1, x2, y2), 'center': (cx, cy), 'width': w, 'height': h})
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceInfo

def save_frame(frame, output_folder, folder_name, gender, age, center):
    '''
    Function to save a frame with a specific filename format.
    
    Args:
        frame: Frame to be saved.
        output_folder: Folder where frames will be saved.
        frame_count: Frame count.
        folder_name: Name of the folder containing the video.
        gender: Gender of the detected face.
        age: Age range of the detected face.
        center: Center coordinates of the detected face bbox.
    '''

    age_List_s = [0,4,8,15,25,38,48,60]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    subfolder_path = os.path.join(output_folder, folder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    height, width = frame.shape[:2]
    height = round(center[0]/height,6)
    width = round(center[1]/width,6)
    cv2.imwrite(os.path.join(subfolder_path, f"{gender}_{age_List_s[age]}_{height}_{width}.jpg"), frame)

    print("save: ",os.path.join(subfolder_path, f"{gender}_{age_List_s[age]}_{height}_{width}.jpg"))

parser = argparse.ArgumentParser()
parser.add_argument('--folder', default='/home/carbox/Desktop/git/dataset/video')
parser.add_argument('--output_folder', default='frame')
parser.add_argument('--capture_interval', type=int, default=50)  # Adjusted frame interval for capturing

args = parser.parse_args()

faceProto = "weights/opencv_face_detector.pbtxt"
faceModel = "weights/opencv_face_detector_uint8.pb"
ageProto = "weights/age_deploy.prototxt"
ageModel = "weights/age_net.caffemodel"
genderProto = "weights/gender_deploy.prototxt"
genderModel = "weights/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

for root, dirs, files in os.walk(args.folder):
    for folder_name in dirs:
        folder_path = os.path.join(root, folder_name)
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                video_path = os.path.join(folder_path, filename)
                break
        else:
            continue

        video = cv2.VideoCapture(video_path)
        padding = 20
        frame_count = 0
        count = 0
        while True:  # Infinite loop for processing each frame
            hasFrame, frame = video.read()
            if not hasFrame:
                break
            if frame_count % args.capture_interval != 0:
                frame_count +=1
                continue

            if count > 4: 
                break

            resultImg, faceInfo = highlightFace(faceNet, frame)
            if faceInfo:  # Process only if faces are detected
                for faceData in faceInfo:
                    bbox = faceData['bbox']
                    center = faceData['center']
                    width = faceData['width']
                    height = faceData['height']
                    
                    face = frame[max(0, bbox[1] - padding): min(bbox[3] + padding, frame.shape[0] - 1),
                                 max(0, bbox[0] - padding): min(bbox[2] + padding, frame.shape[1] - 1)]
                    
                    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                    genderNet.setInput(blob)
                    genderPreds = genderNet.forward()
                    gender = genderList[genderPreds[0].argmax()]

                    ageNet.setInput(blob)
                    agePreds = ageNet.forward()
                    age = agePreds[0].argmax()
                    # age = ageList[agePreds[0].argmax()]

                    # cv2.putText(resultImg, f'{gender}, {age}', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
                    # cv2.putText(resultImg, f'Center: ({center[0]}, {center[1]})', (bbox[0], bbox[1] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
                    # cv2.putText(resultImg, f'Box: ({bbox[0]}, {bbox[1]}, {width}, {height})', (bbox[0], bbox[1] - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
                    
                    # Capture and save frames at specified intervals
                    save_frame(frame, args.output_folder, folder_name, gender, age, center)
                    count +=1
                        
            
            frame_count += 1
            
        
        video.release()
        cv2.destroyAllWindows()