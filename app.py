import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_generator import generate_oee_data
from utils import *

# Page configuration
st.set_page_config(
    page_title="OEE Manufacturing Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .warning-text {
        color: #ff4b4b;
        font-weight: bold;
    }
    .success-text {
        color: #00cc96;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data
if 'data' not in st.session_state:
    with st.spinner('Generating manufacturing data...'):
        st.session_state.data = generate_oee_data(10000)
        st.session_state.filtered_data = st.session_state.data.copy()

# Sidebar - Filters
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/factory.png", width=80)
    st.title("🔧 Control Panel")
    
    # Date range filter
    min_date = st.session_state.data['timestamp'].min().date()
    max_date = st.session_state.data['timestamp'].max().date()
    
    date_range = st.date_input(
        "📅 Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Production line filter
    lines = st.multiselect(
        "🏭 Production Lines",
        options=st.session_state.data['production_line'].unique(),
        default=st.session_state.data['production_line'].unique()
    )
    
    # Shift filter
    shifts = st.multiselect(
        "⏰ Shifts",
        options=['Morning', 'Afternoon', 'Night'],
        default=['Morning', 'Afternoon', 'Night']
    )
    
    # OEE range filter
    oee_range = st.slider(
        "📊 OEE Range",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.05
    )

    # Apply filters
    if st.button("🔄 Apply Filters", type="primary"):
        mask = (
            (st.session_state.data['timestamp'].dt.date >= date_range[0]) &
            (st.session_state.data['timestamp'].dt.date <= date_range[1]) &
            (st.session_state.data['production_line'].isin(lines)) &
            (st.session_state.data['shift'].isin(shifts)) &
            (st.session_state.data['oee'] >= oee_range[0]) &
            (st.session_state.data['oee'] <= oee_range[1])
        )
        st.session_state.filtered_data = st.session_state.data[mask]
        st.success(f"✅ Filtered to {len(st.session_state.filtered_data):,} observations")

    # Reset filters
    if st.button("🔄 Reset Filters"):
        st.session_state.filtered_data = st.session_state.data.copy()
        st.success('Filters reset!')

    # Data refresh button
    if st.button("🔄 Generate New Data"):
        with st.spinner('Generating new dataset...'):
            st.session_state.data = generate_oee_data(10000)
            st.session_state.filtered_data = st.session_state.data.copy()
        st.success("New data generated!")

# Main content
st.markdown('<h1 class="main-header">🏭 Overall Equipment Effectiveness (OEE) Dashboard</h1>',
             unsafe_allow_html=True)
st.markdown("---")

# Get filtered data
df = st.session_state.filtered_data

# Key Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    avg_oee = df['oee'].mean()
    st.metric(
        "📈 Average OEE",
        f"{avg_oee:.1%}",
        delta=f"{(avg_oee - 0.85):.1%} vs World Class"
    )

with col2:
    st.metric(
        "⚙️ Availability",
        f"{df['availability'].mean():.1%}",
        delta=None
    )

with col3:
    st.metric(
        "🏃 Performance",
        f"{df['performance'].mean():.1%}",
        delta=None
    )

with col4:
    st.metric(
        "✨ Quality",
        f"{df['quality'].mean():.1%}",
        delta=None
    )

with col5:
    total_obs = len(df)
    st.metric(
        "📊 Observations",
        f"{total_obs:,}",
        delta=None
    )

st.markdown("---")

# First Row - OEE Distribution and Components
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 OEE Distribution")

    fig = px.histogram(
        df, x ='oee', nbins=50,
        title='Distribution of OEE Values',
        labels={'oee': 'OEE', 'count': 'Frequency'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.add_vline(x=avg_oee, line_dash="dash", line_color="red",
                  annotation_text=f"Mean: {avg_oee:.1%}")
    fig.add_vline(x=0.85, line_dash="dash", line_color='green',
                  annotation_text="World Class")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 OEE Components Box Plot")

    components_df = df[['availability', 'performance', 'quality']].melt()
    fig = px.box(components_df, x='variable', y='value',
                 title='Distribution of OEE Components',
                 labels={'variable': 'Component', 'value': 'value'},
                 color='variable')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Second Row - Prediction Line and Shift Performance
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏭 Performance by Production Line")
    
    line_perf = get_line_performance(df)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bars for components
    x = list(range(len(line_perf)))
    fig.add_trace(go.Bar(name='Availability', x=line_perf.index, 
                         y=line_perf['availability'], offsetgroup=0),
                  secondary_y=False)
    fig.add_trace(go.Bar(name='Performance', x=line_perf.index, 
                         y=line_perf['performance'], offsetgroup=1),
                  secondary_y=False)
    fig.add_trace(go.Bar(name='Quality', x=line_perf.index, 
                         y=line_perf['quality'], offsetgroup=2),
                  secondary_y=False)
    
    # Add line for OEE
    fig.add_trace(go.Scatter(name='OEE', x=line_perf.index, 
                             y=line_perf['oee'] * 100,
                             mode='lines+markers',
                             line=dict(color='red', width=2)),
                  secondary_y=True)
    
    fig.update_layout(
        title="Production Line Comparison",
        xaxis_title="Production Line",
        height=400,
        barmode='group'
    )
    fig.update_yaxes(title_text="Component Value", secondary_y=False)
    fig.update_yaxes(title_text="OEE (%)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⏰ Performance by Shift")

    shift_perf = get_shift_performance(df)

    fig = go.Figure()

    for component in ['availability', 'performance', 'quality']:
        fig.add_trace(go.Bar(
            name=component.capitalize(),
            x=shift_perf.index,
            y=shift_perf[component],
            text=[f"{v:.1%}" for v in shift_perf[component]],
            textposition='auto'
        ))

    fig.update_layout(
        title="Shift Performance Comparison",
        xaxis_title="Shift",
        yaxis_title="Value",
        barmode='group',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

# Third Row - Time Series Analysis
st.subheader("📈 OEE Time Series Analysis")

# Daily aggregation
daily_data = df.groupby('date')['oee'].mean().reset_index()

fig = px.line(daily_data, x='date', y='oee',
              title='OEE Trend Over Time',
              labels={'date': 'Date', 'oee': 'Average OEE'})
fig.add_hline(y=0.85, line_dash='dash', line_color='green',
              annotation_text='World Class Taeget')
fig.add_hline(y=df['oee'].mean(), line_dash='dash', line_color='red',
              annotation_text=f"Average: {df['oee'].mean():.1%}")
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# Fourth Row - Root Cause Analysis
st.subheader("🔍 Root Cause Analysis")

col1, col2 = st.columns(2)

with col1:
    causes, poor_count = identify_root_causes(df)

    if poor_count > 0:
        fig = px.pie(values=list(causes.values()),
                     names=list(causes.keys()),
                     title=f'Root Causes of Poor Performance (OEE < 60%)',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("🎉 No poor performance periods detected! All OEE above 60%.")

with col2:
    st.subheader("💡 Improvement Opportunities")

    # Calculate improvement potential
    improvement_potential = {
        'Performance': (df['performance'].max() - df['performance'].mean()) * 100,
        'Availability': (df['availability'].max() - df['availability'].mean()) * 100,
        'Quality': (df['quality'].max() - df['quality'].mean()) * 100
    }

    fig = px.bar(x=list(improvement_potential.keys()),
                 y=list(improvement_potential.values()),
                 title='Potential Improvement by Component (%)',
                 labels={'x': 'Component', 'y': 'Potential Improvement (%)'},
                 color=list(improvement_potential.keys()))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Fifth Row - Statistical Analysis
st.subheader(" Statistical Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📈 **OEE Classification")
    metrics = calculate_oee_metrics(df)
    st.write(f"✅ World Class (>85%): **{metrics['world_class_pct']:.1f}%**")
    st.write(f"📊 Good (60-85%): **{metrics['good_pct']:.1f}%**")
    st.write(f"⚠️ Poor (60%): **{metrics['poor_pct']:.1f}%**")

with col2:
    st.info("🔬 **Shift Analysis**")
    f_stat, p_value = analyze_shift_differences(df)
    st.write(f"**ANOVA Test Results:**")
    st.write(f"F-statistic: {f_stat:.3f}")
    st.write(f"P-value: {p_value:.4f}")
    if p_value < 0.05:
        st.success("✅ Significant differences exist between shifts")
    else:
        st.info("❌ No significant differences between shifts")

with col3:
    st.info("💰 **Financial Impact**")
    financial = calculate_financial_impact(df)
    if financial:
        st.write(f"**Current OEE:** {financial['current_oee']:.1%}")
        st.write(f"**Target OEE:** {financial['target_oee']:.0%}")
        st.write(f"**Anual Revenue Potential:**")
        st.write(f"**${financial['annual_revenue']:,.0f}**")
        st.caption("Additional revenue at target OEE")

# Sixth Row - Data Explorer
with st.expander("🔍 Data Explorer - View Raw Data"):
    st.dataframe(
        df.head(100),
        use_container_width=True,
        height=400
    )

    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data to CSV",
        data=csv,
        file_name=f"oee_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
            <p> OEE Manufacturing Dashboard | Built with Streamlit | Data refreshes every session</p>
            <p> Tip: Use the sidebar filters to analyze specific time periods, production lines, or OEE ranges</p>
            <p>Author: Luis Alberto Ahumada Sanchez</p>
</div>
""", unsafe_allow_html=True)