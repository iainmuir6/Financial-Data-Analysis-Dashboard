# Iain Muir
# iam9ez

"""
PORTFOLIO DIVERSIFICATION
25 Stocks
    US Stock        (48%)
        Large-Cap       (7 – 28%)
        Small-Cap       (5 – 20%)
    Foreign         (5 – 20%)
    Indices/ETFs    (5 – 20%)
    Options         (3 – 12%)
"""


# from constants import API_KEY
# import yfinance as yf


# largeCap = list(requests.get(
#     'https://finnhub.io/api/v1/index/constituents?symbol=^GSPC&token=' + api_key).json()['constituents'])
largeCap = ['TPR', 'MO', 'USB', 'RL', 'SBAC', 'J', 'FANG', 'SHW', 'DISCK', 'ALK', 'BKR', 'AXP', 'CMA', 'JNPR', 'HAS',
            'LIN', 'HUM', 'SLB', 'CAH', 'WELL', 'PH', 'SEE', 'ATO', 'KMB', 'PCAR', 'SYY', 'HST', 'PM', 'CTSH', 'CRM',
            'WFC', 'PSA', 'ALB', 'BLK', 'UPS', 'INTC', 'ATVI', 'CHTR', 'UNP', 'MDLZ', 'DXCM', 'ALL', 'FB', 'ETN', 'TT',
            'TEL', 'BSX', 'PNW', 'DPZ', 'ADSK', 'DAL', 'DRI', 'PEG', 'REG', 'CSCO', 'LUV', 'FBHS', 'SYF', 'AMP', 'ECL',
            'VNO', 'HSIC', 'DOW', 'PEAK', 'ISRG', 'SO', 'SRE', 'IVZ', 'AAP', 'FOXA', 'CB', 'UAA', 'BEN', 'MCK', 'DHI',
            'AVGO', 'FLIR', 'LVS', 'ITW', 'PG', 'CPRT', 'AME', 'GOOG', 'IDXX', 'MRK', 'BRK.B', 'CAT', 'AEE', 'QCOM',
            'NKE', 'MYL', 'VLO', 'VTR', 'NRG', 'C', 'APTV', 'AJG', 'MAS', 'COG', 'ALLE', 'EVRG', 'MMC', 'MNST', 'TIF',
            'WYNN', 'DRE', 'PHM', 'FMC', 'GPC', 'JBHT', 'HFC', 'GL', 'ILMN', 'POOL', 'GM', 'TXN', 'HES', 'XLNX', 'FAST',
            'LW', 'WBA', 'EBAY', 'CAG', 'STT', 'DFS', 'CHD', 'ROK', 'CTAS', 'MRO', 'PXD', 'HAL', 'GWW', 'SJM', 'DVA',
            'NLSN', 'CFG', 'NWSA', 'INFO', 'BMY', 'GLW', 'EIX', 'RE', 'DOV', 'HIG', 'LMT', 'TWTR', 'IP', 'MS', 'ZION',
            'MTB', 'CBRE', 'MCHP', 'IFF', 'NFLX', 'CVX', 'BK', 'AIV', 'STZ', 'ICE', 'DE', 'BR', 'DVN', 'RMD', 'CTL',
            'TDY', 'AMAT', 'DIS', 'FE', 'EQIX', 'CARR', 'LB', 'AES', 'HOLX', 'MMM', 'CNP', 'COST', 'SWKS', 'MKC', 'CDW',
            'TXT', 'FFIV', 'DTE', 'VRSK', 'ABMD', 'ABT', 'APA', 'MCD', 'PPG', 'A', 'BWA', 'ABBV', 'GPN', 'WST', 'VAR',
            'BIO', 'WAT', 'WEC', 'ORLY', 'COO', 'OXY', 'DG', 'MET', 'ABC', 'KO', 'IBM', 'GS', 'ALXN', 'HPE', 'TAP',
            'MCO', 'CPB', 'DHR', 'CE', 'CMS', 'CHRW', 'IRM', 'BAX', 'LEG', 'KMX', 'PAYC', 'HPQ', 'FTI', 'TDG', 'NWS',
            'F', 'AKAM', 'MA', 'LNT', 'CDNS', 'OTIS', 'EOG', 'ADM', 'INCY', 'HSY', 'FCX', 'PVH', 'LYV', 'KEYS', 'AMD',
            'STX', 'PKG', 'CMI', 'KLAC', 'LLY', 'GILD', 'MOS', 'CTXS', 'UDR', 'JNJ', 'XYL', 'O', 'KMI', 'PBCT', 'BA',
            'JPM', 'PNC', 'WHR', 'PFE', 'LH', 'MPC', 'APH', 'VRTX', 'AMCR', 'CL', 'LOW', 'IPGP', 'PPL', 'NTAP', 'PYPL',
            'STE', 'GRMN', 'CI', 'UNH', 'TFC', 'NLOK', 'EL', 'RHI', 'ULTA', 'COP', 'SPGI', 'FLS', 'CERN', 'WLTW',
            'TMUS', 'ARE', 'NI', 'EXC', 'MSFT', 'AWK', 'FTV', 'TFX', 'DISCA', 'TGT', 'OKE', 'BF.B', 'HBAN', 'ROL',
            'WAB', 'ADI', 'CMCSA', 'NSC', 'SCHW', 'URI', 'SLG', 'CVS', 'ZTS', 'IR', 'ADP', 'NOC', 'YUM', 'DGX', 'FLT',
            'CME', 'CXO', 'HCA', 'PRGO', 'DLR', 'CCL', 'APD', 'MXIM', 'SIVB', 'MLM', 'BAC', 'QRVO', 'ALGN', 'MSI',
            'AZO', 'UHS', 'MKTX', 'AAL', 'CTLT', 'WRB', 'BLL', 'BDX', 'KR', 'XRAY', 'DLTR', 'ZBRA', 'MSCI', 'GD', 'ES',
            'HON', 'NUE', 'CCI', 'SNPS', 'RJF', 'AIZ', 'PWR', 'FOX', 'DD', 'VFC', 'MGM', 'EMR', 'BBY', 'GOOGL', 'ACN',
            'IT', 'EMN', 'ANTM', 'CTVA', 'NTRS', 'UNM', 'TMO', 'WRK', 'NEM', 'EXPD', 'RCL', 'EXR', 'XRX', 'TTWO', 'AIG',
            'TJX', 'INTU', 'HII', 'FITB', 'TSCO', 'DXC', 'BIIB', 'PAYX', 'HBI', 'FISV', 'PGR', 'AEP', 'GPS', 'LNC',
            'MAR', 'NWL', 'EA', 'LDOS', 'FTNT', 'VNT', 'AAPL', 'CNC', 'RF', 'WU', 'FRC', 'FDX', 'EW', 'AOS', 'D', 'HD',
            'RTX', 'MTD', 'JKHY', 'NVR', 'WMT', 'ESS', 'COF', 'ETSY', 'SYK', 'BKNG', 'TRV', 'TYL', 'PKI', 'NOV', 'CBOE',
            'DISH', 'VIAC', 'UAL', 'EFX', 'MHK', 'ODFL', 'L', 'NBL', 'LRCX', 'MDT', 'PSX', 'ANET', 'ED', 'LKQ', 'HLT',
            'IPG', 'SWK', 'FIS', 'WMB', 'PFG', 'AMT', 'NCLH', 'ROP', 'VZ', 'AON', 'VMC', 'LEN', 'HRL', 'WM', 'KIM',
            'GE', 'ADBE', 'PLD', 'ANSS', 'K', 'UA', 'IEX', 'SPG', 'PRU', 'DUK', 'EXPE', 'KSU', 'CLX', 'KEY', 'AVB',
            'FRT', 'AMGN', 'TSN', 'KHC', 'REGN', 'AVY', 'CMG', 'TER', 'SBUX', 'AMZN', 'WDC', 'LYB', 'CSX', 'LHX',
            'NDAQ', 'NOW', 'NEE', 'WY', 'XEL', 'RSG', 'T', 'V', 'MAA', 'GIS', 'ETR', 'TROW', 'BXP', 'AFL', 'NVDA',
            'SNA', 'CF', 'EQR', 'JCI', 'MU', 'ORCL', 'PEP', 'HWM', 'ZBH', 'VRSN', 'ROST', 'PNR', 'XOM', 'CINF',
            'OMC', 'IQV']

# largestCap = list(requests.get(
#     'https://finnhub.io/api/v1/index/constituents?symbol=^DJI&token=' + api_key).json()['constituents'])
largestCap = ['BA', 'DOW', 'AXP', 'CSCO', 'JNJ', 'GS', 'IBM', 'JPM', 'WMT', 'TRV', 'HD', 'NKE', 'AAPL', 'MMM', 'MSFT',
              'PG', 'CAT', 'DIS', 'UNH', 'V', 'CRM', 'VZ', 'WBA', 'HON', 'CVX', 'MCD', 'MRK', 'KO', 'INTC', 'AMGN']

smallCap = []
foreign = []
funds = []

industries = {'Industrial Conglomerates': [('3M', 'MMM'), ('Caterpillar', 'CAT'), ('Boeing', 'BA')],
              'Financial Services': [('American Express', 'AXP'), ('Goldman Sachs', 'GS'), ('JP Morgan', 'JPM')],
              'Technology': [('Apple', 'AAPL'), ('IBM', 'IBM'), ('Microsoft', 'MSFT'),
                             ('Visa', 'V'), ('Intel', 'INTC')],
              'Energy ': [('Chevy', 'CVX')],
              'Communications': [('Cisco', 'CSCO'), ('Verizon', 'VZ'), ('Disney', 'DIS')],
              'Materials': [('Exxon', 'ZOM'), ('Johnson & Johnson', 'JNJ'), ('Merck', 'MRK'),
                            ('Pfizer', 'PFE'), ('Dow Chemical', 'DOW')],
              'Consumer Staples': [('P&G', 'PG'), ('Home Depot', 'HD'), ('Wal-Mart', 'WMT'), ('Walgreen', 'WBA')],
              'Consumer Discretionary': [('Coke', 'KO'), ('Nike', 'NKE'), ("McDonald's", 'MCD')],
              'Real Estate': [('Travelers Companies Inc', 'TRV')],
              'Health Care': [('UnitedHealth', 'UNH')],
              'Utilities': []}
