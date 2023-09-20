import gradio as gr
from breast_cancer_toolkit.pipeline import read

def execute_pipeline(predict):
    def fn(file):
        image = read(file.name)
        return [image, {"birads": ""}]
    return fn

def launch_server():
    gradio_interface = gr.Interface(
      fn = execute_pipeline(pipeline()),
      title = "UABC Breast Cancer Toolkit",
      description="""
        Analyze mammography
      """,
      inputs = gr.File(file_types=['.png', '.jpg', '.ljpeg', '.tiff', '.tff' '.tif', '.dcm', '.npy']),
      outputs = [
         "image",
         "json"
      ]
    )
    gradio_interface.launch()

