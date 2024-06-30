"""
  Name: Python Data Analysis

    - Reads data from the 'Emissions.csv' file.
    - Asks the user for a year and retrieves CO2 emissions for that year.
    - Identifies the countries with the minimum and maximum CO2 emissions for the selected year.
    - Calculates and displays the average CO2 emissions for the selected year.
    - Asks the user for a country to visualize a CO2 emissions plot.
    - Asks the user for two countries to visualize a comparative CO2 emissions plot.
    - Asks the user for three countries to extract a subset of data and save it to a CSV file.
"""

import sys
import matplotlib.pyplot as plt

def main():
    print("#" * 30)
    print("Worlds CO2 Emission - Data available from 1997 to 2010")

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
    """
    Reads a CSV file and returns a dictionary with CO2 emission data.

    Args:
        path (str): The path to the CSV file containing emission data.

    Returns:
        dict: A dictionary where the keys are country names and the values are lists of CO2 emissions.

    Raises:
        IOError: If there is an error while trying to read the CSV file.
        FileNotFoundError: If the file was not found in the given path
    """
    emissions = dict()
    try:
        with open(path, 'rt') as file:
            for row in file.readlines():
                data = row.replace('\n', '').split(',')
                emissions.update({data[0]: data[1:]})
    except FileNotFoundError:
        print(f"File {path} not found....")
    except IOError:
        print(f"Could not read the file in {path}")

    return emissions

def get_user_year() -> str:
    """
    Asks the user for a year and validates that it is within the range of 1997 to 2010.

    Returns:
        str: The year provided by the user.

    """
    is_year_valid = False
    while not is_year_valid:
      inputed_year = input("Inform a year to find statistics (1997 to 2010): ")
      try:
          year = int(inputed_year)
      except ValueError:
          print("Please, insert only numbers")
          continue
      if year < 1997 or year > 2010:
          print("Please, insert an year between 1997 and 2010.")
          continue
      is_year_valid = True
    return year

def get_emissions_by_year(user_year: int, emissions: dict) -> list:
    """
    Retrieves CO2 emissions for a specific year.

    Args:
        user_year (int): The year for which to retrieve CO2 emissions.
        emissions (dict): A dictionary with emission data for countries and years.

    Returns:
        list: A list of CO2 emissions for the specified year.
    """
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
    """
    Identifies the country with the minimum CO2 emission for a specific year.

    Args:
        values (list): A list of CO2 emissions.
        countries (dict): A dictionary with countries and their CO2 emissions.

    Returns:
        tuple: A tuple containing the name of the country with the minimum emission and the emission value.
    """
    min_value = min(values)
    index = values.index(min_value)
    return (list(countries)[index], min_value)

def get_max_country(values: list, countries: dict) -> tuple:
    """
    Identifies the country with the maximum CO2 emission for a specific year.

    Args:
        values (list): A list of CO2 emissions.
        countries (dict): A dictionary with countries and their CO2 emissions.

    Returns:
        tuple: A tuple containing the name of the country with the maximum emission and the emission value.
    """
    max_value = max(values)
    index = values.index(max_value)
    return (list(countries)[index], max_value)

def get_average(values: list) -> float:
    """
    Calculates the average CO2 emissions for a specific year.

    Args:
        values (list): A list of CO2 emissions.

    Returns:
        float: The average CO2 emissions.
    """
    total = sum([x for x in values])
    return total / len(values)

def get_user_countries(country_amount: int, message: str, countries_list: dict):
    """
    Asks the user for a list of countries and validates the input.

    Args:
        country_amount (int): The number of countries the user must enter.
        message (str): Message asking the user for input.
        countries_list (dict): A dictionary of available countries.

    Yields:
        str: Valid countries provided by the user.
    """
    haveValidCountryAnswer = False
    havePrintedCountryList = False
    while not haveValidCountryAnswer:
        user_input = input(message)

        for country in user_input.split(','):
            country = country.strip().capitalize()

            if len(user_input.split(',')) != country_amount:
                print(f"ERR: Sorry, you must enter exactly {country_amount} countries, separated by commas.")
                break
            elif country not in countries_list:
                print("Country not found, please use a country from our list.")
                if not havePrintedCountryList:
                    print(f"Available Countries: {list(countries_list)}")
                    havePrintedCountryList = True
                break

            haveValidCountryAnswer = True
            yield country

def plot_emissions_by_country(country: str, emissions: dict) -> None:
    """
    Plots a graph of CO2 emissions for a specific country.

    Args:
        country (str): The country for which to plot CO2 emissions.
        emissions (dict): A dictionary with emission data for countries and years.
    """
    fig, ax = plt.subplots()
    values = [float(value) for value in emissions.get(country)]
    years = [int(year) for year in emissions.get("CO2 per capita")]
    ax.plot(years, values)

    ax.set_title("Year vs Emission in Capita")
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Emissions in {country}")

    plt.show()

def plot_emissions_by_two_countries(countries: list, emissions: dict) -> None:
    """
    Plots a comparative graph of CO2 emissions for two countries.

    Args:
        countries (list): A list of two countries for which to compare CO2 emissions.
        emissions (dict): A dictionary with emission data for countries and years.
    """
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
    """
    Extracts CO2 emission data for a subset of countries and saves it to a CSV file.

    Args:
        countries (list): A list of three countries for which to extract data.
        emissions (dict): A dictionary with emission data for countries and years.

    Raises:
        IOError: If there is an error while trying to save the CSV file.
    """
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
