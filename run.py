import sys

path = '/home/juanlinares821/mysite/community_garden'
if path not in sys.path:
   sys.path.append(path)

import os
from dotenv import load_dotenv
dotenv_path = os.path.join('/home/juanlinares821/mysite', '.env')  # adjust as appropriate
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from __init__ import app as application