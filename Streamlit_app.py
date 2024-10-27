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
            'CPR:Total Opportunity (EUR), including Logistics Simulation (Global)': 'Total Opportunity',
            'Site Name (Current)': 'Site Name',  # Added missing column mapping
            'Spend (EUR)': 'Spend (EUR)',        # Added missing column mapping
            'Category Code': 'Category Code'      # Added missing column mapping
        }
        
        # Check for required columns
        missing_columns = [col for col in column_mapping.keys() if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
        df = df.rename(columns=column_mapping)

        # Convert numeric columns
        numeric_columns = ['12m Projection Quantity', 'Unit Price in Euros', 'Best Price in Euros', 
                         'Best Price Quantity', 'Total Opportunity', 'Spend (EUR)']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

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

        # Calculate ratios and absolute opportunity
        df_filtered['Qty/projection'] = ((df_filtered['Best Price Quantity'] / df_filtered['12m Projection Quantity']) * 100)
        df_filtered['Absolute Opportunity'] = df_filtered['Total Opportunity'].abs()  # Added missing calculation
        
        # Filter one-time buys
        df_filtered = df_filtered[df_filtered['Qty/projection'] > 5]

        # Format float values
        float_columns = df_filtered.select_dtypes(include=['float64']).columns
        df_filtered[float_columns] = df_filtered[float_columns].round(2)

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
    category_data = df.groupby('Category Code')['Absolute Opportunity'].sum().reset_index()
    category_data = category_data.sort_values('Absolute Opportunity', ascending=False)
    
    fig1 = px.bar(
        category_data,
        x='Absolute Opportunity',
        y='Category Code',
        title='Savings Opportunity by Category (EUR)',
        orientation='h'
    )
    fig1.update_layout(
        yaxis_title="Category Code", 
        xaxis_title="Savings Opportunity (EUR)",
        height=500
    )

    # Opportunity by Supplier (Top 10)
    supplier_data = df.groupby('Supplier Name')['Absolute Opportunity'].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig2 = px.pie(
        supplier_data,
        values='Absolute Opportunity',
        names='Supplier Name',
        title='Top 10 Suppliers by Savings Opportunity'
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(height=500)

    # Add a bar chart for top suppliers
    fig3 = px.bar(
        supplier_data,
        x='Supplier Name',
        y='Absolute Opportunity',
        title='Top 10 Suppliers by Savings Opportunity (EUR)',
    )
    fig3.update_layout(
        xaxis_title="Supplier Name",
        yaxis_title="Savings Opportunity (EUR)",
        xaxis={'tickangle': 45},
        height=500
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
                    figures = create_visualizations(df_processed)
                    st.plotly_chart(figures[0], use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(figures[1], use_container_width=True)
                    with col2:
                        st.plotly_chart(figures[2], use_container_width=True)
                        st.subheader("Top Categories")
                        st.table(insights['top_categories'])
                
                with tab2:
                    st.dataframe(df_processed)
                    st.markdown(get_table_download_link(df_processed), unsafe_allow_html=True)
                
                with tab3:
                    st.subheader("Top Suppliers Analysis")
                    st.table(insights['top_suppliers'])

            else:
                st.warning("No data matches the filtering criteria.")

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.info("Please ensure your file has the required columns and format.")

if __name__ == "__main__":
    main()
