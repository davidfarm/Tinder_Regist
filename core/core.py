from core.check import *
from core.sms_code import *
from core.google_auto import *
from core.tinder_login import *
from lib.geo_randomizer_polygon import get_points, group_id_list
from lib.soax_api import stick


def new_session(session_name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password, latitude, longitude, port, city, group_ids):
    """Creating new session"""
    global profile_id
    profile_id = create_profile(session_name=session_name, port=port)
    time.sleep(2)
    update_profile_proxy(profile_id=str(profile_id), proxy_port=proxy_port, proxy_username=proxy_username,
                         proxy_host=proxy_host,
                         proxy_password=proxy_password, proxy_type=proxy_type, port=str(port))
    latitude, longitude = get_points(city)
    update_profile_geo(profile_id, latitude, longitude, port)
    time.sleep(2)
    driver = create_driver(profile_id, port)
    time.sleep(1)
    update_profile_group(profile_id=str(profile_id), port=port, group_id=group_ids)

    return driver, profile_id


def start_session(port, city, group_id):
    """Starting session"""
    global group_ids
    global session_name
    email, password, reserve = parse_gmail("res/gmail.xlsx")
    latitude, longitude = get_points(city)
    group_ids = group_id_list(group_id, port)
    session_name = parse_line("res/session_names")
    photos_folder = scan_photos_id(session_name)
    name_id = scan_name_id(session_name)
    proxy_path_url = stick(name_id)

    proxy_host = "proxy.soax.com"
    proxy_type = "SOCKS"
    proxy_username = proxy_path_url
    proxy_password = "o9wWEwXm7NH5RG2W"
    proxy_port = "5000"

    driver, profile_id = new_session(session_name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password, latitude,
                         longitude, port, city, group_ids)
    return email, password, reserve, driver, photos_folder, session_name, group_ids, profile_id, name_id

def rename(port, profile_id, session_name, group_ids):
    session_rename = session_name + " !reg"
    update_profile(port=port, session_rename=session_rename, profile_id=profile_id, group_id=group_ids)

