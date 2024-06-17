import numpy as np
import PIL
import pydicom
from PIL import Image, ImageFile


def get_LUT_value(data, window, level):
    """Apply the RGB Look-Up Table for the given
    data and window/level value."""
    return np.piecewise(
        data,
        [
            data <= (level - 0.5 - (window - 1) / 2),
            data > (level - 0.5 + (window - 1) / 2),
        ],
        [
            0,
            255,
            lambda data: ((data - (level - 0.5)) / (window - 1) + 0.5) * (255 - 0),
        ],
    )


class DICOMImageFile(ImageFile.ImageFile):
    format = "DICOM"
    format_description = "DICOM Image"

    def _open(self):
        # Read the DICOM file using pydicom
        self.ds = pydicom.dcmread(self.fp)

        if ("WindowWidth" not in self.ds) or ("WindowCenter" not in self.ds):
            bits = self.ds.BitsAllocated
            samples = self.ds.SamplesPerPixel
            if bits == 8 and samples == 1:
                self._mode = "L"
            elif bits == 8 and samples == 3:
                self._mode = "RGB"
            elif bits == 16:
                # not sure about this -- PIL source says is 'experimental'
                # and no documentation. Also, should bytes swap depending
                # on endian of file and system??
                self._mode = "I;16"
            else:
                raise TypeError(
                    "Don't know PIL mode for %d BitsAllocated "
                    "and %d SamplesPerPixel" % (bits, samples)
                )

            # PIL size = (width, height)
            self._size = (self.ds.Columns, self.ds.Rows)

            # Recommended to specify all details
            # by http://www.pythonware.com/library/pil/handbook/image.htm
            self.im = PIL.Image.frombuffer(
                self._mode, self._size, self.ds.PixelData, "raw", self._mode, 0, 1
            )

        else:
            ew = self.ds["WindowWidth"]
            ec = self.ds["WindowCenter"]
            ww = int(ew.value[0] if ew.VM > 1 else ew.value)
            wc = int(ec.value[0] if ec.VM > 1 else ec.value)
            image = get_LUT_value(self.ds.pixel_array, ww, wc)
            # Convert mode to L since LUT has only 256 values:
            #   http://www.pythonware.com/library/pil/handbook/image.htm
            self.image = PIL.Image.fromarray(image).convert("L")
            self.im = self.image.im
            self._mode = "L"
            self._size = self.im.size

    def load(self):
        if not self.im:
            self._open()
        self.image.load()


def _save(im, fp, filename):
    raise NotImplementedError("Saving DICOM images is not supported")


def register_dicom_plugin():
    Image.register_open(DICOMImageFile.format, DICOMImageFile)
    Image.register_save(DICOMImageFile.format, _save)
    Image.register_extension(DICOMImageFile.format, ".dcm")
    Image.register_mime(DICOMImageFile.format, "application/dicom")
