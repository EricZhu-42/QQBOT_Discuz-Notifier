import hashlib
import json
import time
import re as reg

import requests
from bs4 import BeautifulSoup

def time_equal(cust_time, standard_time):
    year, month, day = standard_time.split('-')
    return cust_time == "{:d}-{:d}-{:d}".format(int(year), int(month), int(day))

def load_file(time_str):
    try:
        f = open("./log/{}.json".format(time_str), "r", encoding='utf-8')
        js = json.loads(f.read())
    except Exception:
        js = {'length':0}
    return js

def save_file(time_str, js):
    with open("./log/{}.json".format(time_str), "w", encoding='utf-8') as f:
        f.write(json.dumps(js, indent=4, ensure_ascii=False))

def compute_hash(item):
    enable_sha256 = True
    string = "{}{}{}{}{}".format(item['section'], item['msg_type'], item['msg_link_id'], item['msg_author'], item['msg_date'])
    if enable_sha256:
        x = hashlib.sha256()
        x.update(string.encode())
        return x.hexdigest()
    else:
        return string

def process_data(data, js):
    ret = list()
    for item in data:
        hash_ = compute_hash(item)
        if hash_ in js.values():
            continue
        else:
            js[js['length']+1] = hash_
            js['length'] = js['length'] + 1
            ret.append(item)
    return ret

headers = {
    "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

# 从论坛获取信息
def get_data(url, section=""):
    sess = requests.session()
    data = list()
    try:
        re = sess.get(url, headers=headers)
    except Exception as e:
        print(e)
        return data
    if re.status_code != 200:
        print("Bad connection!")
        return data
    soup = BeautifulSoup(re.text, features="lxml")
    table = soup.findAll("table")[0] # 定位到包含帖子名称的 table

    for tbody in table.findAll('tbody'):
        if not tbody['id'].startswith('normalthread'):
            continue
        th = tbody.findAll('th')[0]
        try:
            msg_type    = th.findAll('em')[0].text
        except Exception:
            msg_type    = "无"
        msg_content = th.findAll('a')[1].text
        msg_link_id = reg.search(r"tid=(.*?)&", th.findAll('a')[1]['href'])[1]
        for td in tbody.findAll('td'):
            class_ = td['class']
            if 'by' in class_ and 'by-author' in class_:
                    msg_author = td.findAll('a')[0].text
                    msg_date   = td.findAll('em')[0].span['title']

        data.append({
            'section': section,
            'msg_type': msg_type,
            "msg_content":msg_content,
            "msg_author": msg_author,
            "msg_date":msg_date,
            "msg_link_id":msg_link_id,
        })
    return data

# Test, should not be called
if __name__ == '__main__':
    while (1):
        if time.time() - start_time > 10:
            current_date = time.strftime(r"%Y-%m-%d")
            js = load_file(current_date)
            data = list()
            data.extend(process_data(get_data(url=discount_url, section="Discount"), js))
            data.extend(process_data(get_data(url=free_url, section="Free"), js))
            print(data)
            save_file(current_date, js)
            start_time = time.time()
        else:
            time.sleep(5)
