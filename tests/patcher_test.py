from PIL import Image

from breast_cancer_toolkit.io.DicomImagePlugin import register_dicom_plugin

register_dicom_plugin()

# Open a DICOM file
img = Image.open(
    "/home/cest/Workspace/breast-cancer-toolkit/data/raw/datasets/hge/train/x.dcm"
)

# Display the image
img.show()
