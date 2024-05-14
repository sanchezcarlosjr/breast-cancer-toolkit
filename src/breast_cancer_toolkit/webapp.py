import gradio as gr
from breast_cancer_toolkit

theme = gr.themes.Base(font=["DM Sans", 'ui-sans-serif', 'system-ui', '-apple-system'], ).set(
    body_background_fill_dark='transparent', border_color_primary_dark='transparent',
    button_primary_background_fill_dark='rgb(31, 41, 55)', button_primary_text_color_dark='rgb(156, 163, 175)',
    button_primary_border_color_dark='rgb(31, 41, 55)')

css = """
footer{display:none !important}
.dark  {
    --body-background-fill: rgb(18, 18, 18);
}
.gradio-container {
  border: none !important;
}
"""


def predict(x):
    return x


with gr.Blocks(theme=theme, title="breast_cancer_toolkit", css=css, analytics_enabled=False) as demo:
    gr.Markdown("# Greetings from breast_cancer_toolkit!")
    inp = gr.Textbox(placeholder="What is your name?")
    out = gr.Textbox()

    inp.change(fn=predict, inputs=inp, outputs=out)

    demo.queue(default_concurrency_limit=40)
