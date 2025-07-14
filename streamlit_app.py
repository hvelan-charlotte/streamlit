import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")


selected_category = st.selectbox("Category", options=df["Category"].unique())
catdf = df[df["Category"] == selected_category]
st.write(catdf)

selected_subcat = st.multiselect("Sub_Category", options=catdf["Sub_Category"].unique())
subdf = catdf[catdf["Sub_Category"].isin(selected_subcat)]
st.dataframe(subdf)

# Here the Grouper is using our newly set index to group by Month ('M')
monthly = subdf.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(monthly, y="Sales")


formated_sales_sum = f"${df["Sales"].sum():,.2f}"
formated_sales_mean = f"${df["Sales"].mean():,.2f}"

formated_profit_sum = f"${df["Profit"].sum():,.2f}"
formated_profit_mean = f"${df["Profit"].mean():,.2f}"

profit_margin_sum = df["Profit"].sum() - df["Sales"].sum() / df["Sales"].sum()
st.write(profit_margin_sum)
# formated_sales_sum = f"${df["Sales"].sum():,.2f}"
# formated_sales_mean = f"${df["Sales"].sum():,.2f}"

st.write(formated_sales)
st.metric("Formated Total Sales", value = formated_sales_sum, delta = formated_Sales_mean)
st.metric("Formated Total Sales", value = formated_profit_mean, delta = formated_profit_mean)
# st.metric("Total Sales", value = df["Sales"].sum(), delta = df["Sales"].mean())
# st.metric(df["Profit"].sum())
# st.metric(abs(df["Sales"].sum() - df["Profit"].sum()) / df["Sales"].sum())


