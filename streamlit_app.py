import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Top AI Factory Analysis", layout="wide")
st.title("🌡️ Top AI Factory Analysis")

# 2. Initial Data (Enriched with Stargate Roles and Energy Metrics)
data = [
    {"Company": "Nvidia", "Role": "Compute/GPU", "Moat": 5, "Margin %": 55.0, "Growth %": 45.0, "Efficiency Score": 5, "Primary Risk": "Concentration"},
    {"Company": "Arista", "Role": "Networking", "Moat": 4, "Margin %": 38.0, "Growth %": 30.0, "Efficiency Score": 4, "Primary Risk": "Competition"},
    {"Company": "Vertiv", "Role": "CRAHS/Power", "Moat": 4, "Margin %": 25.0, "Growth %": 25.0, "Efficiency Score": 5, "Primary Risk": "Supply Chain"},
    {"Company": "Eaton", "Role": "UPS/Switchgear", "Moat": 4, "Margin %": 18.0, "Growth %": 15.0, "Efficiency Score": 3, "Primary Risk": "Cyclicality"},
    {"Company": "Schneider", "Role": "PDU/UPS", "Moat": 4, "Margin %": 20.0, "Growth %": 18.0, "Efficiency Score": 4, "Primary Risk": "Execution"},
    {"Company": "Speculative AI", "Role": "Software", "Moat": 2, "Margin %": -5.0, "Growth %": 60.0, "Efficiency Score": 2, "Primary Risk": "Liquidity"},
]
df = pd.DataFrame(data)

# 3. Sidebar: Agentic Control Panel
st.sidebar.header("🕹️ Agentic Control Panel")

# Risk Adjustment Agent Slider (from Architecture Diagram)
risk_penalty = st.sidebar.slider(
    "Risk Adjustment Agent Discount (%)",
    min_value=0, max_value=50, value=10,
    help="Applies execution and concentration discounts to the final score."
)

# Power Efficiency Weighting
eff_weight = st.sidebar.slider(
    "Power Efficiency Weighting",
    min_value=1.0, max_value=2.0, value=1.2, step=0.1,
    help="Multiplies score based on the efficiency of Stargate equipment."
)

# Sorting & Filtering
sort_choice = st.sidebar.radio("Ranking Agent Priority:", options=["Profitability First", "Growth % (Highest)", "TAFGS Score"])
selected_role = st.sidebar.multiselect("Filter by AI Factory Role:", options=df["Role"].unique(), default=df["Role"].unique())

df_filtered = df[df["Role"].isin(selected_role)]

# 4. Interactive Data Editor (Company Ingestion Agent)
st.subheader("📝 Company Ingestion & Metric Editing")
edited_df = st.data_editor(df_filtered, num_rows="dynamic")

# 5. Scoring Logic Engine
def get_margin_score(m):
    if m > 40: return 5
    elif m >= 30: return 4
    elif m >= 20: return 3
    elif m >= 10: return 2
    else: return 1 

if not edited_df.empty:
    # Basic Calculations
    edited_df['Status'] = edited_df['Margin %'].apply(lambda x: '✅ Profitable' if x > 0 else '⚠️ Unprofitable')
    edited_df['Margin Score'] = edited_df['Margin %'].apply(get_margin_score)
    
    # Advanced TAFGS Calculation:
    # (Moat * Margin Score * Growth) * (Efficiency Weight) * (Risk Discount)
    base_score = (edited_df['Moat'] * edited_df['Margin Score']) * edited_df['Growth %']
    weighted_score = base_score * (1 + (edited_df['Efficiency Score'] * (eff_weight - 1) / 5))
    edited_df['TAFGS'] = weighted_score * (1 - (risk_penalty / 100))
    
    # Apply Agent Sorting
    if sort_choice == "Profitability First":
        final_df = edited_df.sort_values(["Status", "TAFGS"], ascending=[False, False])
    elif sort_choice == "Growth % (Highest)":
        final_df = edited_df.sort_values("Growth %", ascending=False)
    else:
        final_df = edited_df.sort_values("TAFGS", ascending=False)

    final_df = final_df.reset_index(drop=True)

    # 6. Heatmap Styling (Optimized for Visibility)
    st.subheader(f"📊 Ranking Output: {sort_choice}")

    def style_top_rows(s):
        """Forces high contrast black text on the yellow Top 20 highlight."""
        is_top_20 = s.index < 20
        return ['background-color: #FFF9C4; color: black;' if is_top_20[i] else '' for i in range(len(s))]

    styled_df = final_df.style.apply(style_top_rows, axis=0) \
                       .background_gradient(cmap='YlGn', subset=['TAFGS', 'Growth %']) \
                       .background_gradient(cmap='Blues', subset=['Moat', 'Efficiency Score']) \
                       .background_gradient(cmap='Reds_r', subset=['Margin %']) \
                       .format({'Margin %': '{:.1f}%', 'Growth %': '{:.1f}%', 'TAFGS': '{:.0f}'})

    st.dataframe(styled_df, use_container_width=True)

    # 7. Agentic Reporting
    st.info(f"💡 **Agent Summary:** Risk Discount of {risk_penalty}% and Power Efficiency Weight of {eff_weight}x applied.")
    
    # 8. Export
    st.download_button("📥 Export Investor-Ready Report", data=final_df.to_csv(index=False), file_name='top_ai_factory_analysis.csv')
