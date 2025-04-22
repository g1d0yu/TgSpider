import os
import shutil
from . import symbol
folder_list = symbol.folder_list
file_list = symbol.file_list
def check_path(folder_path):
    work_list = []
    key_datas = os.path.join(folder_path, 'key_datas')
    if os.path.exists(key_datas) == False:
        return work_list
    for i, name in enumerate(file_list):
        info_path = os.path.join(folder_path, name)
        if os.path.exists(info_path):
            map_path = os.path.join(folder_path,folder_list[i])
            if os.path.exists(map_path):
                info_folder_name = name[:-1]
                work_folder = f"work{i}"
                if not os.path.exists(work_folder):
                    os.makedirs(work_folder, exist_ok=True)
                else:
                    work_list.append(work_folder)
                    continue
                info_folder_path = os.path.join(work_folder, info_folder_name)
                if not os.path.exists(info_folder_path):
                    os.mkdir(info_folder_path)
                shutil.copy(info_path, work_folder)
                shutil.copy(map_path, info_folder_path)
                shutil.copy(key_datas, work_folder)
                work_list.append(work_folder)
            else:
                continue
        else:
            continue
    return work_list
if __name__ == '__main__':
    folder_path = r'D:\Project\tgMessage\tdata'
    list = check_path(folder_path)
    print(list)
    #shutil.rmtree("work0")