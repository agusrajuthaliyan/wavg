import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wavg.wavg import Vizu # Assuming the class is in main.py

# --- 1. Create Sample Data ---
# In a real-world scenario, you would load your data from a CSV or other source.
# The data needs to be in a "wide" format:
# - One column for the item name (e.g., 'city').
# - One column for the group (e.g., 'continent').
# - Multiple columns representing values at different points in time (e.g., '1980', '1981', ...).

data = {
    'city': ['Tokyo', 'Delhi', 'Shanghai', 'São Paulo', 'Mumbai', 'Mexico City', 'Beijing', 'Osaka', 'Cairo', 'New York', 'Dhaka', 'Karachi'],
    'continent': ['Asia', 'Asia', 'Asia', 'South America', 'Asia', 'North America', 'Asia', 'Asia', 'Africa', 'North America', 'Asia', 'Asia'],
    '1980': [28557, 10093, 11487, 12093, 9926, 13994, 9225, 16946, 8820, 15600, 4220, 5131],
    '1990': [32530, 12316, 13349, 14776, 12440, 15309, 10862, 18389, 10645, 16079, 6621, 7185],
    '2000': [34450, 15727, 16654, 17015, 16434, 17409, 13619, 18768, 12431, 17890, 10249, 10031],
    '2010': [36830, 21935, 20218, 19672, 18414, 19320, 16760, 19325, 16845, 19416, 14543, 13205],
    '2020': [37393, 29399, 26317, 21846, 20185, 21782, 20035, 19222, 20484, 20140, 20283, 16093]
}
df = pd.DataFrame(data)

# --- 2. Instantiate the Vizu class ---
# Pass your DataFrame to the Vizu object.
visualizer = Vizu(df)

# --- 3. Create the Visualization ---
# Call the method to create the bar chart race.
# Specify the column names and the time range you want to animate.
visualizer.create_bar_chart_race(
    name_field='city',
    group_field='continent',
    time_start=1980,
    time_end=2020,
    title="Top 10 Most Populous Cities",
    output_filename="demo/files/city_population_race.gif"
)