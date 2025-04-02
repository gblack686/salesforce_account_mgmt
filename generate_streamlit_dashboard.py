import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import pyautogui
import time
import os
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Data Enrichment Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    try:
        # Try to load the final version first
        df_account_info = pd.read_excel("sample_data_workbook_final.xlsx", sheet_name="Account Info")
        df_contact_info = pd.read_excel("sample_data_workbook_final.xlsx", sheet_name="Contact Info")
        df_enrichment_cadences = pd.read_excel("sample_data_workbook_final.xlsx", sheet_name="Enrichment Cadences")
        df_account_health_check_kpis = pd.read_excel("sample_data_workbook_final.xlsx", sheet_name="Account Health Checks")
        df_tier_health_check_kpis = pd.read_excel("sample_data_workbook_final.xlsx", sheet_name="Tier Health Checks")
        df_scoring_logic = pd.read_excel("sample_data_workbook_final.xlsx", sheet_name="Scoring Logic")
    except:
        # If that fails, try the updated version
        try:
            df_account_info = pd.read_excel("sample_data_workbook_updated.xlsx", sheet_name="Account Info")
            df_contact_info = pd.read_excel("sample_data_workbook_updated.xlsx", sheet_name="Contact Info")
            df_enrichment_cadences = pd.read_excel("sample_data_workbook_updated.xlsx", sheet_name="Enrichment Cadences")
            df_account_health_check_kpis = pd.read_excel("sample_data_workbook_updated.xlsx", sheet_name="Account Health Checks")
            df_tier_health_check_kpis = pd.read_excel("sample_data_workbook_updated.xlsx", sheet_name="Tier Health Checks")
            df_scoring_logic = pd.read_excel("sample_data_workbook_updated.xlsx", sheet_name="Scoring Logic")
        except:
            # If that fails too, use the original version
            df_account_info = pd.read_excel("sample_data_workbook.xlsx", sheet_name="Account Info")
            df_contact_info = pd.read_excel("sample_data_workbook.xlsx", sheet_name="Contact Info")
            # These may not exist in the original version, so create placeholders
            df_enrichment_cadences = pd.DataFrame()
            df_account_health_check_kpis = pd.DataFrame()
            df_tier_health_check_kpis = pd.DataFrame()
            df_scoring_logic = pd.DataFrame()
    
    return df_account_info, df_contact_info, df_enrichment_cadences, df_account_health_check_kpis, df_tier_health_check_kpis, df_scoring_logic

def take_screenshot():
    """Take a screenshot and save it as PNG"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dashboard_screenshot_{timestamp}.png"
    
    # Give user some time to prepare
    with st.spinner("Taking screenshot in 3 seconds..."):
        time.sleep(3)
    
    # Take the screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    
    return filename

# Function to enable downloading the screenshot
def get_image_download_link(img_path, filename):
    with open(img_path, "rb") as file:
        img_bytes = file.read()
    
    import base64
    b64 = base64.b64encode(img_bytes).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">Download Screenshot</a>'
    return href

df_account_info, df_contact_info, df_enrichment_cadences, df_account_health_check_kpis, df_tier_health_check_kpis, df_scoring_logic = load_data()

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: white;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 60px;
        font-weight: bold;
        color: #1e88e5;
    }
    .metric-label {
        font-size: 18px;
        color: #424242;
    }
    .metric-status {
        font-size: 16px;
        margin-top: 5px;
    }
    .chart-container {
        background-color: white;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    }
    .chart-title {
        font-size: 16px;
        font-weight: bold;
        color: #424242;
        margin-bottom: 10px;
    }
    .stExpander {
        border: none !important;
    }
    .screenshot-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Title with screenshot button
col_title, col_button = st.columns([3, 1])
with col_title:
    st.title("Data Enrichment Dashboard")
with col_button:
    if st.button("Take Screenshot", help="Save dashboard as PNG"):
        screenshot_path = take_screenshot()
        st.success(f"Screenshot saved as {screenshot_path}")
        st.markdown(get_image_download_link(screenshot_path, os.path.basename(screenshot_path)), unsafe_allow_html=True)

# First row - 3 charts
col1, col2, col3 = st.columns(3)

# --- CHART 1: Accounts by Tier (like "Open Cases by Status") ---
with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Accounts by Tier</div>", unsafe_allow_html=True)
    
    # Count accounts by tier
    if not df_enrichment_cadences.empty:
        tier_counts = df_enrichment_cadences['tier'].value_counts().reset_index()
        tier_counts.columns = ['Tier', 'Count']
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=tier_counts['Tier'],
            values=tier_counts['Count'],
            hole=0.6,
            marker_colors=['#1e88e5', '#43a047', '#fb8c00']
        )])
        
        # Add text in the center
        total_accounts = tier_counts['Count'].sum()
        fig.add_annotation(
            text=f'<b>{total_accounts}</b>',
            x=0.5, y=0.5,
            font_size=24,
            showarrow=False
        )
        
        fig.update_layout(
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0),
            height=300,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div style='font-size:12px; color:#666;'>Click the report to see a detailed view.<br>View Report (KPI: Accounts by Tier)</div>", unsafe_allow_html=True)
    else:
        st.info("No tier data available")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- CHART 2: Enrichment Requests This Quarter by Source ---
with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Enrichment Requests This Quarter by Source</div>", unsafe_allow_html=True)
    
    # We'll simulate this with dummy data
    sources = ['ZoomInfo', 'D&B', 'Web Scraping', 'Social Media', 'Internal']
    counts = [12, 18, 8, 5, 3]
    colors = ['#1e88e5', '#43a047', '#fb8c00', '#9c27b0', '#e53935']
    
    source_data = pd.DataFrame({
        'Source': sources,
        'Count': counts
    })
    
    fig = px.bar(
        source_data, 
        x='Count', 
        y='Source',
        orientation='h',
        color='Source',
        color_discrete_sequence=colors
    )
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=300,
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div style='font-size:12px; color:#666;'>Open the report to see a detailed view.<br>View Report (KPI: Enrichment Requests by Source)</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- CHART 3: Enrichment Requests by Account ---
with col3:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Enrichment Requests by Account</div>", unsafe_allow_html=True)
    
    if not df_enrichment_cadences.empty:
        account_data = df_enrichment_cadences[['company_name', 'tier']].copy()
        
        # Define dummy enrichment requests
        account_data['Requests'] = np.random.randint(1, 8, size=len(account_data))
        account_data = account_data.sort_values('Requests', ascending=True)
        
        # Define colors based on tier
        colors = {
            'Tier 1': '#1e88e5',
            'Tier 2': '#43a047',
            'Tier 3': '#fb8c00'
        }
        account_data['Color'] = account_data['tier'].map(colors)
        
        fig = px.bar(
            account_data, 
            x='Requests', 
            y='company_name',
            orientation='h',
            color='tier',
            color_discrete_map=colors
        )
        
        fig.update_layout(
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0),
            height=300,
            xaxis_title=None,
            yaxis_title=None,
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div style='font-size:12px; color:#666;'>Open the report to see a detailed view.<br>View Report (KPI: Enrichment by Account)</div>", unsafe_allow_html=True)
    else:
        st.info("No account data available")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Second row - 3 metric cards
col1, col2, col3 = st.columns(3)

# --- METRIC 1: Percent of Accounts with Complete Data ---
with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Calculate the metric
    if not df_scoring_logic.empty:
        completeness_avg = df_scoring_logic['data_completeness_score'].mean()
        completeness_percent = int(completeness_avg)
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{completeness_percent}%</div>
            <div class='metric-label'>Data Completeness</div>
        </div>
        <div style='font-size:12px; color:#666; margin-top:5px;'>
            Click to set thresholds for your goals.<br>
            View Report (KPI: Data Completeness Score)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No completeness data available")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- METRIC 2: Percentage of Accounts Refreshed This Quarter ---
with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Generate a dummy metric
    refreshed_percent = 76
    
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{refreshed_percent}%</div>
        <div class='metric-label'>Accounts Refreshed This Quarter</div>
    </div>
    <div style='font-size:12px; color:#666; margin-top:5px;'>
        Click to set thresholds for your goals.<br>
        View Report (KPI: Quarterly Refreshes)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- METRIC 3: Average Confidence Score ---
with col3:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Calculate the metric
    if not df_scoring_logic.empty:
        confidence_avg = df_scoring_logic['final_confidence_score'].mean()
        confidence_score = int(confidence_avg)
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{confidence_score}</div>
            <div class='metric-label'>Average Confidence Score</div>
        </div>
        <div style='font-size:12px; color:#666; margin-top:5px;'>
            Click to set thresholds for your goals.<br>
            View Report (KPI: Confidence Scores)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No confidence score data available")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Third row - 3 charts
col1, col2, col3 = st.columns(3)

# --- CHART 4: Enriched Accounts by Tier This Quarter ---
with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Enriched Accounts by Tier This Quarter</div>", unsafe_allow_html=True)
    
    if not df_enrichment_cadences.empty:
        # We'll assume 3 accounts per tier were enriched (dummy data)
        enriched_data = pd.DataFrame({
            'Tier': ['Tier 1', 'Tier 2', 'Tier 3'],
            'Count': [3, 2, 1]
        })
        
        colors = {
            'Tier 1': '#1e88e5',
            'Tier 2': '#43a047',
            'Tier 3': '#fb8c00'
        }
        
        fig = px.bar(
            enriched_data, 
            x='Count', 
            y='Tier',
            orientation='h',
            color='Tier',
            color_discrete_map=colors
        )
        
        fig.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            height=300,
            xaxis_title=None,
            yaxis_title=None,
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div style='font-size:12px; color:#666;'>Open the report to see a detailed view.<br>View Report (KPI: Quarterly Enrichments by Tier)</div>", unsafe_allow_html=True)
    else:
        st.info("No enrichment data available")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- CHART 5: Accounts Closed This Quarter by Source ---
with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Accounts Enriched This Quarter by Day</div>", unsafe_allow_html=True)
    
    # Generate dummy data for enrichment over time
    dates = [(datetime.now() - timedelta(days=x)).strftime('%m/%d/%Y') for x in range(30, 0, -5)]
    sources = ['ZoomInfo', 'D&B', 'Web Scraping', 'Social Media', 'Internal']
    
    enrichment_data = pd.DataFrame()
    for source in sources:
        for date in dates:
            enrichment_data = pd.concat([enrichment_data, pd.DataFrame({
                'Date': [date],
                'Source': [source],
                'Count': [np.random.randint(0, 3)]
            })])
    
    enrichment_data = enrichment_data.reset_index(drop=True)
    
    # Create stacked bar chart
    fig = px.bar(
        enrichment_data, 
        x='Date', 
        y='Count',
        color='Source',
        color_discrete_sequence=['#1e88e5', '#43a047', '#fb8c00', '#9c27b0', '#e53935'],
        barmode='stack'
    )
    
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=300,
        xaxis_title=None,
        yaxis_title=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div style='font-size:12px; color:#666;'>Open the report to see a detailed view.<br>View Report (KPI: Enrichments by Day)</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- CHART 6: Average Hours to Resolution by Channel ---
with col3:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Average Hours to Enrichment by Source</div>", unsafe_allow_html=True)
    
    # Generate dummy data for average enrichment time by source
    enrichment_time_data = pd.DataFrame({
        'Source': ['ZoomInfo', 'D&B', 'Web Scraping', 'Social Media', 'Internal'],
        'Hours': [24, 36, 12, 48, 6]
    })
    
    # Sort by hours
    enrichment_time_data = enrichment_time_data.sort_values('Hours')
    
    fig = px.bar(
        enrichment_time_data, 
        x='Hours', 
        y='Source',
        orientation='h',
        color='Source',
        color_discrete_sequence=['#1e88e5', '#43a047', '#fb8c00', '#9c27b0', '#e53935']
    )
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=300,
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div style='font-size:12px; color:#666;'>Open the report to see a detailed view.<br>View Report (KPI: Enrichment Time by Source)</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Data last updated: March 28, 2025")
