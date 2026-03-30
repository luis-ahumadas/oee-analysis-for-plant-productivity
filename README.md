# OEE Manufacturing Productivity Dashboard

This project provides a comprehensive solution for monitoring and analyzing **Overall Equipment Effectiveness (OEE)** in a manufacturing environment. It includes a synthetic data generator, a statistical analysis engine, and an interactive Streamlit dashboard to visualize plant performance across different production lines and shifts.

## 📊 Overview

The application calculates and visualizes the three key components of OEE:
* **Availability:** Ratio of actual operating time to planned production time.
* **Performance:** Ratio of actual throughput to the maximum possible throughput.
* **Quality:** Ratio of good units produced to total units started.

The project is designed to help manufacturing managers identify bottlenecks, compare shift performance, and estimate the financial impact of productivity improvements.

## 🚀 Features

* **Synthetic Data Generation:** Generates realistic manufacturing telemetry including timestamps, shift patterns, and line-specific performance characteristics.
* **Interactive Dashboard:** A Streamlit-based interface featuring:
    * High-level OEE metrics and KPIs.
    * Shift-based performance comparisons.
    * Financial impact modeling (calculating potential revenue gains from OEE improvements).
    * Interactive data exploration and CSV export.
* **Statistical Analysis:** Built-in ANOVA testing (via Scipy) to determine if performance differences between shifts are statistically significant.
* **Root Cause Analysis:** Automatic identification of primary drivers behind poor performance (Availability vs. Performance vs. Quality).

## 📁 Repository Structure
oee-analysis-for-plant-productivity/

├── app.py       # Streamlit dashboard application

├── data_generator.py       # Synthetic data generator

├── oee-analysis-for-plant-productivity.ipynb       # Jupyter analysis notebook

├── utils.py        # Utility functions for OEE calculations

├── requirements.txt       # Python dependencies

└── .gitignore

## 🛠️ Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Dashboard:**
    ```bash
    streamlit run app.py
    ```

## 📉 Methodology

The project uses a **Beta distribution** to simulate realistic variations in manufacturing quality and availability, ensuring that data isn't just random noise but reflects actual industrial patterns. 

Statistical significance is measured using an **F-statistic (One-way ANOVA)** to compare the mean OEE across Morning, Afternoon, and Night shifts, helping leadership decide where training or maintenance resources are most needed.

## 📋 Requirements

* Python 3.8+
* Streamlit
* Pandas & NumPy
* Plotly & Matplotlib
* Scipy & Statsmodels
