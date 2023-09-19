import gradio as gr

def execute_pipeline(img):
    return [img.convert('L'), {"birads": "2"}]

def launch_server():
    gradio_interface = gr.Interface(
      fn = execute_pipeline,
      title = "UABC Breast Cancer Toolkit",
      description="""
        # UABC Breat Cancer Toolkit
      """,
      inputs = gr.Image(type="pil"),
      outputs = [
         "image",
         "json"
      ]
    )
    gradio_interface.launch()

