#  1. Data Collection

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset from working directory
df = pd.read_csv("owid-covid-data.csv")

# 2. Data Loading & Exploration

# Explore structure
print("📌 Columns:", df.columns.tolist())
print("\n📊 Sample Data:\n", df.head())
print("\n🔍 Missing Values:\n", df.isnull().sum())

# 3. Data Cleaning
# Keep relevant columns
columns_of_interest = ['date', 'location', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations', 'population']
df = df[columns_of_interest]

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Drop rows with missing location or date
df.dropna(subset=['date', 'location'], inplace=True)

# Fill missing numeric values with forward fill
df.fillna(method='ffill', inplace=True)

# Filter countries of interest
countries = ['Kenya', 'United States', 'India']
df_filtered = df[df['location'].isin(countries)]

# 📊 4. Exploratory Data Analysis (EDA)

# Plot total cases over time
plt.figure(figsize=(10, 6))
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title("Total COVID-19 Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.tight_layout()
plt.show()

# Plot total deaths over time
plt.figure(figsize=(10, 6))
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_deaths'], label=country)

plt.title("Total COVID-19 Deaths Over Time")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.legend()
plt.tight_layout()
plt.show()

# Calculate death rate and plot
df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']

plt.figure(figsize=(10, 6))
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['death_rate'], label=country)

plt.title("COVID-19 Death Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Death Rate")
plt.legend()
plt.tight_layout()
plt.show()

# 5. Visualizing Vaccination Progress

plt.figure(figsize=(10, 6))
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)

plt.title("COVID-19 Vaccinations Over Time")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.tight_layout()
plt.show()

# Compare % of population vaccinated (latest date available)
latest = df_filtered.sort_values('date').groupby('location').tail(1)
latest['vaccinated_pct'] = latest['total_vaccinations'] / latest['population'] * 100

plt.figure(figsize=(8, 5))
sns.barplot(x='location', y='vaccinated_pct', data=latest)
plt.title("Percentage of Population Vaccinated")
plt.ylabel("% Vaccinated")
plt.xlabel("Country")
plt.tight_layout()
plt.show()

# -------------------------------------------
# 🗺️ 6. (Optional) Choropleth Map
# -------------------------------------------
# Uncomment if you want to use Plotly for a world map
# import plotly.express as px
# latest_all = df.sort_values('date').groupby('location').tail(1)
# fig = px.choropleth(latest_all,
#                     locations="location",
#                     locationmode="country names",
#                     color="total_cases",
#                     hover_name="location",
#                     title="Total COVID-19 Cases by Country")
# fig.show()

"""
# 📌 Key Insights

1. The United States experienced the highest total number of cases and deaths among the selected countries.
2. India showed a sharp rise in cases during mid-2021, likely due to the Delta variant wave.
3. Kenya had fewer cases overall but lower vaccination coverage compared to the US and India.
4. The death rate in all three countries stabilized after widespread vaccination efforts.
5. The vaccination rollout was fastest in the United States among the three countries.

"""


