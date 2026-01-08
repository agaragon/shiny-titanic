from shiny import reactive
import pandas as pd
from sklearn.model_selection import train_test_split


def register_reactive_calculations(input, output, session, df):
    """
    Registers reactive calculations that depend on user input.
    This approach follows Shiny's reactive programming paradigm, where
    calculations automatically update when their dependencies change.
    """
    
    @reactive.calc
    def filtered_data():
        """
        Reactive calculation that filters the dataframe based on age range.
        The @reactive.calc decorator ensures this function recalculates
        automatically when input.age_min() or input.age_max() changes.
        """
        filtered_df = df[
            (df["Age"] >= input.age_min()) &
            (df["Age"] <= input.age_max())
        ]
        return filtered_df

    @reactive.calc
    def prepared_ml_data():
        """
        Reactive calculation that prepares machine learning datasets.
        Returns train/test splits ready for model training and evaluation.
        """
        data = filtered_data().copy()
        ml_data = data[["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]].dropna()
        
        if len(ml_data) < 10:
            return None
        
        X = ml_data[["Pclass", "Age", "SibSp", "Parch", "Fare"]]
        y = ml_data["Survived"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        return {
            'X_train': X_train, 'X_test': X_test,
            'y_train': y_train, 'y_test': y_test
        }
    
    return filtered_data, prepared_ml_data

