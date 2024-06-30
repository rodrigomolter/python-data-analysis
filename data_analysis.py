import sys
import matplotlib.pyplot as plt

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

  single_country = list(get_user_countries(1, "Select a country to visualize the plot: ", emissions_without_year.keys()))[0]
  plot_emissions_by_country(single_country, emissions)

  two_countries = list(get_user_countries(2, "Write two comma-separated countries for which you want to visualize the data: ", emissions_without_year.keys()))
  plot_emissions_by_two_countries(two_countries, emissions)

  three_countries = list(get_user_countries(3, "Write up three comma-separated countries for which you want to extract the data: ", emissions_without_year.keys()))
  extract_data_to_subset(three_countries, emissions)

def read_file(path: str) -> dict:
  emissions = dict()
  try:
    with open(path, 'rt') as file:
      for row in file.readlines():
        data = row.replace('\n', '').split(',')
        emissions.update({ data[0]: data[1:] })
  except FileNotFoundError:
    print(f"File {path} not found....")
  except IOError:
    print(f"Could not read the file in {path}")
    
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


def get_user_countries(country_amount: int, message: str, countries_list: dict):
  haveValidCountryAnswer = False
  havePrintedCountryList = False
  while not haveValidCountryAnswer:
    user_input = input(message)

    for country in user_input.split(','):
      country = country.strip().capitalize()

      if len(user_input.split(',')) != country_amount:
        print(f"ERR: Sorry, at most {country_amount} countries can be entered, separeted by comma.")
        break
      elif country not in countries_list:
        print("Country not found, please use a country from our list.") 
        if not havePrintedCountryList:
          print(f"Avaiables Countries: {list(countries_list)}")
          havePrintedCountryList = True
        break

      haveValidCountryAnswer = True
      yield country


def plot_emissions_by_country(country: str, emissions: dict) -> None:
  fig, ax = plt.subplots()
  values = [float(value) for value in emissions.get(country)]
  years = [int(year) for year in emissions.get("CO2 per capita")]
  ax.plot(years, values)

  ax.set_title("Year vs Emission in Capita")
  ax.set_xlabel("Year")
  ax.set_ylabel(f"Emissions in {country}")

  plt.show()

def plot_emissions_by_two_countries(countries: list, emissions: dict) -> None:
  fig, ax = plt.subplots()
  values_one = [float(value) for value in emissions.get(countries[0].capitalize())]
  values_two = [float(value) for value in emissions.get(countries[1].capitalize())]
  years = [int(year) for year in emissions.get("CO2 per capita")]

  ax.plot(years, values_one, label=countries[0])
  ax.plot(years, values_two, label=countries[1])

  ax.set_title("Year vs Emission in Capita")
  ax.set_xlabel("Year")
  ax.set_ylabel(f"Emissions in {countries[0]} and {countries[1]}")
  ax.legend()

  plt.show()


def extract_data_to_subset(countries: list, emissions: dict) -> None:
  try:
    with open('Emissions_subset.csv', 'w') as file:
      file.write(f"CO2 per capita,{','.join(emissions.get('CO2 per capita'))}")
      for country in countries:
        file.write(f"\n{country},{','.join(emissions.get(country))}")
    print("Data exported to Emissions_subset.csv")
  except IOError:
    print(f"Error: Could not save the file.")

if __name__ == "__main__":
  main()