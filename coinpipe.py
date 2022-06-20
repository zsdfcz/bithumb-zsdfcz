import pybithumb
import time
from datetime import datetime

all = pybithumb.get_current_price("ALL") 
sort_all = sorted(all.items(), key = lambda x : float(x[1]['fluctate_rate_24H']), reverse=True)
##급등주 찾기 코드 
cycle_time = 1 # 초 간격으로 체크
loop_time = 60 * 60 # 초 동안 체크
ascent = 1 # % 상승

sec = 0
prev_ticker = ''
prev_rate = 0
prev_dict = { 'ticker' : 0 }

for ticker, data in sort_all :        
    prev_dict[ticker] = data['fluctate_rate_24H']

print("현재시간, 이름 , 현재 가격, 현재 상승률, 1초전 상승률, 상승률 차이 ")

while sec < loop_time :
    all = pybithumb.get_current_price("ALL") 
    sort_all = sorted(all.items(), key = lambda x : float(x[1]['fluctate_rate_24H']), reverse=True)
    
    for ticker, data in sort_all :        
        diff = float(data['fluctate_rate_24H']) - float(prev_dict[ticker]) 
           
        if diff >= ascent :
            print(datetime.now(), ticker, data['closing_price'], data['fluctate_rate_24H'], float(prev_dict[ticker]), '%.2f' % diff )

        prev_dict[ticker] = data['fluctate_rate_24H']

    time.sleep(cycle_time)
    sec+=cycle_time