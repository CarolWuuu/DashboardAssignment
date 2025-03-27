from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import json
import plotly

app = Flask(__name__)

# Load the CSV file once when the app starts
df = pd.read_csv("coffee_exports.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    chart_type = request.form.get("chart_type", "box")

    # Use specific columns from your CSV
    df_viz = df.rename(columns={
        'Country': 'Category',
        'Export_Tons': 'Value',
        'Region': 'Group'
    })

    # Filter out rows with missing values in key columns
    df_viz = df_viz.dropna(subset=["Category", "Value", "Group"])

    # Select chart type
    if chart_type == "bar":
        fig = px.bar(df_viz, x="Category", y="Value", color="Group", title="Coffee Exports (Tons) - Bar Chart")
    elif chart_type == "scatter":
        fig = px.scatter(df_viz, x="Category", y="Value", color="Group", title="Coffee Exports (Tons) - Scatter Plot")
    else:
        fig = px.box(df_viz, x="Category", y="Value", color="Group", title="Coffee Exports (Tons) - Box Plot")

    # Dark layout
    fig.update_layout(
        plot_bgcolor='#1a1c23',
        paper_bgcolor='#1a1c23',
        font_color='#ffffff',
        autosize=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600
    )
    fig.update_xaxes(showgrid=False, color='#cccccc')
    fig.update_yaxes(showgrid=False, color='#cccccc')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", graphJSON=graphJSON, chart_type=chart_type)

if __name__ == "__main__":
    app.run(debug=True)

