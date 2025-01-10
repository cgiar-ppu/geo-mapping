import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Set page configuration
st.set_page_config(layout="wide")

# Sidebar settings
st.sidebar.header("Settings")

# Load data
@st.cache_data
def load_data():
    df_countries_map = pd.read_excel("Countries Map 2.xlsx")
    df_priority_countries = pd.read_excel("Priority Countries 2.xlsx")
    return df_countries_map, df_priority_countries

df_countries_map, df_priority_countries = load_data()

# Load geojson for countries
@st.cache_data
def load_geojson():
    with open("geojson.json") as f:
        geojson = json.load(f)
    return geojson

geojson = load_geojson()

# Program, Center, Funder, and Project Selection Side by Side
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("## Program Selection")
    programs = sorted(df_priority_countries['Program'].unique())
    selected_programs = st.multiselect("Select Programs", programs)
    program_countries = df_priority_countries[df_priority_countries['Program'].isin(selected_programs)]['Country'].unique() if selected_programs else []

with col2:
    st.markdown("## Center Selection")
    centers = df_countries_map['Center'].dropna().astype(str)
    centers = centers[centers != '']
    centers = sorted(centers.unique())
    selected_centers = st.multiselect("Select Centers", centers)
    center_countries = df_countries_map[df_countries_map['Center'].isin(selected_centers)]['Country'].unique() if selected_centers else []

with col3:
    st.markdown("## Funder Selection")
    funders = df_countries_map['Funder'].dropna().astype(str)
    funders = funders[funders != '']
    funders = sorted(funders.unique())
    selected_funders = st.multiselect("Select Funders", funders)
    funder_countries = df_countries_map[df_countries_map['Funder'].isin(selected_funders)]['Country'].unique() if selected_funders else []

with col4:
    st.markdown("## Project Selection")
    projects = df_countries_map['Project Name'].dropna().astype(str)
    projects = projects[projects != '']
    projects = sorted(projects.unique())
    selected_projects = st.multiselect("Select Projects", projects)
    project_countries = df_countries_map[df_countries_map['Project Name'].isin(selected_projects)]['Country'].unique() if selected_projects else []

# Combine all selected countries
all_selected_countries = set(program_countries) | set(center_countries) | set(funder_countries) | set(project_countries)

# Function to calculate overlap percentage
def calculate_overlap_percentage(selected_countries, total_countries):
    if total_countries == 0:
        return 0
    return (len(selected_countries) / total_countries) * 100

# Calculate overlap percentages based on selected filters
overlap_percentage = None
overlap_count = 0

# Check the number of selected filters and calculate overlap accordingly
if len(selected_programs) > 0 and len(selected_centers) > 0 and len(selected_funders) > 0 and len(selected_projects) > 0:
    overlap_countries = set(program_countries) & set(center_countries) & set(funder_countries) & set(project_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(program_countries) | set(center_countries) | set(funder_countries) | set(project_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In All Four"

elif len(selected_programs) > 0 and len(selected_centers) > 0 and len(selected_funders) > 0:
    overlap_countries = set(program_countries) & set(center_countries) & set(funder_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(program_countries) | set(center_countries) | set(funder_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Programs, Centers and Funders"

elif len(selected_programs) > 0 and len(selected_centers) > 0 and len(selected_projects) > 0:
    overlap_countries = set(program_countries) & set(center_countries) & set(project_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(program_countries) | set(center_countries) | set(project_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Programs, Centers and Projects"

elif len(selected_programs) > 0 and len(selected_funders) > 0 and len(selected_projects) > 0:
    overlap_countries = set(program_countries) & set(funder_countries) & set(project_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(program_countries) | set(funder_countries) | set(project_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Programs, Funders and Projects"

elif len(selected_centers) > 0 and len(selected_funders) > 0 and len(selected_projects) > 0:
    overlap_countries = set(center_countries) & set(funder_countries) & set(project_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(center_countries) | set(funder_countries) | set(project_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Centers, Funders and Projects"

elif len(selected_programs) > 0 and len(selected_centers) > 0:
    overlap_countries = set(program_countries) & set(center_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(program_countries) | set(center_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Programs and Centers"

elif len(selected_programs) > 0 and len(selected_funders) > 0:
    overlap_countries = set(program_countries) & set(funder_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(program_countries) | set(funder_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Programs and Funders"

elif len(selected_centers) > 0 and len(selected_projects) > 0:
    overlap_countries = set(center_countries) & set(project_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(center_countries) | set(project_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Centers and Projects"

elif len(selected_centers) > 0 and len(selected_funders) > 0:
    overlap_countries = set(center_countries) & set(funder_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(center_countries) | set(funder_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Centers and Funders"

elif len(selected_funders) > 0 and len(selected_projects) > 0:
    overlap_countries = set(funder_countries) & set(project_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(funder_countries) | set(project_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Funders and Projects"

# New condition for two filters: Program and Project
elif len(selected_programs) > 0 and len(selected_projects) > 0:
    overlap_countries = set(program_countries) & set(project_countries)
    overlap_percentage = calculate_overlap_percentage(overlap_countries, len(set(program_countries) | set(project_countries)))
    overlap_count = len(overlap_countries)
    overlap_label = "In Programs and Projects"

# Create visualization dataframe
country_status = {}
for country in all_selected_countries:
    in_program = country in program_countries
    in_center = country in center_countries
    in_funder = country in funder_countries
    in_project = country in project_countries
    
    # Create a list to hold the statuses
    statuses = []
    
    if in_program:
        statuses.append('Programs')
    if in_center:
        statuses.append('Centers')
    if in_funder:
        statuses.append('Funders')
    if in_project:
        statuses.append('Projects')
    
    # Determine the status based on the overlaps
    if len(statuses) == 4:  # In All Four
        status = 'In All Four'
    elif len(statuses) > 1:  # In multiple categories
        status = 'In ' + ' and '.join(statuses)
    elif len(statuses) == 1:  # Only in one category
        status = 'Only in ' + statuses[0]
    else:  # Skip countries not in any selected category
        continue
    
    country_status[country] = status

# Create visualization dataframe
visualization_df = pd.DataFrame([
    {'Country': country, 'Status': status}
    for country, status in country_status.items()
])

# If the DataFrame is empty, create a sample row
if visualization_df.empty:
    visualization_df = pd.DataFrame({
        'Country': ['No selection'],
        'Status': ['No data']
    })

# Visualize using an interactive Mapbox map
color_map = {
    'In All Four': '#2ca02c',
    'In Programs and Centers': '#98df8a',
    'In Programs and Funders': '#1f77b4',
    'In Programs and Projects': '#ff7f0e',
    'In Centers and Funders': '#9467bd',
    'In Centers and Projects': '#d62728',
    'In Funders and Projects': '#8c564b',
    'Only in Programs': '#ffbb78',
    'Only in Centers': '#c5b0d5',
    'Only in Funders': '#2ca02c',
    'Only in Projects': '#98df8a'
}

try:
    fig = px.choropleth_mapbox(
        data_frame=visualization_df,
        geojson=geojson,
        locations='Country',
        featureidkey='properties.name',
        color='Status',
        custom_data=['Country', 'Status'],
        color_discrete_map=color_map,
        mapbox_style='carto-positron',
        zoom=1,
        center={"lat": 20, "lon": 0},
        opacity=0.5,
        height=600,
        title='Country Overlap between Selected Programs, Centers, Funders, and Projects'
    )
    
    # Update hover template
    fig.update_traces(
        hovertemplate="<br>".join([
            "Country: %{customdata[0]}",
            "Status: %{customdata[1]}"
        ])
    )
    
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Error creating visualization: {str(e)}")

# Display overlap percentage below the map
if overlap_percentage is not None:
    st.markdown("### Overlap Percentage")
    st.markdown(f"{overlap_label}: {overlap_percentage:.2f}% ({overlap_count} Countries)")

# Display Selected Programs, Centers, Funders, and Projects Below the Map
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown("### Selected Programs")
    if selected_programs:
        st.markdown('\n'.join(f"- {program}" for program in selected_programs))
    else:
        st.write("No programs selected.")

with col6:
    st.markdown("### Selected Centers")
    if selected_centers:
        st.markdown('\n'.join(f"- {center}" for center in selected_centers))
    else:
        st.write("No centers selected.")

with col7:
    st.markdown("### Selected Funders")
    if selected_funders:
        st.markdown('\n'.join(f"- {funder}" for funder in selected_funders))
    else:
        st.write("No funders selected.")

with col8:
    st.markdown("### Selected Projects")
    if selected_projects:
        st.markdown('\n'.join(f"- {project}" for project in selected_projects))
    else:
        st.write("No projects selected.")

# Provide Data Table and Download Option
st.markdown("## Data Table")
st.dataframe(visualization_df, width=400)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(visualization_df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='visualization_data.csv',
    mime='text/csv',
)

# Additional Data Tables for Cross-Checking
st.markdown("## Selected Programs and Associated Countries")
if len(selected_programs) > 0:
    program_display = df_priority_countries[df_priority_countries['Program'].isin(selected_programs)][['Program', 'Country']].drop_duplicates()
    program_display.columns = ['Program', 'Country']
    st.dataframe(program_display, width=600)
else:
    st.write("No programs selected.")

st.markdown("## Selected Centers and Associated Countries")
if len(selected_centers) > 0:
    center_display = df_countries_map[df_countries_map['Center'].isin(selected_centers)][['Center', 'Country']].drop_duplicates()
    center_display.columns = ['Center', 'Country']
    st.dataframe(center_display, width=600)
else:
    st.write("No centers selected.")

st.markdown("## Selected Funders and Associated Countries")
if len(selected_funders) > 0:
    funder_display = df_countries_map[df_countries_map['Funder'].isin(selected_funders)][['Funder', 'Country']].drop_duplicates()
    funder_display.columns = ['Funder', 'Country']
    st.dataframe(funder_display, width=600)
else:
    st.write("No funders selected.")

st.markdown("## Selected Projects and Associated Countries")
if len(selected_projects) > 0:
    project_display = df_countries_map[df_countries_map['Project Name'].isin(selected_projects)][['Project Name', 'Country']].drop_duplicates()
    project_display.columns = ['Project Name', 'Country']
    st.dataframe(project_display, width=600)
else:
    st.write("No projects selected.")