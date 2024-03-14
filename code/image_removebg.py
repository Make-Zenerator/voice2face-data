from rembg import remove
from PIL import Image

input = Image.open('/root/project/voice2face-data/file/face_detected_256x256.png') # load image
output = remove(input) # remove background
output.save('/root/project/voice2face-data/file/rembg_256x256.png') # save image
