from shiny import render
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def register_model_metrics_outputs(input, output, session, filtered_data):
    """
    Registers text output functions for machine learning model metrics.
    Text outputs in Shiny are rendered using @render.text, which is ideal
    for displaying computed metrics and statistics that update reactively.
    """
    
    @output
    @render.text
    def model_metrics():
        """
        Computes and displays machine learning model accuracy metrics.
        This demonstrates Shiny's reactive evaluation, where model metrics
        automatically recalculate when the underlying filtered data changes,
        enabling real-time model performance assessment.
        """
        ml_data = filtered_data().copy()
        
        ml_data = ml_data[["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]].dropna()
        
        if len(ml_data) < 10:
            return "Insufficient data to train the model. Adjust the filters."
        
        X = ml_data[["Pclass", "Age", "SibSp", "Parch", "Fare"]]
        y = ml_data["Survived"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        return f"Model accuracy: {accuracy:.4f} ({len(X_test)} test samples)"

