import Classes
import numpy
import random
import statistics
import csv

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
productMin = [.1, .05, .05, .05, .04, .03, .03, .02, .02, .02, .02, .01, .01, .01, .005, .005, .005, .005, .005, .005]
productAvg = [.17, .13, .10, .09, .08, .06, .05, .05, .04, .04, .03, .03, .03, .02, .02, .02, .01, .01, .01, .01]
productMax = [.20, .18, .15, .15, .12, .10, .10, .10, .08, .08, .08, .06, .06, .06, .06, .04, .04, .04, .04, .04]
productPConstraint = [0.7000000000000001, 0.6153846153846154, 0.5000000000000001, 0.39999999999999997, 0.5000000000000001,
     0.4285714285714285, 0.28571428571428575, 0.375, 0.33333333333333337, 0.33333333333333337, 0.16666666666666666,
     0.39999999999999997, 0.39999999999999997, 0.2, 0.2727272727272727, 0.4285714285714285, 0.14285714285714285,
     0.14285714285714285, 0.14285714285714285, 0.14285714285714285]
productPrice = [2400,2400,2400,2400,3600,3600,3600,3600,3600,3600,4800,4800,4800,4800,6000,6000,6000,6000,6000,6000]

productDictionary = {
    0: "F10", 1: "K10", 2: "S10", 3: "W10", 4: "F20",
    5: "K20", 6: "L20", 7: "S20", 8: "W20", 9: "X20",
    10: "F30", 11: "K30", 12: "S30", 13: "W30", 14: "F50",
    15: "K50", 16: "L50", 17: "S50", 18: "W50", 19: "X50"
}


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


def write_to_file():
    """writes on a CSV value the randomly generated daily demands from year 2018 to 2023
    """
    ofile = open(filename + "population_final_python", "wb")

    for cities in listOfCities:
        if isinstance(cities, Classes.CityDemandDetails):
            for years in cities.yearlyDemands:
                if isinstance(years, Classes.YearDemand):
                    title = cities.city + " " + years.year + "\n"
                    ofile.write(title)
                    columns = "Day," + "F10,K10,S10,W10,F20,K20,L20,S20,W20,X20,F30,K30,S30,W30,F50,K50,L50,S50,W50,X50\n"
                    ofile.write(columns)

                    for f in range(len(years.dailyDemand)):
                        theDailyDemand = years.dailyDemand[f]
                        if isinstance(theDailyDemand, Classes.DayDemand):
                            day = str(theDailyDemand.day) + ","
                            demand = ""
                            for g in range(len(theDailyDemand.productsDemand)):
                                product = theDailyDemand.productsDemand[g]
                                if isinstance(product, Classes.Model):
                                    demand = demand + str(product.demand) + ","
                                    if g == 19:
                                        demand = demand[:-1]
                            dayInput = day + demand + "\n"
                            ofile.write(dayInput)
                    ofile.write("\n\n\n")
                    title = ""

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
with open('testCSV.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        rowLength = len(row)
        populationList = map(float, row[1:rowLength])
        listOfCities.append(Classes.CityDemandDetails(yearDictionary[rowLength], str(row[0]), populationList))


# this is where all starts might need a for loop or a system that will read a csv file to generate all demand.
# it generates the annual demands and takes into account the national and singles days.
# cityDemand = Classes.CityDemandDetails("2020", "Zhengzhou", [4277842.33, 4287270.71, 4295139.94, 4301538.86, 4306593.06,
#                                                             4310391.36,	4313001.17, 4314462.29])  # MODIFY THIS VARIABLE

# now here is where
for cityDemand in listOfCities:
    # now here we will calculate the segments demands
    for v in range(len(cityDemand.yearlyDemands)):
        if isinstance(cityDemand.yearlyDemands[v], Classes.YearDemand):
            theYear = cityDemand.yearlyDemands[v]
            segmentDemands = []
            monthlyBetas = []
            for j in range(len(cityDemand.monthlyDemandAverage)):
                betaMonth = generate_beta_monthly(cityDemand.monthlyDemandAverage[j],
                                                                         cityDemand.monthlyDemandStandardDeviation[j])
                monthlyBetas.append(betaMonth)

            totalBetas = sum(monthlyBetas)
            for k in range(len(monthlyBetas)):
                segDemand = theYear.yearlyDemand * (monthlyBetas[k] / totalBetas) #normalizing
                segmentDemands.append(segDemand)

            normalizedSum = sum(segmentDemands)
            theYear.demandOfSegments = segmentDemands

        # now we calculate the daily demand of products.
        dailyDemandListForYear = []

        segment = 0
        dayDemand = theYear.demandOfSegments[segment] / 28
        for v in range(1, totalDaysInYear):

            if v % 29 == 0:
                segment = segment + 1
                dayDemand = theYear.demandOfSegments[segment] / 28

            day = Classes.DayDemand(v, segment + 1, dayDemand)
            dailyDemandListForYear.append(day)

        # day 274 = october first (national day) and day 315 = singles day(november 11)
        holiday = dailyDemandListForYear[273]
        if isinstance(holiday, Classes.DayDemand):
            holiday.dayDemand = holiday.dayDemand + theYear.nationalDayDemand

        holiday = dailyDemandListForYear[314]
        if isinstance(holiday, Classes.DayDemand):
            holiday.dayDemand = holiday.dayDemand + theYear.singlesDayDemand

        # now we generate the daily demand of the 20 products... for each day...
        for m in range(len(dailyDemandListForYear)):
            theDay = dailyDemandListForYear[m]
            dailyProductBetas = []
            productList = []
            dailyTotalBetas = 0

            # generate the betas of the products to later normalize.
            for c in range(len(productDictionary)):
                dailyProductBetas.append(generate_raw_product(productPConstraint[c], productMin[c],
                                                                            productAvg[c], productMax[c]))
            dailyTotalBetas = sum(dailyProductBetas)

            for n in range(len(productDictionary)):
                if isinstance(theDay, Classes.DayDemand):
                    productDemand = theDay.dayDemand * (dailyProductBetas[n] / dailyTotalBetas)
                    productList.append(Classes.Model(productDictionary[n], productDemand, productPrice[n]))

            theDay.productsDemand = productList

        theYear.dailyDemand = dailyDemandListForYear      # appending the demand of the 364 days of the year


# # outputs in console the daily demand generated for each year
# count = 1
# for day in dailyDemandList:
#     if isinstance(day, Classes.DailyDemand):
#         print("Year: " + day.year + ", " + day.week + ", " + day.day + ", " + str(day.dailyDemand))
#         if count % 365 == 0:
#             print("\n")
#     count += 1
#
write_to_file()
