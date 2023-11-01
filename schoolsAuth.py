import requests
from bs4 import BeautifulSoup
import func_parse as fp
import constants as const
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="schools_logs",
    filemode="w",
    format="%(acstime)s %(levelname)s %(message)s",
)

session = requests.Session()


hre = fp.get_dairy_page(session=session)
print(f"HREF :{hre}")
