import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from matplotlib import rcParams
from past.builtins import raw_input

RAPIDAPI_KEY = "<YOUR_RAPIDAPI_KEY>"
RAPIDAPI_HOST = "<YOUR_RAPIDAPI_ENDPOINT>"

symbol_string = ""
inputdata = {}


def fetchStockData(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts"

    querystring = {"comparisons": "%5EGDAXI%2C%5EFCHI", "region": "US", "lang": "en", "symbol": symbol,
                   "interval": "5m", "range": "1d"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "275d968795msheb0c2d90f2d7a32p1141eajsnef8c254e756a"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if (response.status_code == 200):

        return json.loads(response.text)
    else:
        return None


def parseTimestamp(inputdata):
    timestamplist = []
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
    calendertime = []
    for ts in timestamplist:
        dt = datetime.fromtimestamp(ts)
        calendertime.append(dt.strftime("%m/%d/%Y"))
    return calendertime


def parseValues(inputdata):
    valueList = []
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])
    return valueList


def attachEvents(inputdata):
    eventlist = []
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("open")
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("close")
    return eventlist


if __name__ == "__main__":
    try:
        while len(symbol_string) <= 2:
            symbol_string = raw_input("Enter the stock symbol: ")
        retdata = fetchStockData(symbol_string)

        if (None != inputdata):
            inputdata["Timestamp"] = parseTimestamp(retdata)
            inputdata["Values"] = parseValues(retdata)
            inputdata["Events"] = attachEvents(retdata)
            df = pd.DataFrame(inputdata)
            sns.set(style="darkgrid")
            rcParams['figure.figsize'] = 13, 5
            rcParams['figure.subplot.bottom'] = 0.2

            ax = sns.lineplot(x="Timestamp", y="Values", hue="Events", dashes=False, markers=True,
                              data=df, sort=False)
            ax.set_title('Symbol: ' + symbol_string)

            plt.xticks(
                rotation=45,
                horizontalalignment='right',
                fontweight='light',
                fontsize='xx-small'
            )
            plt.show()
    except Exception as e:
        print("Error")
        print(e)
