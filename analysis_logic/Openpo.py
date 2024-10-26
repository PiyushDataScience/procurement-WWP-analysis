import pandas as pd

def run(open_po_path, wb_path):
    # Read the Files
    open_po_bef = pd.read_excel(open_po_path, usecols=[
        'ORDER_TYPE', 'LINE_TYPE', 'ITEM', 'VENDOR_NUM', 
        'PO_NUM', 'RELEASE_NUM', 'LINE_NUM', 'SHIPMENT_NUM', 
        'AUTHORIZATION_STATUS', 'PO_SHIPMENT_CREATION_DATE', 
        'QTY_ELIGIBLE_TO_SHIP', 'UNIT_PRICE', 'CURRNECY'
    ])

    wb = pd.read_excel(wb_path, usecols=[
        'PART_NUMBER', 'DESCRIPTION', 'VENDOR_NUM', 
        'VENDOR_NAME', 'DANDB', 'STARS Category Code', 
        'ASL_MPN', 'UNIT_PRICE', 'CURRENCY_CODE'
    ])

    # Filter Open_PO_BEF for LINE_TYPE = Inventory
    open_po_bef = open_po_bef[open_po_bef['LINE_TYPE'] == 'Inventory']

    # Merge Open_PO_BEF and WB on 'ITEM' and 'VENDOR_NUM'
    merged_df = pd.merge(
        wb,
        open_po_bef,
        left_on=['PART_NUMBER', 'VENDOR_NUM'],
        right_on=['ITEM', 'VENDOR_NUM'],
        how='inner'
    )

    merged_df.columns = merged_df.columns.str.strip()

    # Drop the 'ITEM' column
    merged_df = merged_df.drop('ITEM', axis=1)

    # Rename columns
    merged_df = merged_df.rename(columns={
        'DANDB': 'VENDOR_DUNS',
        'UNIT_PRICE_x': 'Unit_Price_WB',
        'CURRENCY_CODE': 'CURRENCY_CODE_WB',
        'UNIT_PRICE_y': 'UNIT_PRICE_OPO',
        'CURRNECY': 'CURRNECY_OPO'
    })

    # Reorder columns
    new_column_order = [
        'ORDER_TYPE', 'PART_NUMBER', 'ASL_MPN', 'DESCRIPTION', 
        'VENDOR_NAME', 'VENDOR_DUNS', 'VENDOR_NUM', 
        'STARS Category Code', 'PO_NUM', 'RELEASE_NUM', 
        'LINE_NUM', 'SHIPMENT_NUM', 'AUTHORIZATION_STATUS', 
        'PO_SHIPMENT_CREATION_DATE', 'QTY_ELIGIBLE_TO_SHIP', 
        'Unit_Price_WB', 'CURRENCY_CODE_WB', 
        'UNIT_PRICE_OPO', 'CURRNECY_OPO'
    ]

    merged_df = merged_df[new_column_order]

    # Drop duplicates
    merged_df = merged_df.drop_duplicates()

    # IG/OG Column
    merged_df.insert(8, 'IG/OG', '')

    # Define a function to map Vendor to IG/OG based on Vendor Name
    def map_vendor_to_ig_og(vendor_name):
        if 'SCHNEIDER' in vendor_name or 'WUXI' in vendor_name:
            return 'IG'
        else:
            return 'OG'

    # Apply the function to populate the 'IG/OG' column
    merged_df['IG/OG'] = merged_df['VENDOR_NAME'].apply(map_vendor_to_ig_og)

    # PO Year
    merged_df.insert(14, 'PO Year', pd.to_datetime(merged_df['PO_SHIPMENT_CREATION_DATE']).dt.year)

    # Prices in Euros
    conversion_rates = {
        'USD': 0.93,  # Example: USD to EUR rate
        'GBP': 1.2,   # Example: GBP to EUR rate
        'INR': 0.011,
        'JPY': 0.0061
    }

    def convert_to_euro(price, currency):
        """Converts a price to Euros based on the provided currency."""
        return price * conversion_rates.get(currency, None)

    # Apply the conversion function
    merged_df['UNIT_PRICE_WB_EUR'] = merged_df.apply(
        lambda row: convert_to_euro(row['Unit_Price_WB'], row['CURRENCY_CODE_WB']),
        axis=1
    )

    merged_df['UNIT_PRICE_OPO_EUR'] = merged_df.apply(
        lambda row: convert_to_euro(row['UNIT_PRICE_OPO'], row['CURRNECY_OPO']),
        axis=1
    )

    # Calculate Price_Delta
    merged_df['Price_Delta'] = merged_df['UNIT_PRICE_OPO_EUR'] - merged_df['UNIT_PRICE_WB_EUR']

    # Calculate Impact in Euros
    merged_df['Impact in Euros'] = merged_df['Price_Delta'] * merged_df['QTY_ELIGIBLE_TO_SHIP']

    # Calculate Open PO Value
    merged_df['Open PO Value'] = merged_df['QTY_ELIGIBLE_TO_SHIP'] * merged_df['UNIT_PRICE_OPO_EUR']

    # Sort the data by Impact in Euros
    merged_df = merged_df.sort_values('Impact in Euros', ascending=False)

    # Return the final DataFrame
    return merged_df

# Example Usage: Uncomment the lines below to run the analysis locally
# open_po_path = "path_to_Open_PO_BEF.xlsx"
# wb_path = "path_to_WB.xlsx"
# result_df = run(open_po_path, wb_path)
# print(result_df)
