# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template
from flask_script import Manager
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

app = Flask(__name__)
manager = Manager(app)


@app.route('/ip/<string:ip_str>', methods=['GET'])
def ip(ip_str):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    try:
        req = Request('https://ip138.com/iplookup.asp?ip={ip}&action=2'.format(ip=ip_str))
        req.add_header('User-agent', user_agent)
    except (HTTPError, URLError) as e:
        return jsonify({'message': e})
    html = urlopen(req)
    bsObj = BeautifulSoup(html.read(), features="html.parser")
    get_asn_data = bsObj.find("ul", {"class": "ul1"}).children
    temp_list = []
    for item in get_asn_data:
        temp_list.append(item)
    return render_template('ip.html', list=temp_list)


if __name__ == '__main__':
    manager.run()
