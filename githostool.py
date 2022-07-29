# coding = utf8

'''
获取github host配置写入本机host文件
目前只支持windows
依赖： requests
原理: 通过get请求获取host配置，取出首行与尾行匹配本机host文件，若存在匹配关系则替换，否则就追加配置
'''

import ctypes
import logging
import os
import re
import sys
import requests

HOST_PATH = r"C:\Windows\System32\drivers\etc\hosts"
# 日志记录在当前脚本目录
cur_dir = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s](%(lineno)d): %(message)s", filename=cur_dir+"/githostool.log", encoding="utf-8")

# 用于申请管理员权限
if ctypes.windll.shell32.IsUserAnAdmin():
    pass
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

# github host配置地址
HOST = ("https://raw.hellogithub.com/hosts",
        "https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts")



def req_host(url) -> str:
    '''在线获取github host配置，返回内容文本'''
    req = requests.get(url)
    if req.status_code != 200:
        logging.error("请求github最新host配置异常，退出...")
        raise Exception("")
    logging.info("从github host源获取配置成功")
    return req.text.strip()


def read_host(file) -> str:
    '''读取host文件内容'''
    text = file.read()
    # 将文件指针方法放到开头
    file.seek(0, 0)
    return text


def search_row(host, new_host:str) -> list:
    '''获取host文件中github配置所在范围，若不存在则返回None'''
    hand = new_host.splitlines()[0]
    tail = new_host.splitlines()[-1]
    search = re.search(
        hand+"([\s\S]*)"+tail, host)
    if search != None:
        return search.span()
    else:
        return None


def creat_host_text(old_text: str, new_conf: str, rows: tuple):
    '''创建新的host文本，将host文本中旧配置先删除，后追加新配置'''
    start = rows[0]
    end = rows[1]
    if end == len(old_text):
        new_text = old_text[0:start]
    else:
        new_text = old_text[0:start]+old_text[end]
    return new_text + new_conf


def main(url):
    new_conf = req_host(url) # 获取的github host配置
    with open(HOST_PATH, "r+", encoding="utf-8") as f:
        host_text = read_host(f)  # 本地host文本
        rows = search_row(host_text, new_conf)
        new_host_tx = None  # 增加或替换github host配置后的host文本
        if rows == None:
            # 原host文件中不存在配置记录
            logging.info("host中不存在旧配置，直接添加新配置")
            new_host_tx = host_text + "\n" + new_conf  
        else:
            logging.info("更新host文件")
            new_host_tx = creat_host_text(host_text, new_conf, rows)
        if new_host_tx != None:
            f.write(new_host_tx)
            f.flush()
            os.system("ipconfig /flushdns")


if __name__ == "__main__":
    # 指定使用哪个源的配置，查看上面HOST变量
    tag = 0
    try:
        main(HOST[tag])
        print("--成功--")
    except Exception as e:
        logging.error("运行异常，行数：")
        logging.error(e)
