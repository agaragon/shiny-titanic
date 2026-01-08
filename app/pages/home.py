from shiny import ui
from shinywidgets import output_widget

def create_app():
    return ui.page_sidebar(
        ui.sidebar(
            ui.h4("📊 Data Filters", class_="text-primary"),
            ui.hr(),
            ui.input_select(
                "variable", 
                "Select Variable:", 
                choices=["Survived", "Pclass", "Sex", "Embarked"],
                selected="Survived"
            ),
            ui.br(),
            ui.h6("Age Range", class_="text-muted"),
            ui.input_slider("age_min", "Minimum Age:", min=0, max=100, value=0),
            ui.input_slider("age_max", "Maximum Age:", min=0, max=100, value=100),
            width=300,
            bg="#f8f9fa",
            title=ui.h3("⚙️ Controls", class_="text-center")
        ),
        ui.page_navbar(
            ui.nav_panel(
                "📈 Overview",
                ui.layout_columns(
                    ui.value_box(
                        "Model Accuracy",
                        ui.output_ui("model_metrics"),
                        showcase=ui.span("🎯", style="font-size: 3rem;"),
                        theme="primary",
                        full_screen=True
                    ),
                    col_widths={"md": 12}
                ),
                ui.br(),
                ui.card(
                    ui.card_header("📋 Data Preview"),
                    ui.card_body(ui.output_table("statistics_table")),
                    full_screen=True
                )
            ),
            ui.nav_panel(
                "📊 Distributions",
                ui.layout_columns(
                    ui.card(
                        ui.card_header("📉 Basic Distribution"),
                        ui.card_body(ui.output_plot("survival_chart", height="400px")),
                        full_screen=True
                    ),
                    ui.card(
                        ui.card_header("📈 Advanced Distribution Analysis"),
                        ui.card_body(ui.output_plot("advanced_distribution_chart", height="400px")),
                        full_screen=True
                    ),
                    col_widths={"md": 6}
                ),
                ui.br(),
                ui.card(
                    ui.card_header("🔍 Interactive Distribution"),
                    ui.card_body(output_widget("interactive_plotly_chart")),
                    full_screen=True
                )
            ),
            ui.nav_panel(
                "🔗 Relationships",
                ui.card(
                    ui.card_header("🌐 Correlation Matrix"),
                    ui.card_body(ui.output_plot("correlation_matrix", height="500px")),
                    full_screen=True
                ),
                ui.br(),
                ui.card(
                    ui.card_header("🌍 Three-Dimensional Analysis"),
                    ui.card_body(output_widget("relationships_3d_chart")),
                    full_screen=True
                )
            ),
            ui.nav_panel(
                "🤖 Machine Learning",
                ui.layout_columns(
                    ui.card(
                        ui.card_header("📊 Confusion Matrix"),
                        ui.card_body(ui.output_plot("confusion_matrix_visual", height="400px")),
                        full_screen=True
                    ),
                    ui.card(
                        ui.card_header("📈 ROC Curve"),
                        ui.card_body(output_widget("interactive_roc_curve")),
                        full_screen=True
                    ),
                    col_widths={"md": 6}
                )
            ),
            title=ui.h2("🚢 Titanic Dataset Analysis", class_="text-center mb-0"),
            id="main_navbar"
        )
    )