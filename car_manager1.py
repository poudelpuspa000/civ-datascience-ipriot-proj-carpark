from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
import time
import pandas as pd

#Car log entry
class LogEntry:
    def __init__(self, event_type, license_plate, timestamp):
        self.timestamp = timestamp
        self.event_type = event_type
        self.license_plate = license_plate

    def entry(self):
        return {
            "timestamp": self.timestamp,
            "event": self.event_type,
            "license_plate": self.license_plate
        }

# NEW LOG MANAGER CLASS
class CarparkLogManager:
    def __init__(self):
        self._logs = []

    def add_log(self, event_type, license_plate, timestamp):
        # entry = {
        #     "timestamp": timestamp,
        #     "event": event_type,
        #     "license_plate": license_plate
        # }
        log = LogEntry(event_type, license_plate, timestamp)
        self._logs.append(log.entry())
        #self._logs.append(entry)
        print(f"[{timestamp}] {event_type}: {license_plate}")
    def get_logs(self):
        return self._logs

    def export_as_dataframe(self, file_path ='C:/Users/user/Downloads/ICTPRG302/carpark_logs.csv'):
        df = pd.DataFrame(self._logs)
        df.to_csv(file_path, index=False)
        print(f"Logs exported successfully to: {file_path}")
        return df

class CarparkManager(CarparkSensorListener,CarparkDataProvider):
    def __init__(self, display_callback):
        self._available_spaces = 100
        self._temperature = 25
        self._display_callback = display_callback
        self._current_time = time.localtime()
        self._parked_vehicles = set() # Parked list of the cars
        self._log_manager = CarparkLogManager()  # use the new log manager # Store history logs

        #CarparkDataProvider interface
    @property
    def available_spaces(self):
        return self._available_spaces

    @property
    def temperature(self):
        return self._temperature

    @property
    def current_time(self):
        return self._current_time
    @property
    def history_log(self):
        return self._log_manager.get_logs() #added

    # CarparkSensorListener interface

    def incoming_car(self, license_plate):
        license_plate = license_plate.strip().upper()
        #timestamp = time.strftime("%Y-%m-%d %H:%M:%S", self._current_time)
        if not license_plate:
            print("Unauthorised Vehical !!!!!")
            return

        if license_plate in self._parked_vehicles:
            print(f"This {license_plate} vehicle is already in the carpark.")
            return

        if self._available_spaces <= 0:
            self._available_spaces = 0
            print("Carpark is Full")            
        else:
            self._available_spaces -= 1
            self._parked_vehicles.add(license_plate)
            self._log_event("CAR IN", license_plate)
            # self._logs.append(log_entry)
            # print(log_entry)

        self._update_time()
        self._notify_display()


    def outgoing_car(self, license_plate):
        license_plate = license_plate.strip().upper()
        #timestamp = time.strftime("%Y-%m-%d %H:%M:%S", self._current_time)
        if not license_plate:
            print("Unauthorised Vehical !!!!!")
            return

        if license_plate not in self._parked_vehicles:
            print(f"This {license_plate} has not entered the carpark properly.")
            return

        self._available_spaces += 1
        self._parked_vehicles.remove(license_plate)
        self._log_event("CAR OUT", license_plate)
        #self._logs.append(log_entry)
        #print(log_entry)

        self._update_time()
        self._notify_display()

    def temperature_reading(self, reading):
        try:
            self._temperature = int(reading)
            
        except ValueError:
            pass
        self._update_time()
        self._notify_display()


    
    # used terms above
    def _update_time(self):
        self._current_time = time.localtime()

    def _notify_display(self):
        if self._display_callback:
            self._display_callback()
    def _log_event(self, event_type, value):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", self._current_time)
        self._log_manager.add_log(event_type, value, timestamp) #added
        
        
    def export_logs_as_dataframe(self):
        return pd.DataFrame(self._logs)
    def export_logs_as_dataframe(self):                 #added
        return self._log_manager.export_as_dataframe()
   

"""Sensors:
EntrySensor: Detects cars entering the carpark.
ExitSensor: Detects cars exiting the carpark.
Carpark Management Center:
Tracks the status of each parking bay (occupied or available).
Maintains a log of all cars entering and exiting, including timestamps.
Display:
Shows the number of available parking bays.
Displays the current temperature (sourced from an external weather data file).
Car Class:
Represents a car with attributes such as license plate, car model, entry time, and exit time.
Carpark Class:
Manages the collection of cars and parking bays.
Interfaces with the sensors to update parking bay status."""

# class TextFileDisplay:
#     def __init__(self, file_path):
#         self.file_path = file_path

#     def show_message(self, message):
#         with open(self.file_path, "w") as file:
#             file.write(message)
import os
print(os.getcwd())