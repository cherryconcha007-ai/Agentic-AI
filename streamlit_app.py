import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="AI Factory Sandbox", layout="wide")
st.title("🌡️ AI Factory: Advanced Sorting & Heatmap")

# 2. Initial Data 
data = [
    {"Company": "Nvidia", "Segment": "Compute", "Moat": 5, "Margin %": 55.0, "Growth %": 45.0},
    {"Company": "Arista", "Segment": "Networking", "Moat": 4, "Margin %": 38.0, "Growth %": 30.0},
    {"Company": "Vertiv", "Segment": "Power", "Moat": 4, "Margin %": 25.0, "Growth %": 25.0},
    {"Company": "Eaton", "Segment": "Power", "Moat": 4, "Margin %": 18.0, "Growth %": 15.0},
    {"Company": "Speculative AI", "Segment": "Compute", "Moat": 2, "Margin %": -5.0, "Growth %": 60.0},
    {"Company": "Equinix", "Segment": "Data Centers", "Moat": 3, "Margin %": 15.0, "Growth %": 12.0},
]
df = pd.DataFrame(data)

# 3. Sidebar Filtering & Sorting
st.sidebar.header("Control Panel")

# Segment Filter
selected_segment = st.sidebar.multiselect(
    "Select Infrastructure Segments:",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

# NEW: Multi-Option Sorting
sort_choice = st.sidebar.radio(
    "Choose Sort Priority:",
    options=["Profitability First", "Growth % (Highest)", "TAFGS Score"]
)

df_filtered = df[df["Segment"].isin(selected_segment)]

# 4. Interactive Data Editor
st.subheader("📝 Edit Metrics")
edited_df = st.data_editor(df_filtered, num_rows="dynamic")

# 5. Scoring & Sorting Logic
def get_margin_score(m):
    if m > 40: return 5
    elif m >= 30: return 4
    elif m >= 20: return 3
    elif m >= 10: return 2
    else: return 1 

if not edited_df.empty:
    # Logic Processing
    edited_df['Status'] = edited_df['Margin %'].apply(lambda x: '✅ Profitable' if x > 0 else '⚠️ Unprofitable')
    edited_df['Margin Score'] = edited_df['Margin %'].apply(get_margin_score)
    edited_df['TAFGS'] = (edited_df['Moat'] * edited_df['Margin Score']) * edited_df['Growth %']
    
    # Apply the User's Sorting Choice
    if sort_choice == "Profitability First":
        # Sorts by Status (✅ before ⚠️) then by TAFGS
        final_df = edited_df.sort_values(["Status", "TAFGS"], ascending=[False, False])
    elif sort_choice == "Growth % (Highest)":
        final_df = edited_df.sort_values("Growth %", ascending=False)
    else:
        final_df = edited_df.sort_values("TAFGS", ascending=False)

    final_df = final_df.reset_index(drop=True)

    # 6. STYLING: Readable Highlights + Heatmaps
    st.subheader(f"📊 Ranking: {sort_choice}")

    def style_top_rows(s):
        """Forces black text on the top 20 highlighted rows for readability."""
        is_top_20 = s.index < 20
        return ['background-color: #FFF9C4; color: black;' if is_top_20[i] else '' for i in range(len(s))]

    # Build the Styled Table
    styled_df = final_df.style.apply(style_top_rows, axis=0) \
                       .background_gradient(cmap='YlGn', subset=['TAFGS', 'Growth %']) \
                       .background_gradient(cmap='Blues', subset=['Moat']) \
                       .background_gradient(cmap='Reds_r', subset=['Margin %']) \
                       .format({'Margin %': '{:.1f}%', 'Growth %': '{:.1f}%', 'TAFGS': '{:.0f}'})

    st.dataframe(styled_df, use_container_width=True)

    # 7. Export
    st.download_button("📥 Export Current View", data=final_df.to_csv(index=False), file_name='ai_factory_export.csv')
