from breast_cancer_toolkit.image_reader import read
from breast_cancer_toolkit.image_denoiser import ClassicDenoiser

def pipeline():
    denoiser = ClassicDenoiser()
    def predict(path):
        reader = read(path)
        return denoiser(reader.numpy())
    return predict

