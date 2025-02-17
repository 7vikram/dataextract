import streamlit as st
import pandas as pd
from io import BytesIO
import plotly.express as px

# Set Streamlit page to wide layout
st.set_page_config(layout="wide")

# Function to load data preview (first 100 rows)
@st.cache_data
def load_data_preview(file_path):
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, nrows=100, engine='openpyxl',)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding="utf-8", nrows=100)
        else:
            return None
        return df
    except FileNotFoundError:
        st.warning(f"File not found: {file_path}. Upload it below if missing.")
        return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Function to load full dataset
@st.cache_data
def load_full_data(file_path):
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl',)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding="utf-8")
        else:
            return None
        return df
    except FileNotFoundError:
        st.warning(f"File not found: {file_path}. Upload it below if missing.")
        return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Function to filter data
def filter_data(df, filters):
    for col, value in filters.items():
        if value and col in df.columns:
            df = df[df[col].astype(str).str.contains(value, case=False, na=False)]
    return df

# Function to filter based on year range (specific to Dataset 1)
def filter_by_year(df, filter_columns, start_year, end_year):
    year_columns = [(col) for col in df_full.columns if str(col).isdigit()]
    year_columns = sorted(year_columns, key=int)
    selected_years = [year for year in year_columns if start_year <= int(year) <= end_year]
    return df[filter_columns + selected_years]

# Function to convert DataFrame to Excel for download
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
# Display logo and title
col1, col2 = st.columns([1, 5])
with col1:
    st.image("SBT_Logo.jpg", width=100)
with col2:
    st.title("Pathway Explorer")

st.write("Here you can find all the raw data, eligible scenarios and pathways that informs the cross sector and sector-specific standards in the SBTi")

# Define tabs for multiple data sources
tabs = st.tabs(["Document", "IPCC", "Cross-Sector Pathways", "Power-Sector", "Chemical", "Building", "Industry"])

# File paths and filter columns for different datasets
datasets_info = {
    "Document": {
        "file_path": "Alldata.xlsx",
        "filter_columns": ["Model", "Scenario", "Region", "Variable"],
        "apply_year_filter": False
    },
    "IPCC": {
        "file_path": "C1-3_summary_2050_variable.csv",
        "filter_columns": ["Category", "Model", "Scenario", "Region", "Variable", "Unit"],
        "apply_year_filter": True
    },
    "Cross-Sector Pathways": {
        "file_path": "Alldata.xlsx",
        "filter_columns": ["Model", "Scenario", "Region", "Variable", "Unit"],
        
        "apply_year_filter": True
    },
    "Power-Sector": {
        "file_path": "Pathway Database - Updated 2024-205.xlsx",
        "filter_columns": ["Metric","Model", "Scenario", "Unit"],
        "apply_year_filter": False
    },
    "Chemical": {
        "file_path": "N2Oandchemical.xlsx",
        "filter_columns": ["Category", "Parameter", "Unit"],
        "apply_year_filter": False
    },
    "Building": {
        "file_path": "Alldata2.xlsx",
        "filter_columns": ["Model", "Scenario"],
        "apply_year_filter": False
    },
    "Industry": {
        "file_path": "Alldata3.xlsx",
        "filter_columns": ["Model", "Scenario"],
        "apply_year_filter": False
    }
}

# Iterate over each tab and display corresponding data
for idx, tab in enumerate(tabs):
    dataset_name = list(datasets_info.keys())[idx]
    dataset_info = datasets_info[dataset_name]
    #st.write(tab)
    # Document Tab

    with tab:
        if dataset_name=='Document':
            
            file_path = dataset_info["file_path"]

            df = load_full_data(file_path)
            # Drop integer and float columns, keeping only categorical columns
            categorical_columns = df.select_dtypes(exclude=['int64', 'float64']).columns

            # Initialize session state for selection persistence
            if "selected_var" not in st.session_state:
                st.session_state["selected_var"] = None

            st.title("Eligible SBTi Scenarios")
            st.write("These are the eligible Scenarios that pass the principled-driven criteria used in cross-sector and sector-specific pathways")
            # Layout: Left (buttons) | Right (data)
            col1, col2 = st.columns([1, 5])

            with col1:
                    
                for col in categorical_columns:
                    if st.button(col):
                        st.session_state["selected_var"] = col  # Store selection persistently

            # Right Column: Display unique values
            with col2:
                if st.session_state["selected_var"]:
                    selected_var = st.session_state["selected_var"]
                    #st.subheader(f"Unique Values for: {selected_var}")

                    # Search box for filtering unique values
                    search_query = st.text_input("Search:", "")

                    # Get unique values and filter based on search query
                    unique_values = df[selected_var].dropna().unique()
                    filtered_values = [val for val in unique_values if search_query.lower() in str(val).lower()]
                        
                    # Convert to DataFrame and display
                    unique_df = pd.DataFrame(filtered_values, columns=[selected_var]).reset_index()
                    print(unique_df[selected_var])
                    st.dataframe(unique_df[selected_var].values, use_container_width=True, height=600)  # Full-width display



        elif dataset_name != "Document":
            st.subheader(f"View and Filter {dataset_name}")
            
            # Load data preview (first 1000 rows only)
            file_path = dataset_info["file_path"]
        
            df_preview = load_data_preview(file_path)

            if df_preview is not None:
                st.write("### Data Preview")
                st.dataframe(df_preview.head())

                # Load full data for filtering purposes (without limiting to preview rows)
                df_full = load_full_data(file_path)

                # Filtering UI based on the full data columns (not preview)
                st.write("### Filter Data")
                filters = {}
                filter_columns = dataset_info["filter_columns"]
                cols = st.columns(len(filter_columns))

                selected_values = {}  # For storing selected filter values
                
                # Update filter options dynamically based on previous selections
                # Update filter options dynamically based on previous selections
                for i, col in enumerate(filter_columns):
                    if col in df_full.columns:
                        options = df_full[col].astype(str).unique().tolist()
                        selected_values[col] = cols[i].multiselect(f"{col}", options, key=f"{col}_{idx}")

                # Apply the filter to the dataset
                for col, values in selected_values.items():
                    if values:  # Ensure selections are made
                        df_full = df_full[df_full[col].astype(str).str.lower().isin([v.lower() for v in values])]

                
                # Add year range filters for 'AllData' dataset or any dataset requiring year filtering
                if dataset_info["apply_year_filter"]:
                    # Get list of years from the dataset
                    year_columns = [str(col) for col in df_full.columns if str(col).isdigit()]
                    year_columns = sorted(year_columns, key=int)  # Sort years in ascending order

                    # Dropdown for Start Year
                    start_year = st.selectbox(
                        "Select Start Year:",
                        options=year_columns,
                        index=0,  # Default to the first year
                        key=f"start_year_{dataset_name}_{idx}"
                    )

                    # Dropdown for End Year
                    end_year = st.selectbox(
                        "Select End Year:",
                        options=year_columns,
                        index=len(year_columns)-1,  # Default to the last year
                        key=f"end_year_{dataset_name}_{idx}"
                    )

                    # Ensure end year is greater than or equal to start year
                    if int(end_year) < int(start_year):
                        st.error("End Year must be greater than or equal to Start Year.")
                        end_year = start_year

                    # Apply the year filter to the dataset
                    df_full = filter_by_year(df_full, filter_columns, int(start_year), int(end_year))

                # Button to load full data and apply filters
                if st.button("Apply Filters", key=f"apply_filters_{dataset_name}_{idx}"):
                    # Show filtered data
                    st.write(f"### Filtered Data {dataset_name}")
                    st.dataframe(df_full.head(10))

                    # Button to download filtered data
                    excel_data = to_excel(df_full)
                    st.download_button(
                        label="Download Excel",
                        data=excel_data,
                        file_name=f"{dataset_name}_filtered_data.xlsx",
                        mime="application/vnd.ms-excel",
                        key=f"download_button_{dataset_name}_{idx}"  # Ensure unique key for download button
                    )

                    # Identify year columns (assuming they are numeric)
                    year_columns = [(col) for col in df_full.columns if str(col).isdigit()]
                    year_columns = sorted(year_columns, key=int)

                    if dataset_name=="IPCC" or dataset_name=="Cross-Sector Pathways":
                        st.write("### Visualizing Data")
                        
                        df_model = df_full.copy()
                        df_model.fillna(0, inplace=True)

                        # Ensure year columns are numeric
                        df_model[year_columns] = df_model[year_columns].apply(pd.to_numeric, errors='coerce')

                        # Reshape data from wide to long format
                        df_melted = df_model.melt(id_vars=["Model", "Scenario", "Region", "Variable", "Unit"], 
                                                value_vars=year_columns, 
                                                var_name="Year", value_name="Value")
                        
                        #df_melted = df_melted.groupby(['Variable','Year'])['Value'].median().reset_index()
                        # Convert Year column to integer
                        df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')
                        df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors='coerce')

                        median_values = df_melted.groupby('Year')['Value'].median().reset_index()
                        median_values['Scenario'] = 'Median'

                        # Combine the original data with the median data
                        df_combined = pd.concat([df_melted, median_values])
                        df_combined.dropna(subset=["Value"], inplace=True)
                        df_combined = df_combined[df_combined['Value']!=0]
                        # Plotly line chart with multiple lines for different models
                        fig = px.line(df_combined, x="Year", y="Value", color="Scenario",
                                    #title="Trend Comparison of Selected Models",
                                    labels={"Value": "Metric Value", "Year": "Year", "Scenario": "Scenario"},
                                    markers=False)  # Add markers to check if points are plotted
                        
                        fig.update_xaxes(type="category")
                        # Set chart height
                        fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                        fig.update_traces(line=dict(color="black", width=4), selector=dict(name="Median"),)

                        st.plotly_chart(fig)      

                    if dataset_name=="Power-Sector":
                        st.write("### Visualizing Data")
                        # Calculate the median line across all years
                        #print(df_full.columns)
                        df_full = df_full[~df_full.apply(lambda row: row.astype(str).str.contains('Median').any(), axis=1)]

                        df_melted = df_full.melt(id_vars=["Metric", "Model", "Scenario", "Unit", "scen_id"], 
                                            value_vars=[(year) for year in range(2020, 2051, 5)], 
                                            var_name="Year", value_name="Value")

                        # Calculate the median across all models for each year
                        median_values = df_melted.groupby('Year')['Value'].median().reset_index()
                        median_values['Model'] = 'Median - ALL'
                        median_values['Scenario'] = 'Median - ALL'
                        median_values['scen_id'] = 'Median - ALL'

                        # Combine the original data with the median data
                        df_combined = pd.concat([df_melted, median_values])
                        unit = df_combined["Unit"].unique()[0]
                        # Plot the line chart
                        fig = px.line(df_combined, x="Year", y="Value", color="scen_id", 
                                    title="Trend Comparison of scen_id and Median", 
                                    labels={"Value": unit, "Year": "Year", "scen_id": "scen_id"})

                        # Set the line styles for median and other models
                        fig.update_traces(line=dict(color="grey"), selector=dict(name="scen_id"))
                        fig.update_traces(line=dict(color="black", width=4), selector=dict(name="Median - ALL"),)

                        # Set chart height
                        fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                        # Display the plot in Streamlit
                        st.plotly_chart(fig)

                    
                    if dataset_name == "Chemical":
                        df_full.columns = df_full.columns.astype(str)

                        # Melt DataFrame for Plotly
                        df_melted = df_full.melt(id_vars=["Category", "Parameter", "Unit"], 
                                                var_name="Year", 
                                                value_name="Value")

                        # Streamlit App
                        st.title("Parameter Trends Over Time")

                        # Loop through each unique Parameter and plot separate charts
                        for i, param in enumerate(df_melted["Parameter"].unique()):
                            df_filtered = df_melted[df_melted["Parameter"] == param]
                            unit = df_melted["Unit"].unique()[0]

                            # Create line chart
                            fig = px.line(df_filtered, 
                                        x="Year", 
                                        y="Value", 
                                        color="Category",
                                        markers=True,  # Add markers to data points
                                        labels={"Value": unit},
                                        title=f"{param} - Line Chart by Category")
                            
                            # Ensure x-axis only shows the available years in data
                            fig.update_xaxes(type="category")

                            # Display chart in Streamlit
                            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Error loading data preview.")
