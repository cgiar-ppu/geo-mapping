import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
import requests

# Set page configuration
st.set_page_config(layout="wide")

# Sidebar settings (you can customize this section)
st.sidebar.header("Settings")
# Add any settings you need here

# Load data
@st.cache_data
def load_data():
    priority_df = pd.read_excel("Priority Countries.xlsx")
    countries_map_df = pd.read_excel("CountriesMap.xlsx")
    return priority_df, countries_map_df

priority_df, countries_map_df = load_data()

# Load geojson for countries
@st.cache_data
def load_geojson():
    url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
    response = requests.get(url)
    geojson = response.json()
    return geojson

geojson = load_geojson()

# Left Column: Programs
st.markdown("## Program Selection")
programs = priority_df['Program'].unique()
selected_programs = st.multiselect("Select Programs", programs)

# Get countries associated with selected programs
program_countries = priority_df[priority_df['Program'].isin(selected_programs)]

# Right Column: Projects
st.markdown("## Project Selection")
projects = countries_map_df['Project Name'].unique()
selected_projects = st.multiselect("Select Projects", projects)

# Get countries associated with selected projects
project_countries = countries_map_df[countries_map_df['Project Name'].isin(selected_projects)]

# Middle Column: Overlap Visualization
st.markdown("## Overlap Visualization")

# Calculate overlaps
countries_in_programs = set(program_countries['Country'])
countries_in_projects = set(project_countries['Country'])

overlap_countries = countries_in_programs.intersection(countries_in_projects)
unique_program_countries = countries_in_programs - countries_in_projects
unique_project_countries = countries_in_projects - countries_in_programs

# Prepare data for visualization
overlap_df = pd.DataFrame({
    'Country': list(overlap_countries),
    'Status': 'In Both'
})
unique_program_df = pd.DataFrame({
    'Country': list(unique_program_countries),
    'Status': 'Only in Programs'
})
unique_project_df = pd.DataFrame({
    'Country': list(unique_project_countries),
    'Status': 'Only in Projects'
})

visualization_df = pd.concat([overlap_df, unique_program_df, unique_project_df])

# Visualize using an interactive Mapbox map
fig = px.choropleth_mapbox(
    data_frame=visualization_df,
    geojson=geojson,
    locations='Country',
    featureidkey='properties.name',
    color='Status',
    hover_name='Country',
    color_discrete_map={
        'In Both': 'green',
        'Only in Programs': 'blue',
        'Only in Projects': 'red'
    },
    mapbox_style='carto-positron',
    zoom=1,
    center={"lat": 20, "lon": 0},
    opacity=0.5,
    title='Country Overlap between Selected Programs and Projects'
)

st.plotly_chart(fig, use_container_width=True)