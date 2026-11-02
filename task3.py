import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import json

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌦️ Advanced Weather App")
        self.root.geometry("450x600")
        self.root.resizable(True, True)
        self.root.configure(bg='#1e1e2e')
        self.API_KEY = "14f7380047b583f6a29a54be499b5561"
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
        self.setup_styles()
        self.create_widgets()
        self.load_last_city()
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.colors = {
            'bg': '#1e1e2e',
            'card_bg': '#2d2d44',
            'accent': '#89b4fa',
            'text_primary': '#cdd6f4',
            'text_secondary': '#a6adc8',
            'success': '#a6e3a1',
            'warning': '#f9e2af',
            'error': '#f38ba8'
        }
        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text_primary'])
        self.style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground=self.colors['accent'])
        self.style.configure('Card.TFrame', background=self.colors['card_bg'], relief='raised', borderwidth=2)
        self.style.configure('Accent.TButton', font=('Arial', 12, 'bold'))
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(main_frame, text="🌦️ Advanced Weather App", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        search_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="📍 City Name:", font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.city_var = tk.StringVar()
        self.city_entry = ttk.Entry(search_frame, textvariable=self.city_var, font=('Arial', 12))
        self.city_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.city_entry.bind('<Return>', lambda e: self.get_weather())
        
        button_frame = ttk.Frame(search_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.search_btn = ttk.Button(button_frame, text="🔍 Get Weather", command=self.get_weather, style='Accent.TButton')
        self.search_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="🗑️ Clear", command=self.clear_fields).grid(row=0, column=1, padx=5)
        
        self.weather_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        self.weather_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        self.weather_frame.columnconfigure(0, weight=1)
        self.weather_frame.grid_remove()
        
        self.city_label = ttk.Label(self.weather_frame, font=('Arial', 16, 'bold'), foreground=self.colors['accent'])
        self.city_label.grid(row=0, column=0, pady=(0, 10))
        
        self.date_label = ttk.Label(self.weather_frame, font=('Arial', 10), foreground=self.colors['text_secondary'])
        self.date_label.grid(row=1, column=0, pady=(0, 20))
        
        main_weather_frame = ttk.Frame(self.weather_frame)
        main_weather_frame.grid(row=2, column=0, pady=10)
        
        self.temp_label = ttk.Label(main_weather_frame, font=('Arial', 24, 'bold'), foreground=self.colors['accent'])
        self.temp_label.grid(row=0, column=0, padx=20)
        
        ttk.Label(main_weather_frame, text="Temperature", style='Subtitle.TLabel').grid(row=1, column=0)
        
        self.weather_icon_label = ttk.Label(main_weather_frame, font=('Arial', 48))
        self.weather_icon_label.grid(row=0, column=1, padx=20)
        
        self.desc_label = ttk.Label(main_weather_frame, font=('Arial', 12, 'bold'))
        self.desc_label.grid(row=1, column=1)
        
        details_frame = ttk.Frame(self.weather_frame, style='Card.TFrame', padding="15")
        details_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=20)
        details_frame.columnconfigure(0, weight=1)
        details_frame.columnconfigure(1, weight=1)
        
        ttk.Label(details_frame, text="💧 Humidity", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W)
        self.humidity_label = ttk.Label(details_frame, font=('Arial', 12, 'bold'))
        self.humidity_label.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(details_frame, text="📊 Pressure", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.pressure_label = ttk.Label(details_frame, font=('Arial', 12, 'bold'))
        self.pressure_label.grid(row=1, column=1, sticky=tk.E, pady=8)
        
        ttk.Label(details_frame, text="💨 Wind Speed", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W)
        self.wind_label = ttk.Label(details_frame, font=('Arial', 12, 'bold'))
        self.wind_label.grid(row=2, column=1, sticky=tk.E)
        
        ttk.Label(details_frame, text="🌡️ Feels Like", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.feels_like_label = ttk.Label(details_frame, font=('Arial', 12, 'bold'))
        self.feels_like_label.grid(row=3, column=1, sticky=tk.E, pady=8)
        
        self.loading_label = ttk.Label(main_frame, text="", font=('Arial', 10))
        self.loading_label.grid(row=3, column=0)
        
        self.status_var = tk.StringVar(value="Ready - Enter a city name and click Get Weather")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, font=('Arial', 9), foreground=self.colors['text_secondary'])
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E))
    
    def get_weather_icon(self, condition_id):
        if 200 <= condition_id <= 232:
            return '⛈️'
        elif 300 <= condition_id <= 321:
            return '🌦️'
        elif 500 <= condition_id <= 531:
            return '🌧️'
        elif 600 <= condition_id <= 622:
            return '❄️'
        elif 701 <= condition_id <= 781:
            return '🌫️'
        elif condition_id == 800:
            return '☀️'
        elif 801 <= condition_id <= 804:
            return '☁️'
        else:
            return '🌈'
    
    def get_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        self.set_loading(True)
        self.status_var.set(f"Searching for weather in {city}...")
        
        try:
            params = {"q": city, "appid": self.API_KEY, "units": "metric", "lang": "en"}
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            data = response.json()
            
            if response.status_code != 200:
                error_message = data.get("message", "Unknown error occurred")
                if response.status_code == 401:
                    error_message = "Invalid API key. Please check your API configuration."
                elif response.status_code == 404:
                    error_message = f"City '{city}' not found. Please check the spelling."
                elif response.status_code == 429:
                    error_message = "API rate limit exceeded. Please try again later."
                self.show_error(error_message)
                return

            self.display_weather_data(data)
            self.save_last_city(city)
            
        except requests.exceptions.ConnectionError:
            self.show_error("Network connection error. Please check your internet connection.")
        except requests.exceptions.Timeout:
            self.show_error("Request timeout. Please try again.")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Network error: {str(e)}")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {str(e)}")
        finally:
            self.set_loading(False)
    
    def display_weather_data(self, data):
        try:
            city_name = data.get("name", "Unknown City")
            country = data.get("sys", {}).get("country", "")
            main_data = data.get("main", {})
            weather_data = data.get("weather", [{}])[0]
            wind_data = data.get("wind", {})
            
            temp = main_data.get("temp", "N/A")
            feels_like = main_data.get("feels_like", "N/A")
            humidity = main_data.get("humidity", "N/A")
            pressure = main_data.get("pressure", "N/A")
            wind_speed = wind_data.get("speed", "N/A")
            condition = weather_data.get("description", "Unknown").title()
            condition_id = weather_data.get("id", 800)
            
            location_text = f"📍 {city_name}"
            if country:
                location_text += f", {country}"
            self.city_label.config(text=location_text)
            
            self.date_label.config(text=datetime.now().strftime("%A, %B %d, %Y • %I:%M %p"))
            
            self.temp_label.config(text=f"{temp:.1f}°C" if temp != "N/A" else "N/A")
            
            icon = self.get_weather_icon(condition_id)
            self.weather_icon_label.config(text=icon)
            
            desc_text = condition
            if feels_like != "N/A":
                desc_text += f"\nFeels like: {feels_like:.1f}°C"
            self.desc_label.config(text=desc_text)
            
            self.humidity_label.config(text=f"{humidity}%" if humidity != "N/A" else "N/A")
            self.pressure_label.config(text=f"{pressure} hPa" if pressure != "N/A" else "N/A")
            self.wind_label.config(text=f"{wind_speed} m/s" if wind_speed != "N/A" else "N/A")
            self.feels_like_label.config(text=f"{feels_like:.1f}°C" if feels_like != "N/A" else "N/A")
            
            self.weather_frame.grid()
            self.status_var.set(f"Weather data loaded for {city_name} • Last updated: {datetime.now().strftime('%H:%M:%S')}")
            
            if temp != "N/A":
                self.update_temperature_color(temp)
                
        except Exception as e:
            self.show_error(f"Error displaying weather data: {str(e)}")
    
    def update_temperature_color(self, temp):
        if temp < 0:
            color = '#89b4fa'
        elif temp < 10:
            color = '#74c7ec'
        elif temp < 20:
            color = '#94e2d5'
        elif temp < 30:
            color = '#a6e3a1'
        else:
            color = '#f38ba8'
        self.temp_label.config(foreground=color)
    
    def set_loading(self, loading):
        if loading:
            self.search_btn.config(state='disabled', text="⏳ Searching...")
            self.loading_label.config(text="🔄 Fetching weather data...", foreground=self.colors['warning'])
        else:
            self.search_btn.config(state='normal', text="🔍 Get Weather")
            self.loading_label.config(text="")
    
    def show_error(self, message):
        messagebox.showerror("Weather Error", message)
        self.status_var.set(f"Error: {message}")
        self.weather_frame.grid_remove()
    
    def clear_fields(self):
        self.city_var.set("")
        self.weather_frame.grid_remove()
        self.status_var.set("Ready - Enter a city name and click Get Weather")
        self.city_entry.focus()
    
    def save_last_city(self, city):
        try:
            with open('last_city.json', 'w') as f:
                json.dump({'last_city': city}, f)
        except:
            pass
    
    def load_last_city(self):
        try:
            with open('last_city.json', 'r') as f:
                data = json.load(f)
                self.city_var.set(data.get('last_city', ''))
        except:
            pass

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
