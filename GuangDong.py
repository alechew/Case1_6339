import Classes
import numpy
import random
import statistics

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
    ofile = open(filename + "_Generated-Random-Demand-Originating Sample City.csv", "wb")

    # writing the title of the columns
    row = "Year,Month,Day,Demand\n"
    ofile.write(row)

    for j in range(0, len(eachYearDailyDemandList),1):
        theYearDemand = eachYearDailyDemandList[j]

        for i in range(0, len(theYearDemand), 1):
            day = theYearDemand[i]
            if isinstance(day, Classes.DailyDemand):
                row = day.year + "," + day.week + "," + day.day + "," + str(day.dailyDemand) + "\n"
            ofile.write(row)
        ofile.write("\n")
    ofile.close()


def generate_beta_monthly(index):
    """generates weekly demand ratio following normal distribution with
     mean and standard deviation for its respective year"""

    return numpy.random.normal(monthlyDemandAverage[index], monthlyDemandStandardDeviation[index])


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


# this is where all starts might need a for loop or a system that will read a csv file to generate all demand.
CityDemand = Classes.CityDemandDetails("2020", "Zhengzhou", [4277842.33, 4287270.71, 4295139.94, 4301538.86, 4306593.06,
                                                            4310391.36,	4313001.17, 4314462.29])  # MODIFY THIS VARIABLE

print "hello"
# Generate yearly random demands;
count = 0
# while count <= years:
#     # if statement to only use triangular distribution after the initial first year.
#     if count > 0:
#         demand = demandDistribution.generate_random_demand()
#     yearlyDemand.append(demand)
#     count = count + 1



# here we calculate the daily demand
for x in range(years):
    if x > 0:
        eachYearDailyDemandList.append(dailyDemandList)

    dailyDemandList = []
    for i in range(months):
        beta = generate_beta_monthly(i)
        monthDemand = beta * yearlyDemand[x]
        monthlyDemand.append(monthDemand)

        rangeOfDaysInMonth = monthInYear[i].totalDays
        firstDay = monthInYear[i].firstDayNumberinWeek
        j = firstDay
        totalIterations = firstDay + rangeOfDaysInMonth

        while j < totalIterations:
            dayOfWeek = j % 7

            raw = generate_raw(dayOfWeek)

            singleDayDemand = round(monthlyDemand[i] * raw, 0)
            dailyDemand = Classes.DailyDemand(yearName[x], str(i + 1), dayName[dayOfWeek], yearlyDemand[x], monthlyDemand[i]
                                              , singleDayDemand, x, i, dayOfWeek)
            dailyDemandList.append(dailyDemand)
            j = j + 1



# outputs in console the daily demand generated for each year
count = 1
for day in dailyDemandList:
    if isinstance(day, Classes.DailyDemand):
        print("Year: " + day.year + ", " + day.week + ", " + day.day + ", " + str(day.dailyDemand))
        if count % 365 == 0:
            print("\n")
    count += 1

write_to_file()


