from shiny import ui
from shinywidgets import output_widget

def create_app():
    return ui.page_sidebar(
        ui.sidebar(
            ui.h3("Filters"),
            ui.input_select("variable", "Select variable:", choices=["Survived", "Pclass", "Sex", "Embarked"]),
            ui.input_slider("age_min", "Minimum age:", min=0, max=100, value=0),
            ui.input_slider("age_max", "Maximum age:", min=0, max=100, value=100),
            title="Controls",
        ),
        ui.h1("Titanic Dataset Analysis"),
        ui.h2("Descriptive Statistics"),
        ui.output_table("statistics_table"),

        ui.h2("Survival Distribution"),
        ui.output_plot("survival_chart"),
        
        ui.h2("Advanced Distribution"),
        ui.output_plot("advanced_distribution_chart"),
        
        ui.h2("Correlation Matrix"),
        ui.output_plot("correlation_matrix"),

        ui.h2("Interactive Plotly Chart"),
        output_widget("interactive_plotly_chart"),
        
        ui.h2("Three-Dimensional Analysis"),
        output_widget("relationships_3d_chart"),
        
        ui.h2("Machine Learning Model"),
        ui.output_text("model_metrics"),
        
        ui.h2("Confusion Matrix"),
        ui.output_plot("confusion_matrix_visual"),
        
        ui.h2("ROC Curve"),
        output_widget("interactive_roc_curve")
    )