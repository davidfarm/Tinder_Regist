import requests, re, string, json, gspread, os, natsort, openpyxl
from selenium import webdriver
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def scan_photos_id(session_name):
    result = re.search(r"/(.+?)/", session_name)
    if result:
        photo_id = result.group(1)
    return photo_id

def scan_name_id(session_name):
    result = re.search(r"(.+?)/", session_name)
    if result:
        name_id = result.group(1)
    return name_id

"""Не используется в Tinder REG"""
def df_to_gsheets(df, spreadsheet_name, worksheet_name):
    """Sending df to google sheets"""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('res/erudite-stratum-316309-a2d8c45cadb8.json', scope)
    gc = gspread.authorize(credentials)
    # Open the Google Sheet
    spreadsheet = gc.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    # Write the DataFrame to the Google Sheet
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def parse_gmail(file):
    """Parse excel to get gmail account"""
    df = pd.read_excel(file)
    row = df.iloc[0]
    email, password, reserve = row

    parsed_df = df.iloc[1:]

    parsed_df.to_excel(file, index=False)
    return email, password, reserve

"""Не используется в Tinder REG"""
def parse_proxy(file):
    df = pd.read_excel(file)
    row = df.iloc[0]
    email, password, reserve = row

    print(email)
    print(password)
    print(reserve)

    parsed_df = df.iloc[1:]

    parsed_df.to_excel(file, index=False)
    return email, password, reserve


def send_cmd(driver, cmd, params={}):
    """Deprecated*, used to send command to browser"""
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')

def parse_line(file):
    """Deprecated*, used to parse first line of text file"""
    with open(file, "r", encoding="UTF-8") as f:
        list = f.readlines()
        line = list[0].strip()

    with open(file, "w", encoding="UTF-8") as f:
        new_list = list[1:]
        content = "".join(new_list)
        f.write(content)

    return line

def create_driver(session, port):
    """create driver"""
    mla_url = f'http://127.0.0.1:{port}/api/v1/profile/start?automation=true&profileId=' + session
    resp = requests.get(mla_url)
    json = resp.json()
    print(json)
    options = webdriver.ChromeOptions()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    driver = webdriver.Remote(command_executor=json['value'], options=options)
    return driver

"""Не используется в Tinder REG"""
def update_profile_proxy(profile_id, proxy_type, proxy_host, proxy_port, proxy_username, proxy_password, port):
    """update profile proxy"""
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "network": {
            "proxy": {
                "type": proxy_type,
                "host": proxy_host,
                "port": proxy_port,
                "username": proxy_username,
                "password": proxy_password
            }
        }
    }
    r = requests.post(url, json.dumps(data), headers=header)
    print(r.status_code)


def update_profile_group(profile_id, port, group_id):
    """Update profile group"""
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "group": group_id,
    }
    r = requests.post(url, json.dumps(data), headers=header)
    print(r.status_code)


def update_profile_geo(profile_id, latitude, longitude, port):
    """update profile geo"""
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id

    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "geolocation": {
            "mode": "ALLOW",
            "fillBasedOnExternalIp": False,
            "lat": latitude,
            "lng": longitude,
            "accuracy": "100"
        },
        "mediaDevices": {
            "mode": "REAL"
        },
    }
    r = requests.post(url, json=data, headers=header)
    print(r.status_code)

def create_profile(session_name, port):
    """create profile"""
    x = {
        "name": f"{session_name}",
        "browser": "mimic",
        "os": "win",
        "enableLock": True,
        "startUrl": f"https://tinder.com/ru"
    }
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    url = f"http://localhost:{port}/api/v2/profile"
    req = requests.post(url, data=json.dumps(x), headers=header)

    return json.loads(req.content).get("uuid")

def list_profiles(port):
    """list all profiles"""
    url = f"http://localhost:{port}/api/v2/profile"
    resp = requests.get(url)
    resp_json = json.loads(resp.content)
    return resp_json


def get_profile_name(session, port):
    """get profile name"""
    data = list_profiles(port)
    df = pd.DataFrame(data)
    locked = df.loc[df['uuid'] == session]
    session_name = locked["name"]
    session_name = session_name.to_list()
    session_name = session_name[0]
    pattern = r'[' + string.punctuation + ']'
    session_name = re.sub(pattern, "", session_name)
    print(session_name)
    return session_name

def update_profile(port, profile_id, session_rename, group_id):
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    x = {
        "group": group_id,
        "name": session_rename
    }
    reqs = requests.post(url, json.dumps(x), headers=header)
    print(reqs.status_code)

def get_photos_path(photos_dir, photos_folder):
    folder_path = os.path.join(photos_dir, photos_folder)

    # Проверяем, существует ли папка
    if not os.path.exists(folder_path):
        raise Exception(f"Folder '{photos_folder}' not found in '{photos_dir}'")

    # Получаем список файлов из нужной папки с расширением .jpg
    jpg_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.jpg')]

    # Если список пустой, значит не было найдено файлов
    if not jpg_files:
        raise Exception(f"No JPG files found in folder '{folder_path}'")

    return jpg_files

def fold_names(photos_dir, photos_folder):
    subfolders = []
    for item in os.listdir(photos_dir):
        item_path = os.path.join(photos_dir, item)
        prefix = ""
        for char in photos_folder:
            if char.isdigit():
                break
            prefix += char
        if os.path.isdir(item_path) and item.startswith(prefix):
            subfolders.append(item)
    return subfolders

def color():
    """ANSI Color"""
    RED = "\033[31m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    YELLOW = "\033[93m"
    PURPLE = "\033[95m"
    LIGRED = "\033[91m"
    DARK_YELLOW = "\033[33m"
    CIAN = "\033[96m"
    return RED, BOLD, BLUE, RESET, YELLOW, PURPLE, LIGRED, DARK_YELLOW, CIAN

def check_gmail():
    workbook = openpyxl.load_workbook('res/gmail.xlsx')
    worksheet = workbook['Sheet1']
    count_email = 0
    for cell in worksheet['A2:A' + str(worksheet.max_row)]:
        for row in cell:
            if row.value:
                count_email += 1

    return count_email