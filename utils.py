import pandas as pd
import numpy as np
from scipy import stats

def calculate_oee_metrics(df):
    """Calculate key OEE metrics"""
    metrics = {
        'avg_oee': df['oee'].mean(),
        'avg_availability': df['availability'].mean(),
        'avg_performance': df['performance'].mean(),
        'avg_quality': df['quality'].mean(),
        'world_class_pct': (df['oee'] > 0.85).mean() * 100,
        'good_pct': ((df['oee'] >= 0.6) & (df['oee'] <= 0.85)).mean() * 100,
        'poor_pct': (df['oee'] < 0.6).mean() * 100,
        'total_obs': len(df)
    }
    return metrics

def get_line_performance(df):
    """Get performance metrics by shift"""
    return df.groupby('shift').agg({
        'availability': 'mean',
        'performance': 'mean',
        'quality': 'mean',
        'oee': 'mean',
        'oee': 'std'
    }).round(4)

def get_shift_performance(df):
    """Get performance metrics by shift"""
    return df.groupby('shift').agg({
        'availability': 'mean',
        'performance': 'mean',
        'quality': 'mean',
        'oee': 'mean',
        'oee': 'std'
    }).round(4)

def analyze_shift_differences(df):
    """Perform statistical analysis on shift differences"""
    morning_oee= df[df['shift'] == 'Morning']['oee']
    afternoon_oee = df[df['shift'] == 'Afternoon']['oee']
    night_oee = df[df['shift'] == 'Night']['oee']

    f_stats, p_value = stats.f_oneway(morning_oee, afternoon_oee, night_oee)
    return f_stats, p_value

def identify_root_causes(df):
    """Identify root causes of poor performance"""
    poor_performance = df[df['oee'] < 0.6]

    causes = {
        'Low Availability': (poor_performance['availability'] < 0.7).mean() * 100,
        'Low Performance': (poor_performance['performance'] < 0.7).mean() * 100,
        'Low Quality': (poor_performance['quality'] < 0.85).mean() * 100
    }
    return causes, len(poor_performance)

def calculate_financial_impact(df, daily_production=10000, unit_value=50):
    """Calculate potential financial impact of improvements"""
    current_oee = df['oee'].mean()
    target_oee = 0.85

    if current_oee < target_oee:
        potential_gain = (target_oee - current_oee) / current_oee
        additional_units = daily_production * potential_gain
        daily_revenue = additional_units * unit_value
        annual_revenue = daily_revenue * 365

        return {
            'current_oee': current_oee,
            'target_oee': target_oee,
            'additional_units': additional_units,
            'daily_revenue': daily_revenue,
            'annual_revenue': annual_revenue
        }
    return None
