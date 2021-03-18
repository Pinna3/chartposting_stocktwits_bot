from candlestick import DailyCandleDataRT
from time import sleep
import json

up_stocks = [
    "AAL",
    "AB",
    "ABB",
    "ABR",
    "ACHC",
    "ACLS",
    "ADTN",
    "AEO",
    "AGRO",
    "AINV",
    "AMG",
    "AMN",
    "AMNB",
    "AMSWA",
    "ANGI",
    "ANGO",
    "APEN",
    "APG",
    "APOG",
    "AR",
    "ARCB",
    "ARI",
    "ARR",
    "ASIX",
    "ASO",
    "ASRV",
    "ASYS",
    "ATEC",
    "ATLC",
    "AVID",
    "AVYA",
    "AWAY",
    "AWH",
    "BALY",
    "BANC",
    "BBW",
    "BC",
    "BCI",
    "BCOR",
    "BCRX",
    "BCSF",
    "BEN",
    "BETZ",
    "BHC",
    "BHR",
    "BIP",
    "BKE",
    "BLMN",
    "BNED",
    "BNO",
    "BOOM",
    "BPFH",
    "BRKS",
    "BSET",
    "BW",
    "BX",
    "BZH",
    "CALX",
    "CAMP",
    "CAPL",
    "CAR",
    "CARS",
    "CASH",
    "CBRE",
    "CCLP",
    "CCS",
    "CDEV",
    "CDR",
    "CDW",
    "CEQP",
    "CHEF",
    "CHUY",
    "CLB",
    "CLIR",
    "CLNE",
    "CLR",
    "CMCO",
    "CMPR",
    "CNDT",
    "CNR",
    "CNX",
    "COHR",
    "COMM",
    "COWZ",
    "CPG",
    "CSLT",
    "CSU",
    "CSV",
    "CTRE",
    "CTRN",
    "CUBI",
    "CVA",
    "CVGW",
    "CVLT",
    "CX",
    "DBC",
    "DBD",
    "DBE",
    "DBO",
    "DBV",
    "DCI",
    "DCOM",
    "DDS",
    "DENN",
    "DIN",
    "DISCA",
    "DJP",
    "DKNG",
    "DLX",
    "DOX",
    "DRN",
    "DS",
    "DSX",
    "DT",
    "DTN",
    "DXJ",
    "EARS",
    "EAT",
    "EB",
    "EFC",
    "ELY",
    "ESGU",
    "ETH",
    "EVC",
    "EVH",
    "EWBC",
    "EWD",
    "EXP",
    "EZA",
    "FAF",
    "FBC",
    "FBK",
    "FC",
    "FCOM",
    "FFG",
    "FIX",
    "FNKO",
    "FOXF",
    "FPI",
    "FRGI",
    "FTGC",
    "FV",
    "FXD",
    "FXG",
    "GAMR",
    "GATX",
    "GBX",
    "GLAD",
    "GLP",
    "GPRO",
    "GPX",
    "GSG",
    "GSLC",
    "GTES",
    "GTIM",
    "GWB",
]

# test = DailyCandleDataRT(up_stocks[2], 365)
# print(test.df)
# print(test.chart(365))

#takes stock dataframe as input and returns number of entries generates by conditions
#indicated and structure of technical indicators, specifically bollinger bands, can
#be expanded.
def entry_counter(ticker):
    dataframe = DailyCandleDataRT(ticker, 365)
    entries = []
    for index, row in dataframe.df.iterrows():
        if row['l'] < row['lower'] and row['sma9'] > row['sma20'] > row['sma50'] > row['sma200']:
            entries.append(index)
    print(entries)
    i = 0
    while i < len(entries):
        try:
            if entries[i] - entries[i + 1] == -1:
                entries.remove(entries[i])
                i -= 1
            else:
                i += 1
        except IndexError:
            break
    print(entries)
    return(len(entries))

###add to entry_counter ability to average repeats... how long on average does
###the stock sit below or above the bollinger band. (under remove entries)

with open('testfile.json', 'r') as infile:
    content = json.load(infile)
print(len(content))
