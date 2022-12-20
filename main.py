from pytrends.request import TrendReq
import yfinance
import sqlite3
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

class WindowManager(MDScreenManager):
    pass

class MainWindow(MDScreen):
    pass

stock = "AMD"

pytrends = TrendReq(hl='en-US')

kw_list = [stock]

# Timeframe works for 1, 3, 12 months and 5 years only
pytrends.build_payload(kw_list, timeframe='today 3-m')
data = pytrends.interest_over_time()

pytrends.build_payload(kw_list, timeframe='today 1-m')
data2 = pytrends.interest_over_time()

# mean for the first month
tren_1m = round(data[kw_list].mean(), 2)
# mean for 3 months, not including first month
tren_3m = round(data2[kw_list].mean(), 2)

# comparison between mean for first month to previous 2 months
tren_change = round(((tren_1m/tren_3m[kw_list])-1) * 100, 2)

finance_stock = yfinance.Ticker(stock)
# valid periods: 1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
fin_1m = finance_stock.history(period="1mo").Open
# Remove recent month from list
fin_3m = finance_stock.history(period="3mo").Open[:-fin_1m.shape[0]]

fin_3m_mean = round(fin_3m.mean(), 2)
fin_1m_mean = round(fin_1m.mean(), 2)

fin_change = round(((fin_1m_mean/fin_3m_mean)-1) * 100, 2)

print('Short Term Investment')
print('-----------------------')
print(f'The last month trend of {kw_list[0]} compared to the previous two months has changed by '
      f'{tren_change[kw_list][0]}%')
print(f'The last month stock price of {kw_list[0]} compared to the previous two months changed by '
      f'{fin_change}%')
if fin_change < 0 and tren_change[kw_list][0] < 0:
      print("Buy: Favorable | Sell: Detrimental")
elif fin_change < 0 and tren_change[kw_list][0] > 0:
      print("Buy: Potential Risk | Sell: Potential Risk")
else:
      print("Buy: Detrimental | Sell: Favorable")

class AnalyticalStockApp(MDApp):
    def build(self):
        pass

if __name__ == "__main__":
    AnalyticalStockApp().run()