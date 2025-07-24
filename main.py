# main.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import random

class Vizu:
    """
    A class for creating advanced and appealing data visualizations,
    inspired by Flourish.

    This library aims to simplify the creation of complex, animated charts
    like bar chart races and animated scatter plots from pandas DataFrames.

    Future versions may include more chart types and integration with
    interactive libraries like Plotly or Bokeh for web-based applications.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the Vizu object.

        Args:
            df (pd.DataFrame): The input data. The expected structure of the
                               DataFrame depends on the visualization you
                               intend to create. See the documentation for each
                               chart type for specific format requirements.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        self.df = df.copy()
        self.colors = {}

    def _get_colors(self, group_field: str, df: pd.DataFrame):
        """Assigns a reproducible random color to each unique group."""
        unique_groups = df[group_field].unique()
        for group in unique_groups:
            if group not in self.colors:
                random.seed(group) # Use group name as seed for consistent colors
                self.colors[group] = '#%06X' % random.randint(0, 0xFFFFFF)
        return df[group_field].map(self.colors)

    def _prepare_bar_chart_race_data(self, name_field: str, group_field: str, time_start: int, time_end: int):
        """Prepares and transforms data for the bar chart race, including interpolation."""
        all_years = [str(year) for year in range(time_start, time_end + 1)]
        original_time_cols = [col for col in self.df.columns if col.isnumeric()]
        df_interpolated = self.df.set_index([name_field, group_field])[original_time_cols]
        df_interpolated = df_interpolated.reindex(columns=all_years)
        df_interpolated = df_interpolated.interpolate(axis=1)
        df_interpolated = df_interpolated.reset_index()

        df_long = df_interpolated.melt(
            id_vars=[name_field, group_field],
            var_name='time',
            value_name='value'
        )
        df_long['time'] = pd.to_numeric(df_long['time'])
        df_long['color'] = self._get_colors(group_field, df_long)
        return df_long

    def create_bar_chart_race(self, 
                              name_field: str, 
                              group_field: str,
                              time_start: int,
                              time_end: int,
                              title: str = "Bar Chart Race",
                              output_filename: str = "bar_chart_race.gif",
                              top_n: int = 10,
                              interval: int = 200,
                              fps: int = 5):
        """Creates an animated bar chart race and saves it as a GIF."""
        df_long = self._prepare_bar_chart_race_data(name_field, group_field, time_start, time_end)
        
        fig, ax = plt.subplots(figsize=(15, 8), dpi=120)
        
        def draw_barchart(current_time):
            ax.clear()
            dff = df_long[df_long['time'].eq(current_time)].sort_values(by='value', ascending=True).tail(top_n).reset_index()
            ax.barh(dff.index, dff['value'], color=dff['color'])
            for i, (value, name) in enumerate(zip(dff['value'], dff[name_field])):
                ax.text(value, i, f' {name}', ha='left', va='center', fontsize=12, weight='bold')
                ax.text(value, i, f' {value:,.0f}  ', ha='right', va='center', fontsize=12, color='white')
            ax.text(1, 0.4, current_time, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
            ax.set_yticks([]); ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')); ax.xaxis.set_ticks_position('top')
            ax.tick_params(axis='x', colors='#777777', labelsize=12); plt.box(False)
            handles = [plt.Rectangle((0,0),1,1, color=self.colors[group]) for group in self.colors]
            ax.legend(handles, self.colors.keys(), title=group_field.title())
            ax.set_title(title, fontsize=22, weight='bold', pad=20)
            ax.set_xlim(0, dff['value'].max() * 1.15)
            plt.tight_layout()

        animator = animation.FuncAnimation(fig, draw_barchart, frames=range(time_start, time_end + 1), interval=interval)
        animator.save(output_filename, writer='pillow', fps=fps)
        plt.close(fig)
        print(f"Success! Animation saved to '{output_filename}'")

    def _prepare_animated_scatter_data(self, time_field, name_field):
        """Interpolates data for a smooth animated scatter plot."""
        df = self.df.copy()
        min_time, max_time = int(df[time_field].min()), int(df[time_field].max())
        all_times = np.arange(min_time, max_time + 1)
        
        interpolated_dfs = []
        for name, group_df in df.groupby(name_field):
            group_df = group_df.set_index(time_field).reindex(all_times)
            group_df = group_df.interpolate().ffill().bfill()
            interpolated_dfs.append(group_df)
            
        return pd.concat(interpolated_dfs).reset_index()

    def create_animated_scatter(self, 
                                time_field: str, x_field: str, y_field: str, size_field: str, 
                                name_field: str, group_field: str,
                                title: str = "Animated Scatter Plot",
                                output_filename: str = "animated_scatter.gif",
                                x_label: str = "", y_label: str = "",
                                size_scale: float = 1.0,
                                interval: int = 150, fps: int = 10):
        """Creates an animated scatter plot from long-format data."""
        df_long = self._prepare_animated_scatter_data(time_field, name_field)
        df_long['color'] = self._get_colors(group_field, df_long)
        
        fig, ax = plt.subplots(figsize=(15, 8), dpi=120)
        min_time, max_time = int(df_long[time_field].min()), int(df_long[time_field].max())

        def draw_scatter(current_time):
            ax.clear()
            dff = df_long[df_long[time_field].eq(current_time)]
            
            ax.scatter(dff[x_field], dff[y_field], s=dff[size_field] * size_scale, 
                       c=dff['color'], alpha=0.7, edgecolors='black')
            
            # Add labels for the largest bubbles to avoid clutter
            for i, row in dff.nlargest(5, size_field).iterrows():
                ax.text(row[x_field], row[y_field], row[name_field], fontsize=10, ha='center', va='center')
            
            ax.text(1, 0.9, current_time, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
            handles = [plt.Rectangle((0,0),1,1, color=self.colors[group]) for group in self.colors]
            
            # --- LEGEND PLACEMENT FIX ---
            # Move legend outside the plot area to prevent it from covering data points.
            ax.legend(handles, self.colors.keys(), title=group_field.title(), loc='upper left', bbox_to_anchor=(1.02, 1))
            
            ax.set_title(title, fontsize=22, weight='bold', pad=20)
            ax.set_xlabel(x_label.title(), fontsize=14); ax.set_ylabel(y_label.title(), fontsize=14)
            ax.set_xlim(self.df[x_field].min(), self.df[x_field].max())
            ax.set_ylim(self.df[y_field].min(), self.df[y_field].max())
            
            # Adjust subplot parameters to make room for the legend
            plt.subplots_adjust(right=0.85)

        animator = animation.FuncAnimation(fig, draw_scatter, frames=range(min_time, max_time + 1), interval=interval)
        animator.save(output_filename, writer='pillow', fps=fps)
        plt.close(fig)
        print(f"Success! Animation saved to '{output_filename}'")
        
    def create_line_chart_race(self):
        """Placeholder for a future line chart race visualization."""
        raise NotImplementedError("This feature is currently under development!")