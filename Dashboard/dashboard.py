import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="Bike Sharing Analysis",
    page_icon="🚲",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("https://github.com/MichaelKuswanto/Dicoding-Proyek-Analisis-Data/blob/main/Dashboard/bike_df.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

bike_df = load_data()

# Helper functions
def get_workingday_stats(df):
    return df.groupby('workingday_daily')['cnt_daily'].mean()

def get_hourly_usage(df):
    return df.groupby('hr')['cnt_hourly'].mean()

# Sidebar
with st.sidebar:
    st.title("🚲 Bike Sharing")
    st.write("Filter the data below:")
    
    # Date range filter
    date_range = st.date_input(
        "Select Date Range",
        value=(bike_df['dteday'].min(), bike_df['dteday'].max()),
        min_value=bike_df['dteday'].min(),
        max_value=bike_df['dteday'].max()
    )
    
    # Season filter
    season = st.multiselect(
        "Select Season",
        options=bike_df['season_daily'].unique(),
        default=bike_df['season_daily'].unique()
    )

# Main content
st.title("🚲 Bike Sharing Dataset Analysis")
st.write("This dashboard analyzes bike sharing patterns based on various factors")

# Filter data based on sidebar selections
filtered_df = bike_df[
    (bike_df['dteday'].dt.date >= date_range[0]) &
    (bike_df['dteday'].dt.date <= date_range[1]) &
    (bike_df['season_daily'].isin(season))
]

# Display key metrics
col1, col2, col3 = st.columns(3)
with col1:
    avg_daily_users = int(filtered_df['cnt_daily'].mean())
    st.metric("Average Daily Users", f"{avg_daily_users:,}")
with col2:
    max_hour = filtered_df.groupby('hr')['cnt_hourly'].mean().idxmax()
    max_users = int(filtered_df.groupby('hr')['cnt_hourly'].mean().max())
    st.metric("Peak Hour", f"{max_hour}:00", f"{max_users} users")
with col3:
    popular_season = filtered_df.groupby('season_daily')['cnt_daily'].mean().idxmax()
    season_avg = int(filtered_df.groupby('season_daily')['cnt_daily'].mean().max())
    st.metric("Most Popular Season", popular_season, f"{season_avg} avg users")

# Question 1: Working Days vs Holidays
st.subheader("1. 🗓️ Bike Usage: Working Days vs Holidays")
workingday_data = get_workingday_stats(filtered_df)

fig1, ax1 = plt.subplots(figsize=(10, 6))
workingday_data.plot(kind='bar', ax=ax1)
plt.title("Average Bike Rentals: Working Days vs Holidays")
plt.xlabel("Day Type")
plt.ylabel("Average Number of Rentals")
st.pyplot(fig1)

# Question 2: Weather Impact
st.subheader("2. 🌤️ Impact of Weather on Bike Usage")
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.boxplot(x='weathersit_daily', y='cnt_daily', data=filtered_df, ax=ax2)
plt.title("Bike Rentals by Weather Condition")
plt.xlabel("Weather Situation")
plt.ylabel("Number of Rentals")
st.pyplot(fig2)

# Question 3: Seasonal Trends
st.subheader("3. 🍁 Seasonal Trends in Bike Usage")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.boxplot(x='season_daily', y='cnt_daily', data=filtered_df, ax=ax3)
plt.title("Bike Rentals by Season")
plt.xlabel("Season")
plt.ylabel("Number of Rentals")
st.pyplot(fig3)

# Question 4: Hourly Patterns
st.subheader("4. ⏰ Hourly Usage Patterns")
hourly_usage = get_hourly_usage(filtered_df)

fig4, ax4 = plt.subplots(figsize=(12, 6))
hourly_usage.plot(kind='line', ax=ax4)
plt.title("Average Hourly Bike Rentals")
plt.xlabel("Hour of Day")
plt.ylabel("Average Number of Rentals")
st.pyplot(fig4)

# Additional insights
st.subheader("Key Insights")
col1, col2 = st.columns(2)

with col1:
    st.write("""
    - Highest usage occurs during Fall season
    - Clear weather significantly increases bike rentals
    - Working days see higher average usage than holidays
    """)

with col2:
    st.write("""
    - Two peak usage times: morning and evening commute hours
    - Lowest usage during early morning hours (2-4 AM)
    - Weather has a significant impact on rental patterns
    """)

# Footer
st.markdown("---")
st.caption("Data Source: Bike Sharing Dataset • Created by Michael Kuswanto")

# Optional: Add CSS styling
st.markdown("""
    <style>
    .stMetric .metric-label { font-size: 16px !important; }
    .stMetric .metric-value { font-size: 24px !important; font-weight: bold; }
    h1 { font-size: 36px !important; }
    h2 { font-size: 24px !important; }
    </style>
    """, unsafe_allow_html=True)
