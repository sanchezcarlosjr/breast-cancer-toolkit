import argparse
import logging
import sys

from breast_cancer_toolkit import __version__
from breast_cancer_toolkit.server import launch_server
from breast_cancer_toolkit.pipeline import read

__author__ = "sanchezcarlosjr"
__copyright__ = "sanchezcarlosjr"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


class LocalViewerAction(argparse.Action):
    def __call__(self, parser, namespace, file, option_string=None):
        _logger.debug("Starting...")
        reader = read(file.name)
        reader.plot()
        _logger.debug("Ending...")


class WebServerLauncherAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        _logger.debug("Starting...")
        launch_server()
        _logger.debug("Ending...")

def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="breast-cancer-toolkit")
    parser.add_argument(
        "--version",
        action="version",
        version=f"breast-cancer-toolkit {__version__}",
    )
    parser.add_argument(
            "-s",
            "--server",
            help="launch webserver",
            nargs='?',
            default='7860',
            action=WebServerLauncherAction
    )
    parser.add_argument(
            "-lv",
            "--lview",
            dest="infile",
            help="file paths",
            nargs="?",
            action=LocalViewerAction,
            type=argparse.FileType('r'),
            default=sys.stdin
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m breast_cancer_toolkit.skeleton 42
    #
    run()
