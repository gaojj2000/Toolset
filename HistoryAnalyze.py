# _*_ coding:utf-8 _*_
# FileName: HistoryAnalyze.py
# IDE: PyCharm

import os
import json
import time
import requests
from urllib import parse
from flask_cors import CORS
from flask import Flask, request, make_response, jsonify

# nohup /www/server/panel/pyenv/bin/python3.7 HistoryAnalyze.py > HistoryAnalyze.log 2>&1 &

base = 'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog'
gacha_type = {
    '角色活动祈愿与角色活动祈愿-2': '301',
    '常驻许愿': '200',
    '武器活动祈愿': '302',
    '新手许愿': '100'
}
params = {
    'init_type': '301',
    'size': '20',
    'authkey_ver': '1',
    'device_type': 'mobile',
    'page': '1',
    'lang': 'zh-cn',
    'plat_type': 'android',
    'gacha_type': '301',
    'timestamp': '1648597985',
    'gacha_id': 'eaa07ae07196ca35c36b48213560ab6df7617e',
    'sign_type': '2',
    'game_biz': 'hk4e_cn',
    'region': 'cn_gf01',
    'end_id': '0',
    'auth_appid': 'webview_gacha'
}

app = Flask(import_name=__name__)
app.config.from_object(__name__)
CORS(app, origins='*', supports_credentials=True)


@app.route('/test_get_history', methods=['GET'])
def test_get_history():
    authkey_url = str(request.args.get('url'))
    params['page'] = '1'
    params['end_id'] = '0'
    params['gacha_type'] = '301'
    params['authkey'] = parse.quote({k: v[0].replace(' ', '+') for k, v in parse.parse_qs(parse.urlsplit(authkey_url).query).items()}.get('authkey', ''))
    url = base + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
    res = requests.get(url).json()
    return make_response(jsonify(res), 200)


@app.route('/get_history', methods=['GET'])
def get_history():
    authkey_url = str(request.args.get('url'))
    all_history = {}
    uid = ''
    for type_ in gacha_type:
        time.sleep(0.5)
        params['page'] = '1'
        params['end_id'] = '0'
        params['gacha_type'] = gacha_type[type_]
        params['authkey'] = parse.quote({k: v[0].replace(' ', '+') for k, v in parse.parse_qs(parse.urlsplit(authkey_url).query).items()}['authkey'])
        url = base + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        res = requests.get(url).json()
        if res['data'] and not res['retcode']:
            history = res['data']['list']
            if history:
                uid = history[0]['uid']
                old = []
                ids = []
                if os.path.exists(f'{uid}_{gacha_type[type_]}.json'):
                    old = json.loads(open(f'{uid}_{gacha_type[type_]}.json', 'r', encoding='utf-8').read())
                    ids = [o['id'] for o in old]
                while 1:
                    params['page'] = str(int(params['page']) + 1)
                    params['end_id'] = res['data']['list'][-1]['id']
                    url = base + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
                    res = requests.get(url).json()
                    if res and res['data'] and res['data']['list']:
                        history += res['data']['list']
                        time.sleep(0.5)
                        if [h['id'] for h in res['data']['list'] if h['id'] in ids]:
                            break
                    else:
                        break
                history = history[::-1]
                if old and ids:
                    for h in history:
                        if h['id'] not in ids:
                            old.append(h)
                    history = old
                all_history[type_] = history
                open(f'{uid}_{gacha_type[type_]}.json', 'w', encoding='utf-8').write(json.dumps(history, indent=4, ensure_ascii=False))
            else:
                if os.path.exists(f'{uid}_{gacha_type[type_]}.json'):
                    all_history[type_] = json.loads(open(f'{uid}_{gacha_type[type_]}.json', 'r', encoding='utf-8').read())
                else:
                    all_history[type_] = []
        else:
            return make_response(jsonify(res), 400)
    return make_response(jsonify(all_history), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22909, threaded=True, processes=1)
