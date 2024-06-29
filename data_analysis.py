import sys
import matplotlib.pyplot as plt
import numpy as np

"""
Name: Python Data Analysis
Purpose: Maximum and Minimum emission in Country + Average emission in year

Algorithm:

Step 1: Take the input from user
Step 2: Extracting index of the year
Step 3: Creating the list of emission in year
Step 4: Performing the analysis
Step 5: Printing the data in required format using formatted string

"""

def main():
  print("#"*30)
  print("Worlds CO2 Emission - Data avaible from 1997 to 2010")

  emissions = read_file('Emissions.csv')
  year = get_user_year()
  year_emissions = get_emissions_by_year(year, emissions)
  emissions_without_year = emissions.copy()
  emissions_without_year.pop("CO2 per capita")
  min = get_min_country(year_emissions, emissions_without_year.keys())
  max = get_max_country(year_emissions, emissions_without_year.keys())

  print(f"In {year}, countries with minimum and maximum CO2 levels were: {min[0]}({min[1]:.6f}) and {max[0]}({max[1]:.6f})")
  print(f"Average CO2 emissions in {year} were {get_average(year_emissions):.6f}")

  country = get_user_country(emissions_without_year.keys())
  plot_emissions_by_country(country, emissions)

def read_file(path: str) -> dict:
  emissions = dict()
  with open(path, 'rt') as file:
    for row in file.readlines():
      data = row.replace('\n', '').split(',')
      emissions.update({ data[0]: data[1:] })
    
  return emissions

def get_user_year() -> str:
  try:
    year = int(input("Inform a year to find statistics (1997 to 2010): "))
    if year < 1997 or year > 2010:
      raise ValueError
    return year
  except ValueError:
    sys.exit("Please, insert only numbers and between 1997 and 2010")

def get_emissions_by_year(user_year: int, emissions: dict) -> list:
  index = -1
  temp_list = emissions.copy()
  for i, year in enumerate(temp_list.pop('CO2 per capita')):
    if int(year) == user_year:
      index = i
      break
  
  emission_list = list()
  for value in temp_list.values():
    value = float(value[index])
    emission_list.append(value)

  return emission_list

def get_min_country(values: list, countries: dict) -> tuple:
  min_value = min(values)
  index = values.index(min_value)
  return (list(countries)[index], min_value)

def get_max_country(values: list, countries: dict) -> tuple:
  max_value = max(values)
  index = values.index(max_value)
  return (list(countries)[index], max_value)

def get_average(values: list) -> float:
  total = sum([x for x in values])
  return total/len(values)

def get_user_country(countries: dict) -> str:
  country = input("Select a country to visualize the plot: ").capitalize()
  
  while country not in countries:
    print("Country not found, please use a country from our list.") 
    print(f"Avaiables Countries: {list(countries)}")
    country = input("Select a country to visualize the plot: ").capitalize()

  return country

def plot_emissions_by_country(country: str, emissions: dict) -> None:
  fig, ax = plt.subplots()
  values = emissions.get(country)
  values = [float(value) for value in values]
  years = emissions.get("CO2 per capita")
  years = [int(year) for year in years]
  ax.set_title("Year vs Emission in Capita")
  ax.set_xlabel("Year")
  ax.set_ylabel(f"Emissions in {country}")
  ax.plot(years, values)
  plt.show()

if __name__ == "__main__":
  main()