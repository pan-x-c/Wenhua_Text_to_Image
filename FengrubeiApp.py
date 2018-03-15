# -*- coding:utf-8 -*-
import urllib
import os
import hashlib
import random
import requests
import json
import sys
from flask import Flask, request, render_template

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/show', methods=['POST'])
def show():
    content = request.form['input']
    appKey = '2a6e165bec543fcc'
    secretKey = 'gMLRjhtH6vF2LaPoXtN4Rb5TMFuxkfi0'

    myurl = 'https://openapi.youdao.com/api'
    q = content.encode('utf-8')
    print(q)
    fromLang = 'zh-CHS'
    toLang = 'EN'
    salt = random.randint(1, 65536)
    sign = appKey + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appKey=' + appKey + '&q=' + urllib.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        http = requests.get(myurl)
        result = json.loads(http.text)['translation'][0]
        result=result.lower()
        print(result)
    except:
        print('error')

    py = "cd ./static/code/ && ./generate.sh " + "\"" + result + "\"  " +" &"
    #command = "echo this is command" + "&&" + "ls"   #command for test
    os.system(py)
    return render_template('show.html')


if __name__ == '__main__':
    app.run(debug=True)
