import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

#  DATABASE CONNECTION 
engine = create_engine(
    "postgresql://postgres@localhost:5432/phonepe_db",
    connect_args={"password": "Paishrs@2"}
)

# LOAD DATA 
def load_data():
    agg_trans = pd.read_sql("SELECT * FROM aggregated_transaction", engine)
    agg_user = pd.read_sql("SELECT * FROM aggregated_user", engine)
    agg_ins = pd.read_sql("SELECT * FROM aggregated_insurance", engine)

    map_trans = pd.read_sql("SELECT * FROM map_transaction", engine)
    map_user = pd.read_sql("SELECT * FROM map_user", engine)
    map_ins = pd.read_sql("SELECT * FROM map_insurance", engine)

    top_trans = pd.read_sql("SELECT * FROM top_transaction", engine)
    top_user = pd.read_sql("SELECT * FROM top_user", engine)
    top_ins = pd.read_sql("SELECT * FROM top_insurance", engine)

    tables = [agg_trans, agg_user, agg_ins,
              map_trans, map_user, map_ins,
              top_trans, top_user, top_ins]

    for df in tables:
        df.columns = [c.lower() for c in df.columns]
        if 'state' in df.columns:
            df['state'] = df['state'].fillna("unknown").str.strip().str.lower()
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce')

    return agg_trans, agg_user, agg_ins, map_trans, map_user, map_ins, top_trans, top_user, top_ins


agg_trans, agg_user, agg_ins, map_trans, map_user, map_ins, top_trans, top_user, top_ins = load_data()

st.set_page_config(page_title="PhonePe Dashboard", layout="wide")
st.title("📊 PhonePe Advanced Analytics Dashboard")

# GLOBAL FILTERS (TRANSACTION ONLY)
st.sidebar.header("Transaction Filters")

year_list = sorted(agg_trans['year'].dropna().unique().tolist())
state_list = sorted(agg_trans['state'].dropna().unique().tolist())

year_filter = st.sidebar.selectbox("Select Year", year_list)
state_filter = st.sidebar.selectbox("Select State", state_list)

# FILTER TRANSACTION DATA
f_agg_trans = agg_trans[(agg_trans['year'] == year_filter) & (agg_trans['state'] == state_filter)]
f_map_trans = map_trans[(map_trans['year'] == year_filter) & (map_trans['state'] == state_filter)]
f_top_trans = top_trans[(top_trans['year'] == year_filter) & (top_trans['state'] == state_filter)]

# KPI
st.subheader("📌 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_users = int(map_user['registeredusers'].sum()) if not map_user.empty else 0
total_insurance = int(agg_ins['amount'].sum()) if not agg_ins.empty else 0

col1.metric("💰 Total Transaction Amount", f"₹ {int(f_agg_trans['amount'].sum()):,}")
col2.metric("🔄 Total Transactions", int(f_agg_trans['count'].sum()))
col3.metric("📱 Total Users", total_users)
col4.metric("🛡 Total Insurance Amount", f"₹ {total_insurance:,}")

# TABS
tab_trans, tab_user, tab_ins = st.tabs(["💳 Transactions", "📱 Users", "🛡 Insurance"])

# TRANSACTIONS 
with tab_trans:
    st.subheader("Transaction Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Top States by Transaction Amount")
        top_states = agg_trans.groupby('state')['amount'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_states)

    with col2:
        st.write("Top Transaction Entities")
        if not f_top_trans.empty:
            top_entities = f_top_trans.groupby('entity')['amount'].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top_entities)
        else:
            st.warning("No top transaction data")

    st.write("Quarter-wise Transaction Trend")
    if not f_agg_trans.empty:
        trend = f_agg_trans.groupby('quarter')['amount'].sum()
        st.line_chart(trend)
    else:
        st.warning("No trend data available")

   

    st.write("All Transaction Data")
    st.dataframe(f_agg_trans)

# USERS 
with tab_user:
    st.subheader("User Analysis")

    # ✅ Separate filters
    user_years = sorted(map_user['year'].dropna().unique().tolist())
    user_states = sorted(map_user['state'].dropna().unique().tolist())

    if not user_years or not user_states:
        st.error("No User Data Available")
    else:
        user_year = st.selectbox("Select Year", user_years, key="user_year")
        user_state = st.selectbox("Select State", user_states, key="user_state")

        f_map_user = map_user[
            (map_user['year'] == user_year) &
            (map_user['state'] == user_state)
        ]

        st.write("Top States by Users")
        st.bar_chart(map_user.groupby('state')['registeredusers'].sum().sort_values(ascending=False).head(10))

        st.write("User Growth")
        st.line_chart(map_user.groupby('year')['registeredusers'].sum())

        st.write("District Users")
        st.dataframe(f_map_user)

# INSURANCE 
with tab_ins:
    st.subheader("Insurance Analysis")

    
    ins_years = sorted(agg_ins['year'].dropna().unique().tolist())
    ins_states = sorted(agg_ins['state'].dropna().unique().tolist())

    if not ins_years or not ins_states:
        st.error("🚫 Insurance data not available")
    else:
        ins_year = st.selectbox("Select Year", ins_years, key="ins_year")
        ins_state = st.selectbox("Select State", ins_states, key="ins_state")

        f_agg_ins = agg_ins[
            (agg_ins['year'] == ins_year) &
            (agg_ins['state'] == ins_state)
        ]

        f_map_ins = map_ins[
            (map_ins['year'] == ins_year) &
            (map_ins['state'] == ins_state)
        ]

        f_top_ins = top_ins[
            (top_ins['year'] == ins_year) &
            (top_ins['state'] == ins_state)
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.write("Top States")
            st.bar_chart(agg_ins.groupby('state')['amount'].sum().sort_values(ascending=False).head(10))

        with col2:
            st.write("Top Entities")
            if not f_top_ins.empty:
                st.bar_chart(f_top_ins.groupby('entity')['amount'].sum())
            else:
                st.warning("No entity data")

        st.write("Quarter Trend")
        if not f_agg_ins.empty:
            st.line_chart(f_agg_ins.groupby('quarter')['amount'].sum())

        st.write("District Data")
        st.dataframe(f_map_ins)

st.sidebar.download_button(
    "Download Transactions",
    f_agg_trans.to_csv(index=False),
    "transactions.csv"
)