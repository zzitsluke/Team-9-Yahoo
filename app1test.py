import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

##call data from yfinance
nvda = yf.Ticker("NVDA")
Df = nvda.history(period = "3y")

##build data into 30 day moving volatility, method found from research on Youtube
Df["percent_change"] = Df["Close"].pct_change()
Df["Volatility30"]=Df["percent_change"].rolling(30).std() * 100

##Build Plot and Display
#Brainstormed ChatGpt for help using matplot to edit axis
COLOR_Price = "#3399e6"
COLOR_Vol = "#FF0000"

fig, ax1 = plt.subplots(figsize=(10,6))
ax1.plot(Df["Close"], label = "Price ($)", color = COLOR_Price)
ax1.set_ylabel("Price($)", color = COLOR_Price)
ax1.set_title("3 Year Price vs Volatility for NVDA")

ax2 = ax1.twinx()
ax2.plot(Df["Volatility30"], label = "30 Day Volatility (%)", linestyle = "--", color = COLOR_Vol)
ax2.set_ylabel("30 Day Volatility(%)", color = COLOR_Vol)

ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))    
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

#legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc="upper left")

#Rotate X Axis for Clarity
plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

plt.tight_layout()
plt.show()