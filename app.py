from flask import Flask, render_template, request
import pytz
from timezone_converter import convert_time_range

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error = None
    common_timezones = sorted(pytz.common_timezones)

    # Get form values for preservation
    from_tz = request.form.get('from_timezone') if request.method == 'POST' else None
    start = request.form.get('start_datetime') if request.method == 'POST' else None
    end = request.form.get('end_datetime') if request.method == 'POST' else None
    to_tzs = request.form.getlist('to_timezones') if request.method == 'POST' else []

    if request.method == 'POST':
        if not all([start, end, from_tz]) or not to_tzs:
            error = "All fields are required"
        else:
            try:
                results = convert_time_range(start, end, from_tz, to_tzs)
            except ValueError as e:
                error = str(e)

    return render_template('index.html', results=results, error=error, common_timezones=common_timezones, from_tz=from_tz, start=start, end=end, to_tzs=to_tzs)

if __name__ == '__main__':
    app.run(debug=True)
