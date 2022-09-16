import operator

import matplotlib.pyplot as plt
import json

with open("deadge.json", 'r') as f:
    data = json.load(f)

# find total deaths per each month and each year
# find the average number of deaths per month
# find the average age of death

total_deaths = 0
people_counter = 0
avg_death_age = 0
avg_death_age_per_year = {}
total_deaths_per_month = {}
total_deaths_per_year = {}
deaths_per_month = {}
names_counter = {}
for month in data['1998'].keys():
    deaths_per_month[month] = 0

for year in data.keys():
    total_deaths_per_year[year] = 0
    avg_death_age_per_year[year] = 0
    yearly_deaths = 0
    yearly_death_age = 0
    yearly_people_death_counter = 0
    for month in data[year].keys():
        monthly_deaths = 0
        total_deaths_per_month[month + " " + year] = 0
        for day, deaths in data[year][month].items():
            num_deaths = len(deaths)
            monthly_deaths += num_deaths
            total_deaths += num_deaths
            for person in deaths:
                people_counter += 1
                yearly_people_death_counter += 1
                avg_death_age += int(person["age"])
                yearly_death_age += int(person["age"])

                name = person["name"].split(" ")[0]
                if name == "Sir":
                    name = person["name"].split(" ")[1]

                if name in names_counter.keys():
                    names_counter[name] += 1
                else:
                    names_counter[name] = 0

        yearly_deaths += monthly_deaths
        deaths_per_month[month] += monthly_deaths
        total_deaths_per_month[month + " " + year] = monthly_deaths
    # print(yearly_death_age, people_counter)
    total_deaths_per_year[year] = yearly_deaths
    avg_death_age_per_year[year] = yearly_death_age // yearly_people_death_counter

avg_death_age = avg_death_age // people_counter

print("Total deaths:", total_deaths)
print("Total deaths per year")
print(total_deaths_per_year)
"""print("Total deaths per month")
print(total_deaths_per_month)"""

avg_deaths_per_month = {key: value // len(deaths_per_month) for key, value in deaths_per_month.items()}
print("Avg deaths per month")
print(avg_deaths_per_month)

print("Avg death age")
print(avg_death_age)
print("Avg monthly death")
avg_monthly_deaths = sum(total_deaths_per_month.values()) // len(total_deaths_per_month.values())
print(avg_monthly_deaths)
print("Avg age of death per year:")
print(avg_death_age_per_year)

names_counter = sorted(names_counter.items(), reverse=True, key=operator.itemgetter(1))

x = total_deaths_per_year.keys()
y = total_deaths_per_year.values()

plt.plot(x, y)
plt.suptitle("Total deaths per year")
plt.xticks(rotation=90)
plt.show()

x = sorted([name for name, num in names_counter[:20]])
y = sorted([num for name, num in names_counter[:20]])
print(x, y)

plt.plot(x, y)
plt.suptitle("Most common death names")
plt.xticks(rotation=45)
plt.show()
