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

        # Strip spaces and remove any hidden characters
        df.columns = [col.strip().lower().replace("\xa0", "").replace("\n", "").replace("\r", "") for col in df.columns]

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

            # Add prefix column to sort by prefix (GLASS, RETAIL, SIT IN)
            def get_prefix(item):
                if isinstance(item, str):
                    for prefix in ['GLASS', 'RETAIL', 'SIT IN']:
                        if item.upper().startswith(prefix):
                            return prefix
                return 'OTHER'

            df['prefix'] = df['item'].apply(get_prefix)
            prefix_order = ['GLASS', 'RETAIL', 'SIT IN', 'OTHER']
            df['prefix'] = pd.Categorical(df['prefix'], categories=prefix_order, ordered=True)

            # Add cleaned item name (base item name) for grouping
            def clean_item_name(item):
                if isinstance(item, str):
                    for prefix in ['RETAIL ', 'GLASS ', 'SIT IN ']:
                        item = item.replace(prefix, '')
                    return item
                return item

            df['base_item'] = df['item'].apply(clean_item_name)

            # Sorting by Prefix and Base Item
            df.sort_values(by=['prefix', 'base_item'], inplace=True)

            # Display the filtered and sorted dataframe
            st.subheader("📈 Filtered & Grouped Data")
            st.dataframe(df)

            # Prepare an Excel writer object
            output = io.BytesIO()

            # Write to a new Excel file with separate sheets for each category using openpyxl
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for category in selected_categories:
                    category_df = df[df['category'] == category]
                    category_df.to_excel(writer, sheet_name=category, index=False)

            # Seek to the beginning of the BytesIO stream
            output.seek(0)

            # Allow the user to download the updated Excel file
            st.download_button(
                label="📥 Download Updated Excel",
                data=output,
                file_name="filtered_stock_by_category.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error reading the Excel file: {e}")

else:
    st.info("⬆️ Please upload an Excel file to begin.")
