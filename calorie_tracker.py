import streamlit as st
import pandas as pd
from datetime import date
import os
import random

FILE_NAME = "calorie_log.csv"
WEIGHT_FILE_NAME = "weight_log.csv"
FOOD_DB_FILE = "cleaned_vegetarian_food_database.csv"

TARGET_CALORIES = 1900
TARGET_PROTEIN = 100

food_db = pd.read_csv(FOOD_DB_FILE)

st.set_page_config(page_title="Saumya’s Wellness Space", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: #F8F8F6;
    color: #2B2B2B;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1 {
    font-size: 3.4rem;
    font-weight: 300;
    letter-spacing: -0.05em;
    color: #2B2B2B;
}

h2, h3 {
    color: #2B2B2B;
    font-weight: 600;
}

p, label, span, div {
    color: #2B2B2B;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: #FFFFFF;
    padding: 0.7rem;
    border-radius: 24px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.05);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 18px;
    padding: 0.7rem 1rem;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: #F6CF71;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 1.2rem;
    border-top: 6px solid #66C5CC;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.05);
    min-height: 120px;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    border-radius: 28px;
    padding: 2rem;
    border: 1px solid #ECECEC;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.04);
}

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #2B2B2B !important;
    border-radius: 18px !important;
    border: 2px solid #E8E8E8 !important;
}

.stButton > button {
    background: #F89C74;
    color: white;
    border-radius: 999px;
    border: none;
    padding: 0.75rem 1.5rem;
    font-weight: 700;
}

.stButton > button:hover {
    background: #F6CF71;
    color: #2B2B2B;
}

.stProgress > div > div > div > div {
    background-color: #66C5CC;
}

div[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 1rem;
    border: 1px solid #ECECEC;
}

.stAlert {
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=["date", "meal", "food", "quantity", "calories", "protein", "notes"])

if os.path.exists(WEIGHT_FILE_NAME):
    weight_df = pd.read_csv(WEIGHT_FILE_NAME)
else:
    weight_df = pd.DataFrame(columns=["date", "weight"])

st.title("Saumya’s Wellness Space")
st.caption("Track food, movement, consistency, and small wins.")

tabs = st.tabs([
    "Dashboard",
    "Log Food",
    "Food Analytics",
    "Log Weight",
    "Weight Analytics",
    "History"
])

quotes = [
    "Consistency matters more than perfection.",
    "One meal does not define your progress.",
    "Small steps still count.",
    "You are building a routine, not punishing yourself.",
    "Progress can be quiet and still be real."
]

with tabs[0]:
    st.subheader("Today’s Dashboard")

    today = str(date.today())
    today_df = df[df["date"] == today]

    total_calories = today_df["calories"].sum() if not today_df.empty else 0
    total_protein = today_df["protein"].sum() if not today_df.empty else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Calories", f"{int(total_calories)} / {TARGET_CALORIES}")
        st.progress(min(total_calories / TARGET_CALORIES, 1))

    with col2:
        st.metric("Protein", f"{int(total_protein)}g / {TARGET_PROTEIN}g")
        st.progress(min(total_protein / TARGET_PROTEIN, 1))

    with col3:
        st.metric("Calories left", f"{int(TARGET_CALORIES - total_calories)} kcal")

    st.info(random.choice(quotes))

with tabs[1]:
    st.subheader("How are we fuelling ourselves today?")

    with st.form("food_form"):
        entry_date = st.date_input("Date", value=date.today())
        meal = st.selectbox("Meal", ["Breakfast", "Lunch", "Snack", "Dinner", "Drink", "Other"])

        food_list = sorted(food_db["food"].unique())
        food = st.selectbox("Food item", food_list)

        quantity_number = st.number_input("Quantity", min_value=1.0, step=0.5, value=1.0)
        quantity = str(quantity_number)

        selected_food = food_db[food_db["food"] == food].iloc[0]

        estimated_calories = int(int(selected_food["calories"]) * quantity_number)
        estimated_protein = int(int(selected_food["protein_g"]) * quantity_number)

        calories = st.number_input("Calories", min_value=0, step=10, value=estimated_calories)
        protein = st.number_input("Protein (g)", min_value=0.0, step=1.0, value=float(estimated_protein))
        notes = st.text_area("Notes", placeholder="Hunger, cravings, fullness, mood, etc.")

        submitted = st.form_submit_button("Add food entry")

        if submitted:
            new_entry = pd.DataFrame([{
                "date": str(entry_date),
                "meal": meal,
                "food": food,
                "quantity": quantity,
                "calories": calories,
                "protein": protein,
                "notes": notes
            }])

            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success("Food entry added.")

with tabs[2]:
    st.subheader("Food Analytics")

    selected_date = st.date_input("View day", value=date.today(), key="view_day")
    day_df = df[df["date"] == str(selected_date)]

    total_calories = day_df["calories"].sum() if not day_df.empty else 0
    total_protein = day_df["protein"].sum() if not day_df.empty else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Calories", f"{int(total_calories)} / {TARGET_CALORIES}")

    with col2:
        st.metric("Protein", f"{int(total_protein)}g / {TARGET_PROTEIN}g")

    with col3:
        st.metric("Calories left", f"{int(TARGET_CALORIES - total_calories)} kcal")

    with col4:
        st.metric("Protein left", f"{max(0, int(TARGET_PROTEIN - total_protein))}g")

    st.progress(min(total_calories / TARGET_CALORIES, 1))
    st.progress(min(total_protein / TARGET_PROTEIN, 1))

    st.subheader("Today’s Entries")
    st.dataframe(day_df, use_container_width=True)

    st.subheader("Weekly Food Analytics")

    if not df.empty:
        temp_df = df.copy()
        temp_df["date"] = pd.to_datetime(temp_df["date"])
        last_7_days = temp_df[temp_df["date"] >= pd.Timestamp.today() - pd.Timedelta(days=7)]

        if not last_7_days.empty:
            daily_summary = last_7_days.groupby("date").agg({
                "calories": "sum",
                "protein": "sum"
            }).reset_index()

            col1, col2 = st.columns(2)

            with col1:
                st.metric("7-day average calories", f"{int(daily_summary['calories'].mean())} kcal")

            with col2:
                st.metric("7-day average protein", f"{int(daily_summary['protein'].mean())}g")
        else:
            st.info("No food entries from the last 7 days yet.")
    else:
        st.info("Add food entries to see weekly food analytics.")

with tabs[3]:
    st.subheader("Gentle check-in")

    with st.form("weight_form"):
        weight_date = st.date_input("Weight date", value=date.today())
        weight = st.number_input("Weight in kg", min_value=0.0, step=0.1, value=0.0)

        weight_submitted = st.form_submit_button("Add weight")

        if weight_submitted:
            new_weight_entry = pd.DataFrame([{
                "date": str(weight_date),
                "weight": weight
            }])

            weight_df = pd.concat([weight_df, new_weight_entry], ignore_index=True)
            weight_df.to_csv(WEIGHT_FILE_NAME, index=False)
            st.success("Weight added.")

with tabs[4]:
    st.subheader("Weekly Weight Analytics")

    if not weight_df.empty:
        temp_weight_df = weight_df.copy()
        temp_weight_df["date"] = pd.to_datetime(temp_weight_df["date"])
        temp_weight_df = temp_weight_df.sort_values("date")

        last_7_weights = temp_weight_df[
            temp_weight_df["date"] >= pd.Timestamp.today() - pd.Timedelta(days=7)
        ]

        if not last_7_weights.empty:
            first_week_weight = last_7_weights.iloc[0]["weight"]
            latest_week_weight = last_7_weights.iloc[-1]["weight"]
            weekly_weight_change = latest_week_weight - first_week_weight

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Latest weight", f"{latest_week_weight:.1f} kg")

            with col2:
                st.metric("7-day change", f"{weekly_weight_change:.1f} kg")
        else:
            st.info("No weight entries from the last 7 days yet.")
    else:
        st.info("Add weight entries to see weekly weight analytics.")

with tabs[5]:
    st.subheader("All Food Logs")
    st.dataframe(df, use_container_width=True)

    st.subheader("All Weight Logs")
    st.dataframe(weight_df, use_container_width=True)

    food_csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Food CSV",
        data=food_csv,
        file_name="calorie_log.csv",
        mime="text/csv"
    )

    weight_csv = weight_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Weight CSV",
        data=weight_csv,
        file_name="weight_log.csv",
        mime="text/csv"
    )