from curl_cffi import requests
from curl_cffi.requests import Response
from curl_cffi.requests.exceptions import (
    RequestException,
    HTTPError,
    ConnectionError,
    Timeout,
    ProxyError,
    SSLError,
)

from bs4 import BeautifulSoup
from pprint import pprint
from rich import print

import pandas as pd
from pandas import DataFrame