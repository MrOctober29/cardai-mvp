import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="CardAi MVP", page_icon="🃏", layout="wide")

# --- SESSION STATE (Temporary Database) ---
# This mimics the "Virtual Collection Portfolio" mentioned in the doc 
if 'collection' not in st.session_state:
    st.session_state.collection = pd.DataFrame(columns=[
        "Player", "Team", "Era", "Condition", "Location", "Value_Est"
    ])

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("CardAi 🃏")
menu = st.sidebar.radio(
    "Menu", 
    ["Dashboard", "Add Card", "My Portfolio", "Market Alerts", "Storage Tracker"]
)

# --- PAGE: DASHBOARD ---
if menu == "Dashboard":
    st.title("CardAi Dashboard")
    st.markdown("### Welcome to your digital vault.")
    
    # Key Metrics based on MVP goals [cite: 4]
    total_cards = len(st.session_state.collection)
    total_value = st.session_state.collection['Value_Est'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cards", total_cards)
    col2.metric("Portfolio Value", f"${total_value:,.2f}")
    col3.metric("Top Storage Loc", "Binder A")  # Placeholder logic

    st.info("💡 Tip: Go to 'Add Card' to start digitizing your assets.")

# --- PAGE: ADD CARD ---
elif menu == "Add Card":
    st.header("Scan & Catalog")
    st.write("Upload card images and tag details manually (Phase 1 MVP)[cite: 17].")
    
    with st.form("add_card_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            player = st.text_input("Player Name", placeholder="e.g. Michael Jordan")
            team = st.text_input("Team", placeholder="e.g. Chicago Bulls")
            era = st.selectbox("Era", ["Modern", "Junk Wax", "Vintage", "Pre-War"]) [cite: 18]
        
        with col2:
            condition = st.selectbox("Condition/Grade", ["Raw", "PSA 10", "PSA 9", "BGS 9.5", "SGC 10"])
            # Feature: Card Storage Tracker 
            location = st.selectbox("Storage Location", ["Binder A", "Box in Garage", "Safe", "Top Loader Box"]) [cite: 22]
            value = st.number_input("Estimated Value ($)", min_value=0.0, step=0.01)

        uploaded_file = st.file_uploader("Upload Card Image")
        
        submitted = st.form_submit_button("Add to Portfolio")
        
        if submitted:
            new_card = {
                "Player": player,
                "Team": team,
                "Era": era,
                "Condition": condition,
                "Location": location,
                "Value_Est": value
            }
            st.session_state.collection = pd.concat(
                [st.session_state.collection, pd.DataFrame([new_card])], 
                ignore_index=True
            )
            st.success(f"Added {player} to your collection!")

# --- PAGE: MY PORTFOLIO ---
elif menu == "My Portfolio":
    st.header("Virtual Collection Portfolio")
    st.write("Sort by player, team, era, stats, grading, condition.")
    
    if not st.session_state.collection.empty:
        # Search/Filter
        filter_team = st.text_input("Filter by Team:")
        df_view = st.session_state.collection
        
        if filter_team:
            df_view = df_view[df_view['Team'].str.contains(filter_team, case=False)]
            
        st.dataframe(df_view, use_container_width=True)
    else:
        st.warning("No cards found. Add some cards first!")

# --- PAGE: MARKET ALERTS ---
elif menu == "Market Alerts":
    st.header("Market Alerts & Trends")
    st.write("Real-time value tracking (Simulated for MVP)[cite: 19, 24].")
    
    # Mock Data for "Upcoming Product Drops" 
    st.subheader("Upcoming Drops 📅")
    drops = [
        {"Date": "2026-06-15", "Product": "Topps Chrome MLB", "Type": "Hobby Box"},
        {"Date": "2026-07-01", "Product": "Panini Prizm NFL", "Type": "Blaster"},
        {"Date": "2026-07-10", "Product": "Pokémon Scarlet Ex", "Type": "Booster"}
    ]
    st.table(pd.DataFrame(drops))

# --- PAGE: STORAGE TRACKER ---
elif menu == "Storage Tracker":
    st.header("Storage Location Tracker")
    st.write("Avoid misplacement by tracking where physical cards are stored[cite: 23].")
    
    if not st.session_state.collection.empty:
        # Group by location to see count and value per box/binder
        storage_summary = st.session_state.collection.groupby("Location").agg(
            Count=('Player', 'count'),
            Total_Value=('Value_Est', 'sum')
        ).reset_index()
        
        st.bar_chart(storage_summary, x="Location", y="Count")
        st.dataframe(storage_summary)
    else:
        st.info("Add cards to see storage analytics.")
