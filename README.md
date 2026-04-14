🏠 Smart Roommate Tracker App
A real-time web application to track, analyze, and optimize household task distribution across roommates.

Live App
https://smart-roommate-tracker-bhxejtnq58qbk7kwva234m.streamlit.app/

Problem
In shared households, task distribution is often unstructured, untracked, and perceived as unfair, leading to imbalance, inefficiency, and frustration among roommates.

Solution
Built an interactive analytics-driven system that:
-Tracks daily tasks across roommates
-Measures effort (time spent) and completion rates
-Identifies workload imbalance using fairness metrics
-Provides real-time insights and recommendations

This project bridges data analysis, product development, and decision-making.
Features
Add new tasks dynamically
Interactive filters (Roommate, Task, Date Range)

KPI Dashboard:
Total Tasks
Completion Rate
Average Time per Task

Fairness Score:
Measures workload imbalance across roommates

Leaderboard:
Ranks contributors by effort

Insights Engine:
Identifies top and least contributors
Highlights consistency issues
Provides smart recommendations

Tableau Integration:
Historical analysis (March 1–21)
Supports deeper exploratory insights
Project Approach

This project follows a two-layer analytics approach:
1. Exploratory Analysis (Tableau)
Analyzed historical data to identify patterns
Detected workload imbalance and performance gaps
2. Product Layer (Streamlit)
Built a real-time interactive application
Enabled continuous tracking and decision-making

This demonstrates an end-to-end data → insight → product workflow.

Tech Stack:
-Python
-Streamlit
-Pandas
-Tableau

Key Insights:
Identified top contributors and underperformers
Measured workload imbalance using statistical metrics
Highlighted inefficiencies in task completion behavior
Enabled visibility into fairness across roommates

Outcome:
Transformed a static dataset into a live, interactive product that:
-Improves transparency
-Encourages accountability
-Enables data-driven decision-making in shared environments
-Future Enhancements

To evolve this into a scalable product, the next phase would include:
Multi-User Login System
-Allow users to create accounts
-Enable different households to use the app independently
-Maintain separate data for each user or group
Cloud Data Storage
-Replace CSV with a database (Firebase or PostgreSQL)
-Enable persistent and scalable data storage
Personalized Dashboards
-Each user sees their own performance metrics
-Custom insights based on behavior
Predictive Analytics
-Predict task completion likelihood
-Recommend optimal task allocation
Smart Notifications
-Alerts for missed or overdue tasks
-Nudges for workload balancing
