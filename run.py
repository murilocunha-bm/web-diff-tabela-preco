#!.venv/bin/python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
#
from app import create_app


app = create_app()


if __name__ == "__main__":
    app.run()
