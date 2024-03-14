import csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import math


def determine_high_periods(df:pd.DataFrame):
  all_activity=[]
  all_indexes_days =[]
  minute_wise_price_movements = []
  indexes = []
  count = 1
  for index, row in df.iterrows():
    if index < len(df)-1:
      if index == 0:continue
      count += 1
      minute_gain=round(df.iloc[index-1]['close'] - row['close'], 5)
      if minute_gain>0:
         minute_wise_price_movements.append('G')
      elif minute_gain<0:
         minute_wise_price_movements.append('L')
      else:
         minute_wise_price_movements.append('N')
      indexes.append(index)
      if row['datetime'].split(" ")[1]=="23:59" :
         all_activity.append("".join(minute_wise_price_movements.copy()))
         all_indexes_days.append(indexes.copy())
         minute_wise_price_movements.clear()
         indexes.clear()
  return all_activity, all_indexes_days
def getDF():
  filename = "src/modified.csv"
  with open(filename, "r") as csv_file:
    df = pd.read_csv(csv_file, header=None, delimiter="\t", names=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    return df


def weelcome_message(df:pd.DataFrame):
   stars = "*" * 20 
   print(f"Welcome, this program shows data analysis of \
         EURUSD data from {df.iloc[0]['datetime']} to {df.iloc[len(df) -1 ]['datetime']}")
   print(f"if consists of {len(df)} rows and here is the first 5 and last 5 respectively")
   print(f"\n\n{stars}")
   print("FIRST 5")
   print(stars)
   print(df.head())
   print(f"\n\n{stars}")
   print("LAST 5")
   print(stars)
   print(df.tail())


def estimate_gains(indexes:list[int], df:pd.DataFrame):
  for index in indexes:
    buy_date_time=df.iloc[index-1]['datetime']
    sell_date_time=df.iloc[index]['datetime']
    sell_price = df.iloc[index]['close']
    buy_price = df.iloc[index-1]['close']
    gain = sell_price - buy_price
    percentage=(gain/buy_price) * 100
    print(f"\n\na {percentage}% gain is made by buying on {buy_date_time} at {buy_price} and selling on {sell_date_time} at {sell_price}\n\n")

def findPatterns(days:list[str], indexes:list[list[int]]):
   print("\nThe current pattern searches for where they are two consecutive losses followed by at least two consective gains\n")
   match_occurences=[]
   match_indexes=[]
   for index, day in enumerate(days):
      start = 0
      occurences =[]
      while True:
        val=day.find("LLGG", start)
        actual_index = indexes[index][val]
        if val == -1:
          break
        else:
          occurences.append(val)
          match_indexes.append(actual_index)
          start += len("LLGG")+val
      print(f"Here are all the indexes in which --LLGG-- is found in day {index+ 1}::  {occurences}")
      match_occurences.append(occurences)
   return match_occurences, match_indexes
df = getDF()
weelcome_message(df)
all_days, indexes_all=determine_high_periods(df=df)
patterns, match_indexes=findPatterns(all_days, indexes_all)

estimate_gains(match_indexes,  df)