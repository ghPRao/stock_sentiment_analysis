#!/usr/bin/env_python3

import numpy as np
import sys
import csv
from urllib.request import urlopen

import warnings
warnings.filterwarnings("ignore")


def download_tickers(top_companies):
    '''
        Pick the top top_number_of_companies in percentage
        Create a comma seperated ticker data in a file named 'tickers.csv' under data directory
    '''
     assert isinstance(percent, int)

        
    with open('../data/tickers.csv', 'w') as csvfile:     
        spamwriter = csv.writer(csvfile, delimiter=',')    
        
    cap_stat, output = np.array([]), []
    
    for exchange in ["NASDAQ", "NYSE", "AMEX"]:
        url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
        repeat_times = 10 # try again if there is http error
        for _ in range(repeat_times):
            try:
                print("Downloading tickers from {}...".format(exchange))
                response = urlopen(url + exchange + '&render=download')
                content = response.read().decode('utf-8').split('\n')
                
                for num, line in enumerate(content):
                    line = line.strip().strip('"').split('","')
                    if num == 0 or len(line) != 9:
                        continue # filter unmatched format
                    # ticker, name, last_sale, market_cap, IPO_year, sector, industry
                    ticker, name, _, market_cap, _, _, _ = line[0:4] + line[5:8]
                    cap_stat = np.append(cap_stat, float(market_cap))
                    output.append([ticker, name.replace(',', '').replace('.', ''),
                                   exchange, market_cap])
                break
            except:
                continue
    for data in output:
        market_cap = float(data[3])
        if market_cap < np.percentile(cap_stat, 100 - percent):
            continue
        writer.writerow(data)