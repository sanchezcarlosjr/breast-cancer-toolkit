import uuid

import gradio as gr
import PIL

import breast_cancer_toolkit as bct
import breast_cancer_toolkit.io.assets as assets
import breast_cancer_toolkit.rembg as rembg

theme = gr.themes.Base(
    font=["DM Sans", "ui-sans-serif", "system-ui", "-apple-system"],
).set(
    button_primary_background_fill_dark="rgb(31, 41, 55)",
    button_primary_text_color_dark="rgb(156, 163, 175)",
    button_primary_border_color_dark="rgb(31, 41, 55)",
)

css = """
footer{display:none !important}
.dark  {
    --body-background-fill: rgb(18, 18, 18);
}
.gradio-container {
  border: none !important;
}
"""


def predict(image: PIL.Image):
    if image is None:
        return None
    output = str(assets.external(str(uuid.uuid4()) + ".png"))
    rembg.model(image)[0].save(output)
    return output


with gr.Blocks(
    theme=theme, title=bct.dist_name, css=css, analytics_enabled=False
) as demo:
    gr.Markdown("# breast-cancer-toolkit from MexicanDICOM project.")
    inp = gr.Image(format="png", type="pil")
    out = gr.Image()

    inp.change(fn=predict, inputs=inp, outputs=out)

    demo.queue(default_concurrency_limit=40)

    demo.launch()
