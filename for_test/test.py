import json
import os

# from core import log_dispatcher


# def search_folder():
#     root_dirs = os.getcwd().split('Tinder_Regist_finalizate')
#     root_dir = root_dirs[0] + 'Tinder_Regist_finalizate\\app\invalid sessions\invalid sessions.txt'
#     # log_dispatcher.info(to_write=f'root dir: {root_dir}')
#     return root_dir



#
# def get_data():
#     with open(search_folder(), mode='r') as file:
#         data_list = []
#         data = file.read().split('\n')
#         for i in data:
#             session_data = i.split(' - ')[-1]
#             if session_data:
#                 data_list.append(json.loads(session_data))
#         return data_list
