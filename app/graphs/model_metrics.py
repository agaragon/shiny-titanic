from shiny import render, ui
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def register_model_metrics_outputs(input, output, session, filtered_data):
    """
    Registers UI output functions for machine learning model metrics.
    UI outputs in Shiny are rendered using @render.ui, which allows for
    rich HTML formatting and is ideal for displaying computed metrics
    in value boxes and other styled components, following Shiny's
    philosophy of flexible output rendering.
    """
    
    @output
    @render.ui
    def model_metrics():
        """
        Computes and displays machine learning model accuracy metrics as HTML.
        This demonstrates Shiny's reactive evaluation and UI rendering capabilities,
        where model metrics automatically recalculate when the underlying filtered
        data changes, enabling real-time model performance assessment with
        visually appealing formatting suitable for value boxes.
        """
        ml_data = filtered_data().copy()
        
        ml_data = ml_data[["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]].dropna()
        
        if len(ml_data) < 10:
            return ui.span("Insufficient data", class_="text-muted")
        
        X = ml_data[["Pclass", "Age", "SibSp", "Parch", "Fare"]]
        y = ml_data["Survived"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        return ui.span(f"{accuracy:.1%}", style="font-size: 2.5rem; font-weight: bold;")

