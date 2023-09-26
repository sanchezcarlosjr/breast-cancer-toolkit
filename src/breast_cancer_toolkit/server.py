import gradio as gr
from breast_cancer_toolkit.pipeline import pipeline
from random import random, sample
import numpy as np
import glob

def softmax_stable(x):
    return(np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

def execute_pipeline(predict):
    def fn(file):
        image = predict(file.name)
        predictions = softmax_stable([random(), random(), random(), random()])
        return [image, {f'birads {i}': predictions[i] for i in range(4)}]
    return fn

def launch_server():
    files = [*glob.glob("**/*.dcm", recursive=True),
             *glob.glob("**/*.tif", recursive=True),
             *glob.glob("**/*.tiff", recursive=True),
             *glob.glob("**/*.npy", recursive=True), 
             *glob.glob("**/*.png", recursive=True), 
             *glob.glob("**/*.jpg", recursive=True), 
             *glob.glob("**/*.jpeg", recursive=True)
            ]
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
      ],
      examples=sample(files, min(5, len(files)))
    )
    gradio_interface.launch(share=True)

