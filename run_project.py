# Run_project
import user_profile

##Cleaning and merging the raw data files

import pandas as pd
import re

# Load demographic data without a header to inspect the structure
df_demographic_raw = pd.read_excel("/content/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx", header=None)

import os
if not os.path.exists("your_path.xlsx"):
    print("File not found.")

# Use row 16 as the header and rows from 17 onwards as data
header_row_index = 16
data_start_row_index = 17

# Extract the header row
header = df_demographic_raw.iloc[header_row_index]

# Extract the data rows and assign the header
df_demographic = df_demographic_raw[data_start_row_index:].copy()
df_demographic.columns = header

# Rename columns by index to be more robust (index 2 for Country, index 51 for 2022_projected_births)
# Ensure the indices are correct based on the raw data inspection
df_demographic.rename(columns={df_demographic.columns[2]: 'Country', df_demographic.columns[51]: '2022_projected_births'}, inplace=True)


# Standardize country names in demographic data
if 'Country' in df_demographic.columns:
    df_demographic['Country'] = df_demographic['Country'].astype(str).str.strip().str.lower()
else:
    print("Error: 'Country' column not found after renaming in df_demographic.")


# Remove irrelevant entries from demographic data.
# Based on inspection, these are likely rows with aggregated data or footnotes.
# We need to be careful not to remove actual country data.
demographic_irrelevant_entries = [
    'world', 'africa', 'african union', 'americas', 'anguilla', 'arab maghreb union (amu)', 'arab states',
    'asia', 'asia and the pacific', 'caribbean', 'central africa', 'central africa (african union)',
    'central america', 'central asia', 'central and southern asia', 'common market for eastern and southern africa (comesa)',
    'community of sahel-saharan states (cen-sad)', 'east african community (eac)', 'east asia',
    'east asia and pacific', 'east and southern africa', 'eastern africa', 'eastern africa (african union)',
    'eastern asia', 'eastern europe', 'eastern europe and central asia', 'eastern mediterranean',
    'eastern and south-eastern asia', 'eastern and southern africa', 'economic community of central african states (eccas)',
    'economic community of west african states (ecowas 2025)', 'economic community of west african states (ecowas)',
    'europe', 'europe and central asia', 'european union', 'footnotes', 'intergovernmental authority on development (igad)',
    'latin america', 'latin america and the caribbean', 'least developed countries', 'less developed regions',
    'less developed regions, excluding least developed countries',
    'less developed regions, excluding least developed countries, in landlocked developing states',
    'less developed regions, excluding least developed countries, in small island developing states',
    'low-income economies', 'lower-middle-income economies', 'melanesia', 'micronesia', 'middle africa',
    'middle east and north africa', 'net migration rate (per 1,000 population)',
    'north america', 'northern africa', 'northern africa (african union)', 'northern africa and western asia',
    'northern america', 'oceania', 'oceania (exc. australia and new zealand)', 'polynesia', 'sdg regions - global',
    'south america', 'south asia', 'south sudan', 'south-east asia', 'south-eastern asia', 'southern africa',
    'southern africa (african union)', 'southern african development community (sadc)', 'southern asia',
    'sub-saharan africa', 'unicef programme regions - global', 'unicef reporting regions - global',
    'unit multiplier: units', 'unit of measure: %', 'united nations economic commission for africa',
    'upper-middle-income economies', 'western africa', 'western africa (african union)', 'western asia',
    'western europe', 'western pacific', 'world bank (high income)', 'world bank (low income)',
    'world bank (lower middle income)', 'world bank (upper middle income)', 'current age: 15 to 49 years old',
    'time period activity related to when the data are collected: end of fieldwork',
    'observation confidentaility: free'
]

df_demographic = df_demographic[~df_demographic['Country'].astype(str).str.lower().isin([entry.lower() for entry in demographic_irrelevant_entries])]
df_demographic = df_demographic.dropna(subset=['Country'])

# Based on inspection, filter out rows where 'Variant' is not 'Estimates' to focus on actual data
if 'Variant' in df_demographic.columns:
    df_demographic = df_demographic[df_demographic['Variant'] == 'Estimates']

# Based on inspection, filter out rows where 'Year' is not 2022 to get only 2022 data
    # Need to handle potential multi-level column index after setting header from row 16
    # Access the 'Year' column correctly based on the actual column names
    # Assuming 'Year' is a top-level column name after setting header=16
    if 'Year' in df_demographic.columns:
        df_demographic['Year'] = pd.to_numeric(df_demographic['Year'], errors='coerce')
        df_demographic = df_demographic[df_demographic['Year'] == 2022]
        df_demographic = df_demographic.dropna(subset=['Year']) # Drop rows where Year couldn't be converted to numeric
    elif ('Year', 'Unnamed: 17_level_1') in df_demographic.columns: # Example for potential multi-level
         df_demographic[('Year', 'Unnamed: 17_level_1')] = pd.to_numeric(df_demographic[('Year', 'Unnamed: 17_level_1')], errors='coerce')
         df_demographic = df_demographic[df_demographic[('Year', 'Unnamed: 17_level_1')] == 2022]
         df_demographic = df_demographic.dropna(subset=[('Year', 'Unnamed: 17_level_1')])


# Load the other two dataframes (assuming they are already cleaned from previous steps)
df_global_dataflow = pd.read_excel("/GLOBAL_DATAFLOW_2018-2022.xlsx", header=1)
df_on_track = pd.read_excel("/On-track and off-track countries.xlsx")

# Clean and standardize country identifiers for global dataflow and on-track data (re-execute cleaning)
df_global_dataflow.rename(columns={'Geographic area': 'Country'}, inplace=True)
df_on_track.rename(columns={'OfficialName': 'Country'}, inplace=True)

df_global_dataflow['Country'] = df_global_dataflow['Country'].astype(str).str.strip().str.lower()
df_on_track['Country'] = df_on_track['Country'].astype(str).str.strip().str.lower()

# Remove parenthesized text and leading/trailing spaces from df_global_dataflow (re-execute cleaning)
df_global_dataflow['Country'] = df_global_dataflow['Country'].apply(lambda x: re.sub(r'\(.*?\)', '', str(x)).strip() if pd.notna(x) else x)

# Remove rows from df_global_dataflow that are not countries (re-execute cleaning)
regions_to_remove_global = ['africa', 'african union', 'americas', 'anguilla', 'arab maghreb union (amu)', 'arab states', 'asia and the pacific', 'caribbean', 'central africa (african union)', 'central america', 'central asia', 'central and southern asia', 'common market for eastern and southern africa (comesa)', 'community of sahel-Saharan states (cen-sad)', 'east african community (eac)', 'east asia and pacific', 'east and southern africa', 'eastern africa', 'eastern africa (african union)', 'eastern asia', 'eastern europe and central asia', 'eastern mediterranean', 'eastern and south-eastern asia', 'eastern and southern africa', 'economic community of central african states (eccas)', 'economic community of west african states (ecowas 2025)', 'economic community of west African states (ECOWAS)', 'europe', 'europe and central asia', 'intergovernmental authority on development (igad)', 'latin america', 'latin america and the caribbean', 'least developed countries (ldc)', 'middle africa', 'middle east and north africa', 'north america', 'northern africa', 'northern africa (african union)', 'northern africa and western asia', 'northern america', 'oceania', 'oceania (exc. australia and new zealand)', 'sdg regions - global', 'south america', 'south asia', 'south sudan', 'south-east asia', 'south-eastern asia', 'southern africa', 'southern africa (african union)', 'southern african development community (sadc)', 'southern asia', 'sub-saharan africa', 'unicef programme regions - global', 'unicef reporting regions - global', 'west and central africa', 'western africa', 'western africa (african union)', 'western asia', 'western europe', 'western pacific', 'world bank (high income)', 'world bank (low income)', 'world bank (lower middle income)', 'world bank (upper middle income)', 'footnotes', 'unit multiplier: units', 'unit of measure: %', 'observation confidentaility: free', 'time period activity related to when the da', 'current age: 15 to 49 years old']

df_global_dataflow = df_global_dataflow[~df_global_dataflow['Country'].astype(str).str.lower().isin([entry.lower() for entry in regions_to_remove_global])]

regions_to_remove_further_global = ['central africa', 'north africa', 'united nations economic commission for africa', 'west africa', 'arab maghreb union', 'common market for eastern and southern africa', 'community of sahel-Saharan states', 'east african community', 'economic community of central african states', 'economic community of west african states', 'intergovernmental authority on development', 'least developed countries', 'southern african development community', 'world bank', 'time period activity related to when the data are collected: end of fieldwork']

df_global_dataflow = df_global_dataflow[~df_global_dataflow['Country'].astype(str).str.lower().isin([entry.lower() for entry in regions_to_remove_further_global])]

df_global_dataflow = df_global_dataflow.dropna(subset=['Country'])
df_on_track = df_on_track.dropna(subset=['Country'])

# Filter and select recent data - re-execute
df_global_dataflow_filtered = df_global_dataflow[
    df_global_dataflow['Indicator'].isin([
        'Antenatal care 4+ visits - percentage of women (aged 15-49 years) attended at least four times during pregnancy by any provider',
        'Skilled birth attendant - percentage of deliveries attended by skilled health personnel'
    ])
]

df_melted = df_global_dataflow_filtered.melt(
    id_vars=['Country', 'Indicator', 'Sex'],
    value_vars=['Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7'],
    var_name='Year_col',
    value_name='Value'
)

year_map = {
    'Unnamed: 3': 2018,
    'Unnamed: 4': 2019,
    'Unnamed: 5': 2020,
    'Unnamed: 6': 2021,
    'Unnamed: 7': 2022
}

df_melted['Year'] = df_melted['Year_col'].map(year_map)

df_melted.dropna(subset=['Value'], inplace=True)
df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')
df_melted.dropna(subset=['Value'], inplace=True)

df_melted_sorted = df_melted.sort_values(by=['Country', 'Indicator', 'Year'], ascending=[True, True, False])
df_most_recent = df_melted_sorted.drop_duplicates(subset=['Country', 'Indicator'], keep='first')

df_pivot = df_most_recent.pivot(index='Country', columns='Indicator', values='Value')


# Merge the dataframes
df_merged = pd.merge(df_pivot, df_on_track, on='Country', how='outer')
df_merged = pd.merge(df_merged, df_demographic[['Country', '2022_projected_births']], on='Country', how='outer')

# The df_merged dataframe is now ready for further analysis or calculations.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# -------------------------------
# CONFIGURATION
# -------------------------------
REGIONS_TO_EXCLUDE = [
    "Africa", "Sub-Saharan Africa", "Northern Africa", "Eastern Africa",
    "Middle Africa", "Southern Africa", "Western Africa", "Asia", "Central Asia",
    "Eastern Asia", "South-eastern Asia", "Southern Asia", "Western Asia", "Europe",
    "Eastern Europe", "Northern Europe", "Southern Europe", "Western Europe",
    "Latin America", "Caribbean", "Central America", "South America", "Oceania",
    "Australia", "Melanesia", "Micronesia", "Polynesia", "World", "More developed",
    "Less developed", "Least developed", "Land Locked", "Small Island", "Low income",
    "Lower-middle income", "Upper-middle income", "High income"
]

# -------------------------------
# DATA LOADING FUNCTIONS
# -------------------------------
def load_demographic_data(path):
    df = pd.read_excel(path, skiprows=16)
    df = df[~df['Region, subregion, country or area *'].isin(REGIONS_TO_EXCLUDE)]
    df = df[df['Year'] == 2022]
    df = df.rename(columns={'Region, subregion, country or area *': 'Country'})
    return df[['Country', '2022', 'Year']].rename(columns={'2022': 'projected_births'})

def load_global_dataflow_data(path, indicator_filter):
    df = pd.read_excel(path)
    df = df[df['Indicator'].isin(indicator_filter)]
    df = df[df['Year'] == 2022]
    df = df[df['Location'].notna()]
    df = df.rename(columns={'Location': 'Country', 'Value': 'Coverage'})
    return df[['Country', 'Indicator', 'Coverage']]

# -------------------------------
# PROCESSING FUNCTIONS
# -------------------------------
def merge_and_calculate_weighted_coverage(demo_df, indicator_df):
    merged = pd.merge(indicator_df, demo_df, on='Country', how='left')
    merged.dropna(subset=['projected_births', 'Coverage'], inplace=True)
    merged['weighted_coverage'] = merged['Coverage'] * merged['projected_births']
    
    result = merged.groupby('Indicator').apply(
        lambda g: g['weighted_coverage'].sum() / g['projected_births'].sum()
    ).reset_index(name='Weighted Coverage')

    return result

# -------------------------------
# PLOTTING FUNCTIONS
# -------------------------------
def plot_coverage_bar_chart(df):
    fig, ax = plt.subplots()
    bars = ax.bar(df['Indicator'], df['Weighted Coverage'], color=['#66c2a5', '#fc8d62'])
    ax.set_ylabel('Coverage (%)')
    ax.set_title('Population-Weighted Coverage by Indicator (2022)')
    ax.set_ylim(0, 100)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    return fig

def render_chart_inline(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    return f'<img src="data:image/png;base64,{encoded}"/>'

# -------------------------------
# MAIN RUNNER
# -------------------------------
def main():
    demographic_path = "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
    dataflow_path = "global-dataflow.xlsx"
    indicators = ['Antenatal care coverage - at least four visits (%)', 
                  'Births attended by skilled health personnel (%)']

    demo_df = load_demographic_data(demographic_path)
    dataflow_df = load_global_dataflow_data(dataflow_path, indicators)
    coverage_df = merge_and_calculate_weighted_coverage(demo_df, dataflow_df)
    
    fig = plot_coverage_bar_chart(coverage_df)
    html_img = render_chart_inline(fig)

    interpretation = (
        "<p>The chart above displays the population-weighted coverage for key maternal health indicators "
        "in 2022. Antenatal care (ANC4+) and skilled birth attendance (SBA) show significant reach, "
        "but discrepancies may remain in lower-resourced settings. These indicators reflect both service "
        "availability and systemic equity in access for pregnant individuals.</p>"
    )

    html_output = html_img + interpretation
    display(HTML(html_output))  # For Jupyter notebooks; otherwise print or write to file

# Uncomment to run as a script
# if __name__ == "__main__":
#     main()

#### Calculate weighted average for each group in 'Status.U5MR' ######

# Calculate population-weighted averages
# Convert '2022_projected_births' to numeric, coercing errors
df_merged['2022_projected_births'] = pd.to_numeric(df_merged['2022_projected_births'], errors='coerce')

# Define the coverage columns
coverage_cols = [
    'Antenatal care 4+ visits - percentage of women (aged 15-49 years) attended at least four times during pregnancy by any provider',
    'Skilled birth attendant - percentage of deliveries attended by skilled health personnel'
]

# Calculate weighted average for each group in 'Status.U5MR' 

weighted_averages = {}
for status in df_merged['Status.U5MR'].unique():
    if pd.notna(status):
        group_df = df_merged[df_merged['Status.U5MR'] == status].copy()
        weighted_averages[status] = {}
        for col in coverage_cols:
            # Drop rows with missing coverage or zero/missing population
            valid_data = group_df.dropna(subset=[col, '2022_projected_births']).copy()
            valid_data = valid_data[valid_data['2022_projected_births'] > 0]

            if not valid_data.empty:
                weighted_avg = (valid_data[col] * valid_data['2022_projected_births']).sum() / valid_data['2022_projected_births'].sum()
                weighted_averages[status][col] = weighted_avg
            else:
                weighted_averages[status][col] = None

# Replace None values in weighted_averages with 0 for plotting
for status in weighted_averages:
    for indicator in weighted_averages[status]:
        if weighted_averages[status][indicator] is None:
            weighted_averages[status][indicator] = 0

# Display the weighted averages (optional)
for status, averages in weighted_averages.items():
    print(f"Weighted Averages for Status: {status}")
    for indicator, avg_value in averages.items():
        print(f"  {indicator}: {avg_value:.2f}" if avg_value is not None else f"  {indicator}: No data")


######      Visualization and producing HTML outputs    #########

import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from IPython.display import HTML, display
import pandas as pd
import re

# Re-calculate weighted averages to ensure they are available
# This code is copied from cell f9030bf8 which successfully calculated the weighted averages

# Load demographic data without a header to inspect the structure
df_demographic_raw = pd.read_excel("/content/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx", header=None)

# Use row 16 as the header and rows from 17 onwards as data
header_row_index = 16
data_start_row_index = 17

# Extract the header row
header = df_demographic_raw.iloc[header_row_index]

# Extract the data rows and assign the header
df_demographic = df_demographic_raw[data_start_row_index:].copy()
df_demographic.columns = header

# Rename columns by index to be more robust (index 2 for Country, index 51 for 2022_projected_births)
# Ensure the indices are correct based on the raw data inspection
df_demographic.rename(columns={df_demographic.columns[2]: 'Country', df_demographic.columns[51]: '2022_projected_births'}, inplace=True)


# Standardize country names in demographic data
if 'Country' in df_demographic.columns:
    df_demographic['Country'] = df_demographic['Country'].astype(str).str.strip().str.lower()
else:
    print("Error: 'Country' column not found after renaming in df_demographic.")


# Remove irrelevant entries from demographic data.
# Based on inspection, these are likely rows with aggregated data or footnotes.
# We need to be careful not to remove actual country data.
demographic_irrelevant_entries = [
    'world', 'africa', 'african union', 'americas', 'anguilla', 'arab maghreb union (amu)', 'arab states',
    'asia', 'asia and the pacific', 'caribbean', 'central africa', 'central africa (african union)',
    'central america', 'central asia', 'central and southern asia', 'common market for eastern and southern africa (comesa)',
    'community of sahel-saharan states (cen-sad)', 'east african community (eac)', 'east asia',
    'east asia and pacific', 'east and southern africa', 'eastern africa', 'eastern africa (african union)',
    'eastern asia', 'eastern europe', 'eastern europe and central asia', 'eastern mediterranean',
    'eastern and south-eastern asia', 'eastern and southern africa', 'economic community of central african states (eccas)',
    'economic community of west african states (ecowas 2025)', 'economic community of west african states (ecowas)',
    'europe', 'europe and central asia', 'european union', 'footnotes', 'intergovernmental authority on development (igad)',
    'latin america', 'latin america and the caribbean', 'least developed countries', 'less developed regions',
    'less developed regions, excluding least developed countries',
    'less developed regions, excluding least developed countries, in landlocked developing states',
    'less developed regions, excluding least developed countries, in small island developing states',
    'low-income economies', 'lower-middle-income economies', 'melanesia', 'micronesia', 'middle africa',
    'middle east and north africa', 'net migration rate (per 1,000 population)',
    'north america', 'northern africa', 'northern africa (african union)', 'northern africa and western asia',
    'northern america', 'oceania', 'oceania (exc. australia and new zealand)', 'polynesia', 'sdg regions - global',
    'south america', 'south asia', 'south sudan', 'south-east asia', 'south-eastern asia', 'southern africa',
    'southern africa (african union)', 'southern african development community (sadc)', 'southern asia',
    'sub-saharan africa', 'unicef programme regions - global', 'unicef reporting regions - global',
    'unit multiplier: units', 'unit of measure: %', 'united nations economic commission for africa',
    'upper-middle-income economies', 'western africa', 'western africa (african union)', 'western asia',
    'western europe', 'western pacific', 'world bank (high income)', 'world bank (low income)',
    'world bank (lower middle income)', 'world bank (upper middle income)', 'current age: 15 to 49 years old',
    'time period activity related to when the data are collected: end of fieldwork',
    'observation confidentaility: free'
]

df_demographic = df_demographic[~df_demographic['Country'].astype(str).str.lower().isin([entry.lower() for entry in demographic_irrelevant_entries])]
df_demographic = df_demographic.dropna(subset=['Country'])

# Based on inspection, filter out rows where 'Variant' is not 'Estimates' to focus on actual data
if 'Variant' in df_demographic.columns:
    df_demographic = df_demographic[df_demographic['Variant'] == 'Estimates']

# Based on inspection, filter out rows where 'Year' is not 2022 to get only 2022 data
if 'Year' in df_demographic.columns:
    # Need to handle potential multi-level column index after setting header from row 16
    # Access the 'Year' column correctly based on the actual column names
    # Assuming 'Year' is a top-level column name after setting header=16
    if 'Year' in df_demographic.columns:
        df_demographic['Year'] = pd.to_numeric(df_demographic['Year'], errors='coerce')
        df_demographic = df_demographic[df_demographic['Year'] == 2022]
        df_demographic = df_demographic.dropna(subset=['Year']) # Drop rows where Year couldn't be converted to numeric
    elif ('Year', 'Unnamed: 17_level_1') in df_demographic.columns: # Example for potential multi-level
         df_demographic[('Year', 'Unnamed: 17_level_1')] = pd.to_numeric(df_demographic[('Year', 'Unnamed: 17_level_1')], errors='coerce')
         df_demographic = df_demographic[df_demographic[('Year', 'Unnamed: 17_level_1')] == 2022]
         df_demographic = df_demographic.dropna(subset=[('Year', 'Unnamed: 17_level_1')])


# Load the other two dataframes (assuming they are already cleaned from previous steps)
df_global_dataflow = pd.read_excel("/GLOBAL_DATAFLOW_2018-2022.xlsx", header=1)
df_on_track = pd.read_excel("/On-track and off-track countries.xlsx")

# Clean and standardize country identifiers for global dataflow and on-track data (re-execute cleaning)
df_global_dataflow.rename(columns={'Geographic area': 'Country'}, inplace=True)
df_on_track.rename(columns={'OfficialName': 'Country'}, inplace=True)

df_global_dataflow['Country'] = df_global_dataflow['Country'].astype(str).str.strip().str.lower()
df_on_track['Country'] = df_on_track['Country'].astype(str).str.strip().str.lower()

# Remove parenthesized text and leading/trailing spaces from df_global_dataflow (re-execute cleaning)
df_global_dataflow['Country'] = df_global_dataflow['Country'].apply(lambda x: re.sub(r'\(.*?\)', '', str(x)).strip() if pd.notna(x) else x)

# Remove rows from df_global_dataflow that are not countries (re-execute cleaning)
regions_to_remove_global = ['africa', 'african union', 'americas', 'anguilla', 'arab maghreb union (amu)', 'arab states', 'asia and the pacific', 'caribbean', 'central africa (african union)', 'central america', 'central asia', 'central and southern asia', 'common market for eastern and southern africa (comesa)', 'community of sahel-Saharan states (cen-sad)', 'east african community (eac)', 'east asia and pacific', 'east and southern africa', 'eastern africa', 'eastern africa (african union)', 'eastern asia', 'eastern europe and central asia', 'eastern mediterranean', 'eastern and south-eastern asia', 'eastern and southern africa', 'economic community of central african states (eccas)', 'economic community of west african states (ecowas 2025)', 'economic community of west African states (ECOWAS)', 'europe', 'europe and central asia', 'intergovernmental authority on development (igad)', 'latin america', 'latin america and the caribbean', 'least developed countries (ldc)', 'middle africa', 'middle east and north africa', 'north america', 'northern africa', 'northern africa (african union)', 'northern africa and western asia', 'northern america', 'oceania', 'oceania (exc. australia and new zealand)', 'sdg regions - global', 'south america', 'south asia', 'south sudan', 'south-east asia', 'south-eastern asia', 'southern africa', 'southern africa (african union)', 'southern african development community (sadc)', 'southern asia', 'sub-saharan africa', 'unicef programme regions - global', 'unicef reporting regions - global', 'west and central africa', 'western africa', 'western africa (african union)', 'western asia', 'western europe', 'western pacific', 'world bank (high income)', 'world bank (low income)', 'world bank (lower middle income)', 'world bank (upper middle income)', 'footnotes', 'unit multiplier: units', 'unit of measure: %', 'observation confidentaility: free', 'time period activity related to when the da', 'current age: 15 to 49 years old']

df_global_dataflow = df_global_dataflow[~df_global_dataflow['Country'].astype(str).str.lower().isin([entry.lower() for entry in regions_to_remove_global])]

regions_to_remove_further_global = ['central africa', 'north africa', 'united nations economic commission for africa', 'west africa', 'arab maghreb union', 'common market for eastern and southern africa', 'community of sahel-Saharan states', 'east african community', 'economic community of central african states', 'economic community of west african states', 'intergovernmental authority on development', 'least developed countries', 'southern african development community', 'world bank', 'time period activity related to when the data are collected: end of fieldwork']

df_global_dataflow = df_global_dataflow[~df_global_dataflow['Country'].astype(str).str.lower().isin([entry.lower() for entry in regions_to_remove_further_global])]

df_global_dataflow = df_global_dataflow.dropna(subset=['Country'])
df_on_track = df_on_track.dropna(subset=['Country'])

# Filter and select recent data - re-execute
df_global_dataflow_filtered = df_global_dataflow[
    df_global_dataflow['Indicator'].isin([
        'Antenatal care 4+ visits - percentage of women (aged 15-49 years) attended at least four times during pregnancy by any provider',
        'Skilled birth attendant - percentage of deliveries attended by skilled health personnel'
    ])
]

df_melted = df_global_dataflow_filtered.melt(
    id_vars=['Country', 'Indicator', 'Sex'],
    value_vars=['Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7'],
    var_name='Year_col',
    value_name='Value'
)

year_map = {
    'Unnamed: 3': 2018,
    'Unnamed: 4': 2019,
    'Unnamed: 5': 2020,
    'Unnamed: 6': 2021,
    'Unnamed: 7': 2022
}

df_melted['Year'] = df_melted['Year_col'].map(year_map)

df_melted.dropna(subset=['Value'], inplace=True)
df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')
df_melted.dropna(subset=['Value'], inplace=True)

df_melted_sorted = df_melted.sort_values(by=['Country', 'Indicator', 'Year'], ascending=[True, True, False])
df_most_recent = df_melted_sorted.drop_duplicates(subset=['Country', 'Indicator'], keep='first')

df_pivot = df_most_recent.pivot(index='Country', columns='Indicator', values='Value')


# Merge the dataframes
df_merged = pd.merge(df_pivot, df_on_track, on='Country', how='outer')
df_merged = pd.merge(df_merged, df_demographic[['Country', '2022_projected_births']], on='Country', how='outer')

# Calculate population-weighted averages
# Convert '2022_projected_births' to numeric, coercing errors
df_merged['2022_projected_births'] = pd.to_numeric(df_merged['2022_projected_births'], errors='coerce')

# Define the coverage columns
coverage_cols = [
    'Antenatal care 4+ visits - percentage of women (aged 15-49 years) attended at least four times during pregnancy by any provider',
    'Skilled birth attendant - percentage of deliveries attended by skilled health personnel'
]

# Calculate weighted average for each group in 'Status.U5MR'
weighted_averages = {}
for status in df_merged['Status.U5MR'].unique():
    if pd.notna(status):
        group_df = df_merged[df_merged['Status.U5MR'] == status].copy()
        weighted_averages[status] = {}
        for col in coverage_cols:
            # Drop rows with missing coverage or zero/missing population
            valid_data = group_df.dropna(subset=[col, '2022_projected_births']).copy()
            valid_data = valid_data[valid_data['2022_projected_births'] > 0]

            if not valid_data.empty:
                weighted_avg = (valid_data[col] * valid_data['2022_projected_births']).sum() / valid_data['2022_projected_births'].sum()
                weighted_averages[status][col] = weighted_avg
            else:
                weighted_averages[status][col] = None

# Replace None values in weighted_averages with 0 for plotting
for status in weighted_averages:
    for indicator in weighted_averages[status]:
        if weighted_averages[status][indicator] is None:
            weighted_averages[status][indicator] = 0


# Prepare data for plotting
statuses = list(weighted_averages.keys())
anc4_coverage = [weighted_averages[status].get('Antenatal care 4+ visits - percentage of women (aged 15-49 years) attended at least four times during pregnancy by any provider', 0) for status in statuses]
sba_coverage = [weighted_averages[status].get('Skilled birth attendant - percentage of deliveries attended by skilled health personnel', 0) for status in statuses]

x = np.arange(len(statuses))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, anc4_coverage, width, label='ANC4+ Coverage')
rects2 = ax.bar(x + width/2, sba_coverage, width, label='SBA Coverage')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Population-Weighted Coverage (%)')
ax.set_title('Population-Weighted Coverage by U5MR Status')
ax.set_xticks(x)
ax.set_xticklabels(statuses)
ax.legend()

# Add value labels on top of the bars
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        # Only add label if height is a valid number and not zero
        if isinstance(height, (int, float)) and height > 0:
            ax.annotate(f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

# Save the plot to a BytesIO object for HTML embedding
buf = BytesIO()
plt.savefig(buf, format='png')
plt.close(fig)  # Close the plot to prevent it from displaying twice
data = base64.b64encode(buf.getvalue()).decode('utf-8')
buf.close()

# Interpretation paragraph
interpretation = """
The visualization displays the population-weighted averages for Antenatal Care (ANC4+) and Skilled Birth Attendant (SBA) coverage across countries grouped by their Under-Five Mortality Rate (U5MR) status: 'Acceleration Needed', 'Achieved', and 'On Track'. The 'Achieved' group, representing countries that have met their U5MR reduction targets, shows the highest population-weighted coverage for both ANC4+ and SBA. The 'On Track' group, making sufficient progress, also exhibits relatively high coverage. Conversely, the 'Acceleration Needed' group, which are not on track to meet their U5MR targets, demonstrates the lowest population-weighted coverage for both indicators. This suggests a strong correlation between higher levels of maternal and child health service coverage and better progress in reducing under-five mortality. A key caveat is that these are population-weighted averages, meaning countries with larger populations have a greater influence on the average for their respective groups. Additionally, the analysis relies on the availability and quality of data for each indicator and the accuracy of the U5MR status classifications and 2022 projected births data. Missing data for some countries or indicators could impact the weighted averages.
"""

# Generate HTML output
html_output = f"""
<!DOCTYPE html>
<html>
<head>
<title>Learning and Skills Data Analyst Consultant – Req. #581598</title>
</head>
<body>
    <h1>Learning and Skills Data Analyst Consultant – Req. #581598</h1>
    <h2>Population-Weighted Coverage by U5MR Status</h2>
    <img src="data:image/png;base64,{data}" alt="Population-Weighted Coverage by U5MR Status Bar Chart">
    <h2>Interpretation of Results</h2>
    <p>{interpretation}</p>
</body>
</html>
"""

# Display the HTML output
display(HTML(html_output))

