# Weather Analysis Project

This project performs comprehensive weather data analysis and visualization using Python. It analyzes temperature and humidity patterns, creating insightful visualizations to help understand weather trends.

## Features

- Data collection and storage using SQLite database
- Temperature and humidity trend analysis
- Data visualization with matplotlib
- Automated database creation and management

## Technologies Used

- Python 3.x
- SQLite3
- Pandas
- Matplotlib
- NumPy

## Project Structure

```
weather-analysis/
│
├── create_db.py           # Database initialization script
├── weather_analysis.py    # Main analysis script
├── requirements.txt       # Project dependencies
├── humidity_plot.png      # Generated humidity visualization
└── temperature_plot.png   # Generated temperature visualization
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-analysis.git
cd weather-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. First, initialize the database:
```bash
python create_db.py
```

2. Run the analysis script:
```bash
python weather_analysis.py
```

## Results

The project generates two visualization plots:
- Temperature trends analysis
- Humidity patterns analysis

## Contributing

Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
