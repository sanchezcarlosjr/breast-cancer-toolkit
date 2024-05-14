import os
import sys
import math
import logging
from pathlib import Path

import numpy as np
import scipy as sp
import sklearn
#import statsmodels.api as sm
#from statsmodels.formula.api import ols
import pystow

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
sns.set_context("poster")
sns.set(rc={"figure.figsize": (16, 9.)})
sns.set_style("whitegrid")

import pandas as pd
pd.set_option("display.max_rows", 120)
pd.set_option("display.max_columns", 120)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)