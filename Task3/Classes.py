import scipy.stats as stat
import numpy
import random
import statistics

# classes used in code.


class CityDemandDetails:
    year = ""
    city = ""
    populationList = []
    yearPConstraints = []
    yearTriangularMin = []
    yearTriangularAvg = []
    yearTriangularMax = []
    monthlyDemandAverage = []
    monthlyDemandStandardDeviation = []

    iterations = 0  # amount of times you have to forecast.
    iterationDic = {
        "2020": 8,
        "2021": 7,
        "2022": 6,
        "2023": 5
    }
    # variables made by me, they are not inputs.

    def generate_raw(self, pconstraint, min, average, max):
        """randomly generates daily demand ratio following triangular distribution"""

        p = random.uniform(0, 1)
        raw = 0
        if p <= pconstraint:
            raw = min + numpy.math.sqrt(p * (max - min) * (average - min))
        else:
            raw = max - numpy.math.sqrt((1 - p) * (max - min) * (max - average))

        return raw

    def __init__(self, year, city, populationList):
        self.year = year
        self.city = city
        self.populationList = populationList
        self.yearTriangularMin = [0.02, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17]
        self.yearTriangularAvg = [0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.2, 0.225]
        self.yearTriangularMax = [0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]
        self.monthlyDemandAverage = [0.05, 0.05, 0.06, 0.08, 0.10, 0.12, 0.16, 0.10, 0.08, 0.06, 0.05, 0.05, 0.04]
        self.monthlyDemandStandardDeviation = [0.01, 0.01, 0.012, 0.016, 0.02, 0.024, 0.032, 0.02, 0.016, 0.012, 0.01,
                                               0.01, 0.008]
        self.iterations = self.iterationDic.get(self.year)

        self.demandFromPopulation = []
        self.yearlyDemands = []

        # calculating the p values for the triangular distribution
        for i in range(len(self.yearTriangularAvg)):
            p_constraint = (self.yearTriangularAvg[i] - self.yearTriangularMin[i]) / \
                           (self.yearTriangularMax[i] - self.yearTriangularMin[i])
            self.yearPConstraints.append(p_constraint)

        # will use to calculate the annual growth demand.
        for j in range(self.iterations):
            raw = self.generate_raw(self.yearPConstraints[j],
            self.yearTriangularMin[j], self.yearTriangularAvg[j], self.yearTriangularMax[j])
            yeardemand = populationList[j] * raw

            # getting out the demand of nationals day and singles day
            nationalDayDemand = yeardemand * 0.12
            singlesDayDemand = yeardemand * 0.04
            yeardemand = yeardemand - nationalDayDemand - singlesDayDemand

            self.demandFromPopulation.append(yeardemand)
            year = YearDemand(str(int(self.year) + j), self.city, yeardemand, nationalDayDemand, singlesDayDemand)
            self.yearlyDemands.append(year)

class YearDemand:
    # this will contain all the information for that specific year.
    year = ""
    city = ""
    yearlyDemand = 0
    dailyDemand = []
    demandOfSegments = []
    currentIteration = 0
    nationalDayDemand = 0
    singlesDayDemand = 0
    productTotals = []

    def __init__(self, year, city, yearlyDemand, nationalday, singlesdaydemand):
        self.year = year
        self.city = city
        self.yearlyDemand = yearlyDemand
        self.nationalDayDemand = nationalday
        self.singlesDayDemand = singlesdaydemand


class ModelDetails:
    # class that will have the demand details for specific type of model

    model = ""
    min = 0
    avg = 0
    max = 0
    price = 0

    def __init__(self, model, min, average, max, price):
        self.model = model
        self.min = min
        self.avg = average
        self.max = max
        self.price = price


class Model:
    # will hold the information of that model demand of one day.
    # will be stored in the modelList for dayDemand. One for each product
    name = ""
    demand = 0
    price = 0

    def __init__(self, name, demand, price):
        self.name = name
        self.demand = demand


class DayDemand:

    day = 0
    segment = 0
    dayDemand = 0
    productsDemand = []

    def __init__(self, day, segment, dayDemand):
        self.day = day
        self.segment = segment
        self.dayDemand = dayDemand


class CityDistance:

    city = ""
    distance = 0
    avgTime = 0
    stdDev = 0

    def __init__(self, city, distance):
        self.city = city
        self.distance = distance
