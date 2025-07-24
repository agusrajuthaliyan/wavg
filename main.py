# main.py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import random

class Vizu:
    """
    A class for creating advanced and appealing data visualizations,
    inspired by Flourish.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the Vizu object.

        Args:
            df (pd.DataFrame): The input data. For a bar chart race, it should
                               be "wide" with categories/names in one column and
                               time-series data in subsequent columns.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        self.df = df.copy()
        self.colors = {}

    def _prepare_bar_chart_race_data(self, value_field: str, time_field: str, name_field: str, group_field: str, time_start: int, time_end: int):
        """
        Prepares and transforms data for the bar chart race.
        It handles data interpolation for missing years and converts the
        DataFrame to a long format suitable for animation.
        """
        # --- Data Interpolation ---
        # Create a list of all years in the desired range
        all_years = [str(year) for year in range(time_start, time_end + 1)]
        
        # Identify original time columns that are numeric strings
        original_time_cols = [col for col in self.df.columns if col.isnumeric()]
        
        # Set index for interpolation
        df_interpolated = self.df.set_index([name_field, group_field])
        
        # Keep only the numeric time columns for interpolation
        df_interpolated = df_interpolated[original_time_cols]

        # Reindex to include all years, creating NaNs for missing years
        df_interpolated = df_interpolated.reindex(columns=all_years)
        
        # Interpolate missing values horizontally (axis=1)
        # This fills the NaNs by creating a smooth transition between existing data points
        df_interpolated = df_interpolated.interpolate(axis=1)

        # Reset index to bring back name and group fields as columns
        df_interpolated = df_interpolated.reset_index()

        # --- Data Transformation (Wide to Long) ---
        # Melt the dataframe to convert it from wide to long format
        df_long = df_interpolated.melt(
            id_vars=[name_field, group_field],
            var_name=time_field,
            value_name=value_field
        )
        # Convert time field to numeric for proper sorting
        df_long[time_field] = pd.to_numeric(df_long[time_field])
        
        # --- Color Mapping ---
        # Assign a unique color to each group
        unique_groups = df_long[group_field].unique()
        for group in unique_groups:
            # Generate a random hex color for reproducibility
            random.seed(group) # Use group name as seed
            self.colors[group] = '#%06X' % random.randint(0, 0xFFFFFF)
        
        # Map colors to each row based on its group
        df_long['color'] = df_long[group_field].map(self.colors)
        
        return df_long, value_field, time_field, name_field

    def create_bar_chart_race(self, 
                              name_field: str, 
                              group_field: str,
                              time_start: int,
                              time_end: int,
                              title: str = "Bar Chart Race",
                              output_filename: str = "bar_chart_race.gif",
                              top_n: int = 10):
        """
        Creates an animated bar chart race and saves it as a GIF.

        Args:
            name_field (str): The column name for the bars (e.g., 'country').
            group_field (str): The column name for grouping/coloring (e.g., 'continent').
            time_start (int): The starting year/period for the race.
            time_end (int): The ending year/period for the race.
            title (str): The title of the chart.
            output_filename (str): The filename for the saved GIF.
            top_n (int): The number of bars to display at any time.
        """
        # Prepare the data (this now includes interpolation)
        df_long, value_field, time_field, name_field = self._prepare_bar_chart_race_data(
            value_field='value',
            time_field='time',
            name_field=name_field,
            group_field=group_field,
            time_start=time_start,
            time_end=time_end
        )

        # --- Matplotlib Animation Setup ---
        fig, ax = plt.subplots(figsize=(15, 8), dpi=120)
        
        # This is the core animation function called for each frame
        def draw_barchart(current_time):
            ax.clear()
            
            # Get data for the current frame/time
            dff = df_long[df_long[time_field].eq(current_time)].sort_values(by=value_field, ascending=True).tail(top_n)
            dff = dff.reset_index()

            # Plot the horizontal bars
            ax.barh(dff.index, dff[value_field], color=dff['color'])

            # Add value labels to the right of the bars
            for i, (value, name) in enumerate(zip(dff[value_field], dff[name_field])):
                ax.text(value, i,     f' {name}',  ha='left',  va='center', fontsize=12, weight='bold') # Name
                ax.text(value, i,     f' {value:,.0f}  ', ha='right', va='center', fontsize=12, color='white') # Value
                
            # Add the current time as text on the plot
            ax.text(1, 0.4, current_time, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
            
            # --- Styling ---
            ax.set_yticks([]) # Hide y-axis ticks
            ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
            ax.xaxis.set_ticks_position('top')
            ax.tick_params(axis='x', colors='#777777', labelsize=12)
            plt.box(False) # Remove plot frame
            
            # Add legend
            handles = [plt.Rectangle((0,0),1,1, color=self.colors[group]) for group in self.colors]
            ax.legend(handles, self.colors.keys(), title=group_field.title())

            # Set title and axis labels
            ax.set_title(title, fontsize=22, weight='bold', pad=20)
            
            # To make the x-axis dynamic, we set the limits based on the current data
            ax.set_xlim(0, dff[value_field].max() * 1.15)

            plt.tight_layout()

        print("Generating animation... This may take a few moments.")
        
        # --- Create and Save Animation ---
        animator = animation.FuncAnimation(
            fig=fig,
            func=draw_barchart,
            frames=range(time_start, time_end + 1),
            interval=200 # milliseconds between frames
        )
        
        # Save the animation as a GIF
        # You may need to install 'Pillow'
        # pip install Pillow
        animator.save(output_filename, writer='pillow', fps=5)
        plt.close(fig)

        print(f"Success! Animation saved to '{output_filename}'")