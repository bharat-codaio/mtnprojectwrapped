from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    data = {}
    return render_template('index.html', data=data)

@app.route('/upload', methods=['POST'])
def upload():
    data = None
    uploaded_file = request.files['csvFile']
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
    else:
        url = request.form["profileURL"]
        if request.form["profileURL"][-1] != "/":
            url = url + "/"
        url = url + "tick-export"
        data = pd.read_csv(url)
    this_year = data[(data['Date'] >= '2024-01-01')]
    routes = this_year.Route.nunique()
    locations = this_year.Location.nunique()
    max_crag = "Not enough data :("
    if (locations > 0 ):
        full_path = this_year.groupby(['Location'])['Location'].count().idxmax()
        path_parts = full_path.split('>')
        max_crag = path_parts[-1].strip()

    max_type = "Not enough data :("
    max_route = "Not enough data :("
    if (routes > 0):
        max_type = this_year.groupby(['Route Type'])['Route Type'].count().idxmax()
        max_route = this_year['Route'][this_year['Your Stars'].idxmax()]
    number_days = this_year['Date'].nunique()
    climbing_style = max_type.lower() if max_type != "Not enough data :(" else "sport"
    return render_template('data.html', routes=routes, locations=locations, max_crag=max_crag, max_type=max_type, max_route=max_route, number_days=number_days, climbing_style=climbing_style)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
