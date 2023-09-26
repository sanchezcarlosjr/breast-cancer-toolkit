import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from PIL import Image
import numpy as np
import pydicom
import re
import tempfile
import tensorflow_io as tfio
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt



class ImageReader:
    def __init__(self, img_path):
        self.img_path = img_path

    def plot(self):
        plt.figure()
        plt.imshow(self.normalize(), cmap='gray')
        plt.title(f'{os.path.basename(self.img_path)}')
        plt.axis('off')
        plt.show() 

    def numpy(self):
        return self.image.numpy()
    
    def normalize(self):
        return self.image

    def get_image(self):
        return self.image


# https://www.tensorflow.org/io/tutorials/dicom
class Dicom(ImageReader):
    def read_tag(self, tag_id):
        return tfio.image.decode_dicom_data(self.image_bytes,tag_id)
    def normalize(self):
        return np.squeeze(self.image.numpy())
    def numpy(self):
        return self.normalize()
    def read(self):
        image_bytes = tf.io.read_file(self.img_path)
        self.image = tfio.image.decode_dicom_image(image_bytes, dtype=tf.uint16)
        return self


class ClassicImage(ImageReader):
    def read(self):
        image_file = tf.io.read_file(self.img_path)
        self.image = tf.io.decode_image(image_file)
        return self

class Tiff(ImageReader):
    def read(self):
        image_array = cv2.imread(self.img_path, cv2.IMREAD_UNCHANGED)
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        self.image = tf.convert_to_tensor(image_array)
        return self


class NPYFile(ImageReader):
    def read(self):
        self.image = tf.convert_to_tensor(np.load(self.img_path))
        return self

class LJPEG(ImageReader):
    def read(self):
        return self

class Url(ImageReader):
    def read(self):
        response = requests.get(self.img_path)
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file.write(response.content)
        return read(file.name)

class FileExtensionError(Exception):
    pass

def tokenize(string):
    match = re.match(r'(.+(\.(?P<Dicom>dcm)|(?P<ClassicImage>png|jpg|jpeg|bmp|gif)|(?P<Tiff>tiff|tif)|(?P<LJPEG>ljpeg)|(?P<NPYFile>npy)))|(?P<Url>https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*))', string, re.IGNORECASE)
    if not match:
        raise FileExtensionError("Pattern did not match the input string")
    for token,symbols in match.groupdict().items():
        if symbols:
            return globals()[token](string)

def read(string):
    reader = tokenize(string)
    return reader.read()


def pipeline():
    def predict(path):
        reader = read(path)
        return reader.numpy()
    return predict

