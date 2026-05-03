import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="AI Factory Sandbox", layout="wide")
st.title("🌡️ AI Factory: Top 20 Interactive Sandbox")

# 2. Initial Data
data = [
    {"Company": "Nvidia", "Segment": "Compute", "Moat": 5, "Margin %": 55, "Growth %": 45},
    {"Company": "Arista", "Segment": "Networking", "Moat": 4, "Margin %": 38, "Growth %": 30},
    {"Company": "Vertiv", "Segment": "Power", "Moat": 4, "Margin %": 25, "Growth %": 25},
    {"Company": "Equinix", "Segment": "Data Centers", "Moat": 3, "Margin %": 15, "Growth %": 12},
    {"Company": "Eaton", "Segment": "Power", "Moat": 4, "Margin %": 18, "Growth %": 15},
]
df = pd.DataFrame(data)

# 3. Interactive Sidebar Filters
st.sidebar.header("Filter Analytics")
selected_segment = st.sidebar.multiselect(
    "Select Infrastructure Segments:",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

# Filter Data based on Sidebar
df_filtered = df[df["Segment"].isin(selected_segment)]
df_filtered = df_filtered[df_filtered['Margin %'] > 0] # Profitability Guardrail

# 4. Interactive Data Editor
st.subheader("📝 Edit Company Metrics (Moat & Growth)")
edited_df = st.data_editor(df_filtered, num_rows="dynamic")

# 5. TAFGS Logic Engine
def get_margin_score(m):
    if m > 40: return 5
    elif m >= 30: return 4
    elif m >= 20: return 3
    elif m >= 10: return 2
    else: return 1

edited_df['Margin Score'] = edited_df['Margin %'].apply(get_margin_score)
edited_df['TAFGS'] = (edited_df['Moat'] * edited_df['Margin Score']) * edited_df['Growth %']
final_df = edited_df.sort_values("TAFGS", ascending=False)

# 6. Top Metrics
c1, c2 = st.columns(2)
with c1:
    top_seg = final_df.groupby("Segment")["TAFGS"].mean().idxmax()
    st.metric("Hottest Segment", top_seg)
with c2:
    st.metric("Avg Growth Score", f"{final_df['TAFGS'].mean():.0f}")

# 7. HEATMAP VISUALIZATION
st.subheader("📊 Ranking Heatmap")

# Applying conditional colors (Heatmap)
def style_heatmap(df):
    return df.style.background_gradient(cmap='YlGn', subset=['TAFGS', 'Growth %']) \
                   .background_gradient(cmap='Blues', subset=['Moat']) \
                   .format({'Margin %': '{:.1f}%', 'Growth %': '{:.1f}%'})

st.dataframe(style_heatmap(final_df), use_container_width=True)

# 8. Export
csv = final_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Export Research to CSV", data=csv, file_name='ai_factory_research.csv')
