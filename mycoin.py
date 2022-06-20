import pybithumb
import time
from datetime import datetime

all = pybithumb.get_current_price("ALL") 
sort_all = sorted(all.items(), key = lambda x : float(x[1]['fluctate_rate_24H']), reverse=True)

cycle_time = 10 # 매수를 위해서 X 초 간격으로 체크
ascent = 3 # % 상승

sell_ascent = 3 # 매수후 % 상승 후 매도
stop_loss = -3 # % 하락일 경우 매도

sell_cycle_time = 1 # 파는 간격을 초 간격으로 체크
sell_time = 600 # 초 안에는 무조건 팔기

init_balance = 1000000 # 원
balance = init_balance
count_deal = 0

while True :

    buy_sec = 0
    sell_sec = 0
    prev_ticker = ''
    prev_rate = 0
    prev_dict = { 'ticker' : 0 }

    for ticker, data in sort_all :        
        prev_dict[ticker] = data['closing_price']

    buy_flag = False

    while buy_flag == False :
        all = pybithumb.get_current_price("ALL") 
        sort_all = sorted(all.items(), key = lambda x : float(x[1]['fluctate_rate_24H']), reverse=True)

        for ticker, data in sort_all :        
            diff = ( float(data['closing_price']) - float(prev_dict[ticker]) ) / float(prev_dict[ticker]) * 100
            if diff >= ascent :
                buy = [ str(datetime.now()), ticker, float(prev_dict[ticker]), float(data['closing_price']), float('%.2f' % diff) ]
                print ('BUY ' , buy ) 
                buy_flag = True
                break;

            prev_dict[ticker] = data['closing_price']
            
        time.sleep(cycle_time)
        buy_sec+=cycle_time

    # 팔기 로직
    sell_flag = False
    buy_price = float (buy[3])

    while sell_flag == False :
        buy_ticker = buy[1]
        current_price = pybithumb.get_current_price(buy_ticker)
        yield_rate = ( current_price - buy_price ) / buy_price * 100

        if ( yield_rate >= sell_ascent) :
            sell = [ str(datetime.now()), buy_ticker, buy_price, current_price , float('%.2f' % yield_rate) ]
            print ( 'SELL', sell )
            sell_flag = True
            break
        
        if ( yield_rate <= stop_loss) :
            sell = [ str(datetime.now()), buy_ticker, buy_price, current_price , float('%.2f' % yield_rate) ]
            print ( 'SELL', sell , "STOP LOSS")
            sell_flag = True
            break
        
        if ( sell_sec > sell_time ) :
            sell = [ str(datetime.now()), buy_ticker, buy_price, current_price , float('%.2f' % yield_rate) ]
            print ( 'SELL', sell , "TIME_OUT" )
            sell_flag = True
            break

        time.sleep(sell_cycle_time)
        sell_sec += sell_cycle_time

    count_deal +=1 
    current_balance = balance + (current_price - buy_price) * ( balance / buy_price )
    rate = ( current_balance - init_balance ) / init_balance * 100
    print (count_deal, "Current Balance : ", float('%.2f' % current_balance), "(", float('%.2f' % rate), "% )" )
    balance = current_balance