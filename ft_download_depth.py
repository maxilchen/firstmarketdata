import websocket
import json
import os
import time
import pandas as pd

time_start = 5800     # 获取整点附近深度数据开始时刻
time_end = 200     # 获取整点附近深度数据开始时刻

file_depth = 'ft_depth.csv'

if os.access(file_depth,os.F_OK):
    print(file_depth,'already exists!  Keep appending data to the end')
else:
    table = pd.DataFrame(columns=['bids 1 price','bids 1 amount','bids 2 price','bids 2 amount',
                                  'bids 3 price','bids 3 amount','bids 4 price',
                                  'bids 4 amount','bids 5 price','bids 5 amount',
                                  'asks 1 price','asks 1 amount','asks 2 price',
                                  'asks 2 amount','asks 3 price','asks 3 amount',
                                  'asks 4 price','asks 4 amount','asks 5 price',
                                  'asks 5 amount'])
    table.to_csv(file_depth)

req = {'cmd':'req','args':['depth.L20.ftusdt'],'id':1}
ws = websocket.create_connection("wss://ws.fcoin.com/api/v2/ws")
ws.recv()

while True:
    t = time.time()
    t_minsec = time.strftime('%M%S',time.localtime(t))
    t_hour = time.strftime('%H',time.localtime(t))
    if int(t_minsec) >= time_start:
        ws = websocket.create_connection("wss://ws.fcoin.com/api/v2/ws")
        ws.recv()
        while int(t_minsec) <= time_end or int(t_minsec) >= time_start:
            ws.send(json.dumps(req))
            depth = json.loads(ws.recv())['data']
            out_data = []
            out_data.extend(depth['bids'][0:10])  # 卖一至卖五
            out_data.extend(depth['asks'][0:10])  # 买一至买五
            t_save = time.strftime('%m-%d,%H:%M:%S',time.localtime(depth['ts']/1000))
            print(depth['ts']/1000,' vs ',time.time())
            print(t_save)
            out_table = pd.DataFrame(out_data,columns=[t_save]).T
            out_table.iloc[[0],:].to_csv(file_depth,mode='a',header=False)
            t=time.time()

            t_minsec = time.strftime('%M%S',time.localtime(t))
        ws.close()
    time.sleep(5)
