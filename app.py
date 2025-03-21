import importlib.util
import streamlit as st
import pandas as pd
import urllib.parse
import os
import base64
import docx
from io import BytesIO
from io import BytesIO
from streamlit import session_state as ss
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer

# Function to load full dataset
@st.cache_data
def load_full_data(file_path,sheet, skip_row):
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding="utf-8")
        elif file_path.endswith("Out.xlsx"):
            df = pd.read_excel(file_path, engine='openpyxl',sheet_name=sheet, skiprows=skip_row)
        else:
            return None
        return df
    except FileNotFoundError:
        st.warning(f"File not found: {file_path}. Upload it below if missing.")
        return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# ✅ Define pages with correct columns
pages = {
    "Power Generation": {
        "file": "power_generation",
        "column": 1,  # First column
        "pathway": "IEA NZE, IPCC",
        "metrics": ["tCO2e", "tCO2/MWh", "% Zero Carbon Capacity"],
        "color": "#6FA8DC",  # Green
    },
    "Other Industries": {
        "file": "other_industry",
        "column": 2,  
        "pathway": "IEA NZE, IPCC",
        "metrics": ["tCO2e", "tCO2/tonne"],
        "color": "#6FA8DC",  # Orange
    },
    "Pulp & Paper": {
        "file": "pulp_paper",
        "column": 3,  
        "pathway": "IEA NZE, IPCC",
        "metrics": ["tCO2e", "tCO2/tonne"],
        "color": "#6FA8DC",  # Orange
    },
    "Oil & Gas": {
        "file": "oil_gas",
        "column": 1,
        "pathway": "IPCC",
        "metrics": ["tCO2e", "tCO2e/boe"],
        "color": "#6FA8DC",  # Purple
    },
    "Rail": {
        "file": "rail",
        "column": 2,  # Second column
        "pathway": "IEA NZE",
        "metrics": ["tCO2e", "tCO2/tonne.km"],
        "color": "#D77932",  # Brown
    },
    "Aluminum Production": {
        "file": "aluminum_production",
        "column": 3,  
        "pathway": "IEA NZE 2021",
        "metrics": ["tCO2e", "tCO2/tonne"],
        "color": "#D77932",  # Grey Blue
    },
    "Residential": {
        "file": "residential",
        "column": 1,  
        "pathway": "CREEM",
        "metrics": ["tCO2e", "tCO2/m2"],
        "color": "#D77932",  # Purple
    },
    "Road": {
        "file": "road",
        "column": 2,  
        "pathway": "IEA NZE",
        "metrics": ["tCO2e", "tCO2/tonne.km"],
        "color": "#D77932",  # Purple
    },
    "Cement": {
        "file": "cement",
        "column": 3,  
        "pathway": "IEA NZE 2021",
        "metrics": ["tCO2e", "tCO2/tonne"],
        "color": "#D77932",  # Grey Blue
    },
    "Commercial": {
        "file": "commercial",
        "column": 1,  # Third column
        "pathway": "CREEM",
        "metrics": ["tCO2e", "tCO2/m2"],
        "color": "#D77932",  # Pink
    },
    "Aviation": {
        "file": "aviation",
        "column": 2,  # Third column
        "pathway": "IEA NZE",
        "metrics": ["tCO2e", "tCO2/tonne.km"],
        "color": "#D77932",  # Pink
    },
    "Steel": {
        "file": "steel",
        "column": 3,  # Third column
        "pathway": "IEA NZE",
        "metrics": ["tCO2e", "tCO2/tonne"],
        "color": "#D77932",  # Pink
    },
    "Chemical": {
        "file": "chemical",
        "column": 1,  # Third column
        "pathway": "IEA NZE",
        "metrics": ["tCO2e", "tCO2/tonne"],
        "color": "#D77932",  # Pink
    },
     "FLAG ": {
        "file": "FLAG",
        "column": 2,  # Third column
        "pathway": "IPCC",
        "metrics": ["tCO2e", "tCO2/m3","tCO2/freshweight"],
        "color": "#D77932",  # Pink
    },
    "Apperal & Footwear": {
        "file": "apparel_footwear",
        "column": 2,  # Third column
        "pathway": "cross sector",
        "metrics": ["tCO2e", "tCO2/MWh"],
        "color": "#C27BA0",  # Pink
    },
    "Financial Institution": {
        "file": "financial_institution",
        "column": 3,  # Third column
        "pathway": "cross sector",
        "metrics": ["tCO2e", "tCO2/MWh"],
        "color": "#C27BA0",  # Pink
    },
    "Other Sector": {
        "file": "other_sector",
        "column": 1,  # Third column
        "pathway": "",
        "metrics": [""],
        "color": "#C27BA0",  # Pink
    },
}

# ✅ Set page config
st.set_page_config(page_title="Pathway Explorer", layout="wide")

# ✅ Get the selected page from URL reference (if exists)
query_params = st.query_params
selected_page = query_params.get("selected_page", None)

# ✅ Initialize session state for navigation
if "selected_page" not in st.session_state:
    st.session_state.selected_page = selected_page if selected_page else "Home"

# ✅ Navigation function using `st.query_params`
def navigate(page):
    st.session_state.selected_page = page
    st.query_params["selected_page"] = page  # Updates the URL dynamically
    st.rerun()  # Forces the page to update



# Create column layout
col1, col2, col3, col4 = st.columns([7, 1, 1, 1])
# Render buttons with conditional highlighting
with col2:
    if st.button("Home", use_container_width=True, 
                 type="primary" if st.session_state.selected_page== "Home" else "secondary"):
        navigate("Home")

with col3:
    if st.button("Reference", use_container_width=True, 
                 type="primary" if st.session_state.selected_page == "Reference" else "secondary"):
        navigate("Reference")

with col4:
    if st.button("Document", use_container_width=True, 
                 type="primary" if st.session_state.selected_page == "Document" else "secondary"):
        navigate("Document")



# ✅ Back Button at Top Left (Only on subpages)
#if st.session_state.selected_page != "Home":
#    col1, col2 = st.columns([0.2, 0.8])  
#    with col1:
#        if st.button("🔙 Back to Home"):
#            navigate("Home")

#    with col2:
#        st.title(st.session_state.selected_page)

# ✅ Main Page with Tiles in 3 Columns
if st.session_state.selected_page == "Home":
    col1, col2 = st.columns([0.15, 0.85])  # Left for image, right for title
    with col1:
        st.image("SBT_Logo.png", width=300)  # Adjust width as needed

    with col2:
        st.markdown(
            """
            <style>
            /* Tooltip styling for title */
            .title-tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }

            /* Tooltip text */
            .title-tooltip:hover::after {
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background-color: rgba(0, 0, 0, 0.7); /* Dark background for the tooltip */
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
                white-space: nowrap;
                z-index: 1;  /* Ensure tooltip is above */
                opacity: 1;
                transition: opacity 0.3s;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Add the title with a tooltip
        st.markdown(
            """
            <style>
            .title-tooltip {
                position: relative;
                top: 10px;   /* Moves the text down */
                color: #8B008B;
                left: 280px; /* Moves the text to the right */
                text-align: left;  /* Aligns the text to the right */
            }
            </style>
            <div class="title-tooltip" data-tooltip="Explore various pathways for climate action">
                <span style="font-size: 50px; font-weight: bold;">Pathway Explorer</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write("Here you can find all the raw data, eligible scenarios and pathways that informs the cross sector and sector-specific standards in the SBTi")
    col1, col2, col3 = st.columns(3)  # Three columns for tiles

    # ✅ Render tiles into assigned columns
    for title, data in pages.items():
        tile_color = data["color"]
        pathway = data["pathway"]
        metrics_html = "<br>- ".join(data["metrics"])
        page_slug = urllib.parse.quote(title)  # Convert title to a valid URL fragment

        col = col1 if data["column"] == 1 else col2 if data["column"] == 2 else col3

        with col:

            # ✅ Clickable Tile with a Link Reference
            st.markdown(
                f"""
                <a href="?selected_page={page_slug}" style="text-decoration: none;">
                    <div style="background-color:{tile_color}; 
                                padding:23px; 
                                border-radius:8px; 
                                text-align:center;
                                margin-bottom: 20px; 
                                cursor:pointer; 
                                box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
                        <h3 style='color:white;'>{title}</h3>
                        <p style='color:white; margin:5px 0;'><b>Pathway:</b> {pathway}</p>
                        <p style='color:white; margin:5px 0;'><b>Metrics:</b><br>- {metrics_html}</p>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )

elif st.session_state.selected_page == "Reference":
    # Streamlit UI
    # Display logo and title
    col1, col2 = st.columns([0.15, 0.85])  # Left for image, right for title
    with col1:
        st.image("SBT_Logo.png", width=300)  # Adjust width as needed

    with col2:
        st.markdown(
            """
            <style>
            /* Tooltip styling for title */
            .title-tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }

            /* Tooltip text */
            .title-tooltip:hover::after {
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background-color: rgba(0, 0, 0, 0.7); /* Dark background for the tooltip */
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
                white-space: nowrap;
                z-index: 1;  /* Ensure tooltip is above */
                opacity: 1;
                transition: opacity 0.3s;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Add the title with a tooltip
        st.markdown(
            """
            <style>
            .title-tooltip {
                position: relative;
                top: 10px;   /* Moves the text down */
                color: #8B008B;
                left: 280px; /* Moves the text to the right */
                text-align: left;  /* Aligns the text to the right */
            }
            </style>
            <div class="title-tooltip" data-tooltip="Explore various pathways for climate action">
                <span style="font-size: 50px; font-weight: bold;">Pathway Explorer</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("Here you can find all the raw data, eligible scenarios and pathways that informs the cross sector and sector-specific standards in the SBTi")

    st.markdown(
        """
        <style>
        /* Style for the tab container to ensure even distribution */
        .stTabs [data-baseweb="tablist"] {
            display: flex;
            justify-content: flex-start;  /* Align tabs to the left without extra space */
            gap: 5px;  /* Reduced space between tabs */
        }

        /* Style for each individual tab */
        .stTabs [data-baseweb="tab"] {
            background-color:rgb(42,52,68);  /* Green background for all tabs */
            color: white;
            padding: 10px;
            text-align: center;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            flex-grow: 0;  /* Ensure tabs are not stretched */
        }

        /* Style for tab when hovered */
        .stTabs [data-baseweb="tab"]:hover {
            background-color:rgb(211, 151, 133);  /* Darker green when hovered */
            cursor: pointer;  /* Change cursor to pointer when hovered */
        }

        /* Style for active tab (clicked tab) */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color:rgb(234,137,71);  /* Dark green when tab is selected */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Define tabs for multiple data sources
    tabs = st.tabs(["Document", "Criteria", "Phase-Out", "Residuals"])

    # File paths and filter columns for different datasets
    datasets_info = {
        "Document": {
            "file_path": "Alldata.xlsx",
            "filter_columns": ["Model", "Scenario", "Region", "Variable"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Criteria": {
            "file_path": "Phase-Out.xlsx",
            "filter_columns": ["Model", "Scenario", "Region", "Variable"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Phase-Out": {
            "file_path": "Phase-Out.xlsx",
            "filter_columns": ["Model", "Scenario"],
            "remove_columns": [],
            "apply_year_filter": False
        },
            "Residuals": {
            "file_path": "Phase-Out.xlsx",
            "filter_columns": ["Model", "Scenario"],
            "remove_columns": [],
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

                df = load_full_data(file_path,None,None)

                # Drop integer and float columns, keeping only categorical columns
                #categorical_columns = df.select_dtypes(exclude=['int64', 'float64']).columns

                # Remove unwated columns
                categorical_columns = dataset_info['filter_columns']

                # Initialize session state for selection persistence
                if "selected_var" not in st.session_state:
                    st.session_state["selected_var"] = categorical_columns[0]

                st.title("Eligible SBTi Scenarios")
                st.write("These are the eligible Scenarios that pass the principled-driven criteria used in cross-sector and sector-specific pathways")
                # Layout: Left (buttons) | Right (data)
                col1, col2 = st.columns([1, 5])

                with col1:
                        
                    for col in categorical_columns:
                        if st.button(str(df[col].nunique())+" "+col):
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
                        #st.write(f'{unique_df[selected_var].nunique()}, unique {selected_var}')
                        st.dataframe(unique_df[selected_var].values, use_container_width=True, height=600)  # Full-width display


            elif dataset_name == 'Criteria':

                file_path = dataset_info["file_path"]
                remove_cols = dataset_info['remove_columns']
                df = load_full_data(file_path,None, None)
                st.write('This sheet shows the phase out dates for some fossil commodities')
                st.write('Disclaimer: The sector-specific requirements for key economic activities are derived from specific scenarios e.g IEA to provide additional guidelines on how activities need to transition at interim period on the way to net zero. The activity specific milestones are not available in all IPCC scenarios and there may be wide variations across  IPCC models. Therefore, the granularity that IEA provides for these indicators are useful, even though they may not align with the assumptions from the overall IPCC scenarios.')
                st.dataframe(df, hide_index=True)

            elif dataset_name=="Phase-Out":
                file_path = dataset_info["file_path"]
                remove_cols = dataset_info['remove_columns']
                df = pd.read_excel(file_path,sheet_name='Phase out dates',skiprows=3)
                st.dataframe(df, hide_index=True)
            
            elif dataset_name=="Residuals":
                file_path = dataset_info["file_path"]
                remove_cols = dataset_info['remove_columns']
                df = pd.read_excel(file_path,sheet_name='Residuals',skiprows=2)
                st.dataframe(df, hide_index=True)
            else:
                st.error("Error loading data preview.")
elif st.session_state.selected_page == "Document":
 # Redirect to document page
        st.title("PDF Viewer")

        # Local file path (Replace this with your actual path)
        pdf_path = "documents/sample.pdf"


        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                ss.pdf_ref = f.read()  # Store binary content
        else:
            st.error("File not found. Please check the path.")
            ss.pdf_ref = None

        # Display PDF using `streamlit_pdf_viewer`
        if st.session_state.pdf_ref:
            pdf_viewer(input=st.session_state.pdf_ref, width="100%")
            # Download Button
            st.download_button(label="📥 Download PDF", 
                            data=ss.pdf_ref, 
                            file_name="sample.pdf", 
                            mime="application/pdf")
            
# ✅ Handle Page Navigation and Load Content
else:
    module_name = pages.get(st.session_state.selected_page, {}).get("file")
    if module_name:
        try:
            spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  
        except Exception as e:
            st.error(f"⚠️ Error loading {module_name}: {e}")
