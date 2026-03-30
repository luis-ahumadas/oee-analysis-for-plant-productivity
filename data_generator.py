import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_oee_data(n_observations=10000, random_seed=42):
    """Generate synthetic OEE dataset"""
    np.random.seed(random_seed)
    
    start_date = datetime(2024, 1, 1)
    timestamps = [start_date + timedelta(minutes=30 * i) 
                  for i in range(n_observations)]
    
    # Production lines with different characteristics
    production_lines = [f"Line_{i}" for i in range(1, 6)]
    line_assignments = np.random.choice(production_lines, n_observations, 
                                         p=[0.25, 0.20, 0.20, 0.18, 0.17])
    
    # Generate OEE components with line-specific variations
    availability = np.zeros(n_observations)
    performance = np.zeros(n_observations)
    quality = np.zeros(n_observations)
    
    for i, line in enumerate(production_lines):
        mask = line_assignments == line
        if line == "Line_1":  # Best performer
            availability[mask] = np.random.beta(a=16, b=2, size=mask.sum()) * 0.95 + 0.05
            performance[mask] = np.random.normal(loc=0.88, scale=0.06, size=mask.sum())
            quality[mask] = np.random.beta(a=19, b=1.5, size=mask.sum()) * 0.95 + 0.05
        elif line == "Line_5":  # Worst performer
            availability[mask] = np.random.beta(a=12, b=4, size=mask.sum()) * 0.95 + 0.05
            performance[mask] = np.random.normal(loc=0.80, scale=0.10, size=mask.sum())
            quality[mask] = np.random.beta(a=16, b=3, size=mask.sum()) * 0.95 + 0.05
        else:  # Medium performers
            availability[mask] = np.random.beta(a=14, b=3, size=mask.sum()) * 0.95 + 0.05
            performance[mask] = np.random.normal(loc=0.85, scale=0.08, size=mask.sum())
            quality[mask] = np.random.beta(a=17, b=2.5, size=mask.sum()) * 0.95 + 0.05
    
    # Clip values to realistic ranges
    availability = np.clip(availability, 0.60, 0.98)
    performance = np.clip(performance, 0.60, 0.99)
    quality = np.clip(quality, 0.70, 0.995)
    
    # Add breakdown events
    breakdown_indices = np.random.choice(n_observations, 
                                        size=int(n_observations * 0.03), 
                                        replace=False)
    availability[breakdown_indices] *= np.random.uniform(0.2, 0.6, 
                                                          size=len(breakdown_indices))
    
    # Calculate OEE
    oee = availability * performance * quality
    
    # Add shift information with time-based patterns
    hours = np.array([ts.hour for ts in timestamps])
    shifts = np.where(hours < 6, 'Night',
                     np.where(hours < 14, 'Morning', 'Afternoon'))
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'production_line': line_assignments,
        'shift': shifts,
        'availability': availability,
        'performance': performance,
        'quality': quality,
        'oee': oee
    })
    
    # Add derived columns
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['day_name'] = df['timestamp'].dt.day_name()
    df['week'] = df['timestamp'].dt.isocalendar().week
    df['month'] = df['timestamp'].dt.month
    
    return df

if __name__ == "__main__":
    # Test data generation
    df = generate_oee_data()
    print(f"Generated {len(df)} observations")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Average OEE: {df['oee'].mean():.2%}")
