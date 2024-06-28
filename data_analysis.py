import sys

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
  min = get_min_country(year_emissions, emissions.keys())
  max = get_max_country(year_emissions, emissions.keys())

  print(f"In {year}, countries with minimum and maximum CO2 levels were: {min[0]}({min[1]:.6f}) and {max[0]}({max[1]:.6f})")
  print(f"Average CO2 emissions in {year} were {get_average(year_emissions):.6f}")

def read_file(path: str) -> dict:
  emissions = dict()
  with open(path, 'rt') as file:
    for row in file.readlines():
      data = row.split(',')
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
  for i, year in enumerate(emissions.pop('CO2 per capita')):
    if year.replace('\n', '') == str(user_year):
      index = i
      break
  
  emission_list = list()
  for value in emissions.values():
    value = float(value[index].replace('\n', ''))
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

if __name__ == "__main__":
  main()