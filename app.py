import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load the dataset
file_path = 'data/merged_data.csv'  # Ensure the CSV file is in the same directory as this script or change the path accordingly
data = pd.read_csv(file_path)

# Ensure 'date' column is datetime and add 'year' column if missing
if 'year' not in data.columns:
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year

# For the purpose of this example, let's assume we have a column 'survived_count' which gives the count of survived trees
# If this column does not exist, you might need to create it based on your criteria. 
# Here, we'll randomly generate this column for demonstration purposes.
np.random.seed(0)
data['survived_count'] = np.random.randint(0, data['tree_count'] + 1, size=len(data))

# Calculate survival rate
data['survival_rate'] = data['survived_count'] / data['tree_count'] * 100

# Title of the app
st.title('Tree Planting Dashboard')

# Filters
st.sidebar.header('Filters')

# Dropdown for selecting species
selected_species = st.sidebar.selectbox(
    "Select Species",
    options=data['species'].unique()
)

# Dropdown for selecting year
selected_year = st.sidebar.selectbox(
    "Select Year",
    options=data['year'].unique()
)

# Dropdown for selecting system
selected_system = st.sidebar.selectbox(
    "Select System",
    options=data['system'].unique()
)

# Filter data based on selection
filtered_data = data[(data['species'] == selected_species) & 
                     (data['year'] == selected_year) & 
                     (data['system'] == selected_system)]

# Bar chart for tree count by species
tree_count_fig = px.bar(filtered_data, x='plot_id', y='tree_count', 
                        title=f'Tree Count for {selected_species} in {selected_year} ({selected_system})',
                        color='tree_count', color_continuous_scale='Viridis')

st.plotly_chart(tree_count_fig)

# Summary statistics
total_trees = filtered_data['tree_count'].sum()
avg_trees_per_plot = filtered_data['tree_count'].mean()
num_plots = filtered_data['plot_id'].nunique()
total_survived_trees = filtered_data['survived_count'].sum()
avg_survival_rate = filtered_data['survival_rate'].mean()

st.subheader('Summary Statistics')
st.write(f"Total Trees: {total_trees}")
st.write(f"Average Trees per Plot: {avg_trees_per_plot:.2f}")
st.write(f"Number of Plots: {num_plots}")
st.write(f"Total Survived Trees: {total_survived_trees}")
st.write(f"Average Survival Rate: {avg_survival_rate:.2f}%")

# Pie chart for species distribution
species_distribution_fig = px.pie(data, names='species', values='tree_count', 
                                  title='Species Distribution',
                                  color_discrete_sequence=px.colors.qualitative.Pastel)

st.plotly_chart(species_distribution_fig)

# Line chart for tree count over time
time_series_data = data[(data['species'] == selected_species) & 
                        (data['system'] == selected_system)]
tree_count_over_time_fig = px.line(time_series_data, x='date', y='tree_count', 
                                   title=f'Tree Count Over Time for {selected_species} ({selected_system})',
                                   markers=True, line_shape='spline', 
                                   color_discrete_sequence=['#FF5733'])

st.plotly_chart(tree_count_over_time_fig)

# Bar chart for survival rate by plot
survival_rate_fig = px.bar(filtered_data, x='plot_id', y='survival_rate', 
                           title=f'Survival Rate by Plot for {selected_species} in {selected_year} ({selected_system})',
                           color='survival_rate', color_continuous_scale='Bluered')

st.plotly_chart(survival_rate_fig)
