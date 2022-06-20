import pybithumb
import time

con_key = "1111111"
sec_key = "11111111"
 
 # 원화 잔고 얻기
def balance_won() :
    return bithumb.get_balance('BTC')[2]

 # 매수 호가 정하기
def buyPrice ( ticker ) :
    buy_price = pybithumb.get_orderbook(ticker)['bids'][1]['price']
    return buy_price

# 매수 수량 정하기
def buyQuantity ( buy_price ) :
    buy_quantity = balance_won() *  0.9970 / buy_price     # 수수료 0.25% 계산
    buy_quantity = float ( "{:.4f}".format(buy_quantity) ) # 소수점 4자리 수 버림
    print ( balance_won(), buy_price, buy_quantity)
    return buy_quantity

 # 매수 로직
def buy ( ticker, price ) :
    ticker = ticker.split('_')[0]
    buy_price = buyPrice ( ticker )
    buy_quantity = buyQuantity ( buy_price )
    
    order = bithumb.buy_limit_order(ticker, buy_price, buy_quantity)
    print (current_time() , "원화잔고 :", balance_won(), ", 매수 종목 :", ticker, ", 매수 주문가 :" , buy_price , ", 매수 수량 :", buy_quantity)
    print (order)
    
print(balance_won())