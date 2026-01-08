# Titanic Dataset Analysis - Shiny Application

A modular Shiny web application for exploratory data analysis and machine learning model evaluation of the Titanic dataset.

## Architecture

This project follows a modular architecture aligned with Shiny's philosophy of separation of concerns, where distinct responsibilities are organized into specialized modules for enhanced maintainability and code clarity.

### Project Structure

```
titanic/
├── app/
│   ├── entry_point.py          # Application entry point and server orchestration
│   ├── data/
│   │   └── titanic_data.csv    # Dataset
│   ├── pages/
│   │   └── home.py             # UI definition
│   └── graphs/
│       ├── __init__.py
│       ├── reactive.py          # Reactive calculations and data filtering
│       ├── tables.py            # Table output renderers
│       ├── static_plots.py      # Static visualization outputs (matplotlib/seaborn)
│       ├── interactive_plots.py # Interactive visualization outputs (Plotly)
│       └── model_metrics.py     # Machine learning model evaluation metrics
├── requirements.txt             # Python dependencies
└── makefile                     # Build automation
```

### Architecture Overview

**Entry Point (`app/entry_point.py`)**
- Loads the dataset and initializes the Shiny application
- Orchestrates the registration of all reactive functions and output renderers
- Demonstrates the composition root pattern, centralizing dependency wiring

**UI Layer (`app/pages/home.py`)**
- Defines the application interface using Shiny's UI components
- Implements a sidebar layout with filters and main content area
- Exposes output placeholders for tables, plots, and widgets

**Business Logic Layer (`app/graphs/`)**
The graphs module is organized by output type, each handling a specific visualization or calculation concern:

- **`reactive.py`**: Implements reactive calculations that automatically update when user inputs change. Uses Shiny's `@reactive.calc` decorator to create reactive data pipelines, filtering the dataset based on age range and preparing machine learning datasets for model training.

- **`tables.py`**: Handles table output rendering, transforming filtered data into formatted statistical summaries.

- **`static_plots.py`**: Generates static visualizations using matplotlib and seaborn, including distribution charts, correlation matrices, and confusion matrices.

- **`interactive_plots.py`**: Creates interactive Plotly visualizations, enabling user exploration through zooming, panning, and hover interactions.

- **`model_metrics.py`**: Trains machine learning models (e.g., logistic regression) and computes evaluation metrics, including ROC curves and confusion matrix visualizations.

This modular design facilitates:
- **Maintainability**: Each module has a single, well-defined responsibility
- **Testability**: Components can be tested in isolation
- **Reusability**: Modules can be easily extended or modified without affecting others
- **Clarity**: The codebase structure clearly communicates its organization

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. Clone or navigate to the project directory:
```bash
cd /path/to/titanic
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Using Make (recommended)

```bash
make start
```

This command runs `shiny run --reload app/entry_point.py`, which starts the development server with auto-reload enabled.

### Using Shiny directly

```bash
shiny run --reload app/entry_point.py
```

The application will be available at `http://127.0.0.1:8000` by default.

### Auto-reload

The `--reload` flag enables automatic application reloading when source files change, facilitating rapid development cycles.

## Features

- **Interactive Filtering**: Filter passengers by age range and analyze selected variables
- **Descriptive Statistics**: View statistical summaries of the filtered dataset
- **Visualizations**: 
  - Static charts (survival distribution, advanced distributions, correlation matrices)
  - Interactive Plotly charts for exploratory analysis
  - 3D relationship visualizations
- **Machine Learning**: Train logistic regression models and evaluate performance through:
  - Model metrics display
  - Confusion matrix visualization
  - Interactive ROC curve analysis

