import streamlit as st
import pandas as pd

# 1. Page Config (Makes it look like a mobile app)
st.set_page_config(page_title="Tims Top Picks", page_icon="☕", layout="centered")

st.title("☕ Tims Hockey Challenge Helper")
st.markdown("The top 3 mathematical picks for each tier based on the xG/HD model.")

# 2. Load your data (Make sure the filename matches exactly)
@st.cache_data(ttl=600) # Caches the data so it loads instantly
def load_data():
    # Assuming your file is named apple.csv and is in the same folder
    df = pd.read_csv("apple.csv")
    return df

try:
    df = load_data()

    # 3. Loop through Picks 1, 2, and 3
    for pick_num in [1, 2, 3]:
        # Filter the dataframe for the specific pick
        pick_df = df[df['Pick'] == pick_num]
        
        # Sort by our goal probability, highest to lowest
        pick_df = pick_df.sort_values(by='p_at_least_1_goal', ascending=False)
        
        # Get the top 3
        top_3 = pick_df.head(3)

        st.subheader(f"🏒 Pick {pick_num}")

        if top_3.empty:
            st.write("No players found for this pick.")
            continue

        # Display the Top 3 cleanly
        for index, row in top_3.iterrows():
            # Format the percentage
            prob = f"{row['p_at_least_1_goal'] * 100:.1f}%"
            
            # Create a nice layout for each player
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                # Big bold probability
                st.markdown(f"### {prob}")
            with col2:
                # Player name and team
                st.markdown(f"**{row['name']}**")
                st.caption(f"{row['team']} vs {row['opponent']}")
            with col3:
                # Model Math (hidden in a little dropdown so it's clean)
                with st.expander("Math"):
                    st.write(f"xG: {row['expectedGoals']:.3f}")
                    st.write(f"HD: {row['expectedLambda_hd']:.2f}")
        
        st.divider() # Add a line between picks

except FileNotFoundError:
    st.error("Could not find 'apple.csv'. Make sure the file is in the same folder as app.py.")