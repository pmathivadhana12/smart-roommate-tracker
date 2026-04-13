import streamlit as st
import pandas as pd
from datetime import datetime


# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Smart Roommate Tracker", layout="wide")
=======
# PAGE CONFIG
st.set_page_config(page_title="Roommate App", layout="wide")

st.title("🏠 Smart Roommate Tracker")
>>>>>>> ff24919c2b949d60867b720e4464cbe133bc9c75

# ==============================
# LOAD DATA
# ==============================

@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ==============================
# USER (LOGIN SIMULATION)
# ==============================
st.sidebar.header("👤 User")

user = st.sidebar.selectbox(
    "Who are you?",
    options=df["Roommate"].unique()
)

st.title(f"🏠 Smart Roommate Tracker — Welcome {user}")

# ==============================
# FILTERS
# ==============================
st.sidebar.header("🔍 Filters")

roommates = st.sidebar.multiselect(
    "Roommate",
=======
df = pd.read_csv("data.csv")

# ==============================
# FILTERS (LIKE TABLEAU)
# ==============================
st.sidebar.header("🔍 Filters")

selected_roommate = st.sidebar.multiselect(
    "Select Roommate",
>>>>>>> ff24919c2b949d60867b720e4464cbe133bc9c75
    options=df["Roommate"].unique(),
    default=df["Roommate"].unique()
)


tasks = st.sidebar.multiselect(
    "Task",
=======
selected_task = st.sidebar.multiselect(
    "Select Task",
>>>>>>> ff24919c2b949d60867b720e4464cbe133bc9c75
    options=df["Task"].unique(),
    default=df["Task"].unique()
)


date_range = st.sidebar.date_input(
    "Date Range",
    [df["Date"].min(), df["Date"].max()]
)

filtered_df = df[
    (df["Roommate"].isin(roommates)) &
    (df["Task"].isin(tasks)) &
=======
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
>>>>>>> ff24919c2b949d60867b720e4464cbe133bc9c75
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# ==============================

# TABS (CLEAN UI)
# ==============================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ Add Task", "🧠 Insights"])

# ==============================
# TAB 1: DASHBOARD
# ==============================
with tab1:

    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    total_tasks = len(filtered_df)
    completion_rate = (filtered_df["Completed"] == "Yes").mean() * 100
    avg_time = filtered_df["Time_Taken"].mean()

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completion Rate (%)", round(completion_rate, 2))
    col3.metric("Avg Time (mins)", round(avg_time, 2))

    # ==========================
    # VISUALS
    # ==========================
    st.subheader("📈 Performance Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Workload Distribution")
        st.bar_chart(filtered_df.groupby("Roommate")["Time_Taken"].sum())

    with col2:
        st.write("### Completion Rate")
        comp = filtered_df.groupby("Roommate")["Completed"].apply(
            lambda x: (x == "Yes").mean()
        )
        st.bar_chart(comp)

    # ==========================
    # FAIRNESS VISUAL (WOW VISUAL)
    # ==========================
    st.subheader("⚖️ Workload Balance")

    effort = filtered_df.groupby("Roommate")["Time_Taken"].sum()
    st.bar_chart(effort)

    fairness = effort.std()

    st.metric("Workload Imbalance Score", round(fairness, 2))

    if fairness < 10:
        st.success("✅ Tasks are evenly distributed")
    else:
        st.warning("⚠️ Some roommates may be overloaded")

    # ==========================
    # WEEKLY TREND
    # ==========================
    if "Week Number" in filtered_df.columns:
        st.subheader("📅 Weekly Trend")
        weekly = filtered_df.groupby("Week Number")["Time_Taken"].sum()
        st.line_chart(weekly)

# ==============================
# TAB 2: ADD TASK
# ==============================
with tab2:

    st.subheader("➕ Log a Task")

    col1, col2, col3 = st.columns(3)

    with col1:
        new_task = st.selectbox("Task", df["Task"].unique())

    with col2:
        new_time = st.number_input("Time (mins)", min_value=1)

    with col3:
        new_completed = st.selectbox("Completed?", ["Yes", "No"])

    if st.button("Add Task"):
        new_row = pd.DataFrame([{
            "Date": datetime.today(),
            "Roommate": user,
            "Task": new_task,
            "Time_Taken": new_time,
            "Completed": new_completed,
            "Effort_Score": new_time * (1 if new_completed == "Yes" else 0.5)
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("data.csv", index=False)

        st.success("✅ Task logged successfully!")

# ==============================
# TAB 3: INSIGHTS
# ==============================
with tab3:

    st.subheader("🧠 Smart Insights")

    if not filtered_df.empty:

        effort_sum = filtered_df.groupby("Roommate")["Time_Taken"].sum()
        completion_rate_rm = filtered_df.groupby("Roommate")["Completed"].apply(
            lambda x: (x == "Yes").mean()
        )

        top_worker = effort_sum.idxmax()
        least_worker = effort_sum.idxmin()
        best_completion = completion_rate_rm.idxmax()
        worst_completion = completion_rate_rm.idxmin()

        st.write(f"🏆 **{top_worker}** is contributing the most effort.")
        st.write(f"⚠️ **{least_worker}** is contributing the least.")
        st.write(f"✅ **{best_completion}** has the highest completion reliability.")
        st.write(f"❌ **{worst_completion}** needs improvement in consistency.")

        # ==========================
        # WOW FEATURE 🤯
        # ==========================
        st.subheader("🤖 Smart Recommendation Engine")

        if user == least_worker:
            st.warning("💡 You can take up more tasks to balance workload.")
        elif user == top_worker:
            st.info("🔥 You're contributing the most — consider delegating tasks.")
        elif user == worst_completion:
            st.error("📉 Focus on completing assigned tasks more consistently.")
        else:
            st.success("✨ You're doing great! Keep it up.")

        # ==========================
        # LEADERBOARD
        # ==========================
        st.subheader("🥇 Leaderboard")

        leaderboard = effort_sum.sort_values(ascending=False).reset_index()
        leaderboard.columns = ["Roommate", "Total Effort"]

        st.dataframe(leaderboard)

    # ==========================
    # DOWNLOAD
    # ==========================
    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name="roommate_data.csv",
        mime="text/csv"
    )

=======
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
>>>>>>> ff24919c2b949d60867b720e4464cbe133bc9c75
