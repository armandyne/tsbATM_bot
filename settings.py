# -*- coding: utf-8 -*-
import os
from urllib import parse

BOT_TOKEN = os.environ['BOT_TOKEN']
HEROKU_APP_URL = os.environ['HEROKU_APP_URL']

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

DATABASE_NAME = url.path[1:]
DATABASE_USER = url.username
DATABASE_PASSWORD = url.password
DATABASE_HOST = url.hostname
DATABASE_PORT = url.port