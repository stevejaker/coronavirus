#!/usr/bin/env python3

import os
import sys
import random
import requests
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

class CovidTracker(object):
    """
    """
    def __init__(self, cli_args=None):
        """
        Default setup for
        """
        self.base_url = "https://covidtracking.com/api/v1"
        self.url = None
        self.data_type_list = ['state', 'national']
        self.style_options = ['default', 'seaborn']

        self.delim = ','
        self.date = "daily"
        self.data_type = 'state'
        self.state = 'ut'
        self.colors = {
            "aqua": {
                "is_used": False,
                "color_type": "good"
            },
            "aquamarine": {
                "is_used": False,
                "color_type": "good"
            },
            "azure": {
                "is_used": False,
                "color_type": "good"
            },
            "beige": {
                "is_used": False,
                "color_type": "neutral"
            },
            "black": {
                "is_used": False,
                "color_type": "neutral"
            },
            "blue": {
                "is_used": False,
                "color_type": "good"
            },
            "brown": {
                "is_used": False,
                "color_type": "neutral"
            },
            "chartreuse": {
                "is_used": False,
                "color_type": "good"
            },
            "chocolate": {
                "is_used": False,
                "color_type": "neutral"
            },
            "coral": {
                "is_used": False,
                "color_type": "bad"
            },
            "crimson": {
                "is_used": False,
                "color_type": "bad"
            },
            "cyan": {
                "is_used": False,
                "color_type": "good"
            },
            "darkblue": {
                "is_used": False,
                "color_type": "good"
            },
            "darkgreen": {
                "is_used": False,
                "color_type": "good"
            },
            "fuchsia": {
                "is_used": False,
                "color_type": "bad"
            },
            "gold": {
                "is_used": False,
                "color_type": "neutral"
            },
            "goldenrod": {
                "is_used": False,
                "color_type": "neutral"
            },
            "green": {
                "is_used": False,
                "color_type": "good"
            },
            "grey": {
                "is_used": False,
                "color_type": "neutral"
            },
            "indigo": {
                "is_used": False,
                "color_type": "good"
            },
            "ivory": {
                "is_used": False,
                "color_type": "neutral"
            },
            "khaki": {
                "is_used": False,
                "color_type": "neutral"
            },
            "lavender": {
                "is_used": False,
                "color_type": "neutral"
            },
            "lightblue": {
                "is_used": False,
                "color_type": "good"
            },
            "lightgreen": {
                "is_used": False,
                "color_type": "good"
            },
            "lime": {
                "is_used": False,
                "color_type": "good"
            },
            "magenta": {
                "is_used": False,
                "color_type": "bad"
            },
            "maroon": {
                "is_used": False,
                "color_type": "bad"
            },
            "navy": {
                "is_used": False,
                "color_type": "good"
            },
            "olive": {
                "is_used": False,
                "color_type": "neutral"
            },
            "orange": {
                "is_used": False,
                "color_type": "bad"
            },
            "orangered": {
                "is_used": False,
                "color_type": "bad"
            },
            "orchid": {
                "is_used": False,
                "color_type": "neutral"
            },
            "pink": {
                "is_used": False,
                "color_type": "bad"
            },
            "plum": {
                "is_used": False,
                "color_type": "neutral"
            },
            "purple": {
                "is_used": False,
                "color_type": "neutral"
            },
            "red": {
                "is_used": False,
                "color_type": "bad"
            },
            "salmon": {
                "is_used": False,
                "color_type": "bad"
            },
            "sienna": {
                "is_used": False,
                "color_type": "neutral"
            },
            "silver": {
                "is_used": False,
                "color_type": "neutral"
            },
            "tan": {
                "is_used": False,
                "color_type": "good/bad/neutral"
            },
            "teal": {
                "is_used": False,
                "color_type": "neutral"
            },
            "tomato": {
                "is_used": False,
                "color_type": "bad"
            },
            "turquoise": {
                "is_used": False,
                "color_type": "good"
            },
            "violet": {
                "is_used": False,
                "color_type": "neutral"
            },
            "wheat": {
                "is_used": False,
                "color_type": "neutral"
            },
            "white": {
                "is_used": False,
                "color_type": "neutral"
            },
            "yellow": {
                "is_used": False,
                "color_type": "neutral"
            },
            "yellowgreen": {
                "is_used": False,
                "color_type": "good"
            }
        }

        self.loadDefaults()
        if cli_args is not None or len(cli_args) > 1:
            self.processCliArgs(cli_args)
        else:
            print('Running with only Default Values')

    def loadDefaults(self):
        # Default Printing and Plotting Arguments
        self.plot_all = False
        self.plot = False
        self.print_all = False
        self.print = False

        # Argument for handling the last # of data points to print
        self.modifier = None

        # Plotting formatting
        self.chart_title = "Utah COVID-19 Cases\nData sources: https://covidtracking.com/api (via https://coronavirus-dashboard.utah.gov/)"
        self.y_axis_title = "Total Cases"
        self.x_axis_title = "Date"
        self.legend_location = "upper left"
        self.style = 'default'
        self.index_vals = []
        self.x_index = [] # IDX for labeling the x axis (Dates)
        self.x_labels = [] # Dates to place on the x axis
        self.width = 0.8 # Approx width of the bars
        self.num_dates = 5 # Total Number of dates printed on plot
        self.length = 12 # Length of the graph in inches
        self.height = 6 # Length of the graph in inches
        self.figsize = (self.length, self.height) # Tuple passed to plt.figure()

        # Full Parsed Data
        #   This data will be processed and placed in chronological order
        self.data = {
            "dates":{
                "data": np.array([], dtype='object'),
                "title": "Dates",
                "plot": False,
                "print": False,
                "is_plottable": False,
                "is_printable": True,
            },
            "active_cases":{
                "data": np.array([], dtype='int64'),
                "title": "Active Cases",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["active_cases", "ac"]
            },
            "negative":{
                "data": np.array([], dtype='int64'),
                "title": "Negative Cases",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "green",
                "color_type": "good",
                "keywords": ["negative", "ng"]
            },
            "hospitalized":{
                "data": np.array([], dtype='int64'),
                "title": "Currently Hospitalized",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["hospitalized", "ch"]
            },
            "total_hospitalized":{
                "data": np.array([], dtype='int64'),
                "title": "Total Hospitalized",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["total_hospitalized", "th"]
            },
            "in_icu":{
                "data": np.array([], dtype='int64'),
                "title": "Currently in ICU",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["in_icu", "ci"]
            },
            "total_in_icu":{
                "data": np.array([], dtype='int64'),
                "title": "Total in ICU",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["total_in_icu", "ti"]
            },
            "on_ventilator":{
                "data": np.array([], dtype='int64'),
                "title": "New on Ventilator",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["on_ventilator", "cv"]
            },
            "total_on_ventilator":{
                "data": np.array([], dtype='int64'),
                "title": "Total on Ventilator",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["total_on_ventilator", "tv"]
            },
            "total_recovered":{
                "data": np.array([], dtype='int64'),
                "title": "Total Recovered",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "green",
                "color_type": "green",
                "keywords": ["total_recovered", "tr"]
            },
            "total_deaths":{
                "data": np.array([], dtype='int64'),
                "title": "Total Deaths",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["total_deaths", "td"]
            },
            "total_tested":{
                "data": np.array([], dtype='int64'),
                "title": "Total Tested",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "goldenrod",
                "color_type": "neutral",
                "keywords": ["total_tested", "tt"]
            },
            "pos_neg":{
                "data": np.array([], dtype='int64'),
                "title": "Pos/Neg",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "goldenrod",
                "color_type": "neutral",
                "keywords": ["pos_neg", "pn"]
            },
            "new_deaths":{
                "data": np.array([], dtype='int64'),
                "title": "New Deaths",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["new_deaths", "nd"]
            },
            "new_hospitalized":{
                "data": np.array([], dtype='int64'),
                "title": "New Hospitalized",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["new_hospitalized", "nh"]
            },
            "new_cases":{
                "data": np.array([], dtype='int64'),
                "title": "New Cases",
                "plot": False,
                "print": False,
                "is_plottable": True,
                "is_printable": True,
                "bottom": None,
                "color": "red",
                "color_type": "bad",
                "keywords": ["new_cases", "nc"]
            }
        }

    def processCliArgs(self, cli_args): #DONE
        for i, arg in enumerate(cli_args):
            if arg in ['-h', '--help']: # Prints this message and exits
                self.help()

            elif arg in ['-all', '--printall']: # Prints all data
                self.print_all = True

            elif arg in ['-p', '--plot']:
                print("Non Functional, Yo...")
                opt = cli_args[i+1].lower()
                if opt == '':
                    pass

            elif '--plot=' in arg or '--print=' in arg: # Toggles custom plotting.
                bottom = None
                typ = "print" if "print" in arg else "plot"
                if typ == "print":
                    self.print = True
                else:
                    self.plot = True
                idx = arg.rfind('=') + 1
                opts = arg[idx:]
                if self.delim in opts:
                    opts = opts.strip().split(self.delim)
                else:
                    opts = [opts]
                for opt in opts:
                    # Adding colors is not set up quite yet
                    self.processFlag(opt, typ, color=None)
                    # if self.stack_bars:
                    #     if bottom is not None:
                    #         bottom = f", {opt}"
                    #     else:
                    #         bottom = opt

            elif arg in ['-l', '--last']: # Declares the last # of data points to print
                val = cli_args[i+1]
                try:
                    if "last" in val:
                        val = val.replace("last", "")
                    self.modifier = int(val) * -1
                except:
                    sys.exit(f"ERROR with `{arg}`: {val} is not a valid integer.")

            elif arg in ['-nd', '--num_dates']: # Declares the number of dates to print on plot
                try:
                    self.num_dates = int(cli_args[i+1])
                except:
                    sys.exit(f"ERROR with `{arg}`: {cli_args[i+1]} is not a valid integer.")

            elif arg in ['-D', '--delim']: # Sets custom delimiter (Must be declared first) Default delimiter is ','
                self.delim = ','

            elif arg in ['-S', '--state']: # Declares state (Default: 'UT')
                self.state = cli_args[i+1].lower()

            elif arg in ['-yt', '--y-title']: # Declares Y Axis Title
                self.y_axis_title = cli_args[i+1]

            elif arg in ['-xt', '--x-title']: # Declares X Axis Title
                self.x_axis_title = cli_args[i+1]

            elif arg in ['-L', '--legend']: # Declares the graph's legend location
                self.legend_location = cli_args[i+1]

            elif arg in ['-s', '--style']: # Declares the style of the graph
                self.style = cli_args[i + 1]
                if self.style not in self.style:
                    sys.exit(f"ERROR with `{arg}`: {self.style_options} is not a valid style.")

            elif arg in ['-w', '--width']: # Declares width of the bar graphs
                try:
                    self.width = float(cli_args[i+1])
                except:
                    sys.exit(f"ERROR with `{arg}`: {cli_args[i+1]} is not a valid number.")

            elif arg in ['-dt', '--data-type']: # Declares whether you want state/national data
                self.data_type = cli_args[i + 1]
                if self.data_type not in self.data_type_list:
                    sys.exit(f"ERROR with `{arg}`: {self.data_type} is not a valid data type.")

            elif arg in ['-d', '--date']: # Declares the specific date
                date = cli_args[i + 1]
                self.plot_all = False # Don't plot if it's only one date

            elif arg in ['-df',  '--date-format']: # Declares the date format (Default: YYYYDDMM)
                print("Not Functional Yet")
                pass

            elif arg in ['-xy', '--size']: # Declares length & height of the graph window
                try:
                    x, y = cli_args[i+1].split('x')
                    self.length = float(x)
                    self.height = float(y)
                except:
                    sys.exit(f"ERROR with `{arg}`: {cli_args[i+1]} must have format 3x5.")

    def processFlag(self, opt, typ, color=None, bottom=None):
        if opt in self.data["active_cases"]["keywords"]:
            self.setPrintPlotInfo("active_cases", typ, color=color, bottom=bottom)

        elif opt in self.data["negative"]["keywords"]:
            self.setPrintPlotInfo("negative", typ, color=color, bottom=bottom)

        elif opt in self.data["hospitalized"]["keywords"]:
            self.setPrintPlotInfo("hospitalized", typ, color=color, bottom=bottom)

        elif opt in self.data["total_hospitalized"]["keywords"]:
            self.setPrintPlotInfo("total_hospitalized", typ, color=color, bottom=bottom)

        elif opt in self.data["in_icu"]["keywords"]:
            self.setPrintPlotInfo("in_icu", typ, color=color, bottom=bottom)

        elif opt in self.data["total_in_icu"]["keywords"]:
            self.setPrintPlotInfo("total_in_icu", typ, color=color, bottom=bottom)

        elif opt in self.data["on_ventilator"]["keywords"]:
            self.setPrintPlotInfo("on_ventilator", typ, color=color, bottom=bottom)

        elif opt in self.data["total_on_ventilator"]["keywords"]:
            self.setPrintPlotInfo("total_on_ventilator", typ, color=color, bottom=bottom)

        elif opt in self.data["total_recovered"]["keywords"]:
            self.setPrintPlotInfo("total_recovered", typ, color=color, bottom=bottom)

        elif opt in self.data["total_deaths"]["keywords"]:
            self.setPrintPlotInfo("total_deaths", typ, color=color, bottom=bottom)

        elif opt in self.data["total_tested"]["keywords"]:
            self.setPrintPlotInfo("total_tested", typ, color=color, bottom=bottom)

        elif opt in self.data["pos_neg"]["keywords"]:
            self.setPrintPlotInfo("pos_neg", typ, color=color, bottom=bottom)

        elif opt in self.data["new_deaths"]["keywords"]:
            self.setPrintPlotInfo("new_deaths", typ, color=color, bottom=bottom)

        elif opt in self.data["new_hospitalized"]["keywords"]:
            self.setPrintPlotInfo("new_hospitalized", typ, color=color, bottom=bottom)

        elif opt in self.data["new_cases"]["keywords"]:
            self.setPrintPlotInfo("new_cases", typ, color=color, bottom=bottom)

    def setPrintPlotInfo(self, kwd, typ, color=None, bottom=None):
        if typ == 'print':
            if self.data[kwd]["is_printable"]:
                self.data[kwd]["print"] = True
        else:
            if self.data[kwd]["is_plottable"]:
                self.data[kwd]["plot"] = True
                if bottom is not None:
                    self.data[kwd]["bottom"] = bottom
        if color:
            self.data[kwd]["color"] = color

    def generateRandomColor(self, kwd):
        possible_colors = []
        for color, data in self.colors.items():
            if not data["is_used"] and data["color_type"] == self.data[kwd]["color_type"]:
                possible_colors.append(color)
        color = random.choice(possible_colors)
        self.data[kwd]["color"] = color
        self.setColorAsUsed(color)

    def setColorAsUsed(self, color):
        self.colors[color]["is_used"] = True

    def setFigsize(self): #DONE
        figsize = (self.length, self.height)

    def setStyle(self): #DONE
        mpl.style.use(self.style)

    def insert(self, dct, kwd, value_kwd, pos=0): #DONE
        value = self.getVal(dct, value_kwd)
        if kwd == 'dates':
            value = self.formatDate(value)
        self.data[kwd]['data'] = np.insert(self.data[kwd]['data'], pos, value)

    def makeRequest(self, method='GET', return_type='json'): #DONE
        if self.url is None:
            self.generateUrl()
            # sys.exit("Error: No URL is set!")
        if method == 'POST':
            r = requests.post(self.url)
        else:
            r = requests.get(self.url)
        if r.status_code != 200:
            print("ERROR: Status code is not 200")
        if return_type == 'json':
            return r.json()
        if return_type == 'text':
            return r.text
        else:
            return r

    def generateUrl(self, format='json'): #DONE
        # Comment Line
        if self.data_type == 'national':
            self.url = f"{self.base_url}/us/{self.date}.{self.format}"
        else:
            self.url = f"{self.base_url}/states/{self.state}/{self.date}.{format}"

    def formatDate(self, date, include_year=False): #DONE
        date = str(date)
        if include_year:
            return f"{date[4:6]}/{date[6:]}/{date[:4]}"
        else:
            return f"{date[4:6]}/{date[6:]}"

    def getVal(self, dct, kwd): #DONE
        # Comment Line
        if kwd not in dct:
            return 0
        else:
            return dct[kwd] or 0

    def parse(self, data): #DONE?
        # Comment Line
        if type(data) is dict:
            data = [data]
        for d in data:
            self.insert(d, "dates", "date")
            self.insert(d, "active_cases", "positive")
            self.insert(d, "negative", "negative")
            self.insert(d, "hospitalized", "hospitalizedCurrently")
            self.insert(d, "total_hospitalized", "hospitalizedCumulative")
            self.insert(d, "in_icu", "inIcuCurrently")
            self.insert(d, "total_in_icu", "inIcuCumulative")
            self.insert(d, "on_ventilator", "onVentilatorCurrently")
            self.insert(d, "total_on_ventilator", "onVentilatorCumulative")
            self.insert(d, "total_recovered", "recovered")
            self.insert(d, "total_deaths", "death")
            self.insert(d, "total_tested", "total")
            self.insert(d, "pos_neg", "posNeg")
            self.insert(d, "new_deaths", "deathIncrease")
            self.insert(d, "new_hospitalized", "hospitalizedIncrease")
            self.insert(d, "new_cases", "positiveIncrease")

    def printDataOLD(self, data): # Don't run this yet. It doesn't work...
        if print_total or print_current or print_accum or print_all:
            print(f"Date: {date}")
        if print_total or print_all:
            print(f"""TOTALS:
    Total Positive:         {positive}
    Total Deaths:           {deaths}
    Total Recovered:        {recovered}
    Total Hospitalized:     {hospitalized}
    Total ICU:              {inIcuCumulative}
    Total Ventilator:       {onVentilatorCumulative}
""")
        if print_current or print_all:
            print(f"""Current:
    Currently Hospitalized: {hospitalizedCurrently}
    In ICU:                 {inIcuCurrently}
""")
        if print_accum or print_all:
            print(f"""Accumulators:
    On Ventilator:          {onVentilatorCurrently}
    New Deaths:             {deathIncrease}
    New Hospitalized:       {hospitalizedIncrease}
    New Cases:              {positiveIncrease}
""")

    def formatAxis(self): #DONE
        # Comment Line
        dates = self.data["dates"]["data"]
        self.setIndexValues()
        self.x_index = []
        self.x_labels = []
        l = len(self.index_vals)
        idx = [(l*i)//(self.num_dates - 1) for i in range(self.num_dates - 1)]
        idx.append(-1)
        for i in idx:
            self.x_index.append(self.index_vals[i])
            self.x_labels.append(dates[i])

    def applyModifier(self): #DONE
        if self.modifier is not None:
            if self.modifier * -1 < len(self.data["dates"]["data"]):
                for k, v in self.data.items():
                    self.data[k]["data"] = v["data"][self.modifier:]

    def setIndexValues(self): #DONE
        self.index_vals = [x for x, _ in enumerate(self.data["dates"]["data"])]

    def addBar(self, data, label, color, bottom):
        plt.bar(self.index_vals, data, width=self.width, label=label, color=color, bottom=bottom)

    def plotData(self): #DONE?
        # print(self.data)
        self.setStyle()
        self.formatAxis()
        plt.figure(figsize=self.figsize)
        for kwd, data in self.data.items():
            # print(f"{kwd:<25}{data['is_plottable']}\t{data['plot']}")
            if data["is_plottable"] and data["plot"]:
                # Plot data
                color = data["color"]
                if not self.colors[color]["is_used"]:
                    self.setColorAsUsed(color)
                else:
                    self.generateRandomColor(kwd)
                    print()
                self.addBar(data["data"], data["title"], data["color"], data["bottom"])
        plt.xticks(self.x_index, self.x_labels)
        plt.ylabel(self.y_axis_title)
        plt.xlabel(self.x_axis_title)
        plt.legend(loc=self.legend_location)
        plt.title(self.chart_title)
        plt.show()

    def printData(self): # NOT FUNCTIONAL
        for kwd, data in self.data.items():
            if data["is_printable"] and data["print"]:
                # Print Data
                # print(f"{data["title"]}: {data[""]}")
                pass

    def run(self):
        self.generateUrl()
        json_data = Tracker.makeRequest()
        self.parse(json_data)
        self.applyModifier()
        if self.plot:
            self.plotData()
        if self.print:
            self.printData()

    def help(self):
        """
        Old Menu Crap
        Info:
            Utah went to YELLOW (low risk) status on
        """
        sys.exit("""Usage:
    `covid_tracker.py` tracks local COVID-19 information

Usage:
    python covid_tracker.py [options]

Help:
    -h,  --help                   Prints this message and exits

Options:
    -all, --printall              Prints all data
    -dt,  --data-type             Declares whether you want state/national data
    -d,   --date                  Declares the specific date
    -df,  --date-format           Declares the date format (Default: YYYYDDMM)
    -nd,  --num_dates             Declares the number of dates to print on plot
    -l,   --last                  Declares the last # of data points to print
    -p,   --plot                  Sets to plot the data in a bar graph
    -S,   --state                 Declares state (Default: 'UT')
    -xy,  --size                  Declares length & height of the graph window
        Required Format:          `length`x`height` where length & height are
                                  integers. Default is (12x6)

Advanced Plotting:
    -st,  --stack                 Toggles whether to stack bar graphs
    -L,   --legend                Declares the Graph's legend location
    -yt,  --y-title               Declares y Axis Title
    -xt,  --x-title               Declares X Axis Title
    -s,   --style                 Declares the style of the graph
    -w,   --width                 Declares width of the bar graphs
    -D,   --delim                 Sets custom delimiter (Default ',')
    --plot=<options>              Toggles custom plotting.
    Options Include:
        ac, active_cases          ng, negative
        ch, hospitalized          th, total_hospitalized
        ci, in_icu                ti, total_in_icu
        cv, on_ventilator         tv, total_on_ventilator
        tr, total_recovered       td, total_deaths
        tt, total_tested          pn, pos_neg
        nd, new_deaths            nh, new_hospitalized
        nc, new_cases


Examples:
    -all -l 30 --plot=nc      Prints all data, plots new cases for last 30 days
    --plot=nc                 Plots new cases only
    --plot=ac,tr,td           Plots active, recovered, and deaths

""")

if __name__ == '__main__':
    Tracker = CovidTracker(cli_args=sys.argv)
    Tracker.run()
