import ast
import os
import sqlite3


from utils import symbol


def _format_path(path):
    try:
        set1 = set(path)
        set2 = set(symbol.list)
        common_elements = set1.intersection(set2)
        if len(common_elements) > 0:
            for element in common_elements:
                target = symbol.list1[symbol.list.index(element)]
                path = path.replace(element, target)
    except:
        print('请对照说明检查路径输入是否正确')
    return path

def _format_proxy(proxy):
    try:
        if isinstance(proxy,tuple) == False:
            proxy = tuple(ast.literal_eval(proxy))
    except:
        print('请对照说明检查代理输入是否正确')
    return proxy

def _get_last(user):
    db_dir = os.path.dirname(__file__)
    db_path = os.path.join(db_dir, 'inner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND  name='curr_user'")
    exits = cursor.fetchone()
    if exits:
        conn.execute(f"UPDATE curr_user SET user_id = ?", (user,))
    else:
        cursor.execute("CREATE TABLE IF NOT EXISTS curr_user (user_id TEXT)")
        insert_query = f"INSERT INTO curr_user (user_id) VALUES (?);"
        data = (user,)
        cursor.execute(insert_query, data)

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND  name=? ",('user'+user,))
    id_exits = cursor.fetchone()
    if id_exits:
        cursor.execute(f"SELECT * FROM {'user' + user}")
        result = cursor.fetchone()
    else:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {'user' + user} (id INTEGER);")
        insert_query = f"INSERT INTO {'user' + user} (id) VALUES (?);"
        result = (0,)
        cursor.execute(insert_query, result)

    conn.commit()
    cursor.close()
    conn.close()

    return result[0]

def clear_curr():
    db_dir = os.path.dirname(__file__)
    db_path = os.path.join(db_dir, 'inner.db')
    conn = sqlite3.connect(db_path)
    with conn:
        conn.execute(f"UPDATE {'curr_user'} SET user_id = ?", (None,))

def dele_wprk(path):
    os.rmdir(path)

def str_to_bool(value):
    if value.lower() in ['true', '1', 'yes']:
        return True
    elif value.lower() in ['false', '0', 'no']:
        return False
    raise ValueError(f'Cannot convert {value} to boolean')