import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog

# Function to upload CSV file
def upload_csv():
    Tk().withdraw()  # Hide the root Tkinter window
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            data = pd.read_csv(file_path)
            print("Data uploaded successfully!")
            print(data.head())
            return data
        except Exception as e:
            print(f"Error reading the file: {e}")
            return None
    else:
        print("No file selected.")
        return None

# Function to plot vaccination rates
def plot_vaccination_rates(data):
    if 'Country' in data.columns and 'VaccinationRate' in data.columns:
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Country', y='VaccinationRate', data=data)
        plt.title("Vaccination Rates by Country")
        plt.xlabel("Country")
        plt.ylabel("Vaccination Rate (%)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Required columns 'Country' and 'VaccinationRate' are missing in the dataset.")

# Function to query health data by country
def query_country(data, country):
    country_data = data[data['Country'].str.lower() == country.lower()]
    if not country_data.empty:
        print(f"Health Data for {country}:")
        print(country_data)
    else:
        print(f"No data found for {country}.")

# Function to plot trends over time
def plot_trend(data, country, indicator):
    if 'Country' in data.columns and 'Year' in data.columns and indicator in data.columns:
        country_data = data[data['Country'].str.lower() == country.lower()]
        if not country_data.empty:
            plt.figure(figsize=(10, 6))
            plt.plot(country_data['Year'], country_data[indicator], marker='o', label=country)
            plt.title(f"{indicator} Trend for {country}")
            plt.xlabel("Year")
            plt.ylabel(indicator)
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()
        else:
            print(f"No data found for {country}.")
    else:
        print(f"Required columns are missing or invalid indicator: {indicator}.")

# Function to filter data by region
def filter_by_region(data, region):
    if 'Region' in data.columns:
        filtered_data = data[data['Region'].str.lower() == region.lower()]
        if not filtered_data.empty:
            print(f"Filtered Data for Region: {region}")
            print(filtered_data.head())
            return filtered_data
        else:
            print(f"No data found for {region}.")
    else:
        print("Column 'Region' is missing in the dataset.")
        return None

# Main dashboard function
def main():
    print("Welcome to the Enhanced Health Awareness Dashboard!")
    data = upload_csv()
    if data is None:
        print("No data to work with. Exiting.")
        return

    while True:
        print("\nMenu:")
        print("1. View Vaccination Rates (Bar Chart)")
        print("2. Query Health Data by Country")
        print("3. Plot Trends Over Time")
        print("4. Filter Data by Region")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")
        
        if choice == '1':
            plot_vaccination_rates(data)
        elif choice == '2':
            country = input("Enter the country name: ")
            query_country(data, country)
        elif choice == '3':
            country = input("Enter the country name: ")
            indicator = input("Enter the indicator (e.g., LifeExpectancy): ")
            plot_trend(data, country, indicator)
        elif choice == '4':
            region = input("Enter the region: ")
            filter_by_region(data, region)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the dashboard
if __name__ == "__main__":
    main()
