import streamlit as st
from data_loader import get_data
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Red Sox Stats Dashboard")

batters_df, pitchers_df = get_data()

st.header("Team Batting Stats")
st.dataframe(batters_df)

st.header("Team Pitching Stats")
st.dataframe(pitchers_df)

stat_to_analyze = st.selectbox(
    "Select stat to visualize", ["avg", "obp", "ops", "era", "whip"]
)

if stat_to_analyze in batters_df.columns:
    df = batters_df
    ascending = False
elif stat_to_analyze in pitchers_df.columns:
    df = pitchers_df
    ascending = True if stat_to_analyze in ["era", "whip"] else False

fig, ax = plt.subplots(figsize=(10, 6))
sorted_df = df.sort_values(by=stat_to_analyze, ascending=ascending)
sns.barplot(data=sorted_df, x=stat_to_analyze, y="name", ax=ax)
st.pyplot(fig)
