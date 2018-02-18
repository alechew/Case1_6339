import scipy.stats as stat
import numpy
import random
import statistics

# classes used in code.


class CityDemandDetails:
    year = ""
    city = ""
    populationList = []
    demandFromPopulation = []
    yearPConstraints = []
    yearTriangularMin = []
    yearTriangularAvg = []
    yearTriangularMax = []
    monthlyDemandAverage = []
    monthlyDemandStandardDeviation = []
    iterations = 0  # amount of times you have to forecast.
    iterationDic = {
        "2020": 9,
        "2021": 8,
        "2022": 7,
        "2023": 6
    }

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
        self.yearTriangularMin = [0.02, 0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.2]
        self.yearTriangularAvg = [0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.2, 0.225]
        self.yearTriangularMax = [0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]
        self.monthlyDemandAverage = [0.05, 0.05, 0.06, 0.08, 0.10, 0.12, 0.16, 0.10, 0.08, 0.06, 0.05, 0.05, 0.04]
        self.monthlyDemandStandardDeviation = [0.01, 0.01, 0.012, 0.016, 0.02, 0.024, 0.032, 0.02, 0.016, 0.012, 0.01,
                                               0.01, 0.008]
        self.iterations = self.iterationDic.get(self.year)

        # calculating the p values for the triangular distribution
        for i in range(len(self.yearTriangularAvg)):
            p_constraint = (self.yearTriangularAvg[i] - self.yearTriangularMin) / \
                           (self.yearTriangularMax[i] - self.yearTriangularMin[i])
            self.yearPConstraints.append(p_constraint)

        # will use to calculate the annual growth demand.
        for i in range(self.iterations):
            yeardemand = populationList[i]
            if i > 0:
                yeardemand = populationList[i - 1] * self.generate_raw(self.yearPConstraints[i - 1],
                self.yearTriangularMin[i - 1], self.yearTriangularAvg[i - 1], self.yearTriangularMax[i - 1])

        self.demandFromPopulation.append(yeardemand)


class YearDemand:
    # this will contain all the information for that specific year.
    year = ""
    city = ""
    yearlyDemand = 0
    dailyDemand = []
    currentIteration = 0

    def __init__(self, year, city, yearlyDemand):
        self.year = year
        self.city = city
        self.yearlyDemand = yearlyDemand


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

    def __init__(self, name, demand):
        self.name = name
        self.demand = demand























# commented out
# class DayDemand:
#     # class that will have the demand information of one day.
#     # will hold all the products demands for that one day of the year
#     year = "2018"
#     period = "1"
#     city = ""
#     yearlyDemand = 0
#     periodDemand = 0
#     dailyDemand = 0
#     modelList = []
#
#     def __init__(self, year, city, period, yearlyDemand, periodDemand, dailyDemand, modelList):
#         self.year = year
#         self.period = period
#         self.city = city
#         self.yearlyDemand = yearlyDemand
#         self.periodDemand = periodDemand
#         self.dailyDemand = dailyDemand
#         self.modelList = modelList
#
#         # Define Demand
#         class DemandVar:
#             standard_Deviation = 0
#             mean = 0
#             demandGenerated = 0
#
#             def __init__(self, mean, standardDeviation):
#                 self.mean = mean
#                 self.standard_Deviation = standardDeviation
#
#             def generate_random_demand(self):
#                 self.demandGenerated = round(numpy.random.normal(self.mean, self.standard_Deviation), 0)
#                 return self.demandGenerated
#
#         # Target level we want to satisfy
#         class FactorySpecifications:
#             leadTimes = [30.0, 15.0, 10.0, 5.0, 2.0, 1.0, 0.5, 0.25, 0.1]
#             demandRequirements = [32549, 16802, 11472, 6041, 2658, 1466, 1658, 1932, 2480]
#             dailyCapacity = [1085, 1120, 1147, 1208, 1329, 1466, 1658, 1932, 2480]
#             serviceTargetLevel = 0.99
#             zNormalValue = zNormalValue = stat.norm.ppf(serviceTargetLevel)
#             numberDays = 364
#             numberScenarios = 100  # number Years we want to run
#             leadTime = 10
#             scenario = 0
#             scenarioValues = {30: 0,
#                               15: 1,
#                               10: 2,
#                               5: 3,
#                               2: 4,
#                               1: 5,
#                               0.5: 6,
#                               0.25: 7,
#                               0.1: 8}
#
#             def __init__(self):
#                 print("Creating the scenario foe the case")
#
#             def set_lead_time(self, leadtime):
#
#                 if leadtime >= 1:
#                     self.leadTime = leadtime
#                     self.scenario = self.scenarioValues.get(leadtime)
#                 elif leadtime == 0.5:
#                     self.leadTime = 1
#                     self.scenario = self.scenarioValues.get(0.5)
#                 elif leadtime == 0.25:
#                     self.leadTime = 1
#                     self.scenario = self.scenarioValues.get(0.25)
#                 else:
#                     self.leadTime = 1
#                     self.scenario = self.scenarioValues.get(0.1)
#
#                     # def calculate_capacity():
#                     #     demand_satisfaction_capacity = (meanInPeriod * orderToShipping / basePeriod) \
#                     #                                    + (zNormalValue * numpy.math.sqrt(
#                     #         stdDevInPeriod * orderToShipping / basePeriod))
#                     #     return demand_satisfaction_capacity
#
#         # Object that will have all the information of daily demand generated compared with our production capacity.
#         class DailyScenario:
#             demand = 0
#             demandSatisfied = 0
#             demandNotSatisfied = 0
#
#             def __init__(self):
#                 print("Daily Demand Scenario")
#
#         class DailyDemand:
#             year = "2018"
#             week = "1"
#             day = "Monday"
#             dayNumber = 0
#             weekNumber = 0
#             yearNumber = 0
#             yearlyDemand = 0
#             weeklyDemand = 0
#             dailyDemand = 0
#
#             def __init__(self, year, week, day, yearlyDemand, weeklyDemand, dailyDemand, yearindex, weekindex,
#                          dayindex):
#                 self.year = year
#                 self.week = week
#                 self.day = day
#                 self.yearlyDemand = yearlyDemand
#                 self.weeklyDemand = weeklyDemand
#                 self.dailyDemand = dailyDemand
#                 self.yearIndex = yearindex
#                 self.weekNumber = weekindex
#                 self.dayNumber = dayindex
#
#         class DayManufactured:
#             prevDayBacklog = 0
#             thisDayBackLog = 0
#             demand = 0
#             needToProduce = 0
#             produced = 0
#             inventory = 0
#             ordersToShip = 0
#             amountShipped = 0
#             demandUnfilled = 0
#             satisfactionPercentage = 0.00
#
#             def __init__(self, backlog, receivedDemand, inventory, orderstoship):
#                 self.prevDayBacklog = backlog
#                 self.needToProduce = self.prevDayBacklog + receivedDemand
#                 self.demand = receivedDemand
#                 self.inventory = inventory
#                 self.ordersToShip = orderstoship
#
#         class YearSummary:
#             yearDemand = "0"
#             totalCapacity = "0"
#             totalProduced = "0"
#             totalShipped = "0"
#             satisfactionLevel = "0"
#
#             def __init__(self, yeardemand, totalcapacity, totalproduced, totalshipped, satisfactionlevel):
#                 self.yearDemand = yeardemand
#                 self.totalCapacity = totalcapacity
#                 self.totalProduced = totalproduced
#                 self.totalShipped = totalshipped
#                 self.satisfactionLevel = satisfactionlevel
#
#         class FactorySpecificationsTask2:
#             leadTimes = []
#             yearlyDemandRequirements = []
#             yearlyStandardDeviations = []
#             dailyCapacity = []
#             serviceTargetLevel = 0.99
#             zNormalValue = zNormalValue = stat.norm.ppf(serviceTargetLevel)
#             numberDays = 365
#             numberScenarios = 6  # number Years we want to run
#             leadTime = 10
#             scenario = 0
#             scenarioValues = {15.0: 0,
#                               7.0: 1,
#                               5.0: 2,
#                               2.0: 3,
#                               1.0: 4}
#
#             def __init__(self, leadtimes, yearlyDemandRequirements, demandStandardDeviations, servicelevel,
#                          leadtimeselected):
#                 self.leadTimes = leadtimes
#                 self.yearlyDemandRequirements = yearlyDemandRequirements
#                 self.yearlyStandardDeviations = demandStandardDeviations
#                 self.serviceTargetLevel = servicelevel
#                 self.leadTime = leadtimeselected
#
#             def set_lead_time(self, leadtime):
#                 self.leadTime = leadtime
#                 self.scenario = self.scenarioValues.get(leadtime)
#
#         class MonthInfo:
#             totalDays = 0
#             firstDayNumberinWeek = 0
#
#             def __init__(self, daysItHas, firstDayInWeek):
#                 self.totalDays = daysItHas
#                 self.firstDayNumberinWeek = firstDayInWeek