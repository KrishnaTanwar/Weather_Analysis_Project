import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from datetime import datetime

class WeatherDataAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherstack.com/current"
        
    def celsius_to_fahrenheit(self, celsius):
        return (celsius * 9/5) + 32
    
    def fetch_weather_data(self, cities):
        weather_data = []
        
        for city in cities:
            params = {
                'access_key': self.api_key,
                'query': city
            }
            
            try:
                response = requests.get(self.base_url, params=params)
                data = response.json()
                
                if 'current' in data:
                    current = data['current']
                    weather_data.append({
                        'City': city,
                        'Temperature': self.celsius_to_fahrenheit(current['temperature']),
                        'Feels_Like': self.celsius_to_fahrenheit(current['feelslike']),
                        'Humidity': current['humidity']
                    })
                else:
                    print(f"Error fetching data for {city}: {data.get('error', 'Unknown error')}")
            
            except Exception as e:
                print(f"Error fetching data for {city}: {str(e)}")
        
        return pd.DataFrame(weather_data)

    def store_to_database(self, df):
        # PostgreSQL connection parameters
        conn_params = {
            'dbname': 'weatherdb',
            'user': 'postgres',
            'password': 'admin',
            'host': 'localhost',
            'port': '5432'
        }
        
        try:
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    city VARCHAR(100),
                    temperature FLOAT,
                    feels_like FLOAT,
                    humidity INTEGER
                )
            """)
            
            # Clear existing data
            cursor.execute("DELETE FROM weather_data")
            
            # Insert new data
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO weather_data (city, temperature, feels_like, humidity)
                    VALUES (%s, %s, %s, %s)
                """, (row['City'], row['Temperature'], row['Feels_Like'], row['Humidity']))
            
            conn.commit()
            print("Data successfully stored in database")
            
        except Exception as e:
            print(f"Database error: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def create_temperature_plot(self, df):
        plt.figure(figsize=(12, 6))
        
        x = range(len(df['City']))
        width = 0.35
        
        plt.bar(x, df['Temperature'], width, label='Temperature', color='skyblue')
        plt.bar([i + width for i in x], df['Feels_Like'], width, label='Feels Like', color='lightcoral')
        
        plt.xlabel('Cities')
        plt.ylabel('Temperature (°F)')
        plt.title('Temperature and Feels Like Temperature by City')
        plt.xticks([i + width/2 for i in x], df['City'], rotation=45)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('temperature_plot.png')
        plt.close()

    def create_humidity_plot(self, df):
        plt.figure(figsize=(10, 6))
        
        sns.barplot(x='City', y='Humidity', data=df, color='lightgreen')
        
        plt.xlabel('Cities')
        plt.ylabel('Humidity (%)')
        plt.title('Humidity by City')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('humidity_plot.png')
        plt.close()

def main():
    # Your WeatherStack API key
    api_key = "7904f6c3e0b537eedd215893399ec6c7"
    
    # List of cities to analyze
    cities = ['London', 'Paris', 'New York', 'Tokyo', 'Mumbai']
    
    # Create analyzer instance
    analyzer = WeatherDataAnalyzer(api_key)
    
    # Fetch and process data
    df = analyzer.fetch_weather_data(cities)
    
    # Store data in database
    analyzer.store_to_database(df)
    
    # Create visualizations
    analyzer.create_temperature_plot(df)
    analyzer.create_humidity_plot(df)
    
    print("Analysis complete! Check temperature_plot.png and humidity_plot.png for visualizations.")

if __name__ == "__main__":
    main()
