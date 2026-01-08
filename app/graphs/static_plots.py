from shiny import render
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix


def register_static_plot_outputs(input, output, session, filtered_data):
    """
    Registers static matplotlib plot rendering functions.
    Static plots are rendered server-side and sent to the client as images,
    following Shiny's server-side rendering philosophy for performance.
    """
    
    @output
    @render.plot
    def survival_chart():
        """
        Creates a basic bar chart showing the distribution of a selected variable.
        Uses matplotlib for static rendering, suitable for quick visualizations.
        """
        data = filtered_data()
        variable = input.variable()
        count = data[variable].value_counts()
        fig, ax = plt.subplots()
        ax.bar(count.index.astype(str), count.values)
        ax.set_xlabel(variable)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Distribution of {variable}")
        return fig

    @output
    @render.plot
    def advanced_distribution_chart():
        """
        Creates an advanced multi-panel visualization with histogram and boxplot.
        Demonstrates Shiny's capability to generate complex static visualizations
        that update reactively based on user input.
        """
        data = filtered_data()
        variable = input.variable()

        plt.style.use('seaborn-v0_8-darkgrid')
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        sns.histplot(data=data, x=variable, kde=True, ax=axes[0],
                    hue='Survived' if variable != 'Survived' else None)

        axes[0].set_title(f"Distribution of {variable}")
        axes[0].set_xlabel(variable)
        axes[0].set_ylabel('Frequency')

        if variable != 'Survived':
            sns.boxplot(data=data, x='Survived', y=variable, ax=axes[1])
            axes[1].set_title(f'{variable} by Survival Status')
            axes[1].set_xlabel('Survived')
            axes[1].set_ylabel(variable)
        else:
            count = data[variable].value_counts()
            axes[1].pie(count.values, labels=count.index, autopct='%1.1f%%')
            axes[1].set_title('Survival Proportion')
        
        plt.tight_layout()
        return fig

    @output
    @render.plot
    def correlation_matrix():
        """
        Renders a correlation heatmap for numeric variables.
        This visualization helps identify relationships between features,
        demonstrating Shiny's integration with seaborn for statistical graphics.
        """
        data = filtered_data()
        numeric_variables = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_variables) < 2:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'Insufficient numeric variables', 
                    ha='center', va='center', fontsize=14)
            return fig
        
        corr_matrix = data[numeric_variables].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, ax=ax, cbar_kws={'shrink': 0.8})
        ax.set_title('Correlation Matrix between Numeric Variables')
        plt.tight_layout()
        return fig

    @output
    @render.plot
    def confusion_matrix_visual():
        """
        Visualizes the confusion matrix of the machine learning model.
        This static visualization provides insights into model performance
        by showing true vs predicted classifications.
        """
        ml_data = filtered_data().copy()
        ml_data = ml_data[["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]].dropna()
        
        if len(ml_data) < 10:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center')
            return fig
        
        X = ml_data[["Pclass", "Age", "SibSp", "Parch", "Fare"]]
        y = ml_data["Survived"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        cm = confusion_matrix(y_test, y_pred)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=['Did Not Survive', 'Survived'],
                    yticklabels=['Did Not Survive', 'Survived'])
        ax.set_ylabel('True')
        ax.set_xlabel('Predicted')
        ax.set_title('Confusion Matrix')
        
        return fig

