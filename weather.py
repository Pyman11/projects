#
# A modern weather application built with customtkinter.
# It fetches current and forecast weather data from the OpenWeatherMap API
# and presents it in a visually appealing, story-like interface.
#
# This code requires the 'customtkinter' and 'requests' libraries.
# You can install them using pip:
# pip install customtkinter
# pip install requests
#

import customtkinter as ctk
import requests
from datetime import datetime

# It's a best practice to use an environment variable for the API key.
# For this example, we'll keep the key here for simplicity.
# You should replace this with your own API key.
API_KEY = "b9504f3d4e4ce7e7c9464542c56e6c53"

class WeatherApp(ctk.CTk):
    """
    Main application class for the Weather App, inheriting from CTk.
    This class manages the GUI layout, API calls, and state of the app.
    """
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Weather Stories")
        self.geometry("400x600")
        self.resizable(False, False) # Prevent window resizing for consistent layout
        ctk.set_appearance_mode("dark")  # Set the theme to dark
        ctk.set_default_color_theme("blue")  # Set the default color theme

        # Instance variables to hold application data
        self.forecast_data = []
        self.current_page = 0

        # Create and place widgets on the window
        self._create_widgets()

    def _create_widgets(self):
        """Creates and configures all GUI widgets for the application."""
        # Main frame for the content
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title Label
        self.title_label = ctk.CTkLabel(
            main_frame,
            text="Weather Stories",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#64B5F6"
        )
        self.title_label.pack(pady=(0, 10))

        # Search Frame containing input and button
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(pady=10)

        self.city_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter a city",
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.city_entry.pack(side="left", padx=(0, 10))
        self.city_entry.bind("<Return>", self.get_weather) # Bind Enter key

        self.search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.get_weather,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.search_button.pack(side="right")

        # Story-style display box
        self.story_box = ctk.CTkFrame(
            main_frame,
            height=300,
            corner_radius=15
        )
        self.story_box.pack(pady=20, padx=10, fill="x", expand=False)
        self.story_box.pack_propagate(False) # Prevents the box from shrinking

        self.story_label = ctk.CTkLabel(
            self.story_box,
            text="🔍 Search for a city",
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="center",
            wraplength=350,
            text_color="#B0BEC5"
        )
        self.story_label.pack(expand=True)

        # Navigation Buttons Frame
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(pady=(0, 20))

        self.prev_button = ctk.CTkButton(
            nav_frame,
            text="⬅️ Prev",
            command=self.prev_page,
            state="disabled",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.prev_button.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(
            nav_frame,
            text="Next ➡️",
            command=self.next_page,
            state="disabled",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.next_button.pack(side="right", padx=10)

    def get_weather(self, event=None):
        """
        Fetches both current and forecast weather data from the API.
        This function is an event handler for the search button and the enter key.
        """
        city = self.city_entry.get().strip()
        if not city:
            self.story_label.configure(text="⚠️ Please enter a city")
            self.update_nav_buttons()
            return

        self.story_label.configure(text="Loading...")
        self.update_idletasks() # Force UI update to show "Loading..."

        try:
            # Fetch current weather
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            current_response = requests.get(current_url)
            current_response.raise_for_status()
            current_data = current_response.json()

            # Fetch 5-day forecast
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url)
            forecast_response.raise_for_status()
            forecast_data_json = forecast_response.json()

            self.forecast_data = []
            
            # Create the story for the current weather
            current_story = (
                f"🏙️ Current weather in {current_data['name']}\n\n"
                f"🌡️ {current_data['main']['temp']:.1f}°C\n"
                f"🌤️ {current_data['weather'][0]['description'].capitalize()}\n\n"
                f"💧 Humidity: {current_data['main']['humidity']}%\n"
                f"💨 Wind: {current_data['wind']['speed']:.1f} m/s"
            )
            self.forecast_data.append(current_story)

            # Create stories for the 5-day forecast
            today = datetime.now().strftime("%Y-%m-%d")
            for entry in forecast_data_json["list"]:
                timestamp = entry["dt_txt"]
                date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                
                # Check for 12:00 PM forecast for each day, excluding today
                if date.hour == 12 and date.strftime("%Y-%m-%d") != today:
                    day_name = date.strftime("%a, %d %b")
                    temp = entry["main"]["temp"]
                    desc = entry["weather"][0]["description"].capitalize()
                    humidity = entry["main"]["humidity"]
                    wind = entry["wind"]["speed"]

                    forecast_story = (
                        f"🗓️ 5-Day Forecast\n\n"
                        f"📅 {day_name}\n\n"
                        f"🌡️ {temp:.1f}°C\n"
                        f"🌤️ {desc}\n\n"
                        f"💧 Humidity: {humidity}%\n"
                        f"💨 Wind: {wind:.1f} m/s"
                    )
                    self.forecast_data.append(forecast_story)

            self.current_page = 0
            self._show_page()
            self.update_nav_buttons()

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                self.story_label.configure(text="❌ City not found.")
            else:
                self.story_label.configure(text=f"❌ API Error: {err}")
            self.forecast_data = []
            self.update_nav_buttons()
        except requests.exceptions.RequestException:
            self.story_label.configure(text="❌ A network error occurred.")
            self.forecast_data = []
            self.update_nav_buttons()
        except Exception as e:
            self.story_label.configure(text=f"❌ An unexpected error occurred: {e}")
            self.forecast_data = []
            self.update_nav_buttons()

    def _show_page(self):
        """Displays the weather information for the current page."""
        if self.forecast_data:
            self.story_label.configure(text=self.forecast_data[self.current_page])

    def update_nav_buttons(self):
        """Updates the state (enabled/disabled) of the navigation buttons."""
        if self.current_page == 0:
            self.prev_button.configure(state="disabled")
        else:
            self.prev_button.configure(state="normal")
        
        if self.current_page >= len(self.forecast_data) - 1:
            self.next_button.configure(state="disabled")
        else:
            self.next_button.configure(state="normal")

    def next_page(self):
        """Moves to the next page of the forecast."""
        if self.current_page < len(self.forecast_data) - 1:
            self.current_page += 1
            self._show_page()

    def prev_page(self):
        """Moves to the previous page of the forecast."""
        if self.current_page > 0:
            self.current_page -= 1
            self._show_page()

# Main entry point to run the application
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
