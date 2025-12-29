# Time Zone Conversion App

A simple web application for converting time ranges across different time zones.

## Features

- Select a source timezone and datetime range
- Choose multiple target timezones for conversion
- Automatic detection of user's local timezone
- Responsive design with Bootstrap
- Native HTML form validation
- Handles daylight saving time transitions correctly
- Preserves form inputs after submission

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. The "From Timezone" field is pre-filled with your current timezone
2. Set the start and end date/time (defaults to next hour and hour after)
3. Add target timezones by typing or selecting from the dropdown
4. Click "Convert" to see the time range in all selected timezones
5. Form inputs are preserved if there are errors or for easy adjustments

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Project Structure

```
tzapp/
├── app.py                 # Main Flask application
├── timezone_converter.py  # Timezone conversion logic
├── templates/
│   └── index.html         # Main page template
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles (if needed)
│   └── js/
│       └── app.js         # Minimal JavaScript
├── tests/
│   ├── test_app.py        # Integration tests
│   └── test_timezone_converter.py  # Unit tests
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, Bootstrap 5, minimal vanilla JavaScript
- **Timezone Handling**: pytz library
- **Testing**: pytest

## License

This project is open source. Feel free to use and modify as needed.
