# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64
from streamlit_lottie import st_lottie
import requests
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

def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

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
        </style>
    """, unsafe_allow_html=True)

def show_loading_animation():
    """Display a loading animation"""
    loading_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_qjosmr4w.json")
    if loading_animation:
        st_lottie(loading_animation, height=200, key="loading")

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
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://www.se.com/ww/en/assets/564/media/59531/570/320/logo-schneider-electric.png", width=150)
    with col2:
        st.title("Procurement Data Analysis Tool")
        st.markdown("""
        <div style='color: #3DCD58; margin-bottom: 2rem;'>
        Transform your procurement data into actionable insights
        </div>
        """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your data file", type=['xlsx', 'csv'])

    if uploaded_file is not None:
        show_loading_animation()
        
        try:
            with st.spinner('Processing your data...'):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                time.sleep(1)  # Add slight delay for visual effect

            st.success("✅ File uploaded and processed successfully!")

            # Process data
            df_processed = process_dataframe(df)
            
            if df_processed is not None and not df_processed.empty:
                # Generate insights
                insights = generate_insights(df_processed)
                
                # Display metrics with animation
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
