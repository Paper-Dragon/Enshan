import requests, json, time, os, sys
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
from lxml import etree

cookie = os.environ.get("cookie_enshan")

def send_message(content):
    api_url = 'https://wxpusher.zjiecode.com/api/send/message'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "appToken": "AT_Jsii9rLkDRpw7WWkhqZN1oNXIH8hHhqP",
        "content": content,
        "contentType": 1,
        "topicIds": [33380]
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    return response.json()

def run(cookie):
    msg = ""
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0'})

    # 签到
    url = "https://www.right.com.cn/forum/home.php?mod=spacecp&ac=credit&op=log&suboperation=creditrulelog"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    try:
        r = s.get(url, headers=headers, timeout=120)
        # print(r.text)
        if '每天登录' in r.text:
            h = etree.HTML(r.text)
            data = h.xpath('//tr/td[6]/text()')
            msg += f'签到成功或今日已签到，最后签到时间：{data[0]}'
            print(msg)
        else:
            msg += '签到失败，可能是cookie失效了！'
            print(send_message(msg))
    except:
        msg = '无法正常连接到网站，请尝试改变网络环境，试下本地能不能跑脚本，或者换几个时间点执行脚本'
        print(send_message(msg))


if __name__ == "__main__":
    if cookie:
        print("----------恩山论坛开始尝试签到----------")
        msg = ""
        if "\\n" in cookie:
            clist = cookie.split("\\n")
        else:
            clist = cookie.split("\n")
        i = 0
        while i < len(clist):
            msg += f"第 {i+1} 个账号开始执行任务\n"
            cookie = clist[i]
            run(cookie)
            i += 1
        print("----------恩山论坛签到执行完毕----------")
    else:
        print("cookie为空")
