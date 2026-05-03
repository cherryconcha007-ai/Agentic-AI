import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="AI Factory Sandbox", layout="wide")
st.title("🌡️ AI Factory: Full Dataset & Top 20 Highlights")

# 2. Initial Data (Including a negative margin example for testing)
data = [
    {"Company": "Nvidia", "Segment": "Compute", "Moat": 5, "Margin %": 55.0, "Growth %": 45.0},
    {"Company": "Arista", "Segment": "Networking", "Moat": 4, "Margin %": 38.0, "Growth %": 30.0},
    {"Company": "Vertiv", "Segment": "Power", "Moat": 4, "Margin %": 25.0, "Growth %": 25.0},
    {"Company": "Equinix", "Segment": "Data Centers", "Moat": 3, "Margin %": 15.0, "Growth %": 12.0},
    {"Company": "Eaton", "Segment": "Power", "Moat": 4, "Margin %": 18.0, "Growth %": 15.0},
    {"Company": "Speculative AI", "Segment": "Compute", "Moat": 2, "Margin %": -5.0, "Growth %": 60.0}, # Example of unprofitable
]
df = pd.DataFrame(data)

# 3. Sidebar Filtering
st.sidebar.header("Filter Analytics")
selected_segment = st.sidebar.multiselect(
    "Select Infrastructure Segments:",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

# Apply Filters (Notice: No more margin filter here!)
df_filtered = df[df["Segment"].isin(selected_segment)]

# 4. Interactive Data Editor
st.subheader("📝 Edit All Company Metrics")
edited_df = st.data_editor(df_filtered, num_rows="dynamic")

# 5. Scoring Logic Engine
def get_margin_score(m):
    if m > 40: return 5
    elif m >= 30: return 4
    elif m >= 20: return 3
    elif m >= 10: return 2
    else: return 1 # Minimum score for unprofitable/low margin

if not edited_df.empty:
    edited_df['Margin Score'] = edited_df['Margin %'].apply(get_margin_score)
    edited_df['TAFGS'] = (edited_df['Moat'] * edited_df['Margin Score']) * edited_df['Growth %']
    # Sorting by TAFGS so the top 20 are at the top
    final_df = edited_df.sort_values("TAFGS", ascending=False).reset_index(drop=True)

    # 6. Metrics
    c1, c2 = st.columns(2)
    with c1:
        top_seg = final_df.groupby("Segment")["TAFGS"].mean().idxmax()
        st.metric("Leading Segment", top_seg)
    with c2:
        st.metric("Total Companies Tracked", len(final_df))

    # 7. TOP 20 HIGHLIGHTING & HEATMAP
    st.subheader("📊 Full Dataset Ranking (Top 20 Highlighted)")

    def highlight_top_20(s):
        # Create a boolean mask for the first 20 rows
        is_top_20 = s.index < 20
        return ['background-color: #fff4d1' if is_top_20[i] else '' for i in range(len(s))]

    # Apply styling
    styled_df = final_df.style.apply(highlight_top_20, axis=0) \
                       .background_gradient(cmap='YlGn', subset=['TAFGS', 'Growth %']) \
                       .background_gradient(cmap='Blues', subset=['Moat']) \
                       .format({'Margin %': '{:.1f}%', 'Growth %': '{:.1f}%'})

    st.dataframe(styled_df, use_container_width=True)

    # 8. Export
    csv = final_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Full Research", data=csv, file_name='full_ai_factory_research.csv')
