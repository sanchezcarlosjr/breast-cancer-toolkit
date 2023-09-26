import gradio as gr
from breast_cancer_toolkit.pipeline import pipeline
from random import random
import numpy as np

def softmax_stable(x):
    return(np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

def execute_pipeline(predict):
    def fn(file):
        image = predict(file.name)
        predictions = softmax_stable([random(), random(), random(), random()])
        return [image, {f'birads {i}': predictions[i] for i in range(4)}]
    return fn

def launch_server():
    gradio_interface = gr.Interface(
      fn = execute_pipeline(pipeline()),
      title = "UABC Breast Cancer Toolkit",
      description="""
        # Analyze mammographies from different image formats.
      """,
      inputs = gr.File(file_types=['.png', '.jpg', '.ljpeg', '.tiff', '.tff' '.tif', '.dcm', '.npy']),
      outputs = [
         "image",
         gr.Label(num_top_classes=4)
      ]
    )
    gradio_interface.launch()

