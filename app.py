import streamlit as st
import pandas as pd

st.set_page_config(page_title="PR Tourism Tax Extractor", page_icon="🇵🇷")

st.title("🇵🇷 PR Tourism Tax Data Extractor")
st.markdown("Upload your Airbnb Earnings CSV to calculate your 7% Room Tax totals.")

uploaded_file = st.file_uploader("Upload Airbnb CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # Filter for Taxable Rows (Reservations and Cancellation Fees)
    taxable_df = df[df['Type'].isin(['Reservation', 'Cancellation Fee'])].copy()

    # Convert columns to numbers
    for col in ['Gross earnings', 'Occupancy taxes', 'Nights']:
        if col in taxable_df.columns:
            taxable_df[col] = pd.to_numeric(taxable_df[col], errors='coerce').fillna(0)

    # Calculate Totals
    gross_rev = taxable_df['Gross earnings'].sum()
    tax_collected = taxable_df['Occupancy taxes'].sum()
    total_nights = taxable_df['Nights'].sum()

    # Identify Month
    try:
        taxable_df['Start date'] = pd.to_datetime(taxable_df['Start date'])
        month_label = taxable_df['Start date'].dt.strftime('%B %Y').iloc[0]
    except:
        month_label = "Selected Month"

    st.subheader(f"Results for {month_label}")
    summary = {
        "Reporting Month": [month_label],
        "Gross Taxable Revenue": [f"${gross_rev:,.2f}"],
        "7% Occupancy Tax": [f"${tax_collected:,.2f}"],
        "Nights Occupied": [int(total_nights)]
    }
    st.table(pd.DataFrame(summary))

    st.divider()
    st.subheader("Values for PR Tourism Portal")
    st.code(f"Gross Revenue: {gross_rev:.2f}")
    st.code(f"7% Tax: {tax_collected:.2f}")
    st.code(f"Nights: {int(total_nights)}")
