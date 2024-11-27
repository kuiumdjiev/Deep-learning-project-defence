import tkinter as tk
from tkinter import ttk

from tkintermapview import TkinterMapView
import requests
import pandas as pd
import numpy as np
import tensorflow as tf
from APIResponse import APIResponse 
import datetime

def get_forecast(lat , lon):
    
    base= f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,sunshine_duration,relative_humidity_2m,dew_point_2m,apparent_temperature,rain,snowfall,snow_depth,pressure_msl,surface_pressure,cloud_cover,evapotranspiration,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_80m,wind_direction_80m,soil_temperature_54cm,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,global_tilted_irradiance_instant,terrestrial_radiation_instant&daily=sunshine_duration&forecast_days=16"
    response = requests.get(base)
    data = response.json()
    return data

def get_information_from_last_year(lat , lon):
    current_date = datetime.datetime.now()
    last_year_date = datetime.datetime.now() - datetime.timedelta(days=365)
     
    base= f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={last_year_date.strftime('%Y-%m-%d')}&end_date={current_date.strftime('%Y-%m-%d')}&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,rain,snowfall,snow_depth,pressure_msl,surface_pressure,cloud_cover,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_100m,wind_direction_100m,soil_temperature_100_to_255cm,sunshine_duration,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,global_tilted_irradiance_instant,terrestrial_radiation_instant&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean,daylight_duration,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours"
    response = requests.get(base)
    data = response.json()
    return data

def get_elevation(lat, lon):
        base_url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key=AIzaSyCZ734PDZl-Yv8e710uAq7D6h-d3E9SIAE"
        response = requests.get(base_url)
        data = response.json()
        if data['status'] == 'OK':
            elevation = data['results'][0]['elevation']
            return elevation
    
def add_values_to_futher_dataframe(lat , lon):
        api_information= get_forecast(lat,lon)
        instance = APIResponse(api_information)
        climatic_data_frame = pd.DataFrame()

        for j in np.arange(0, len(instance.hourly['time'])):
            frame = pd.DataFrame()
            frame.loc[0,'Latitude'] = lat
            frame.loc[0,'Longitude'] = lon
            frame.loc[0,'date'] = instance.hourly['time'][j].split('T')[0]
            frame.loc[0,'time'] = instance.hourly['time'][j].split('T')[1] + ':00'
            frame.loc[0,'Temperature'] = instance.hourly['temperature_2m'][j]
            frame.loc[0,'Humidity'] = instance.hourly['relative_humidity_2m'][j]
            frame.loc[0,'Dew Point'] = instance.hourly['dew_point_2m'][j]
            frame.loc[0,'Apparent Temperature'] = instance.hourly['apparent_temperature'][j]
            frame.loc[0,'Rain'] = instance.hourly['rain'][j]
            frame.loc[0,'Snowfall'] = instance.hourly['snowfall'][j]
            frame.loc[0,'Snow Depth'] = instance.hourly['snow_depth'][j]
            frame.loc[0,'Pressure MSL'] = instance.hourly['pressure_msl'][j]
            frame.loc[0,'Surface Pressure'] = instance.hourly['surface_pressure'][j]
            frame.loc[0,'Cloud Cover'] = instance.hourly['cloud_cover'][j]
            frame.loc[0,'ET0 FAO Evapotranspiration'] = instance.hourly['et0_fao_evapotranspiration'][j]
            frame.loc[0,'Vapour Pressure Deficit'] = instance.hourly['vapour_pressure_deficit'][j]
            frame.loc[0,'Wind Speed'] = instance.hourly['wind_speed_80m'][j]
            frame.loc[0,'Wind Direction'] = instance.hourly['wind_direction_80m'][j]
            frame.loc[0,'Soil Temperature'] = instance.hourly['soil_temperature_54cm'][j]
            frame.loc[0,'Sunshine Duration'] = instance.hourly['sunshine_duration'][j]
            frame.loc[0,'Shortwave Radiation'] = instance.hourly['shortwave_radiation'][j]
            frame.loc[0,'Direct Radiation'] = instance.hourly['direct_radiation'][j]
            frame.loc[0,'Diffuse Radiation'] = instance.hourly['diffuse_radiation'][j]
            frame.loc[0,'Direct Normal Irradiance'] = instance.hourly['direct_normal_irradiance'][j]
            frame.loc[0,'Global Tilted Irradiance'] = instance.hourly['global_tilted_irradiance'][j]
            frame.loc[0,'Terrestrial Radiation'] = instance.hourly['terrestrial_radiation'][j]
            frame.loc[0,'Shortwave Radiation Instant'] = instance.hourly['shortwave_radiation_instant'][j]
            frame.loc[0,'Direct Radiation Instant'] = instance.hourly['direct_radiation_instant'][j]
            frame.loc[0,'Diffuse Radiation Instant'] = instance.hourly['diffuse_radiation_instant'][j]
            frame.loc[0,'Direct Normal Irradiance Instant'] = instance.hourly['direct_normal_irradiance_instant'][j]
            frame.loc[0,'Global Tilted Irradiance Instant'] = instance.hourly['global_tilted_irradiance_instant'][j]
            frame.loc[0,'Terrestrial Radiation Instant'] = instance.hourly['terrestrial_radiation_instant'][j]
            frame.loc[0,'hour'] = int(frame.loc[0,'time'].split(':')[0])
            climatic_data_frame = pd.concat([climatic_data_frame, frame], ignore_index=True)
        return climatic_data_frame

def add_values_to_climatic_data_frame_from_last_year(lat , lon):
    api_information= get_information_from_last_year(lat,lon)
    instance = APIResponse(api_information)
    climatic_data_frame = pd.DataFrame()

    for j in np.arange(0, len(instance.hourly['time'])):
        frame = pd.DataFrame()
        frame.loc[0,'Latitude'] = lat
        frame.loc[0,'Longitude'] = lon
        frame.loc[0,'date'] = instance.hourly['time'][j].split('T')[0]
        frame.loc[0,'time'] = instance.hourly['time'][j].split('T')[1] + ':00'
        frame.loc[0,'Temperature'] = instance.hourly['temperature_2m'][j]
        frame.loc[0,'Humidity'] = instance.hourly['relative_humidity_2m'][j]
        frame.loc[0,'Dew Point'] = instance.hourly['dew_point_2m'][j]
        frame.loc[0,'Apparent Temperature'] = instance.hourly['apparent_temperature'][j]
        frame.loc[0,'Rain'] = instance.hourly['rain'][j]
        frame.loc[0,'Snowfall'] = instance.hourly['snowfall'][j]
        frame.loc[0,'Snow Depth'] = instance.hourly['snow_depth'][j]
        frame.loc[0,'Pressure MSL'] = instance.hourly['pressure_msl'][j]
        frame.loc[0,'Surface Pressure'] = instance.hourly['surface_pressure'][j]
        frame.loc[0,'Cloud Cover'] = instance.hourly['cloud_cover'][j]
        frame.loc[0,'ET0 FAO Evapotranspiration'] = instance.hourly['et0_fao_evapotranspiration'][j]
        frame.loc[0,'Vapour Pressure Deficit'] = instance.hourly['vapour_pressure_deficit'][j]
        frame.loc[0,'Wind Speed'] = instance.hourly['wind_speed_100m'][j]
        frame.loc[0,'Wind Direction'] = instance.hourly['wind_direction_100m'][j]
        frame.loc[0,'Soil Temperature'] = instance.hourly['soil_temperature_100_to_255cm'][j]
        frame.loc[0,'Sunshine Duration'] = instance.hourly['sunshine_duration'][j]
        frame.loc[0,'Shortwave Radiation'] = instance.hourly['shortwave_radiation'][j]
        frame.loc[0,'Direct Radiation'] = instance.hourly['direct_radiation'][j]
        frame.loc[0,'Diffuse Radiation'] = instance.hourly['diffuse_radiation'][j]
        frame.loc[0,'Direct Normal Irradiance'] = instance.hourly['direct_normal_irradiance'][j]
        frame.loc[0,'Global Tilted Irradiance'] = instance.hourly['global_tilted_irradiance'][j]
        frame.loc[0,'Terrestrial Radiation'] = instance.hourly['terrestrial_radiation'][j]
        frame.loc[0,'Shortwave Radiation Instant'] = instance.hourly['shortwave_radiation_instant'][j]
        frame.loc[0,'Direct Radiation Instant'] = instance.hourly['direct_radiation_instant'][j]
        frame.loc[0,'Diffuse Radiation Instant'] = instance.hourly['diffuse_radiation_instant'][j]
        frame.loc[0,'Direct Normal Irradiance Instant'] = instance.hourly['direct_normal_irradiance_instant'][j]
        frame.loc[0,'Global Tilted Irradiance Instant'] = instance.hourly['global_tilted_irradiance_instant'][j]
        frame.loc[0,'Terrestrial Radiation Instant'] = instance.hourly['terrestrial_radiation_instant'][j]
        frame.loc[0,'hour'] = frame.loc[0,'time'].split(':')[0]
        climatic_data_frame = pd.concat([climatic_data_frame, frame], ignore_index=True)
    return climatic_data_frame

class App:
    def __init__(self, root):
        style = ttk.Style()


        self.root = root
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "light")
        self.root.title("Графично приложение за фотоволтаична система")
        self.root.geometry("1920x1080")
        #self.root.configure(bg="#ffffff")
        # Main window configuration


        # Style configuration




        self.lаt = 0
        self.lon = 0

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Power input frame
        power_frame = ttk.Frame(main_frame)
        power_frame.grid(row=0, column=0, sticky="w")

        self.power_label = ttk.Label(power_frame, text="Максимална мощност (kW):")
        self.power_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.power_entry = ttk.Entry(power_frame, font=("Helvetica", 12))
        self.power_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=1, sticky="w")

        self.search_label = ttk.Label(search_frame, text="Търсене на адрес:")
        self.search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(search_frame, font=("Helvetica", 12))
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.search_button = ttk.Button(search_frame, text="Търси", command=self.search_location)
        self.search_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Map frame
        map_frame = ttk.Frame(main_frame)
        map_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.map_widget = TkinterMapView(map_frame, width=1700, height=500, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(42.6977, 23.3219)  # Set initial position to Sofia, Bulgaria
        self.map_widget.set_zoom(10)

        # Coordinates label
        self.coord_label = ttk.Label(main_frame, text="Координати: Няма избрани")
        self.coord_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Calculation button
        self.calculate_button = ttk.Button(main_frame, text="Пресмятане", command=self.calculate)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Results frame
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.power_for_the_next_16_days_label = ttk.Label(results_frame, text="")
        self.power_for_the_next_16_days_label.pack(padx=5, pady=5)

        self.power_from_last_year_label = ttk.Label(results_frame, text="")
        self.power_from_last_year_label.pack(padx=5, pady=5)

        # Bind map click event to update coordinates
        self.map_widget.add_right_click_menu_command(label="Избери координати", command=self.update_coordinates, pass_coords=True)

    

    def search_location(self):
        """Търси местоположение по въведен адрес."""
        address = self.search_entry.get()
        self.map_widget.set_address(address)

    def update_coordinates(self, coords):
        """Актуализира координатите в основния прозорец."""
        lat, lon = coords
        self.coord_label.config(text=f"Координати: {lat:.6f}, {lon:.6f}")
        self.lаt = lat
        self.lon = lon

    def calculate(self):
        """Пресмята нещо въз основа на въведените данни."""
        max_power = self.power_entry.get()
        coords = self.coord_label.cget("text")
        dataframe = pd.DataFrame()
        dataframe = add_values_to_futher_dataframe(self.lаt, self.lon)
        dataframe.insert(0, 'Size', float(max_power))

        eval = get_elevation(self.lаt, self.lon)
        dataframe.insert(1, 'Elevation', eval)
        dataframe.drop(['date', 'time', 'Latitude', 'Longitude'], axis=1, inplace=True)
        model = tf.keras.models.load_model('the_best.h5')
        dataframe.fillna(0, inplace=True)
        
        # Debug print to check DataFrame values
        print("DataFrame before conversion to float32:")
        print(dataframe)

        dataframe_values = dataframe.values.astype('float32')
        
        real_powers = model.predict(np.squeeze(dataframe_values))
        sum_of_real_power = 0
        for i in range(0, len(real_powers)):
            sum_of_real_power += real_powers[i][0]

        self.power_for_the_next_16_days_label.config(text=f"Сума на реалната мощност за следващите 16 дена: {sum_of_real_power/1000:.2f} kWh")
        dataframe_from_the_last_year = pd.DataFrame()
        dataframe_from_the_last_year = add_values_to_climatic_data_frame_from_last_year(self.lаt, self.lon)
        dataframe_from_the_last_year.insert(0, 'Size', float(max_power))
        dataframe_from_the_last_year.insert(1, 'Elevation', eval)
        dataframe_from_the_last_year.drop(['date', 'time', 'Latitude', 'Longitude'], axis=1, inplace=True)
        dataframe_from_the_last_year.fillna(0, inplace=True, axis=1)
        real_powers = model.predict(dataframe_from_the_last_year.values.astype('float32'))
        sum_of_real_power = 0
        for i in range(0, len(real_powers)):
            sum_of_real_power += real_powers[i][0]

        self.power_from_last_year_label.config(text=f"Сума на реалната мощност от миналата година: {sum_of_real_power/1000:.2f} kWh")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
