"""Config for flask app(web-server)"""

import os
from secret import csrf_token_secret

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = csrf_token_secret

UPLOAD_FILE_DIR = 'server/static/files/upload/' 
TEMP_FILE_DIR = 'server/static/files/temp/' 