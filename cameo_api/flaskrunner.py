# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
import thread
from flask import Flask
from flask import request
from flask import jsonify
from cameo_api.spiderForYahooCurrency import SpiderForYahooCurrency

app = Flask(__name__.split(".")[0])

#啟動 server
def start_flask_server():
    #啟動 spider 抓取 yahoo 網頁並更新匯率資料庫
    spider = SpiderForYahooCurrency()
    thread.start_new_thread(spider.runSpider, ())
    #啟動 flask server
    app.run(host="0.0.0.0", port=5000, debug=True)
    
#取得指定貨幣匯率 GET
@app.route("/currency", methods=["GET"])
def getCurrency():
    strDate = request.args.get("date", None, type=str) #歷史匯率(暫不處理)
    strMoney = request.args.get("money", 0.0, type=float) #金額
    strFromCurrency = request.args.get("from", "USD", type=str) #原幣別
    strToCurrency = request.args.get("to", "TWD", type=str) #目標幣別
    return jsonify(date=strDate,
               money=strMoney,
               form=strFromCurrency,
               to=strToCurrency)
    
if __name__ == "__main__":
    start_flask_server()