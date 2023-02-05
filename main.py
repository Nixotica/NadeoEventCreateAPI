import copy
import datetime as dt
import os.path
import sys

from selenium import webdriver
from selenium.webdriver import ChromeOptions

import create_event_from_config
from utils.create_competition import *
from utils.forms import *
from utils.map_finder import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_event_from_config.create_event("DeltaBracket24.yaml")
