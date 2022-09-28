import re
import sqlite3


def query(DB_PATH, sql, args=None):
    """
        执行查询
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cu = conn.cursor()
    if args is None:
        cu.execute(sql)
    else:
        cu.execute(sql, args)
    if cu.arraysize > 0:
        results = cu.fetchall()
    else:
        results = None
    conn.close()
    return results


def update(DB_PATH, sql, args=None):
    """
        执行更新
        return: bool
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cu = conn.cursor()
        if args is None:
            cu.execute(sql)
        else:
            cu.execute(sql, args)
        conn.commit()
        conn.close()
        if cu.rowcount < 1:
            return False
        return True
    except Exception as ex:
        print(ex)
        return False


def dict_factory(cursor, row):
    """
        结果转换字典
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def format_sql(sql):
    """
        sql语句转格式化返回dict
    """
    args_temp = ()
    args = ()

    tag_list = sql.split('{n}')
    for index,item in enumerate(tag_list):
        tag = tag_list[index]
        default_count = sql.count('{?}')/2
        like_count = sql.count('{like}')/2
        
        if '{?}' in tag:

            if index < 1 or index == len(tag_list):
                sql = sql.replace(tag, '?')
            if index > 1 or index < len(tag_list)-1:
                sql = sql.replace(tag, '?,')

            tag = tag.replace('{?}','').replace('{?}','')
            if tag == 'None':
                args_temp = (None ),
            else:
                args_temp = (tag),
            args = args + tag

        if '{like}' in tag:
            if index < 1 or index == len(tag_list):
                sql = sql.replace(tag, '?')
            if index > 1 or index < len(tag_list)-1:
                sql = sql.replace(tag, '?,')
            tag = tag.replace('{like}','').replace('{like}','')
            if tag == 'None':
                args_temp = (None ),
            else:
                args_temp = ('%'+tag+'%'),
            args = args + args_temp

    sql = sql.replace('{n}','')
    return {'sql': sql, 'args': args}
