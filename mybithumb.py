import pybithumb
import time
import datetime

buycheck = False
#########내지갑 잔고 조회 및 출력까지
with open("asdf.txt") as f: ##내지갑 열기
     lines = f.readlines()
     key = lines[0].strip()
     secret = lines[1].strip()
     bithumb = pybithumb.Bithumb(key, secret) #bithumb라는 클래스에 나의 키 매칭

won = 0
wcoin = 'ETH'
targetpvt = 0
def balance_won (): #내 지갑 조회 
    return bithumb.get_balance('BTC')[2]



############ 아래로 변동성 돌파 + 상승장 투자 전략  및 사용 함수

def get_yesterday_maX(ticker, X): ###조회일 기준으로 전일의 X일 이동평균 값을 반환하는 함수
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=X).mean()
    return ma[-2]

def get_target_price(ticker): ##변동성 돌파 전략 함수
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target


def buy_crypto_currency(ticker):##구매 함수
    krw = balance_won() ##현 원화 잔고
    orderbook = pybithumb.get_orderbook(ticker) ##목표 코인의 딕셔너리를 리턴
    sell_price = orderbook['asks'][0]['price']  ##asks키를 이용해 매수 호가내역을 불러오고 price를 통해 매도 금액을 알수 있다.
    unit = krw/float(sell_price) ##원화잔고를 최우선 매도 호가금액으로 나누어 매수 수량을 결정
    global buycheck
    if(minbalance(sell_price) <= unit * 0.7 ):
        print("주문할 코인 : ",ticker,", 주문 수량 : ",unit * 0.7 ,", 주문 금액 : ", sell_price*unit*0.7)
       ## ret = bithumb.buy_market_order(ticker, unit * 0.7) #시장가 매수
       ## print(ret)
        buycheck = True 
    else:
        print("최소 주문 수량에 달하지 못합니다.")
        buycheck = True
    

def minbalance(kk):
    if(kk < 100 ):
        return 100
    elif(100 <= kk < 1000):
        return 10
    elif(1000 <= kk < 10000):
        return 1
    elif(10000 <= kk < 100000):
        return 0.1
    elif(100000 <= kk < 1000000):
        return 0.01
    elif(1000000 <= kk ):
        return 0.001

def sell_crypto_currency(ticker):##판매 함수 전량 매도
    global buycheck
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)
    buycheck = False
 
def bigger(a1 , a2):
    if a1>a2:
        return a1
    else:
        return a2 
        
def get_pvt(ticker): ##pvt
    df = pybithumb.get_ohlcv(ticker)
    score = 0
    #(당일종가 - 전일종가) /전일 종가 *거래량 - 전일pvt  = 당일pvt
    for i in (-3,6):
       one = df.iloc[i-7]
       two = df.iloc[i-8]
       thr = df.iloc[i-9]
       
       pvt = (one['close'] - two['close'])/two['close'] * one['volume']
       pvt2 = (two['close'] - thr['close'])/thr['close'] * two['volume']
       if(pvt2 >= pvt):
           score += 1
    print("이름 : ",ticker," 점수 : ",score)
    return score

count2 = 0

def targetsel():
    global count2,targetpvt,wcoin,won
    for ticker in pybithumb.get_tickers() : ##초기 실행시 나의 지갑 정보
        balance = bithumb.get_balance(ticker)
        count2 +=1
        if count2 > 150 :
            continue
    
        if balance[0] >= 0 :
            print(ticker, "-", "보유수량", format(balance[0],'f'), ", 평가금액", format(balance[0] * pybithumb.get_current_price(ticker),'f'))
            won = won + balance[0] * pybithumb.get_current_price(ticker)
    
        if (targetpvt < get_pvt(ticker)):
            targetpvt = get_pvt(ticker)
            wcoin = ticker
        print("타겟은 " ,wcoin)
        time.sleep(0.1)
        
    print ( "총 코인 자산 을 원화로 :", won + balance[2])
    print ("원화 잔고 : ", balance_won())
    count2 = 0

targetsel()

 ####초기값 설정



now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_maX(wcoin , 5)
ma20 = get_yesterday_maX(wcoin, 20)
ma100 = get_yesterday_maX(wcoin, 100)
pvtscore = get_pvt(wcoin)
target_price = get_target_price(wcoin)
current_price = pybithumb.get_current_price(wcoin)
#####설정 끝

print("-----------",wcoin,"------------")
print("현재가 : ",current_price, ", 변동성 목표가 : ", target_price, "이동평균가 : ", ma5)
print("단기 이동 평균가 : ",ma5,", 중기 이동 평균가 : ",ma20,"장기 이동 평균가 : ", ma100 )
print("PVT 점수 : ", pvtscore)
print("타겟 목표 가 : ",bigger(target_price,ma5))
########프로그램 기본 구조 
while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.delta(seconds=10): ##자정에 전량 매도 & 변동성,이동성 재평가
            target_price = get_target_price(wcoin)
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma5 = get_yesterday_maX(wcoin, 5)
            sell_crypto_currency(wcoin)
            targetsel()
            
    
        current_price = pybithumb.get_current_price(wcoin) ##현재가 조회
        
        if (current_price > target_price) and (current_price > ma5) and (buycheck == False):
            buy_crypto_currency(wcoin)
                   
    except:
        print("에러 발생")        
    time.sleep(1)