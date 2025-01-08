import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from CSV
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully!")
        return data
    except FileNotFoundError:
        print("Error: File not found. Please ensure 'health_data.csv' is in the same folder.")
        exit()

# Display basic stats
def display_stats(data):
    print("\nHealth Data Overview:")
    print(data.describe())

# Plot vaccination rates
def plot_vaccination_rates(data):
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Country', y='VaccinationRate', data=data, palette='viridis')
    plt.title('Vaccination Rates by Country')
    plt.ylabel('Vaccination Rate (%)')
    plt.xlabel('Country')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Query country statistics
def query_country(data, country):
    result = data[data['Country'].str.lower() == country.lower()]
    if not result.empty:
        print(f"\nHealth Statistics for {country}:")
        print(result.to_string(index=False))
    else:
        print(f"\nNo data available for {country}.")

# Main Function
def main():
    print("Welcome to the Health Awareness Dashboard!")
    
    # Load health data
    file_path = 'health_data.csv'
    data = load_data(file_path)
    
    # Display dataset statistics
    display_stats(data)
    
    # Interactive menu
    while True:
        print("\nMenu:")
        print("1. View Vaccination Rates (Bar Chart)")
        print("2. Query Health Data by Country")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            plot_vaccination_rates(data)
        elif choice == '2':
            country = input("Enter the country name: ")
            query_country(data, country)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
