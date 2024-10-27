# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import base64

def load_css():
    """Load custom CSS styles"""
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stAlert {
            margin-top: 1rem;
        }
        .metric-card {
            border: 1px solid #e6e6e6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
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
    top_suppliers = df['Supplier Name'].value_counts().head(5)
    top_categories = df['Category Code'].value_counts().head(5)
    
    return {
        'total_opportunity': total_opportunity,
        'avg_qty_projection': avg_qty_projection,
        'top_suppliers': top_suppliers,
        'top_categories': top_categories
    }

def create_visualizations(df):
    """Create visualizations using Plotly"""
    # Opportunity by Category
    fig1 = px.bar(
        df.groupby('Category Code')['Total Opportunity'].sum().reset_index(),
        x='Category Code',
        y='Total Opportunity',
        title='Total Opportunity by Category'
    )

    # Opportunity by Supplier (Top 10)
    fig2 = px.pie(
        df.groupby('Supplier Name')['Total Opportunity'].sum().sort_values()
        .head(10).reset_index(),
        values='Total Opportunity',
        names='Supplier Name',
        title='Top 10 Suppliers by Opportunity'
    )

    # Scatter plot of Quantity vs Projection
    fig3 = px.scatter(
        df,
        x='12m Projection Quantity',
        y='Best Price Quantity',
        color='Category Code',
        title='Quantity vs Projection by Category'
    )

    return [fig1, fig2, fig3]

def get_table_download_link(df):
    """Generate a download link for the processed data"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="processed_data.csv">Download Processed Data</a>'
    return href

def main():
    st.set_page_config(
        page_title="Procurement Analysis Tool",
        page_icon="📊",
        layout="wide"
    )
    
    load_css()

    st.title("Procurement Data Analysis Tool")
    st.markdown("""
    This tool analyzes procurement data to identify cost-saving opportunities.
    Upload your procurement data file (Excel/CSV) to get started.
    """)

    uploaded_file = st.file_uploader("Upload your data file", type=['xlsx', 'csv'])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("File uploaded successfully!")

            # Process data
            df_processed = process_dataframe(df)
            
            if df_processed is not None and not df_processed.empty:
                # Generate insights
                insights = generate_insights(df_processed)
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Opportunity (EUR)", f"{insights['total_opportunity']:,.2f}")
                with col2:
                    st.metric("Average Qty/Projection Ratio", f"{insights['avg_qty_projection']:.2f}%")
                with col3:
                    st.metric("Number of Parts", len(df_processed))
                with col4:
                    st.metric("Number of Suppliers", df_processed['Supplier Name'].nunique())

                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["Visualizations", "Data Table", "Top Analysis"])

                with tab1:
                    # Display visualizations
                    figures = create_visualizations(df_processed)
                    for fig in figures:
                        st.plotly_chart(fig, use_container_width=True)

                with tab2:
                    st.dataframe(df_processed)
                    st.markdown(get_table_download_link(df_processed), unsafe_allow_html=True)

                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Top Suppliers")
                        st.table(insights['top_suppliers'])
                    with col2:
                        st.subheader("Top Categories")
                        st.table(insights['top_categories'])

            else:
                st.warning("No data matches the filtering criteria.")

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please ensure your file has the required columns and format.")

if __name__ == "__main__":
    main()
