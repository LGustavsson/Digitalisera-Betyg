import configparser
import csv
import FreeSimpleGUI as sg
import os
import sys

# Importera egna funktioner.
import SkapaInställningar
from DigitaliseraBetygSettingsGUI import DigitaliseraBetygSettingsGUI

class DigitaliseraBetygSettings:
    def __init__(self):
        # Mappsökvägar och filnamn
        self.settings_folder_path = rf"{os.path.dirname(__file__)}\Settings"
        self.settings_file = "Settings.ini"
        self.metadata_file = "Metadata.csv"
        self.error_file = "Fellista.csv"

        # Text är de fält som visar datan i text i GUI:t, data är dict-namnet för datan.
        self.text_fields, self.data_fields = DigitaliseraBetygSettingsGUI().get_lists()
        
        # !!!
        # PRIMÄR VARIABEL! Påverkar detta program, DigitaliseraBetyg, och DigitaliseraBetygGUI.        
        self.metadata_category = [
            "Namn", #[0] Namn
            "Personnummer", #[1] Personnummer
            "Skola",    #[2] Skola
            "Klass",    #[3] Klass
            "År",   #[4] År
            "Handlingstyp", #[5] Handlingstyp
            "Filsökväg",    #[6] Filsökväg
            "Filnamn",  #[7] Filnamn
            ]

    def main(self):
        self.window, self.error_color = DigitaliseraBetygSettingsGUI().main()

        if self.read_settings():
            bool = True

        while True:
            event, self.values = self.window.read()

            # Kopierar över sögvägarna för mapparna till dict-datan. 
            if "bool" in locals():
                for data, text in zip(self.data_fields[:4], self.text_fields[:4]):
                    try:
                        self.values[data] = self.window[text].get()
                    except TypeError:   # Vet inte varför denna dyker upp, det verkar fungera ändå....
                        pass

            match event:
                case sg.WIN_CLOSED:
                    break

                case "clear":
                    self.values[self.data_fields[0]] = ""
                    self.window["scan_text"].update("")

                case "Spara inställningarna":
                    if self.check_fields():
                        continue
                    if self.check_value():
                        continue
                    if self.check_folder():
                        continue
                    self.create_settings()
        self.window.close()
        sys.exit()

    # Läser in uppgifterna från befintlig inställningsfil
    def read_settings(self):
        if os.path.exists(os.path.join(self.settings_folder_path, self.settings_file)):
            settings = configparser.ConfigParser()
            settings.read(os.path.join(self.settings_folder_path, self.settings_file), encoding="UTF-8")

            # Kopierar över befintliga inställningar till GUI:t.
            for text, data in zip(self.text_fields, self.data_fields):
                self.window[text].update(settings["DEFAULT"][data])

            DigitaliseraBetygSettingsGUI().show_popup("read_settings")
            return True

    def check_folder(self):
        if self.values[self.data_fields[1]] == self.values[self.data_fields[3]]:
            self.window[self.text_fields[1]].update(background_color=self.error_color)
            self.window[self.text_fields[3]].update(background_color=self.error_color)

            DigitaliseraBetygSettingsGUI().show_popup("check_folder")
            return True

    def create_settings(self):      
        # Skapa mappar.
        if self.values[self.data_fields[0]] != "":
            os.makedirs(self.values[self.data_fields[0]], exist_ok=True) #Skanningsmapp
        os.makedirs(self.values[self.data_fields[1]], exist_ok=True) #Arkivmapp
        os.makedirs(self.values[self.data_fields[2]], exist_ok=True) #Metadatamapp
        os.makedirs(self.values[self.data_fields[3]], exist_ok=True) #Fellistemapp
        os.makedirs(self.settings_folder_path, exist_ok=True) #Inställningsmapp
        
        # Formatera till korrekt str-format
        self.values[self.data_fields[5]] = ",".join(item.strip() for item in str(self.values[self.data_fields[5]]).strip(",").split(",")) 
        self.values[self.data_fields[6]] = ",".join(item.strip() for item in str(self.values[self.data_fields[6]]).strip(",").split(",")) 

        # Generera en inställningsfil med all data.
        settings = {data: self.values[data] for data in self.data_fields}
        SkapaInställningar.create_settings_file(os.path.join(self.settings_folder_path, self.settings_file), settings)

        # Skapa metadatafil standard
        if not os.path.exists(os.path.join(self.values[self.data_fields[2]], self.metadata_file)):
            with open(os.path.join(self.values[self.data_fields[2]], self.metadata_file), encoding="UTF-8", mode="w") as metadata_file:   
                csvwriter = csv.writer(metadata_file, delimiter=",", lineterminator="\n")
                csvwriter.writerow(self.metadata_category)
        
        # Skapa metadatafil fellista
        if not os.path.exists(os.path.join(self.values[self.data_fields[3]], self.error_file)):
            with open(os.path.join(self.values[self.data_fields[3]], self.error_file), encoding="UTF-8", mode="w") as error_file:   
                csvwriter = csv.writer(error_file, delimiter=",", lineterminator="\n")
                csvwriter.writerow(self.metadata_category)        

        # Töm fönstret på inmatad information.
        for text in self.text_fields:
            self.window[text].update("")

        DigitaliseraBetygSettingsGUI().show_popup("create_settings")
        self.window.close()
        sys.exit()

    # Kontroll att samtliga fält har fyllts i.
    def check_fields(self):
        for text, data in zip(self.text_fields[1:], self.data_fields[1:]):
            if self.values[data] == "":
                self.window[text].update(background_color=self.error_color)
                bool = True
            else:
                if text.endswith("text"):
                    self.window[text].update(background_color=sg.theme_background_color())
                else:
                    self.window[text].update(background_color=sg.theme_input_background_color())
        
        if "bool" in locals():
            DigitaliseraBetygSettingsGUI().show_popup("check_fields")
            return True

    # Kontroll att antal studenter är en siffra. 
    def check_value(self):
         if not str(self.values[self.data_fields[7]]).isdigit():
            self.window[self.data_fields[7]].update(background_color=self.error_color)

            DigitaliseraBetygSettingsGUI().show_popup("check_value")
            return True
         
    def get_metadata_category(self):
        return self.metadata_category[:6]

    def get_settings_file(self):
        return os.path.join(self.settings_folder_path, self.settings_file)
    
    def get_file_names(self):
        return self.metadata_file, self.error_file
            
if __name__ == "__main__":
    digitalisera_betyg_settings = DigitaliseraBetygSettings()
    digitalisera_betyg_settings.main()