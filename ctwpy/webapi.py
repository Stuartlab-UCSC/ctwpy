"""
Functions for interacting with the UCSC Cell Atlas API.
"""
import requests
from bs4 import BeautifulSoup
from ctwpy.io import read_json
from requests_toolbelt.multipart import encoder
import os


def read_credentials(creds_path):
    return read_json(creds_path)


def upload(ctw_path, credentials, url_base="http://localhost:5555/"):
    assert credentials['email'] is not None and credentials["password"] is not None
    print("Attempting login")
    login_url = url_base + "user/sign-in"
    session = requests.Session()
    r = session.post(login_url, data=credentials)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find('input', {'name': 'csrf_token'})['value']

    credentials.update({"csrf_token": token})
    r = session.post(login_url, data=credentials)
    print("Successful login...")
    worksheet_name = os.path.basename(ctw_path.split(".ctw.")[0])
    upload_url = url_base + "user/worksheet/" + worksheet_name
    form = encoder.MultipartEncoder({
        "documents": (os.path.basename(ctw_path), open(ctw_path, "rb"), "application/octet-stream"),
        "composite": "NONE",
    })
    print(form.content_type)
    headers = {"Prefer": "respond-async", "Content-Type": form.content_type}

    session.post(upload_url, headers=headers, data=form)