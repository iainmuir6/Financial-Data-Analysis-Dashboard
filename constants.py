"""
Iain Muir, iam9ez

"""

import os

if os.environ['USER'] == 'iainmuir':
    API_KEY = os.environ["API_KEY"]
else:
    API_KEY = 'bvgk9c748v6oab530k90'

DOW_JONES = ['BA', 'DOW', 'AXP', 'CSCO', 'JNJ', 'GS', 'IBM', 'JPM', 'WMT', 'TRV', 'HD', 'NKE', 'AAPL', 'MMM', 'MSFT',
             'PG', 'CAT', 'DIS', 'UNH', 'V', 'CRM', 'VZ', 'WBA', 'HON', 'CVX', 'MCD', 'MRK', 'KO', 'INTC', 'AMGN']
