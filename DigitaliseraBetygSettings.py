# Standardmoduler.
import configparser
import csv
import os
import sys

# Tredjepartsmoduler.
import FreeSimpleGUI as sg

# Egna, lokala moduler.
import SkapaInställningar
from Data import Data
from DigitaliseraBetygSettingsGUI import DigitaliseraBetygSettingsGUI


class DigitaliseraBetygSettings:
    def __init__(self):
        self.path_settings = Data.path_settings()
        self.folder_settings = Data.folder_settings()
        self.file_metadata = Data.file_metadata()
        self.file_double = Data.file_double()
        self.color_error = Data.color_error()
        self.metadata_settings = Data.metadata_settings()
        self.metadata_grade = Data.metadata_grade()
        self.metadata_system = Data.metadata_system()

    def main(self):
        self.window= DigitaliseraBetygSettingsGUI().main()
        if self.read_settings():
            state = True
        while True:
            event, self.values = self.window.read()
            # Kopierar över sökvägarna för mapparna till dicten. 
            if "state" in locals():
                for data in self.metadata_settings[:3]:
                    try:
                        self.values[data] = self.window[f"text{data}"].get()
                    except TypeError:   # Vet inte varför denna dyker upp, det verkar fungera ändå.
                        pass
            match event:
                case sg.WIN_CLOSED: break
                case "folder_scan_clear":
                    self.values[self.metadata_settings[0]] = ""
                    self.window[f"text{self.metadata_settings[0]}"].update("")
                case "Spara inställningarna":
                    if self.error_check(): continue
                    self.create_settings()
        self.window.close()
        sys.exit()

    def read_settings(self):
        """ Läser in uppgifterna från befintlig inställningsfil"""
        if os.path.exists(self.path_settings):
            settings = configparser.ConfigParser()
            settings.read(os.path.join(self.path_settings), encoding="UTF-8")
            for data in self.metadata_settings[:3]: # Mappar
                self.window[f"text{data}"].update(settings["DEFAULT"][data])
            for data in self.metadata_settings[3:]: # Inputält
                self.window[data].update(settings["DEFAULT"][data])
            DigitaliseraBetygSettingsGUI().show_popup("read_settings")
            return True

    def error_check(self):
        """Samtliga funktioner som kontrollerar fel som behöver åtgärdas."""
        # Kontroll att samtliga fält har fyllts i.
        for data in self.metadata_settings[1:3]:    # Mappar förutom skanningsmappen
            if self.values[data] == "":
                self.window[f"text{data}"].update(background_color=self.color_error)
                state = True
            else:
                self.window[f"text{data}"].update(background_color=sg.theme_background_color())
        for data in self.metadata_settings[3:]: # Inputfält
            if self.values[data] == "":
                self.window[data].update(background_color=self.color_error)
                state = True
            else:
                self.window[data].update(background_color=sg.theme_input_background_color())
        if "state" in locals():
            DigitaliseraBetygSettingsGUI().show_popup("check_fields")
            return True       

        # Arkivmapp och dubblettmapp kan inte vara samma
        if self.values[self.metadata_settings[1]] == self.values[self.metadata_settings[2]]:
            self.window[f"text{self.metadata_settings[1]}"].update(background_color=self.color_error)
            self.window[f"text{self.metadata_settings[2]}"].update(background_color=self.color_error)
            DigitaliseraBetygSettingsGUI().show_popup("check_folder")
            return True
    
        # Kontroll att antal studenter är en siffra. 
        if not str(self.values[self.metadata_settings[4]]).isdigit():
            self.window[self.metadata_settings[4]].update(background_color=self.color_error)
            DigitaliseraBetygSettingsGUI().show_popup("check_value")
            return True
        
        # Testar skrivrättigheter.
        if not os.access(self.values[self.metadata_settings[1]], os.W_OK):
            state = True
        if not os.access(self.values[self.metadata_settings[2]], os.W_OK):
            state = True
        try:
            os.makedirs(self.folder_settings, exist_ok=True)
        except OSError:
            state = True
        if "state" in locals():
            DigitaliseraBetygSettingsGUI.show_popup("OSError")
            return True
        
    def create_settings(self):    
        """Sparar uppgifterna i inställingsfilen."""  
        # Skapa mappar.
        os.makedirs(self.folder_settings, exist_ok=True)
        if self.values[self.metadata_settings[0]] != "":    #Skanningsmapp
            os.makedirs(self.values[self.metadata_settings[0]], exist_ok=True)
        for data in self.metadata_settings[1:3]:    #Övriga mappar
            os.makedirs(self.values[data], exist_ok=True)

        # Formatera till korrekt str-format
        for data in self.metadata_settings[5:]:
            self.values[data] = ",".join(item.strip() for item in str(self.values[data]).strip(",").split(",")) 

        # Generera en inställningsfil med all data.
        settings = {data: self.values[data] for data in self.metadata_settings}
        SkapaInställningar.create_settings_file(self.path_settings, settings)

        # Skapa metadatafil standard
        if not os.path.exists(os.path.join(self.values[self.metadata_settings[1]], self.file_metadata)):
            with open(os.path.join(self.values[self.metadata_settings[1]], self.file_metadata), 
                      encoding="UTF-8", mode="w") as file:   
                csvwriter = csv.writer(file, delimiter=",", lineterminator="\n")
                csvwriter.writerow(self.metadata_system + self.metadata_grade[1:])

        # Skapa metadatafil fellista
        if not os.path.exists(os.path.join(self.values[self.metadata_settings[2]], self.file_double)):
            with open(os.path.join(self.values[self.metadata_settings[2]], self.file_double), 
                      encoding="UTF-8", mode="w") as file:   
                csvwriter = csv.writer(file, delimiter=",", lineterminator="\n")
                csvwriter.writerow(self.metadata_system + self.metadata_grade[1:]) 
                      
        DigitaliseraBetygSettingsGUI().show_popup("create_settings")
        self.window.close()
        sys.exit()
                   
            
if __name__ == "__main__":
    digitalisera_betyg_settings = DigitaliseraBetygSettings()
    digitalisera_betyg_settings.main()
