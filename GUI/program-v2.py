from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout 

with suppress_stdout():

    import customtkinter
    from tkintermapview import TkinterMapView
    import requests
    from urllib.parse import quote
    import pandas as pd
    import numpy as np
    import tensorflow as tf
    from APIResponse import APIResponse 
    import datetime
    import os
    import requests_cache
    from openmeteo_requests import Client
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    from retry_requests import retry
    import pickle
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import traceback

    customtkinter.set_default_color_theme("blue")
    
    def log_error_to_file(file_path, error_message):
        with open(file_path, 'a') as file:
            file.write(error_message + '\n')

    class WeatherAPI:
        @staticmethod
        def get_forecast(lat, lon):
            base = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,sunshine_duration,relative_humidity_2m,dew_point_2m,apparent_temperature,rain,snowfall,snow_depth,pressure_msl,surface_pressure,cloud_cover,evapotranspiration,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_80m,wind_direction_80m,soil_temperature_54cm,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,global_tilted_irradiance_instant,terrestrial_radiation_instant&daily=sunshine_duration&forecast_days=16"
            response = requests.get(base)
            return response.json()

        @staticmethod
        def get_information_from_last_year(lat, lon, year):
            current_date = datetime.datetime.now() - datetime.timedelta(days=(365*year))
            last_year_date = datetime.datetime.now() - datetime.timedelta(days=365*(year+1))
            base = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={last_year_date.strftime('%Y-%m-%d')}&end_date={current_date.strftime('%Y-%m-%d')}&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,rain,snowfall,snow_depth,pressure_msl,surface_pressure,cloud_cover,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_100m,wind_direction_100m,soil_temperature_100_to_255cm,sunshine_duration,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,global_tilted_irradiance_instant,terrestrial_radiation_instant&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean,daylight_duration,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours"
            response = requests.get(base)
            return response.json()

        @staticmethod
        def get_elevation(lat, lon):
            base_url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key=AIzaSyCZ734PDZl-Yv8e710uAq7D6h-d3E9SIAE"
            response = requests.get(base_url)
            data = response.json()
            if data['status'] == 'OK':
                return data['results'][0]['elevation']
            return None
        
        @staticmethod
        def get_information_for_january_2025(lat, lon):
                start_date = "2025-01-01"
                end_date = "2025-01-31"
                base = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,rain,snowfall,snow_depth,pressure_msl,surface_pressure,cloud_cover,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_100m,wind_direction_100m,soil_temperature_100_to_255cm,sunshine_duration,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,global_tilted_irradiance_instant,terrestrial_radiation_instant&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean,daylight_duration,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours"
                response = requests.get(base)
                return response.json()

    class DataFrameBuilder:
        @staticmethod
        def add_air_values_to_futher_dataframe(lat, lon):
                try:
                    params = {
                        "latitude": lat,
                        "longitude": lon,
                        "hourly": ["pm10", "pm2_5", "nitrogen_dioxide", "ozone", "european_aqi", "european_aqi_pm2_5", "european_aqi_pm10", "european_aqi_nitrogen_dioxide", "european_aqi_ozone"],
                        "forecast_days": 5

                    }
                    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

                    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
                    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
                    openmeteo = Client(session=retry_session)
                    responses = openmeteo.weather_api(url, params=params)
                    response = responses[0]
                    hourly = response.Hourly()

                    hourly_data = {
                        "date": pd.date_range(
                            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                            freq=pd.Timedelta(seconds=hourly.Interval()),
                            inclusive="left"
                        )
                    }

                    hourly_data["pm10"] = hourly.Variables(0).ValuesAsNumpy()
                    hourly_data["pm2_5"] = hourly.Variables(1).ValuesAsNumpy()
                    hourly_data["nitrogen_dioxide"] = hourly.Variables(2).ValuesAsNumpy()
                    hourly_data["ozone"] = hourly.Variables(3).ValuesAsNumpy()
                    hourly_data["european_aqi"] = hourly.Variables(4).ValuesAsNumpy()
                    hourly_data["european_aqi_pm2_5"] = hourly.Variables(5).ValuesAsNumpy()
                    hourly_data["european_aqi_pm10"] = hourly.Variables(6).ValuesAsNumpy()
                    hourly_data["european_aqi_nitrogen_dioxide"] = hourly.Variables(7).ValuesAsNumpy()
                    hourly_data["european_aqi_ozone"] = hourly.Variables(8).ValuesAsNumpy()
                    hourly_data["Latitude"] = lat
                    hourly_data["Longitude"] = lon
                    hourly_data['hour'] = pd.to_datetime(hourly_data['date']).hour
                    hourly_data['time'] = pd.to_datetime(hourly_data['date']).time
                    hourly_data['date'] = pd.to_datetime(hourly_data['date']).date

                    hourly_dataframe = pd.DataFrame(data=hourly_data)
                    return hourly_dataframe

                except Exception as e:
                    print(f"Error: {e}")
                    return None
        @staticmethod
        def add_values_to_futher_dataframe(lat, lon):
            def retry(session, retries, backoff_factor):
                retry = Retry(
                    total=retries,
                    read=retries,
                    connect=retries,
                    backoff_factor=backoff_factor,
                    status_forcelist=(500, 502, 504),
                )
                adapter = HTTPAdapter(max_retries=retry)
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                return session

            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = Client(session=retry_session)

            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": [
                    "temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "snowfall", 
                    "snow_depth", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", 
                    "cloud_cover_mid", "cloud_cover_high", "et0_fao_evapotranspiration", 
                    "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_100m", "wind_direction_10m", 
                    "wind_direction_100m", "wind_gusts_10m", "wet_bulb_temperature_2m", 
                    "total_column_integrated_water_vapour", "is_day", "sunshine_duration", "albedo", 
                    "snow_depth_water_equivalent", "shortwave_radiation", "direct_radiation", 
                    "diffuse_radiation", "direct_normal_irradiance", "global_tilted_irradiance", 
                    "terrestrial_radiation", "shortwave_radiation_instant", "direct_radiation_instant", 
                    "diffuse_radiation_instant", "direct_normal_irradiance_instant", 
                    "global_tilted_irradiance_instant", "terrestrial_radiation_instant"
                ],
                "daily": ["sunrise", "sunset", "daylight_duration", "sunshine_duration"],
                "forecast_days": 5

            }

            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]

            hourly = response.Hourly()
            hourly_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left"
                )
            }

            for i, var in enumerate(params["hourly"]):
                hourly_data[var] = hourly.Variables(i).ValuesAsNumpy()

            hourly_data['hour'] = pd.to_datetime(hourly_data['date']).hour
            hourly_data['time'] = pd.to_datetime(hourly_data['date']).time
            hourly_data['date'] = pd.to_datetime(hourly_data['date']).date

            hourly_dataframe = pd.DataFrame(data=hourly_data)
            hourly_dataframe['Latitude'] = lat
            hourly_dataframe['Longitude'] = lon

            daily = response.Daily()
            daily_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=daily.Interval()),
                    inclusive="left"
                )
            }

            for i, var in enumerate(params["daily"]):
                daily_data[var] = daily.Variables(i).ValuesAsNumpy()

            daily_dataframe = pd.DataFrame(data=daily_data)
            daily_dataframe['Latitude'] = lat
            daily_dataframe['Longitude'] = lon
            daily_dataframe['date'] = pd.to_datetime(daily_dataframe['date']).dt.date

            merged_dataframe = pd.merge(hourly_dataframe, daily_dataframe, on="date", how="outer")

            return merged_dataframe

        @staticmethod
        def add_values_to_climatic_data_frame_from_last_year(lat, lon, year):

            def retry(session, retries, backoff_factor):
                retry = Retry(
                    total=retries,
                    read=retries,
                    connect=retries,
                    backoff_factor=backoff_factor,
                    status_forcelist=(500, 502, 504),
                )
                adapter = HTTPAdapter(max_retries=retry)
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                return session

            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = Client(session=retry_session)

            current_date = datetime.datetime.now() - datetime.timedelta(days=(365*year))
            last_year_date = datetime.datetime.now() - datetime.timedelta(days=365*(year+1))

            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": lat,
                "longitude": lon,
                "start_date": last_year_date.strftime('%Y-%m-%d'),
                "end_date": current_date.strftime('%Y-%m-%d'),
                "hourly": [
                    "temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "snowfall", "snow_depth", "pressure_msl", 
                    "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", 
                    "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_100m", 
                    "wind_direction_10m", "wind_direction_100m", "wind_gusts_10m",  
                    "wet_bulb_temperature_2m", "total_column_integrated_water_vapour", "is_day", "sunshine_duration", 
                    "albedo", "snow_depth_water_equivalent", "shortwave_radiation", "direct_radiation", "diffuse_radiation", 
                    "direct_normal_irradiance", "global_tilted_irradiance", "terrestrial_radiation", "shortwave_radiation_instant", 
                    "direct_radiation_instant", "diffuse_radiation_instant", "direct_normal_irradiance_instant", 
                    "global_tilted_irradiance_instant", "terrestrial_radiation_instant"
                ],
                "daily": ["sunrise", "sunset", "daylight_duration", "sunshine_duration"]
            }
            responses = openmeteo.weather_api(url, params=params)

            response = responses[0]

            hourly = response.Hourly()
            hourly_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left"
                )
            }

            for i, var in enumerate(params["hourly"]):
                hourly_data[var] = hourly.Variables(i).ValuesAsNumpy()
            
            hourly_data['hour'] = pd.to_datetime(hourly_data['date']).hour
            hourly_data['time'] = pd.to_datetime(hourly_data['date']).time
            hourly_data['date'] = pd.to_datetime(hourly_data['date']).date

            hourly_dataframe = pd.DataFrame(data=hourly_data)
            hourly_dataframe['Latitude'] = lat
            hourly_dataframe['Longitude'] = lon

            daily = response.Daily()
            daily_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=daily.Interval()),
                    inclusive="left"
                )
            }

            for i, var in enumerate(params["daily"]):
                daily_data[var] = daily.Variables(i).ValuesAsNumpy()

            daily_dataframe = pd.DataFrame(data=daily_data)
            daily_dataframe['Latitude'] = lat
            daily_dataframe['Longitude'] = lon
            daily_dataframe['date'] = pd.to_datetime(daily_dataframe['date']).dt.date

            merged_dataframe = pd.merge(hourly_dataframe, daily_dataframe, on="date", how="outer")

            return merged_dataframe
        @staticmethod
        def add_air_quality_to_dataframe(lat, lon, start_date, end_date):
                try:
                    params = {
                        "latitude": lat,
                        "longitude": lon,
                        "hourly": ["pm10", "pm2_5", "nitrogen_dioxide", "ozone", "european_aqi", "european_aqi_pm2_5", "european_aqi_pm10", "european_aqi_nitrogen_dioxide", "european_aqi_ozone"],
                        "start_date": start_date,
                        "end_date": end_date
                    }
                    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

                    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
                    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
                    openmeteo = Client(session=retry_session)
                    responses = openmeteo.weather_api(url, params=params)
                    response = responses[0]
                    hourly = response.Hourly()

                    hourly_data = {
                        "date": pd.date_range(
                            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                            freq=pd.Timedelta(seconds=hourly.Interval()),
                            inclusive="left"
                        )
                    }

                    hourly_data["pm10"] = hourly.Variables(0).ValuesAsNumpy()
                    hourly_data["pm2_5"] = hourly.Variables(1).ValuesAsNumpy()
                    hourly_data["nitrogen_dioxide"] = hourly.Variables(2).ValuesAsNumpy()
                    hourly_data["ozone"] = hourly.Variables(3).ValuesAsNumpy()
                    hourly_data["european_aqi"] = hourly.Variables(4).ValuesAsNumpy()
                    hourly_data["european_aqi_pm2_5"] = hourly.Variables(5).ValuesAsNumpy()
                    hourly_data["european_aqi_pm10"] = hourly.Variables(6).ValuesAsNumpy()
                    hourly_data["european_aqi_nitrogen_dioxide"] = hourly.Variables(7).ValuesAsNumpy()
                    hourly_data["european_aqi_ozone"] = hourly.Variables(8).ValuesAsNumpy()
                    hourly_data["Latitude"] = lat
                    hourly_data["Longitude"] = lon
                    hourly_data['hour'] = pd.to_datetime(hourly_data['date']).hour
                    hourly_data['time'] = pd.to_datetime(hourly_data['date']).time
                    hourly_data['date'] = pd.to_datetime(hourly_data['date']).date

                    hourly_dataframe = pd.DataFrame(data=hourly_data)
                    return hourly_dataframe

                except Exception as e:
                    print(f"Error: {e}")
                    return None
                
    class App(customtkinter.CTk):
        APP_NAME = "Предсказване на мощност от фотоволтаична система"
        WIDTH = 1080
        HEIGHT = 1920
        
        def set_icon(self):
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            self.iconbitmap(icon_path)

        
        def __init__(self, *args, **kwargs):
            try:
                super().__init__(*args, **kwargs)
                self.title(App.APP_NAME)
                self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
                self.minsize(App.WIDTH, App.HEIGHT)
                self.protocol("WM_DELETE_WINDOW", self.on_closing)
                self.bind("<Command-q>", self.on_closing)
                self.bind("<Command-w>", self.on_closing)
                self.createcommand('tk::mac::Quit', self.on_closing)
                self.marker_list = []
                self.lаt = 0
                self.lon = 0
                self.setup_ui()
                self.set_icon()        
            except Exception as e:
                error_message = traceback.format_exc()
                log_error_to_file('error_log.txt', error_message)


        def setup_ui(self):
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.frame_left = customtkinter.CTkFrame(master=self, width=250, corner_radius=0, fg_color=None)
            self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
            self.frame_left.grid_propagate(False)
            self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
            self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")
            self.setup_left_frame()
            self.setup_right_frame()

        def setup_left_frame(self):
            self.frame_left.grid_rowconfigure(7, weight=1)
            self.power_label = customtkinter.CTkLabel(self.frame_left, text="Максимална мощност (kW):", anchor="w", font=("Helvetica", 16))
            self.power_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))
            self.power_entry = customtkinter.CTkEntry(self.frame_left, font=("Helvetica", 12))
            self.power_entry.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))
            self.button_1 = customtkinter.CTkButton(master=self.frame_left, anchor="w", text="Изчисли", font=("Helvetica", 16), command=self.calculate)
            self.button_1.grid(row=2, column=0, padx=(20, 20), pady=(20, 0))
            self.power_for_the_next_16_days_label = customtkinter.CTkLabel(self.frame_left, text="", anchor="w")
            self.power_for_the_next_16_days_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
            self.power_from_last_year_label = customtkinter.CTkLabel(self.frame_left, text="", anchor="w")
            self.power_from_last_year_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 0))
            self.power_from_year_1_label = customtkinter.CTkLabel(self.frame_left, text="", anchor="w")
            self.power_from_year_1_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
            self.power_from_year_2_label = customtkinter.CTkLabel(self.frame_left, text="", anchor="w")
            self.power_from_year_2_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 0))
            self.show_predictions_button = customtkinter.CTkButton(self.frame_left, text="Покажи визуално прогнозите", anchor="w")
            self.show_predictions_button.grid_forget()
            self.map_label = customtkinter.CTkLabel(self.frame_left, text="Вид терен:", anchor="w", font=("Helvetica", 16))
            self.map_label.grid(row=8, column=0, padx=(20, 20), pady=(20, 0))
            self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"], command=self.change_map)
            self.map_option_menu.grid(row=9, column=0, padx=(20, 20), pady=(10, 0))
            self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Тема:", anchor="w", font=("Helvetica", 16))
            self.appearance_mode_label.grid(row=10, column=0, padx=(20, 20), pady=(20, 0))
            self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
            self.appearance_mode_optionemenu.grid(row=11, column=0, padx=(20, 20), pady=(10, 20))

        def setup_right_frame(self):
            self.frame_right.grid_rowconfigure(1, weight=1)
            self.frame_right.grid_rowconfigure(0, weight=0)
            self.frame_right.grid_columnconfigure(0, weight=1)
            self.frame_right.grid_columnconfigure(1, weight=0)
            self.frame_right.grid_columnconfigure(2, weight=1)
            script_directory = os.path.dirname(os.path.abspath(__file__))
            database_path = os.path.join(script_directory, "offline_tiles.db")
            self.map_widget = TkinterMapView(self.frame_right, corner_radius=0, database_path=database_path)
            self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
            self.entry = customtkinter.CTkEntry(master=self.frame_right, placeholder_text="Въведете адрес")
            self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
            self.entry.bind("<Return>", self.search_event)
            self.button_5 = customtkinter.CTkButton(master=self.frame_right, text="Търси", font=("Helvetica", 16), width=90, command=self.search_event)
            self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)
            self.coord_label = customtkinter.CTkLabel(self.frame_right, text="Координати: Няма избрани", font=("Helvetica", 16))
            self.coord_label.grid(row=0, column=2, sticky="w", padx=(12, 0), pady=12)
            self.map_widget.set_position(42.6977, 23.3219)
            self.map_option_menu.set("OpenStreetMap")
            self.appearance_mode_optionemenu.set("Dark")
            self.map_widget.add_right_click_menu_command(label="Избери координати", command=self.update_coordinates, pass_coords=True)

        def update_coordinates(self, coords):
            lat, lon = coords
            self.coord_label.configure(text=f"Координати: {lat:.6f}, {lon:.6f}")
            self.lаt = lat
            self.lon = lon

        def search_event(self, event=None):
            address = self.entry.get()
            encoded_address = quote(address)
            url = f"https://nominatim.openstreetmap.org/search?q={encoded_address}&format=jsonv2&addressdetails=1&limit=1"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = data[0]['lat']
                    lon = data[0]['lon']
                    self.map_widget.set_position(float(lat), float(lon))
                else:
                    print("Address not found")
            else:
                print(f"Error: {response.status_code}")

        def change_appearance_mode(self, new_appearance_mode: str):
            customtkinter.set_appearance_mode(new_appearance_mode)

        def change_map(self, new_map: str):
            if new_map == "OpenStreetMap":
                self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            elif new_map == "Google normal":
                self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
            elif new_map == "Google satellite":
                self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        
        def show_predictions(self, year, year1, year2):
            fig, axs = plt.subplots(3, 1, figsize=(12, 18), constrained_layout=True)
            
            date = 0
            current_date = datetime.datetime.now() - datetime.timedelta(days=(365*date))

            days = pd.date_range(start=current_date, periods=len(year), freq='D')
        
            months = pd.date_range(start=current_date, end=days[-1], freq='MS')
            tick_positions = [days.get_loc(m) for m in months]
            # First plot (2024-2025)
            axs[0].plot(year, label='2024-2025', color='tab:blue')
            axs[0].set_xlabel('Месец')
            axs[0].set_ylabel('Добита мощност (kWh)')
            axs[0].set_title('Прогнозирана мощност за периода 2024-2025')
            axs[0].legend()
            axs[0].grid(True)
            axs[0].set_xticks(tick_positions)
            axs[0].set_xticklabels([m.strftime('%m') for m in months], rotation=45, ha='right')   
            
            # Second plot (2023-2024)
            axs[1].plot(year1, label='2023-2024', color='tab:orange')
            axs[1].set_xlabel('Месец')
            axs[1].set_ylabel('Добита мощност (kWh)')
            axs[1].set_title('Прогнозирана мощност за периода 2023-2024')
            axs[1].legend()
            axs[1].grid(True)
            axs[1].set_xticks(tick_positions)
            axs[1].set_xticklabels([m.strftime('%m') for m in months], rotation=45, ha='right')   
            
            # Third plot (2022-2023)
            axs[2].plot(year2, label='2022-2023', color='tab:green')
            axs[2].set_xlabel('Месец')
            axs[2].set_ylabel('Добита мощност (kWh)')
            axs[2].set_title('Прогнозирана мощност за периода 2022-2023')
            axs[2].legend()
            axs[2].grid(True)
            axs[2].set_xticks(tick_positions)
            axs[2].set_xticklabels([m.strftime('%m') for m in months], rotation=45, ha='right')   
            
            try:
                new_window = customtkinter.CTkToplevel(self)
                new_window.title("Прогнозирана мощност")
                new_window.geometry("1920x1080")
                new_window.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico"))

                canvas = FigureCanvasTkAgg(fig, master=new_window)
                canvas.draw()
                canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=1)

                toolbar = customtkinter.CTkFrame(new_window)
                toolbar.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH)
                canvas._tkcanvas.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=1)

                new_window.update_idletasks()
                new_window.after(100, new_window.lift)  # Ensure window appears on top

            except Exception as e:
                print(f"Error creating window: {e}")

        def calculate(self):
            def invTransform(scaler, data):
                dummy = pd.DataFrame(np.zeros((len(data), scaler.n_features_in_)))
                dummy[1] = data
                dummy = pd.DataFrame(scaler.inverse_transform(dummy), columns=dummy.columns)
                return dummy[1].values
            
            script_directory = os.path.dirname(os.path.abspath(__file__))
            scaler_path = os.path.join(script_directory, 'scaler.sav')
            if not os.path.exists(scaler_path):
                raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
            min_max_scaler = pickle.load(open(scaler_path, 'rb'))

            max_power = self.power_entry.get()
            dataframe = DataFrameBuilder.add_values_to_futher_dataframe(self.lаt, self.lon)
            air_quality_data = DataFrameBuilder.add_air_values_to_futher_dataframe(self.lаt, self.lon)
            if air_quality_data is not None:
                dataframe = pd.merge(dataframe, air_quality_data, on=['date', 'hour'], how='left')
            
            eval = WeatherAPI.get_elevation(self.lаt, self.lon)

            # Process dataframe
            dataframe.insert(0, 'Substation', float(max_power))
            dataframe.insert(1, 'Power', 0)
            dataframe.insert(2, 'Elevation', eval)
            dataframe.drop(['date', 'Latitude', 'Longitude','Latitude_x','Latitude_y','Longitude_x','Longitude_y','time_x','time_y'], axis=1, inplace=True)
            dataframe.fillna(0, inplace=True, axis=1)

            # Store columns and apply min_max_scaler
            columns = dataframe.columns
            dataframe = min_max_scaler.transform(dataframe)
            dataframe = pd.DataFrame(dataframe, columns=columns)

            # Drop Power column and reshape
            dataframe.drop(['Power'], axis=1, inplace=True)
            dataframe_len = len(dataframe)
            dataframe_to_remove = dataframe_len % 24
            dataframe = dataframe.drop(dataframe.index[:dataframe_to_remove])
            dataframe = dataframe.values.reshape((int(dataframe_len/24), 24, dataframe.shape[1]))

            
        
            model_directory = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(model_directory, 'LSTM200-Dense50-Dense150-Dense150-Dense150-Dense150-Dense150-Dense150-Dense150-Dense150-Dense150-Dense50-Dense1-.h5')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            model = tf.keras.models.load_model(model_path)
            self.power_for_the_next_16_days_label.configure(text="Изчисляване...", font=("Helvetica", 16))
            self.update_idletasks()
            
        

            self.power_for_the_next_16_days_label.configure(text="Изчисляване...", font=("Helvetica", 16))
            self.update_idletasks()  # Update the GUI to show the message
            real_powers = model.predict(dataframe)
            real_powers = invTransform(min_max_scaler, real_powers)

            sum_of_real_power = 0
            for i in range(0, len(real_powers)):
                sum_of_real_power += real_powers[i]

            self.power_for_the_next_16_days_label.configure(text=f"Сума на реалната мощност\nза следващите 5 дена:\n{sum_of_real_power:.2f} kWh" , font=("Helvetica", 16))
            
            # Data from last year
            dataframe_from_the_last_year = DataFrameBuilder.add_values_to_climatic_data_frame_from_last_year(self.lаt, self.lon, 0)
            air_quality_data = DataFrameBuilder.add_air_quality_to_dataframe(self.lаt, self.lon, (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%Y-%m-%d'))
            if air_quality_data is not None:
                dataframe_from_the_last_year = pd.merge(dataframe_from_the_last_year, air_quality_data, on=['date', 'hour'], how='left')
            dataframe_from_the_last_year.insert(0, 'Substation', float(max_power))
            dataframe_from_the_last_year.insert(1, 'Power', 0)
            dataframe_from_the_last_year.insert(2, 'Elevation', eval)
            dataframe_from_the_last_year.drop(['date', 'Latitude', 'Longitude','Latitude_x','Latitude_y','Longitude_x','Longitude_y','time_x','time_y'], axis=1, inplace=True)
            dataframe_from_the_last_year.fillna(0, inplace=True, axis=1)
            columns= dataframe_from_the_last_year.columns
            dataframe_from_the_last_year = min_max_scaler.transform(dataframe_from_the_last_year)
            dataframe_from_the_last_year = pd.DataFrame(dataframe_from_the_last_year, columns=columns)


            dataframe_from_the_last_year.drop(['Power'], axis=1, inplace=True)
            dataframe_from_the_last_year_len = len(dataframe_from_the_last_year)
            dataframe_from_the_last_year_to_remove = dataframe_from_the_last_year_len % 24
            dataframe_from_the_last_year = dataframe_from_the_last_year.drop(dataframe_from_the_last_year.index[:dataframe_from_the_last_year_to_remove])
            dataframe_from_the_last_year = dataframe_from_the_last_year.values.reshape((int(dataframe_from_the_last_year_len/24), 24, dataframe_from_the_last_year.shape[1]))

            
            real_powers = model.predict(dataframe_from_the_last_year)
            real_powers = invTransform(min_max_scaler, real_powers)
            sum_of_real_power = 0
            for i in range(0, len(real_powers)):
                sum_of_real_power += real_powers[i]

            self.power_from_last_year_label.configure(text=f"Сума на реалната мощност\nот 2024 до 2025 година:\n{sum_of_real_power:.2f} kWh" , font=("Helvetica", 16))
            year = real_powers

            # Data from year 1
            dataframe_from_year_1 = DataFrameBuilder.add_values_to_climatic_data_frame_from_last_year(self.lаt, self.lon, 1)
            air_quality_data = DataFrameBuilder.add_air_quality_to_dataframe(self.lаt, self.lon, (datetime.datetime.now() - datetime.timedelta(days=365*2)).strftime('%Y-%m-%d'), (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d'))
            if air_quality_data is not None:
                dataframe_from_year_1 = pd.merge(dataframe_from_year_1, air_quality_data, on=['date', 'hour'], how='left')
            dataframe_from_year_1.insert(0, 'Substation', float(max_power))
            dataframe_from_year_1.insert(1, 'Power', 0)
            dataframe_from_year_1.insert(2, 'Elevation', eval)
            dataframe_from_year_1.drop(['date', 'Latitude', 'Longitude','Latitude_x','Latitude_y','Longitude_x','Longitude_y','time_x','time_y'], axis=1, inplace=True)
            dataframe_from_year_1.fillna(0, inplace=True, axis=1)
            columns= dataframe_from_year_1.columns
            dataframe_from_year_1 = min_max_scaler.transform(dataframe_from_year_1)
            dataframe_from_year_1 = pd.DataFrame(dataframe_from_year_1, columns=columns)

            dataframe_from_year_1.drop(['Power'], axis=1, inplace=True)
            dataframe_from_year_1_len = len(dataframe_from_year_1)
            dataframe_from_year_1_to_remove = dataframe_from_year_1_len % 24
            dataframe_from_year_1 = dataframe_from_year_1.drop(dataframe_from_year_1.index[:dataframe_from_year_1_to_remove])
            dataframe_from_year_1 = dataframe_from_year_1.values.reshape((int(dataframe_from_year_1_len/24), 24, dataframe_from_year_1.shape[1]))

            real_powers = model.predict(dataframe_from_year_1)
            real_powers = invTransform(min_max_scaler, real_powers)
            sum_of_real_power = 0
            for i in range(0, len(real_powers)):
                sum_of_real_power += real_powers[i]

            self.power_from_year_1_label.configure(text=f"Сума на реалната мощност\nот 2023 до 2024:\n{sum_of_real_power:.2f} kWh" , font=("Helvetica", 16))
            year1 = real_powers

            # Data from year 2
            dataframe_from_year_2 = DataFrameBuilder.add_values_to_climatic_data_frame_from_last_year(self.lаt, self.lon, 2)
            air_quality_data = DataFrameBuilder.add_air_quality_to_dataframe(self.lаt, self.lon, (datetime.datetime.now() - datetime.timedelta(days=365*3)).strftime('%Y-%m-%d'), (datetime.datetime.now() - datetime.timedelta(days=365*2)).strftime('%Y-%m-%d'))
            if air_quality_data is not None:
                dataframe_from_year_2 = pd.merge(dataframe_from_year_2, air_quality_data, on=['date', 'hour'], how='left')
            dataframe_from_year_2.insert(0, 'Substation', float(max_power))
            dataframe_from_year_2.insert(1, 'Power', 0)
            dataframe_from_year_2.insert(2, 'Elevation', eval)
            dataframe_from_year_2.drop(['date', 'Latitude', 'Longitude','Latitude_x','Latitude_y','Longitude_x','Longitude_y','time_x','time_y'], axis=1, inplace=True)
            dataframe_from_year_2.fillna(0, inplace=True, axis=1)
            columns= dataframe_from_year_2.columns
            dataframe_from_year_2 = min_max_scaler.transform(dataframe_from_year_2)
            dataframe_from_year_2 = pd.DataFrame(dataframe_from_year_2, columns=columns)

            dataframe_from_year_2.drop(['Power'], axis=1, inplace=True)
            dataframe_from_year_2_len = len(dataframe_from_year_2)
            dataframe_from_year_2_to_remove = dataframe_from_year_2_len % 24
            dataframe_from_year_2 = dataframe_from_year_2.drop(dataframe_from_year_2.index[:dataframe_from_year_2_to_remove])
            dataframe_from_year_2 = dataframe_from_year_2.values.reshape((int(dataframe_from_year_2_len/24), 24, dataframe_from_year_2.shape[1]))

            real_powers = model.predict(dataframe_from_year_2)
            real_powers = invTransform(min_max_scaler, real_powers)
            sum_of_real_power = 0
            for i in range(0, len(real_powers)):
                sum_of_real_power += real_powers[i]

            self.power_from_year_2_label.configure(text=f"Сума на реалната мощност\nот 2022 до 2023:\n{sum_of_real_power:.2f} kWh" , font=("Helvetica", 16))
            year2 = real_powers

            self.show_predictions_button.configure(command=lambda: self.show_predictions(year, year1, year2))
            self.show_predictions_button.grid(row=7, column=0, padx=(20, 20), pady=(20, 0))

        def on_closing(self, event=0):
            self.destroy()

        def start(self):
            self.mainloop()

    

    if __name__ == "__main__":
        try:
            app = App()
            app.start()
        except Exception as e:
            error_message = f"[{datetime.datetime.now()}] Error in main:\n{traceback.format_exc()}\n"
            print(f"Critical error: {str(e)}")
            try:
                log_error_to_file('error_log.txt', error_message)
            except Exception as log_error:
                print(f"Failed to log error: {str(log_error)}")

