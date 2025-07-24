import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wavg.wavg import Vizu # Assuming the class is in main.py

# --- 1. Create Sample Data for Animated Scatter ---
# This type of chart works best with "long" format data, where each
# row is a single observation at a point in time.
# This data shows fictional metrics for different tech companies over time.
data = {
    'year': [2010, 2015, 2020] * 4,
    'company': ['Alpha', 'Alpha', 'Alpha', 
                'Beta', 'Beta', 'Beta', 
                'Gamma', 'Gamma', 'Gamma', 
                'Delta', 'Delta', 'Delta'],
    'sector': ['Software', 'Software', 'Software', 
               'Hardware', 'Hardware', 'Hardware',
               'Cloud', 'Cloud', 'Cloud', 
               'Hardware', 'Hardware', 'Hardware'],
    # Metric 1 (e.g., Market Share %)
    'market_share': [10, 15, 25, 30, 25, 22, 5, 15, 30, 20, 18, 15],
    # Metric 2 (e.g., Customer Satisfaction / 100)
    'satisfaction': [70, 75, 85, 90, 82, 80, 60, 80, 92, 85, 80, 75],
    # Metric 3 (e.g., Revenue in Millions)
    'revenue': [500, 1200, 3000, 4000, 3500, 3200, 200, 1500, 4000, 2500, 2200, 1800]
}
df_scatter = pd.DataFrame(data)

# --- 2. Instantiate the Vizu class with the new data ---
scatter_visualizer = Vizu(df_scatter)

# --- 3. Create the Animated Scatter Plot ---
scatter_visualizer.create_animated_scatter(
    time_field='year',
    x_field='market_share',
    y_field='satisfaction',
    size_field='revenue',
    name_field='company',
    group_field='sector',
    title="Tech Company Growth (2010-2020)",
    x_label="Market Share (%)",
    y_label="Customer Satisfaction",
    size_scale=0.1,  # Adjust this to get appropriately sized bubbles
    output_filename="demo/files/tech_growth_scatter.gif"
)
