import streamlit as st
import pandas as pd
from datetime import datetime

# PAGE CONFIG
st.set_page_config(page_title="Roommate App", layout="wide")

st.title("🏠 Smart Roommate Tracker")

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("data.csv")

# ==============================
# FILTERS (LIKE TABLEAU)
# ==============================
st.sidebar.header("🔍 Filters")

selected_roommate = st.sidebar.multiselect(
    "Select Roommate",
    options=df["Roommate"].unique(),
    default=df["Roommate"].unique()
)

selected_task = st.sidebar.multiselect(
    "Select Task",
    options=df["Task"].unique(),
    default=df["Task"].unique()
)

# DATE FILTER
df["Date"] = pd.to_datetime(df["Date"])

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

# APPLY FILTERS
filtered_df = df[
    (df["Roommate"].isin(selected_roommate)) &
    (df["Task"].isin(selected_task)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# ==============================
# USER INPUT FORM
# ==============================
st.subheader("➕ Add New Task")

with st.form("task_form"):
    roommate = st.selectbox("Select Roommate", df["Roommate"].unique())
    task = st.selectbox("Select Task", df["Task"].unique())
    time_taken = st.number_input("Time Taken (minutes)", min_value=1)
    completed = st.selectbox("Completed?", ["Yes", "No"])

    submit = st.form_submit_button("Add Task")

    if submit:
        new_row = {
            "Date": datetime.today().strftime('%Y-%m-%d'),
            "Roommate": roommate,
            "Task": task,
            "Time_Taken": time_taken,
            "Completed": completed,
            "Effort_Score": time_taken / 10,
            "Day of Week": datetime.today().strftime('%A'),
            "Week Number": 1,
            "Completed Flag (for calculations)": 1 if completed == "Yes" else 0,
            "Helper column": 1,
            "Missed Task Flag": 0 if completed == "Yes" else 1
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("data.csv", index=False)

        st.success("✅ Task Added Successfully!")

# ==============================
# KPIs (VERY IMPORTANT)
# ==============================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total_tasks = len(filtered_df)

completion_rate = 0
if len(filtered_df) > 0:
    completion_rate = filtered_df["Completed Flag (for calculations)"].mean() * 100

avg_time = 0
if len(filtered_df) > 0:
    avg_time = filtered_df["Time_Taken"].mean()

col1.metric("Total Tasks", total_tasks)
col2.metric("Completion Rate (%)", f"{completion_rate:.2f}")
col3.metric("Avg Time (mins)", f"{avg_time:.2f}")

# ==============================
# SHOW DATA
# ==============================
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df)

# ==============================
# CHARTS
# ==============================

# Total Tasks by Roommate
st.subheader("📊 Total Tasks by Roommate")
st.bar_chart(filtered_df["Roommate"].value_counts())

# Completion Rate
st.subheader("📈 Completion Rate by Roommate")
completion = filtered_df.groupby("Roommate")["Completed Flag (for calculations)"].mean()
st.bar_chart(completion)

# Avg Time per Task (Dot Plot Style)
st.subheader("⏱ Avg Time per Task")
avg_time_task = filtered_df.groupby("Task")["Time_Taken"].mean()
st.scatter_chart(avg_time_task)

# ==============================
# FAIRNESS SCORE (USP 🔥)
# ==============================
st.subheader("⚖️ Workload Fairness (Effort Distribution)")

effort = filtered_df.groupby("Roommate")["Effort_Score"].sum()
st.bar_chart(effort)
# ==============================
# SMART INSIGHTS (🔥 DIFFERENTIATOR)
# ==============================

st.subheader("🧠 Insights & Observations")

if len(filtered_df) > 0:

    # Highest workload
    workload = filtered_df.groupby("Roommate")["Effort_Score"].sum()
    top_worker = workload.idxmax()
    least_worker = workload.idxmin()

    # Completion rate
    completion = filtered_df.groupby("Roommate")["Completed Flag (for calculations)"].mean()
    best_completion = completion.idxmax()
    worst_completion = completion.idxmin()

    st.write(f"🏆 **{top_worker}** is contributing the most effort.")
    st.write(f"⚠️ **{least_worker}** has the lowest workload.")
    st.write(f"✅ **{best_completion}** has the highest completion rate.")
    st.write(f"❌ **{worst_completion}** needs improvement in task completion.")

else:
    st.write("No data available for insights.")
# ==============================
# LEADERBOARD
# ==============================

st.subheader("🏅 Leaderboard (Top Contributors)")

leaderboard = (
    filtered_df
    .groupby("Roommate")["Effort_Score"]
    .sum()
    .sort_values(ascending=False)
)

st.dataframe(
    leaderboard.reset_index().rename(columns={"Effort_Score": "Total Effort"})
)