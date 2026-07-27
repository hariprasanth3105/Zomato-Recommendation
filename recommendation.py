import streamlit as st
import pandas as pd
import numpy as np

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("zomato_recommender.csv")
    return df

df = load_data()

# ==============================
# Recommendation Function
# ==============================
def recommend_restaurants(df, preferred_locations=None, preferred_cuisines=None,
                          max_budget=None, min_rating=None, top_n=10):

    data = df.copy()

    # Hard Filters
    if preferred_locations:
        data = data[data['LOCATION_CLEAN'].isin(preferred_locations)]

    if preferred_cuisines:
        cuisine_mask = data['CUISINES'].str.contains('|'.join(preferred_cuisines), case=False, na=False)
        data = data[cuisine_mask]

    if max_budget is not None:
        data = data[data['APPROX_COST_FOR_TWO_PEOPLE'] <= max_budget]

    if min_rating is not None:
        data = data[data['RATE'] >= min_rating]

    if data.empty:
        return pd.DataFrame({"Message": ["No restaurants found with the given filters."]})

    # Scoring
    min_rate, max_rate = data['RATE'].min(), data['RATE'].max()
    data['rating_score'] = ((data['RATE'] - min_rate) / (max_rate - min_rate)) * 100 if max_rate > min_rate else 50

    data['log_votes'] = np.log1p(data['VOTES'])
    min_v, max_v = data['log_votes'].min(), data['log_votes'].max()
    data['popularity_score'] = ((data['log_votes'] - min_v) / (max_v - min_v)) * 100 if max_v > min_v else 50

    if max_budget is not None:
        data['budget_fit_score'] = (1 - (max_budget - data['APPROX_COST_FOR_TWO_PEOPLE']) / max_budget) * 100
        data['budget_fit_score'] = data['budget_fit_score'].clip(0, 100)
    else:
        data['budget_fit_score'] = 50

    data['cuisine_match'] = data['CUISINES'].str.contains('|'.join(preferred_cuisines), case=False, na=False).astype(int) * 100 if preferred_cuisines else 50
    data['location_match'] = data['LOCATION_CLEAN'].isin(preferred_locations).astype(int) * 100 if preferred_locations else 50
    data['book_table_bonus'] = data['BOOK_TABLE'].apply(lambda x: 5 if x == True else 0)

    data['final_score_raw'] = (
        0.35 * data['rating_score'] +
        0.25 * data['popularity_score'] +
        0.20 * data['budget_fit_score'] +
        0.10 * data['cuisine_match'] +
        0.10 * data['location_match'] +
        data['book_table_bonus']
    )

    min_s, max_s = data['final_score_raw'].min(), data['final_score_raw'].max()
    data['final_score'] = ((data['final_score_raw'] - min_s) / (max_s - min_s)) * 100 if max_s > min_s else 50

    result = (
        data.sort_values('final_score', ascending=False)
        [['NAME', 'LOCATION_CLEAN', 'CUISINES', 'PRIMARY_REST_TYPE', 'RATE', 'VOTES',
          'APPROX_COST_FOR_TWO_PEOPLE', 'BOOK_TABLE', 'final_score']]
        .head(top_n)
        .reset_index(drop=True)
        .round({'final_score': 2, 'RATE': 1})
    )
    return result


# ==============================
# Streamlit UI
# ==============================
st.set_page_config(page_title="Bengaluru Restaurant Recommender", layout="wide")

st.title("Bengaluru Restaurant Recommendation System")
st.markdown("Find the best restaurants based on your preferences")

# Sidebar Inputs
st.sidebar.header("Your Preferences")

locations = sorted(df['LOCATION_CLEAN'].dropna().unique())
cuisines = sorted(df['PRIMARY_CUISINE'].dropna().unique())

selected_locations = st.sidebar.multiselect("Preferred Locations", locations)
selected_cuisines = st.sidebar.multiselect("Preferred Cuisines", cuisines)
max_budget = st.sidebar.slider("Maximum Budget (for two)", 100, 3000, 800, step=50)
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5, step=0.1)
top_n = st.sidebar.slider("Number of Recommendations", 5, 20, 10)

# Run Recommendation
if st.sidebar.button("Get Recommendations"):
    results = recommend_restaurants(
        df=df,
        preferred_locations=selected_locations if selected_locations else None,
        preferred_cuisines=selected_cuisines if selected_cuisines else None,
        max_budget=max_budget,
        min_rating=min_rating,
        top_n=top_n
    )

    st.subheader("Top Recommended Restaurants")
    st.dataframe(results, use_container_width=True)
else:
    st.info("Set your preferences in the sidebar and click **Get Recommendations**")
