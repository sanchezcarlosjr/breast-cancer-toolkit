from PIL import Image

from breast_cancer_toolkit import __version__, _logger, setup_logging

__author__ = "sanchezcarlosjr"
__copyright__ = "sanchezcarlosjr"
__license__ = "MIT"

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.

import getpass
import os
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from breast_cancer_toolkit.rembg import Rembg

app = typer.Typer()


@app.command()
def version():
    print(f"breast-cancer-toolkit {__version__}")


@app.command()
def run_demo(
    share: Annotated[bool, typer.Option(help="Share with Gradio servers.")] = False
):
    _logger.info("Starting webapp..")
    from breast_cancer_toolkit.webapp import demo

    demo.launch(share=share)


@app.command()
def rembg(
    file: str,
    model: Annotated[str, typer.Option(help="Model.")] = "rembg_yolov9e-seg.pt",
):
    _logger.info("Removing background...")
    rembg = Rembg(model)
    image = rembg(Image.open(file))[0]
    image.show()
    _logger.info("Prediction...")


@app.command()
def convert(input: str, output: str):
    _logger.info("Converting...")
    img = Image.open(input)
    img.save(output)


def write_systemd_service(
    service_name,
    description,
    exec_start,
    working_directory="/",
    after="network.target",
    restart="on-failure",
    restart_sec=5,
    service_file_dir="/etc/systemd/system",
):
    """
    Create a systemd service unit file.

    Parameters:
    - service_name: Name of the service (e.g., 'my_service')
    - description: Description of the service
    - exec_start: Command to start the service
    - working_directory: Working directory for the service (default is '/')
    - after: Dependencies to start after (default is 'network.target')
    - restart: Restart policy (default is 'on-failure')
    - restart_sec: Delay before restarting (default is 5 seconds)
    - service_file_dir: Directory to place the service file
    (default is '/etc/systemd/system')
    """
    service_file_path = os.path.join(service_file_dir, f"{service_name}.service")
    user = getpass.getuser()  # Get the current user

    service_content = f"""[Unit]
Description={description}
After={after}

[Service]
ExecStart={exec_start}
WorkingDirectory={working_directory}
User={user}
Restart={restart}
RestartSec={restart_sec}
Type=simple

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file_path, "w") as service_file:
            service_file.write(service_content)
        print(f"Service file '{service_file_path}' created successfully.")

        # Reload systemd manager configuration
        os.system("systemctl daemon-reload")

        # Enable the service to start on boot
        os.system(f"systemctl enable {service_name}.service")

        # Start the service
        os.system(f"systemctl start {service_name}.service")

        print(f"Service '{service_name}' started successfully.")

    except Exception as e:
        print(f"An error occurred while creating the service file: {e}")


@app.command()
def create_service(
    working_directory: Annotated[
        str, typer.Option(help="Working directory for the service", default="/")
    ] = "/",
    after: Annotated[
        str, typer.Option(help="Dependencies to start after", default="network.target")
    ] = "network.target",
    restart: Annotated[
        str, typer.Option(help="Restart policy", default="on-failure")
    ] = "on-failure",
    service_file_dir: Annotated[
        str,
        typer.Option(
            help="Directory to place the service file", default="/etc/systemd/system"
        ),
    ] = "/etc/systemd/system",
):
    """
    Command to create a systemd service unit file.
    """
    # Suggested exec_start commands
    suggestions = [
        f"conda run -n {__name__} {__name__} run_webservice",
        f"{__name__} run_webservice",
    ]

    print("Here are some suggestions for the ExecStart command:")
    for suggestion in suggestions:
        print(f"  - {suggestion}")

    exec_start = typer.prompt(
        "Please enter the ExecStart command", default=suggestions[0]
    )

    write_systemd_service(
        "breast-cancer-toolkit",
        "Add a short description here!",
        exec_start,
        working_directory,
        after,
        restart,
        5,
        service_file_dir,
    )


def main(
    verbose: Optional[int] = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Increase verbosity by augmenting the count of 'v's, and enhance "
        "the total number of messages.",
    )
):
    setup_logging(verbose * 10)
    app()


def run():
    app()


if __name__ == "__main__":
    typer.run(app)
