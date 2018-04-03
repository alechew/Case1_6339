import csv
import random

import Classes
import numpy

filename = ""

yearName = ["2020", "2021", "2022", "2023", "2023", "2024", "2025", "2026", "2027"]
dayName = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

yearlyDemand = []     # this can be said is the mean of every new year demand

totalDaysInYear = 365
years = 9
months = 13
days = 7

monthlyDemand = []
monthlyDemandAverage = [0.05, 0.05, 0.06, 0.08, 0.10, 0.12, 0.16, 0.10, 0.08, 0.06, 0.05, 0.05, 0.04]
monthlyDemandStandardDeviation = [0.01, 0.01, 0.012, 0.016, 0.02, 0.024, 0.032, 0.02, 0.016, 0.012, 0.01, 0.01, 0.008]

# monthInYear = [Classes.MonthInfo(31, 0), Classes.MonthInfo(28, 3), Classes.MonthInfo(31, 3), Classes.MonthInfo(30, 6),
#                Classes.MonthInfo(31, 1), Classes.MonthInfo(30, 4), Classes.MonthInfo(31, 6), Classes.MonthInfo(31, 2),
#                Classes.MonthInfo(30, 5), Classes.MonthInfo(31, 0), Classes.MonthInfo(30, 3), Classes.MonthInfo(31, 5)]


dailyDemand = []
dailyDemandStandardDeviation = []

# yearly factors
yearPConstraints = []
yearTriangularMin = [0.02, 0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.2]
yearTriangularAvg = [0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.2, 0.225]
yearTriangularMax = [0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]


# here we will generate the demand for each product on the day.
productMin = [50]
productAvg = [80]
productMax = [110]
productPConstraint = [0.5]
productPrice = [2400,2400,2400,2400,3600,3600,3600,3600,3600,3600,4800,4800,4800,4800,6000,6000,6000,6000,6000,6000]

# productDictionary = {
#     0: "F10", 1: "K10", 2: "S10", 3: "W10", 4: "F20",
#     5: "K20", 6: "L20", 7: "S20", 8: "W20", 9: "X20",
#     10: "F30", 11: "K30", 12: "S30", 13: "W30", 14: "F50",
#     15: "K50", 16: "L50", 17: "S50", 18: "W50", 19: "X50"
# }

# for i in range(len(yearName)):
#     p_constraint = (yearTriangularAvg[i] - yearTriangularMin) / (yearTriangularMax[i] - yearTriangularMin[i]);
#     yearPConstraints.append(p_constraint)

# this contain the demand of everyday for every year as a single list. This gets later divided into their respective
# years.
dailyDemandList = []

# this is the mean and deviation of the generated daily random demands.
yearMeanOfRandomDemand = []
yearDeviationOfRandomDemand = []

# will have 5 list with the demand for every year iteration
eachYearDailyDemandList = []

ofile = open(filename + "time_from_warehouse_to_cityhub.csv", "wb")


def write_to_file():
    """writes on a CSV value the randomly generated daily demands from year 2018 to 2023
    """
    # ofile = open(filename + "CityDemands_9_test.csv", "wb")
    counter = 1
    for cities in listOfCities:
        print(str(counter))
        if isinstance(cities, Classes.CityDemandDetails):
            for years in cities.yearlyDemands:
                if isinstance(years, Classes.YearDemand):
                    title = cities.city + " " + years.year + "\n"
                    ofile.write(title)
                    columns = "Day," + "F10,K10,S10,W10,F20,K20,L20,S20,W20,X20,F30,K30,S30,W30,F50,K50,L50,S50,W50,X50\n"
                    ofile.write(columns)

                    totalsRow = "Totals,"
                    for h in range(len(years.productTotals)):
                        totalsRow = totalsRow + str(years.productTotals[h]) + ","

                    totalsRow = totalsRow + str(sum(years.productTotals))
                    ofile.write(totalsRow)
                    ofile.write("\n")
                    moneyPerModel = []
                    totalsPriceRow = "Total in Price,"
                    for d in range(len(years.productTotals)):
                        profit = years.productTotals[d] * productPrice[d]
                        moneyPerModel.append(profit)
                        totalsPriceRow = totalsPriceRow + str(profit) + ","

                    totalsPriceRow = totalsPriceRow + str(sum(moneyPerModel))
                    ofile.write(totalsPriceRow)
                    ofile.write("\n\n\n")
                    title = ""
        counter = counter + 1
    # for j in range(0, len(eachYearDailyDemandList),1):
    #     theYearDemand = eachYearDailyDemandList[j]
    #
    #     for i in range(0, len(theYearDemand), 1):
    #         day = theYearDemand[i]
    #         if isinstance(day, Classes.DailyDemand):
    #             row = day.year + "," + day.week + "," + day.day + "," + str(day.dailyDemand) + "\n"
    #         ofile.write(row)
    #     ofile.write("\n")
    ofile.close()


def generate_beta_monthly_backup(index):
    """generates weekly demand ratio following normal distribution with
     mean and standard deviation for its respective year"""

    return numpy.random.normal(monthlyDemandAverage[index], monthlyDemandStandardDeviation[index])

def generate_beta_monthly(monthlyaverage, standarddeviation):
    """generates weekly demand ratio following normal distribution with
     mean and standard deviation for its respective year"""

    return numpy.random.normal(monthlyaverage, standarddeviation)

def generate_raw(index):
    """randomly generates daily demand ratio following triangular distribution"""
    yearTriangularMin = []
    yearTriangularAvg = []
    yearTriangularMax = []
    
    p = random.uniform(0, 1)
    raw = 0
    if p <= yearPConstraints[index]:
        raw = yearTriangularMin[index] \
              + numpy.math.sqrt(p * (yearTriangularMax[index] - yearTriangularMin[index]) * (yearTriangularAvg[index] - yearTriangularMin[index]))
    else:
        raw = yearTriangularMax[index] \
              - numpy.math.sqrt((1 - p) * (yearTriangularMax[index] - yearTriangularMin[index]) * (yearTriangularMax[index] - yearTriangularAvg[index]))
    return raw


def generate_raw_product(pconstraint, min, average, max):
    """randomly generates daily demand ratio following triangular distribution"""

    p = random.uniform(0, 1)
    raw = 0
    if p <= pconstraint:
        raw = min + numpy.math.sqrt(p * (max - min) * (average - min))
    else:
        raw = max - numpy.math.sqrt((1 - p) * (max - min) * (max - average))

    return raw

def generate_raw_backup(index):
    """randomly generates daily demand ratio following triangular distribution"""
    p = random.uniform(0, 1)
    raw = 0
    if p <= yearPConstraints[index]:
        raw = yearTriangularMin[index] \
              + numpy.math.sqrt(p * (yearTriangularMax[index] - yearTriangularMin[index]) * (yearTriangularAvg[index] - yearTriangularMin[index]))
    else:
        raw = yearTriangularMax[index] \
              - numpy.math.sqrt((1 - p) * (yearTriangularMax[index] - yearTriangularMin[index]) * (yearTriangularMax[index] - yearTriangularAvg[index]))
    return raw


yearDictionary = {
    9: "2020",
    8: "2021",
    7: "2022",
    6: "2023",
}



listOfCities = []
# code to open the excel spreadsheet
with open('distaces_from_selected_warehouses.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        rowLength = len(row)
        populationList = map(float, row[1:rowLength])
        listOfCities.append(Classes.CityDistance(row[0], row[1]))

for cityDistance in listOfCities:
    # now here we will calculate the segments demands
    print cityDistance.city
    productDictionary = {
        0: {"time": [], "avg": 0, "std": 0},
    }

    theDistance = int(cityDistance.distance);
    # for loop that will run 100 scenarios per day per year
    for scenario in range(100):

        # theDay = dailyDemandListForYear[m]

        # generate the betas of the products to later normalize.
        for c in range(len(productDictionary)):
            speed = generate_raw_product(productPConstraint[c], productMin[c],
                                                          productAvg[c], productMax[c])
            productDictionary.get(c).get("time").append(theDistance/speed)

        avg = numpy.mean(productDictionary.get(0).get("time"))
        std = numpy.std(productDictionary.get(0).get("time"))
        productDictionary.get(0)["avg"] = (avg)
        productDictionary.get(0)["std"] = (std)

    cityDistance.avgTime = productDictionary.get(0).get("avg")
    cityDistance.stdDev = productDictionary.get(0).get("std")


# Writing to file now
title = "City" + "," + "Distance from Shenzhen" + "," + "Average Time" + "," + "Standard Deviation" "\n"
ofile.write(title)
for city in listOfCities:
    row = city.city + "," + str(city.distance) + "," + str(city.avgTime) + "," + str(city.stdDev) + "\n"
    ofile.write(row)

ofile.close()


# # outputs in console the daily demand generated for each year
# count = 1
# for day in dailyDemandList:
#     if isinstance(day, Classes.DailyDemand):
#         print("Year: " + day.year + ", " + day.week + ", " + day.day + ", " + str(day.dailyDemand))
#         if count % 365 == 0:
#             print("\n")
#     count += 1
#
#write_to_file()
