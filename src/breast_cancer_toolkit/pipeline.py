from PIL import Image
import numpy as np
import pydicom
import re
import tempfile


class ImageReader:
    def __init__(self, img_path):
        self.img_path = img_path


# https://github.com/pydicom/contrib-pydicom/tree/master
class Dicom(ImageReader):
    def get_LUT_value(self, data, window, level):
        """Apply the RGB Look-Up Table for the given data and window/level value."""
        return np.piecewise(data,
                            [data <= (level - 0.5 - (window - 1) / 2),
                             data > (level - 0.5 + (window - 1) / 2)],
                            [0, 255, lambda data: ((data - (level - 0.5)) /
                                                   (window - 1) + 0.5) * (255 - 0)])

    def read(self):
        ds = pydicom.dcmread(self.img_path)

        if 'PixelData' not in ds:
            raise TypeError("Cannot show image -- DICOM dataset does not have pixel data")

        if ('WindowWidth' not in ds) or ('WindowCenter' not in ds):
            bits = ds.BitsAllocated
            samples = ds.SamplesPerPixel
            if bits == 8 and samples == 1:
                mode = "L"
            elif bits == 8 and samples == 3:
                mode = "RGB"
            elif bits == 16:
                mode = "I;16"
            else:
                raise TypeError("Don't know PIL mode for %d BitsAllocated and %d SamplesPerPixel" % (bits, samples))

            size = (ds.Columns, ds.Rows)  # PIL size = (width, height)
            im = Image.frombuffer(mode, size, ds.PixelData, "raw", mode, 0, 1)
        else:
            ew = ds['WindowWidth']
            ec = ds['WindowCenter']
            ww = int(ew.value[0] if ew.VM > 1 else ew.value)
            wc = int(ec.value[0] if ec.VM > 1 else ec.value)
            image = self.get_LUT_value(ds.pixel_array, ww, wc)
            im = Image.fromarray(image).convert('L')

        return im


class ClassicImage(ImageReader):
    def read(self):
        return Image.open(self.img_path)

class NPYFile(ImageReader):
    def read(self):
        return Image.fromarray(np.load(self.img_path))

class LJPEG(ImageReader):
    def read(self):
        return

class Url(ImageReader):
    def read(self):
        response = requests.get(self.img_path)
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file.write(response.content)
        return read(file.name)

class FileExtensionError(Exception):
    pass

def tokenize(string):
    match = re.match(r'(.+(\.(?P<Dicom>dcm)|(?P<ClassicImage>tiff|tff|png|jpg|tif)|(?P<LJPEG>ljpeg)|(?P<NPYFile>npy)))|(?P<Url>https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*))', string, re.IGNORECASE)
    if not match:
        raise FileExtensionError("Pattern did not match the input string")
    for token,symbols in match.groupdict().items():
        if symbols:
            return globals()[token](string)

def read(string):
    reader = tokenize(string)
    image = reader.read()
    return image


def pipeline():
    def predict(path):
        image = read(path)
        return image
    return predict

