from shinywidgets import render_widget
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc


def register_interactive_plot_outputs(input, output, session, filtered_data):
    """
    Registers interactive Plotly widget rendering functions.
    Interactive plots leverage client-side rendering capabilities through
    shinywidgets, enabling user interactions like zooming and hovering
    without server roundtrips, following Shiny's widget extension philosophy.
    """
    
    @output
    @render_widget
    def interactive_plotly_chart():
        """
        Creates an interactive Plotly histogram or bar chart.
        The @render_widget decorator enables client-side interactivity,
        allowing users to explore data through zoom, pan, and hover actions.
        """
        data = filtered_data()
        variable = input.variable()
        
        if data[variable].dtype in ['int64', 'float64']:
            fig = px.histogram(data, x=variable, color='Survived' if 'Survived' in data.columns else None,
                            nbins=30, title=f'Interactive Distribution of {variable}',
                            labels={variable: variable, 'count': 'Frequency'})
        else:
            count = data[variable].value_counts()
            fig = px.bar(x=count.index.astype(str), y=count.values,
                        title=f'Distribution of {variable}',
                        labels={'x': variable, 'y': 'Frequency'})
        
        fig.update_layout(
            template='plotly_white',
            hovermode='closest',
            height=500
        )
        
        return fig

    @output
    @render_widget
    def relationships_3d_chart():
        """
        Creates an interactive 3D scatter plot visualizing multi-dimensional relationships.
        This demonstrates Shiny's ability to render complex interactive visualizations
        that enable spatial data exploration through Plotly's 3D capabilities.
        """
        data = filtered_data()
        
        valid_data = data[['Age', 'Fare', 'Pclass', 'Survived']].dropna()
        
        if len(valid_data) < 10:
            return px.scatter(title='Insufficient data for 3D visualization')
        
        fig = px.scatter_3d(
            valid_data,
            x='Age',
            y='Fare',
            z='Pclass',
            color='Survived',
            size='Survived',
            title='Three-Dimensional Relationship: Age, Fare and Class',
            labels={'Age': 'Age', 'Fare': 'Fare', 'Pclass': 'Class'},
            hover_data=['Age', 'Fare', 'Pclass']
        )
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Age',
                yaxis_title='Fare',
                zaxis_title='Class',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            height=600
        )
        
        return fig

    @output
    @render_widget
    def interactive_roc_curve():
        """
        Creates an interactive ROC curve visualization for model evaluation.
        The interactive nature allows users to examine the curve at different
        threshold points, demonstrating Shiny's integration with ML evaluation metrics.
        """
        ml_data = filtered_data().copy()
        ml_data = ml_data[["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]].dropna()
        
        if len(ml_data) < 10:
            return px.scatter(title='Insufficient data')
        
        X = ml_data[["Pclass", "Age", "SibSp", "Parch", "Fare"]]
        y = ml_data["Survived"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            name=f'ROC (AUC = {roc_auc:.3f})',
            line=dict(width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode='lines',
            name='Random (AUC = 0.500)',
            line=dict(dash='dash', color='red')
        ))
        
        fig.update_layout(
            title='ROC Curve - Receiver Operating Characteristic',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            template='plotly_white',
            height=500,
            hovermode='closest'
        )
        
        return fig

