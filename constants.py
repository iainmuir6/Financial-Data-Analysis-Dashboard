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

STATE_CODES = {
    'Washington, D.C.': 'DC', 'Mississippi': 'MS', 'Oklahoma': 'OK',
    'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR',
    'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA',
    'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ',
    'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT',
    'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT',
    'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV',
    'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI',
    'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND',
    'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY',
    'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH',
    'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD',
    'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA',
    'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX',
    'Nevada': 'NV', 'Maine': 'ME'
}
