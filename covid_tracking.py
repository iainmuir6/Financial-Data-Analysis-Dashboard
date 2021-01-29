"""
Iain Muir, iam9ez@virginia.edu

Web scrape and compilation of data from covidtracking.com
    Now using the website's API to collect data

Output:
    - COVID Data for all 50 states
    - Total U.S. Data
    - Figure displaying U.S. Daily Deaths, 7-day M.A. overlayed
    - Figure displaying U.S. 7-day M.A. for New Cases, Daily Deaths and Current Hospitalizations
    - Figure displaying subplots of the U.S. total new deaths and new deaths of the top ten most affected states
        --> determined by the most new deaths within the last month

    * optional figures *
    - 50 individual figures displaying state 7-day M.A. for New Cases, Daily Deaths and Current Hospitalizations
"""

from matplotlib.lines import Line2D
from datetime import date, datetime
import matplotlib.pyplot as plt
from matplotlib import dates
import pandas as pd
import numpy as np
import time


def us_data():
    url = "https://covidtracking.com/api/v1/us/daily.csv"
    df = pd.read_csv(url)
    df = df[['date',
             'states',
             'positive',
             'positiveIncrease',
             'negative',
             'negativeIncrease',
             'pending',
             'death',
             'deathIncrease',
             'hospitalizedCurrently',
             'hospitalizedIncrease',
             'hospitalizedCumulative',
             'inIcuCurrently',
             'inIcuCumulative',
             'onVentilatorCurrently',
             'onVentilatorCumulative',
             'recovered',
             'dateChecked',
             'hospitalized',
             'lastModified',
             'total',
             'totalTestResults',
             'totalTestResultsIncrease',
             'posNeg',
             'hash']]
    df = df.drop(columns=['dateChecked', 'hospitalized', 'lastModified', 'hash'])
    df['date'] = pd.to_datetime(df['date'].astype(str))
    df = df.iloc[::-1]

    df = df.set_index("date")

    adjusted_dates = dates.date2num(
        [datetime.strptime(d.date().strftime('%Y-%m-%d'), '%Y-%m-%d') for d in df.index.tolist()])

    try:
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))
        ax.plot(
            adjusted_dates,
            df.positiveIncrease.rolling(window=7).mean(),
            color='red')
        ax.plot(
            adjusted_dates,
            df.hospitalizedCurrently.rolling(window=7).mean(),
            color='blue')
        ax.set_facecolor('lavender')
        ax.grid(b=True, axis='y', color='white')
        ax.set_ylabel("New Cases and Current Hospitalizations", fontsize=12)
        ax.set_xlabel("Dates", fontsize=12)

        ax2 = ax.twinx()
        ax2.plot(
            adjusted_dates,
            df.deathIncrease.rolling(window=7).mean(),
            color='black')
        ax2.set_ylabel("Daily Deaths", fontsize=12)

        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 7))
        ax.tick_params(axis='x', labelsize=8)

        plt.title('U.S. New Daily Cases, Deaths and Current Hospitalizations, 7 Day M.A.', fontsize=16)
        figure = plt.gcf()
        figure.legend(
            handles=[Line2D([0], [0], c='r', lw=2), Line2D([0], [0], c='b', lw=2), Line2D([0], [0], c='k', lw=2)],
            labels=['New Cases', 'Current Hospitalizations', 'New Deaths'],
            loc='upper left',
            frameon=True,
            ncol=1,
            bbox_to_anchor=(0.15, 0.85),
            shadow=True,
            prop={'size': 10})
        figure.set_size_inches(16, 9)

        plt.clf()
    except Exception as e:
        print("Error in creation of moving average figures: " + str(e))

    try:
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))
        ax.bar(
            adjusted_dates,
            df.deathIncrease,
            color='salmon',
            label='Daily Deaths')
        ax.plot(
            adjusted_dates,
            df.deathIncrease.rolling(window=7).mean(),
            color='maroon',
            label='7 Day M.A.')
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 7))

        ax.tick_params(axis='x', labelsize=8)
        plt.grid(b=True, axis='y', color='silver')
        plt.title("US Daily Deaths Over Time", fontsize=28, fontweight='bold')
        plt.xlabel("Dates", fontsize=12)
        plt.ylabel("Daily Deaths", fontsize=12)
        plt.legend(frameon=True, loc='upper left', prop={'size': 12})
        figure = plt.gcf()
        figure.set_size_inches(16, 9)

        plt.clf()
    except Exception as e:
        print("Error in creation of total deaths figure: " + str(e))

    print("--- Completed U.S. Data in %s seconds ---" % (time.time() - start_time))     # ~ 2.0 secs


def state_data():
    states = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "DC": "District of Colombia",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming"}

    data = {}

    url = "https://covidtracking.com/api/v1/states/daily.csv"
    df = pd.read_csv(url)
    groups = df.groupby(pd.Grouper(key="state"))
    for name, group in groups:
        if name in ["AS", "GU", "PR", "MP", "VI"]:  # Skips US territories
            continue
        group = group[['date', 'state', 'positive', 'positiveIncrease', 'negative', 'negativeIncrease', 'pending',
                       'death', 'deathIncrease', 'hospitalizedCurrently', 'hospitalizedIncrease',
                       'hospitalizedCumulative', 'inIcuCurrently', 'inIcuCumulative', 'onVentilatorCurrently',
                       'onVentilatorCumulative', 'totalTestResults', 'totalTestResultsIncrease', 'totalTestsViral',
                       'positiveTestsViral', 'negativeTestsViral', 'recovered', 'dataQualityGrade', 'lastUpdateEt',
                       'dateModified', 'checkTimeEt', 'hospitalized', 'dateChecked', 'positiveCasesViral',
                       'deathConfirmed', 'deathProbable', 'fips', 'total', 'posNeg', 'hash', 'commercialScore',
                       'negativeRegularScore', 'negativeScore', 'positiveScore', 'score', 'grade']]
        group = group.drop(columns=['lastUpdateEt', 'dateModified', 'checkTimeEt', 'deathConfirmed', 'deathProbable',
                                    'dateChecked', 'hospitalized', 'hash', 'commercialScore', 'negativeRegularScore',
                                    'negativeScore', 'positiveScore', 'score', 'grade'])
        group['date'] = pd.to_datetime(group['date'].astype(str))
        group = group.set_index("date")
        group = group.iloc[::-1]

        adjusted_dates = dates.date2num(
            [datetime.strptime(d.date().strftime('%Y-%m-%d'), '%Y-%m-%d') for d in group.index.tolist()])

        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))
        ax.plot(
            adjusted_dates,
            group.positiveIncrease.rolling(
                window=7).mean(),
            color='red')
        ax.plot(
            adjusted_dates,
            group.hospitalizedCurrently.rolling(
                window=7).mean(),
            color='blue')
        ax.set_facecolor('lavender')
        ax.grid(b=True, axis='y', color='white')
        ax.set_ylabel("New Cases and Current Hospitalizations", fontsize=12)
        ax.set_xlabel("Dates", fontsize=12)

        ax2 = ax.twinx()
        ax2.plot(
            adjusted_dates,
            group.deathIncrease.rolling(
                window=7).mean(),
            color='black')
        ax2.set_ylabel("Daily Deaths", fontsize=12)

        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 7))

        ax.tick_params(axis='x', labelsize=8)

        plt.title(states[name] + ' - New Daily Cases, Deaths and Current Hospitalizations, 7 Day M.A.', fontsize=16)
        figure = plt.gcf()
        figure.legend(
            handles=[Line2D([0], [0], c='r', lw=2), Line2D([0], [0], c='b', lw=2), Line2D([0], [0], c='k', lw=2)],
            labels=['New Cases', 'Current Hospitalizations', 'New Deaths'],
            loc='upper left',
            frameon=True,
            ncol=1,
            bbox_to_anchor=(0.15, 0.85),
            shadow=True,
            prop={'size': 10})
        figure.set_size_inches(16, 9)
        data[name] = figure

        plt.clf()
        plt.close('all')

    return data


if __name__ == '__main__':
    start_time = time.time()
    curr_date = str(date.today())
    delta = (datetime.today() - datetime.strptime("2020-03-15", "%Y-%m-%d")).days

    # us_data()
    figures = state_data()
    plt.show(figures['VA'])

    print("--- Completed State Data in %s seconds ---" % (time.time() - start_time))     # ~ 3.0 secs
    print("--- Finished in %s seconds ---" % (time.time() - start_time))
