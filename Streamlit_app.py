# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64
import time

# Schneider Electric Brand Colors
SCHNEIDER_COLORS = {
    'primary_green': '#3DCD58',
    'dark_green': '#004F3B',
    'light_gray': '#F5F5F5',
    'dark_gray': '#333333',
    'white': '#FFFFFF',
    'accent_blue': '#007ACC',
    'chart_colors': ['#3DCD58', '#004F3B', '#007ACC', '#00A6A0', '#676767', '#CCCCCC']
}

def load_css():
    """Load custom CSS styles with Schneider Electric branding"""
    st.markdown(f"""
        <style>
        .main {{
            background-color: #1E1E1E;
            color: {SCHNEIDER_COLORS['white']};
        }}
        .stApp {{
            background-color: #1E1E1E;
        }}
        .metric-card {{
            background-color: {SCHNEIDER_COLORS['dark_green']};
            border: 1px solid {SCHNEIDER_COLORS['primary_green']};
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin: 0.5rem 0;
            transition: transform 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 15px rgba(61, 205, 88, 0.2);
        }}
        .stMetric {{
            background-color: {SCHNEIDER_COLORS['dark_green']};
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid {SCHNEIDER_COLORS['primary_green']};
        }}
        .stMetric:hover {{
            border-color: {SCHNEIDER_COLORS['accent_blue']};
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2rem;
            background-color: transparent;
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {SCHNEIDER_COLORS['white']};
            background-color: transparent;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: {SCHNEIDER_COLORS['primary_green']};
            background-color: rgba(61, 205, 88, 0.1);
        }}
        .stDataFrame {{
            background-color: #2D2D2D;
            border-radius: 0.5rem;
            border: 1px solid {SCHNEIDER_COLORS['primary_green']};
        }}
        .download-link {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: {SCHNEIDER_COLORS['primary_green']};
            color: white;
            text-decoration: none;
            border-radius: 0.3rem;
            margin: 1rem 0;
            transition: background-color 0.3s ease;
        }}
        .download-link:hover {{
            background-color: {SCHNEIDER_COLORS['dark_green']};
        }}
        .title-container {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: linear-gradient(90deg, {SCHNEIDER_COLORS['dark_green']}, transparent);
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }}
        .upload-message {{
            text-align: center;
            padding: 2rem;
            border: 2px dashed {SCHNEIDER_COLORS['primary_green']};
            border-radius: 1rem;
            margin: 2rem 0;
        }}
        .header-container {{
            display: flex;
            align-items: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: linear-gradient(90deg, rgba(0,79,59,0.2), transparent);
            border-radius: 0.5rem;
        }}
        </style>
    """, unsafe_allow_html=True)
def process_dataframe(df):
    """Process the input dataframe according to business logic"""
    try:
        # Rename columns
        column_mapping = {
            'Part Number (Standardized)': 'Part Number',
            'Supplier DUNS Elementary Code': 'DUNS Elementary Code',
            'Next 12m Projection Quantity (Normalized UoM)': '12m Projection Quantity',
            'Line Price (EUR/NUoM) (Includes SQL FX)': 'Unit Price in Euros',
            'CPR:Best Line Price (including Logistics Simulation Delta if any) (EUR/NUoM) (Global)': 'Best Price in Euros',
            'CPR:Quantity of Best Price Line (NUoM) (Global)': 'Best Price Quantity',
            'CPR:Site Name of Best Price Line (Global)': 'Best Price Site',
            'CPR:Site Region of Best Price Line (Global)': 'Best Price Region',
            'CPR:Supplier Name of Best Price Line (Global)': 'Best Price Supplier',
            'CPR:Total Opportunity (EUR), including Logistics Simulation (Global)': 'Total Opportunity'
        }
        df = df.rename(columns=column_mapping)

        # Convert numeric columns
        for col in df.select_dtypes(include=['object']).columns:
            try:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''))
            except:
                pass

        # Apply filters
        india_sites = ['IN Bangalore ITB', 'IN Chennai', 'IN Hyderabad', 'IN Bangalore SEPFC']
        category_codes = ('A', 'B', 'C', 'D', 'H', 'K', 'G', 'E', 'P1', 'P2', 'M1', 'M2')
        
        df_filtered = df[
            (df['Site Name'].isin(india_sites)) & 
            (df['Category Code'].str.startswith(category_codes))
        ]

        # Apply spend and region filters
        df_filtered = df_filtered[
            (df_filtered['Spend (EUR)'] > 50000) & 
            (df_filtered['Best Price Region'] != 'India / MEA') & 
            (df_filtered['Total Opportunity'] <= -5000)
        ]

        # Calculate ratio
        df_filtered['Qty/projection'] = ((df_filtered['Best Price Quantity'] / df_filtered['12m Projection Quantity']) * 100)
        
        # Filter one-time buys
        df_filtered = df_filtered[df_filtered['Qty/projection'] > 5]

        # Add absolute opportunity column for visualization
        df_filtered['Absolute Opportunity'] = df_filtered['Total Opportunity'].abs()

        # Format float values
        for col in df_filtered.select_dtypes(include=['float64']).columns:
            df_filtered[col] = df_filtered[col].round(2)

        return df_filtered
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

def generate_insights(df):
    """Generate key insights from the processed data"""
    total_opportunity = df['Total Opportunity'].sum()
    avg_qty_projection = df['Qty/projection'].mean()
    
    # Use absolute values for top suppliers
    top_suppliers = df.groupby('Supplier Name')['Absolute Opportunity'].sum().sort_values(ascending=False).head(5)
    top_categories = df.groupby('Category Code')['Absolute Opportunity'].sum().sort_values(ascending=False).head(5)
    
    return {
        'total_opportunity': total_opportunity,
        'avg_qty_projection': avg_qty_projection,
        'top_suppliers': top_suppliers,
        'top_categories': top_categories
    }
def create_visualizations(df):
    """Create visualizations using Plotly with Schneider Electric theme"""
    template = {
        'layout': {
            'plot_bgcolor': '#1E1E1E',
            'paper_bgcolor': '#1E1E1E',
            'font': {'color': SCHNEIDER_COLORS['white']},
            'title': {'font': {'color': SCHNEIDER_COLORS['white']}},
            'xaxis': {'gridcolor': '#333333', 'linecolor': '#333333'},
            'yaxis': {'gridcolor': '#333333', 'linecolor': '#333333'}
        }
    }

    # Opportunity by Category
    category_data = df.groupby('Category Code')['Absolute Opportunity'].sum().reset_index()
    category_data = category_data.sort_values('Absolute Opportunity', ascending=True)
    
    fig1 = px.bar(
        category_data,
        x='Absolute Opportunity',
        y='Category Code',
        title='Savings Opportunity by Category (EUR)',
        orientation='h',
        color_discrete_sequence=[SCHNEIDER_COLORS['primary_green']]
    )
    fig1.update_layout(
        template=template,
        yaxis_title="Category Code",
        xaxis_title="Savings Opportunity (EUR)",
        height=500,
        showlegend=False,
        hovermode='closest',
        hoverlabel=dict(bgcolor=SCHNEIDER_COLORS['dark_green'])
    )

    # Opportunity by Supplier (Top 10)
    supplier_data = df.groupby('Supplier Name')['Absolute Opportunity'].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig2 = px.pie(
        supplier_data,
        values='Absolute Opportunity',
        names='Supplier Name',
        title='Top 10 Suppliers by Savings Opportunity',
        color_discrete_sequence=SCHNEIDER_COLORS['chart_colors']
    )
    fig2.update_layout(
        template=template,
        hoverlabel=dict(bgcolor=SCHNEIDER_COLORS['dark_green'])
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')

    # Bar chart for top suppliers
    fig3 = px.bar(
        supplier_data,
        x='Supplier Name',
        y='Absolute Opportunity',
        title='Top 10 Suppliers by Savings Opportunity (EUR)',
        color_discrete_sequence=[SCHNEIDER_COLORS['primary_green']]
    )
    fig3.update_layout(
        template=template,
        xaxis_title="Supplier Name",
        yaxis_title="Savings Opportunity (EUR)",
        xaxis={'tickangle': 45},
        height=500,
        showlegend=False,
        hoverlabel=dict(bgcolor=SCHNEIDER_COLORS['dark_green'])
    )

    return [fig1, fig2, fig3]

def get_table_download_link(df):
    """Generate a styled download link for the processed data"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="processed_data.csv" class="download-link">📥 Download Processed Data</a>'
    return href

def main():
    st.set_page_config(
        page_title="Schneider Electric - Procurement Analysis Tool",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    load_css()

    # Header with logo
    st.markdown("""
        <div class="header-container">
            <img src="https://www.se.com/ww/en/assets/wiztopic/615aeb0184d20b323d58575e/Schneider-Electric-logo-jpg-_original.jpg" 
                 style="width: 150px; margin-right: 20px;">
            <div>
                <h1 style="margin: 0;">Procurement Data Analysis Tool</h1>
                <p style="color: #3DCD58; margin: 0;">Transform your procurement data into actionable insights</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # File upload with styled message
    st.markdown("""
        <div class="upload-message">
            <h3 style="color: #3DCD58;">Upload Your Data File</h3>
            <p>Supported formats: Excel (.xlsx) or CSV (.csv)</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=['xlsx', 'csv'])

    if uploaded_file is not None:
        try:
            with st.spinner('Processing your data...'):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                time.sleep(0.5)  # Short delay for visual feedback

            st.success("✅ File uploaded and processed successfully!")

            # Process data
            df_processed = process_dataframe(df)
            
            if df_processed is not None and not df_processed.empty:
                # Generate insights
                insights = generate_insights(df_processed)
                
                # Display metrics with enhanced styling
                st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "💰 Total Savings Opportunity",
                        f"€{abs(insights['total_opportunity']):,.2f}"
                    )
                with col2:
                    st.metric(
                        "📊 Avg Qty/Projection Ratio",
                        f"{insights['avg_qty_projection']:.2f}%"
                    )
                with col3:
                    st.metric(
                        "🔢 Number of Parts",
                        f"{len(df_processed):,}"
                    )
                with col4:
                    st.metric(
                        "🏢 Number of Suppliers",
                        f"{df_processed['Supplier Name'].nunique():,}"
                    )
                st.markdown("</div>", unsafe_allow_html=True)

                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📈 Visualizations", "📋 Data Table", "🎯 Top Analysis"])

                with tab1:
                    figures = create_visualizations(df_processed)
                    st.plotly_chart(figures[0], use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(figures[1], use_container_width=True)
                    with col2:
                        st.plotly_chart(figures[2], use_container_width=True)

                with tab2:
                    st.dataframe(df_processed, height=400)
                    st.markdown(get_table_download_link(df_processed), unsafe_allow_html=True)

                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h3 style='color: {SCHNEIDER_COLORS["primary_green"]}'>
                                🏆 Top Suppliers by Savings Opportunity
                            </h3>
                        """, unsafe_allow_html=True)
                        supplier_table = pd.DataFrame({
                            'Supplier': insights['top_suppliers'].index,
                            'Savings Opportunity (EUR)': insights['top_suppliers'].values.round(2)
                        })
                        st.table(supplier_table)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h3 style='color: {SCHNEIDER_COLORS["primary_green"]}'>
                                📊 Top Categories by Savings Opportunity
                            </h3>
                        """, unsafe_allow_html=True)
                        category_table = pd.DataFrame({
                            'Category': insights['top_categories'].index,
                            'Savings Opportunity (EUR)': insights['top_categories'].values.round(2)
                        })
                        st.table(category_table)
                        st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.warning("⚠️ No data matches the filtering criteria.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("📝 Please ensure your file has the required columns and format.")

if __name__ == "__main__":
    main()
