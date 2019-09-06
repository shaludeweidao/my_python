# -*- coding: UTF-8-* -*-
# __author__ = 'fzj'
import configparser
import os
from datetime import datetime, timedelta

import pymysql
import redis

# 此变量控制着运行的环境
DEFAULT_ENV = "local"


def set_run_env(key="env"):
    """从系统环境中获取key的参数,来确定要运行环境，如果系统变量中无参数，使用默认值"""
    global DEFAULT_ENV
    try:
        value = os.environ.get(key)
    except Exception:
        value = os.environ.get(key.upper())

    if (value):
        print("env param has value,  env=[{}]".format(value))
        DEFAULT_ENV = value
    else:
        print("env param is null")
    print("finally DEFAULT_ENV=[{}]".format(DEFAULT_ENV))


def get_props():
    """从db.ini 配置文件中获取参数,返回对应环境中的参数字典"""
    conf_file_path = os.path.join(os.path.dirname(__file__), "db.ini")
    print("conf file path is [{}]".format(conf_file_path))
    config_parser = configparser.ConfigParser()
    config_parser.read(conf_file_path, encoding="utf-8")
    # 确定要使用的环境参数
    set_run_env()
    items = config_parser.items(DEFAULT_ENV)
    props = {}
    for (key, value) in items.__iter__():
        print("key=[{}]  value=[{}]".format(key, value))
        props[key] = value
    return props


def get_mysql_conn():
    props = get_props()
    mysql_conn = pymysql.connect(props['mysql_host'], props['mysql_user'], props["mysql_password"], props["mysql_db"],
                                 charset="utf8")
    return mysql_conn


def get_redis_conn():
    props = get_props()
    redis_conn = redis.Redis(host=props["redis_host"], port=int(props["redis_port"]))
    return redis_conn


def get_str_times(str_start_time, str_end_str, str_parse="%Y-%m-%d %H:%M:%S", hours=24):
    """传入 str_start_time 开始时间的字符串，str_end_str 结束时间的字符串，str_parse 字符串格式， hours 步长，   返回此时间范围内的日期列表 """
    str_times = []
    str_times.append(str_start_time)
    while True:
        # strptime = datetime.strptime(str_start_time, "%Y-%m-%d %H:%M:%S")
        stat_datetime = datetime.strptime(str_start_time, str_parse)
        str_time = (stat_datetime + timedelta(hours=int(hours))).strftime(str_parse)
        if str_end_str < str_time:
            break
        str_times.append(str_time)
        str_start_time = str_time
    return str_time


if __name__ == '__main__':
    # get_props()

    # 测试redis
    r = get_redis_conn()
    r.set("key", "value")
    print("redis test value=[{}]".format(r.get("key")))
