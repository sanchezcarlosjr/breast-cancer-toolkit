#!/usr/bin/env python
import logging
import os
import sys

import click
from IPython.core import ultratb
from roboflow import Roboflow

# Fallback to debugger on error
sys.excepthook = ultratb.FormattedTB(mode="Verbose", color_scheme="Linux", call_pdb=1)

# Turn UserWarning messages to errors to find the actual cause
# import warnings
# warnings.simplefilter("error")

_logger = logging.getLogger(__name__)


@click.command()
@click.option("--model_path", type=click.Path(), help="Path to the model.")
@click.option("--model_type", type=str, help="Type of the model.")
def main(model_type: str, model_path: str):
    rf = Roboflow(api_key=os.environ["ROBOFLOW_API_KEY"])
    project = rf.workspace(os.environ["ROBOFLOW_WORKSPACE"]).project(
        os.environ["ROBOFLOW_PROJECT"]
    )
    version = project.version(1)
    version.deploy(model_type=model_type, model_path=model_path)


if __name__ == "__main__":
    main()
