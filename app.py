import dash
from dash import html, dcc, Input, Output, State,dash_table
import json
from ai import chat_session  # Import your API module
from flask import Flask

# Create the Dash app
server = Flask(__name__)
app = dash.Dash(server=server)

app.title = "Trip Planner"

# Layout
app.layout = html.Div([
    html.H1("Trip Planner", style={"text-align": "center"}),

    html.Div([
        html.Label("Enter unstructured trip data:"),
        dcc.Textarea(
            id="input-text",
            placeholder="Enter trip description...",
            style={"width": "100%", "height": 200}
        ),
    ], style={"padding": "10px"}),

    html.Button("Submit", id="submit-button", n_clicks=0, style={"margin-top": "10px"}),

    html.Div(id="output-table", style={"margin-top": "20px"}),
])

# Callback to handle API calls and display results
@app.callback(
    Output("output-table", "children"),
    Input("submit-button", "n_clicks"),
    State("input-text", "value"),
)
def process_input(n_clicks, text):
    if n_clicks > 0 and text:
        try:
            # Send the input to the API and get structured data
            response = chat_session.send_message(text)  # Call the API
            structured_data = json.loads(response.text)

            # Prepare the data for the table
            activities = structured_data.get("activity", [])
            best_seasons = structured_data.get("best-season", [])
            times = [
                f"{item['time'][0]}" if item["time"] else "N/A"
                for item in structured_data.get("amount-of-time", [])
            ]

            # Convert to tabular format
            table_data = [
                {"Activity": activity, "Best Season": season, "Time Required": time}
                for activity, season, time in zip(activities, best_seasons, times)
            ]

            # Return a Dash DataTable
            return dash_table.DataTable(
                columns=[
                    {"name": "Activity", "id": "Activity"},
                    {"name": "Best Season", "id": "Best Season"},
                    {"name": "Time Required", "id": "Time Required"},
                ],
                data=table_data,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "padding": "5px"},
                style_header={
                    "backgroundColor": "lightgrey",
                    "fontWeight": "bold"
                },
            )
        except Exception as e:
            return html.Div(f"Error: {str(e)}", style={"color": "red"})
    return html.Div("Enter data and click Submit.")

# Run the Dash app
if __name__ == "__main__":
    print("Dash app is running at http://127.0.0.1:8000/")
    app.run_server(host="0.0.0.0",port=8000,debug=True)