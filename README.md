<div align="center">

# wavG 📊

**Create stunning, animated, and insightful data visualizations with ease.**

</div>

<div align="center">

<!-- Placeholder Badges: Replace with actual links when ready -->
![PyPI](https://img.shields.io/pypi/v/wavG?style=for-the-badge)
![Build](https://img.shields.io/github/actions/workflow/status/your-username/wavG/main.yml?style=for-the-badge)
![License](https://img.shields.io/github/license/agusrajuthaliyan/wavG?style=for-the-badge)

</div>

wavG is a Python library inspired by the dynamic data stories from platforms like Flourish. It provides a simple, high-level interface to turn your data into compelling animated charts like bar chart races and animated scatter plots.

---

## ✨ Features

* **Bar Chart Race**: Create animated bar charts that show changing ranks and values over time.
* **Animated Scatter Plot**: Generate "Gapminder-style" charts to visualize relationships between multiple variables.
* **Data Interpolation**: Automatically handles missing time-series data to create smooth, continuous animations.
* **Customization**: Control animation speed, titles, labels, and more.
* **GIF Export**: Save your creations as high-quality `.gif` files to share anywhere.

---

## 🚀 Getting Started

### Prerequisites

wavG requires the following Python libraries. You can install them using pip:

```bash
pip install pandas matplotlib
```

### Installation

To get started, clone this repository and install the library in "editable" mode. This is the recommended approach for local development, as it allows your project to automatically recognize any changes you make to the library code.

1.  **Navigate to the project's root directory** (`FLOURISH LIBRARY/`).
2.  **Run the following command in your terminal**:
    ```bash
    pip install -e .
    ```

---

## Quickstart & API

Here’s how you can create your first visualization with wavG.

### 1. Bar Chart Race

This example creates a bar chart race showing the population growth of different cities.

```python
import pandas as pd
from wavg.wavg import Vizu

# Sample Data
data = {
    'city': ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'],
    'continent': ['Asia', 'Europe', 'Asia', 'America', 'Europe'],
    '1980': [100, 80, 120, 90, 70],
    '1990': [110, 85, 130, 100, 75],
    '2000': [150, 95, 160, 110, 85],
    '2010': [200, 110, 210, 130, 100],
    '2020': [280, 130, 290, 150, 120]
}
df = pd.DataFrame(data)

# Instantiate wavG and create the visualization
visualizer = wavG(df)
visualizer.create_bar_chart_race(
    name_field='city',
    group_field='continent',
    title='City Population Growth (1980-2020)',
    output_filename='city_population_race.gif'
)
```

### 2. Animated Scatter Plot

This example creates an animated scatter plot showing the growth of fictional tech companies.

```python
import pandas as pd
from wavg.wavg import Vizu

# Sample Data
data = {
    'year': [2010, 2015, 2020] * 4,
    'company': ['Alpha', 'Beta', 'Gamma', 'Delta'],
    'sector': ['Software', 'Hardware', 'Cloud', 'Hardware'],
    'market_share': [10, 15, 25, 30, 25, 22, 5, 15, 30, 20, 18, 15],
    'satisfaction': [70, 75, 85, 90, 82, 80, 60, 80, 92, 85, 80, 75],
    'revenue': [500, 1200, 3000, 4000, 3500, 3200, 200, 1500, 4000, 2500, 2200, 1800]
}
df_scatter = pd.DataFrame(data)

# Instantiate wavG and create the visualization
scatter_visualizer = wavG(df_scatter)
scatter_visualizer.create_animated_scatter(
    time_field='year',
    x_field='market_share',
    y_field='satisfaction',
    size_field='revenue',
    name_field='company',
    group_field='sector',
    title="Tech Company Growth (2010-2020)",
    output_filename="tech_growth_scatter.gif"
)
```

---

## 🎯 Roadmap

* **More Chart Types**: Add a line chart race, animated network graphs, and more.
* **Interactivity**: Integrate with backends like Plotly or Bokeh.
* **Advanced Customization**: Allow for full control over colors, fonts, and layouts.
* **Export Formats**: Add support for exporting animations as MP4 video files.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.