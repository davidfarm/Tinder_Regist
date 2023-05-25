from core.check import *
from core.sms_code import *
from core.core import *
from core.google_auto import *
from core.tinder_login import *
from lib.geo_randomizer_polygon import get_points, group_id_list

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
    proxy_host = "proxy.soax.com"
    proxy_type = "SOCKS"
    proxy_username = "rUfgRb6QMNgjiLYv"
    proxy_password = "wifi;fr;;;paris"
    ports = ["9266", "9267", "9268", "9269", "9270", "9271", "9272", "9273", "9274", "9275",
                "9276", "9277", "9278", "9279", "9280", "9281", "9282", "9283", "9284", "9285",
                "9286", "9287", "9288", "9289", "9290", "9291", "9292", "9293", "9294", "9295",
                "9296", "9297", "9298", "9299", "9300", "9301", "9302", "9303", "9304", "9305",
                "9306", "9307", "9308", "9309", "9310", "9311", "9312", "9313", "9314", "9315",
                "9316", "9317", "9318", "9319", "9320", "9321", "9322", "9323", "9324", "9325",
                "9326", "9327", "9328", "9329", "9330", "9331", "9332", "9333", "9334", "9335",
                "9336", "9337", "9338", "9339", "9340", "9341", "9342", "9343", "9344", "9345",
                "9346", "9347", "9348", "9349", "9350", "9351", "9352", "9353", "9354", "9355",
                "9356", "9357", "9358", "9359", "9360", "9361", "9362", "9363", "9364", "9365"]
    proxy_port = ports[random.randint(0,99)]
    driver, profile_id = new_session(session_name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password, latitude,
                         longitude, port, city, group_ids)
    return email, password, reserve, driver, photos_folder, session_name, group_ids, profile_id

def rename(port, profile_id, session_name, group_ids):
    session_rename = session_name + " !reg"
    update_profile(port=port, session_rename=session_rename, profile_id=profile_id, group_id=group_ids)

