# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
import threading
import logging
from flask import Flask
from flask import request
from flask import jsonify
from cameo_api.spiderForYahooCurrency import SpiderForYahooCurrency

app = Flask(__name__.split(".")[0])

#啟動 server
def start_flask_server():
    #啟動 spider 抓取 yahoo 網頁並更新匯率資料庫
    spider = SpiderForYahooCurrency()
    spiderThread = SpiderThread(spiderInstance=spider)
    spiderThread.start()
    #啟動 flask server
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    
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
               
#獨立執行 更新匯率資料庫 spider
class SpiderThread(threading.Thread):
    #thread 建構子
    def __init__(self, spiderInstance=None):
        threading.Thread.__init__(self) #初始化父層 Thread
        self.spider = spiderInstance
        
    #run
    def run(self):
        try:
            logging.info("SpiderThread running...")
            self.spider.runSpider()
        except Exception as ex:
            logging.warning("spider did not work.")
            print(ex)
        finally:
            logging.info("SpiderThread stoped.")
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_flask_server()