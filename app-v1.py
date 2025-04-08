import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📊 Retail Stock Dashboard")

# Upload XLSX file
uploaded_file = st.file_uploader("Upload your monthly stock Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded and parsed successfully!")

        # Debugging: Show the raw column names before processing
        st.write("Raw column names from the uploaded file:", df.columns)

        # Strip spaces and remove any hidden characters
        df.columns = [col.strip().lower().replace("\xa0", "").replace("\n", "").replace("\r", "") for col in df.columns]

        # Debugging: Show the processed column names after conversion to lowercase and cleaning
        st.write("Processed column names (lowercase, cleaned):", df.columns)

        # Check if necessary columns exist after lowering the case
        if 'category' not in df.columns or 'item' not in df.columns:
            st.error("❌ Your Excel file must include 'Category' and 'Item' columns.")
        else:
            # Sidebar filters
            st.sidebar.header("🔍 Filter Options")

            # Filter by category
            categories = df['category'].dropna().unique().tolist()
            selected_categories = st.sidebar.multiselect(
                "Filter by Category",
                options=categories,
                default=categories
            )
            df = df[df['category'].isin(selected_categories)]

            # Add prefix column
            def get_prefix(item):
                if isinstance(item, str):
                    for prefix in ['GLASS', 'RETAIL', 'SIT IN']:
                        if item.upper().startswith(prefix):
                            return prefix
                return 'OTHER'

            df['prefix'] = df['item'].apply(get_prefix)
            prefix_order = ['GLASS', 'RETAIL', 'SIT IN', 'OTHER']
            df['prefix'] = pd.Categorical(df['prefix'], categories=prefix_order, ordered=True)
            df.sort_values(by='prefix', inplace=True)

            # Add cleaned item name
            def clean_item_name(item):
                if isinstance(item, str):
                    for prefix in ['RETAIL ', 'GLASS ', 'SIT IN ']:
                        item = item.replace(prefix, '')
                    return item
                return item

            df['base_item'] = df['item'].apply(clean_item_name)

            # Restore original column names for display (title case)
            display_df = df.copy()
            display_df.columns = [col.title() for col in display_df.columns]  # Title case for display

            st.subheader("📈 Filtered & Grouped Data")
            st.dataframe(display_df)

            # Download filtered data with original column names
            csv = display_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Updated CSV",
                data=csv,
                file_name="filtered_stock.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"❌ Error reading the Excel file: {e}")

else:
    st.info("⬆️ Please upload an Excel file to begin.")
