from shiny import App
import pandas as pd

from pages.home import create_app
from graphs.reactive import register_reactive_calculations
from graphs.tables import register_table_outputs
from graphs.static_plots import register_static_plot_outputs
from graphs.interactive_plots import register_interactive_plot_outputs
from graphs.model_metrics import register_model_metrics_outputs


app_ui = create_app()

df = pd.read_csv('app/data/titanic_data.csv')

def server(input, output, session):
    """
    Server function that orchestrates the registration of all reactive functions
    and output renderers. This modular approach follows Shiny's philosophy of
    separation of concerns, where different types of visualizations and calculations
    are organized into specialized modules, enhancing maintainability and code clarity.
    """
    filtered_data, _ = register_reactive_calculations(input, output, session, df)
    
    register_table_outputs(input, output, session, filtered_data)
    register_static_plot_outputs(input, output, session, filtered_data)
    register_interactive_plot_outputs(input, output, session, filtered_data)
    register_model_metrics_outputs(input, output, session, filtered_data)

app = App(app_ui, server)

