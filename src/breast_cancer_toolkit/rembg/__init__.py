from ultralytics import YOLO

from breast_cancer_toolkit.io.assets import model_path


class Rembg:
    def __init__(self, model):
        self.model = YOLO(model_path(model))

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)
