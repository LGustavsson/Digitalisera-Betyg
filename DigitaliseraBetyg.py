import configparser
import csv
import FreeSimpleGUI as sg
import os
import re
import sys
import webbrowser
from datetime import datetime
from pypdf import PdfReader, PdfWriter
from send2trash import send2trash   # Istället för os.remove för att förhindra permanent borttagning. Upp till använder nu istället.
from uuid import uuid4

# Hämta egna moduler
import SkapaInställningar
from DigitaliseraBetygGUI import DigitaliseraBetygGUI
from DigitaliseraBetygSettings import DigitaliseraBetygSettings

class DigitaliseraBetyg():
    def __init__(self):
        self.students = 0 
        self.metadata = []  # Här läses metadatafilen in för återkommande kontroll av kommande inläggningar av elever.
        self.settings_file_path = DigitaliseraBetygSettings().get_settings_file()
        self.metadata_category = DigitaliseraBetygSettings().get_metadata_category()
        self.metadata_file, self.error_file = DigitaliseraBetygSettings().get_file_names()
    
    def main(self):
        # Läser inställningarna och visar det GUI som är relevant. 
        if self.read_settings():
            DigitaliseraBetygGUI().gui_error(self.error_list)
            sys.exit()
        else:
            self.error_color, self.window = DigitaliseraBetygGUI().gui_main(
                self.max_students, self.schools, self.gradetypes, self.scan_folder_path, self.institution)
        self.read_metadata()

        # Main-loopen för programmet. 
        while True:
            event, self.values = self.window.read()
            match event:            
                case sg.WIN_CLOSED | "Avsluta":
                    break

                case "Hjälp":
                    self.window["output"].update("")
                    for row in DigitaliseraBetygGUI().help_text(self.max_students):
                        print(row)

                case "file_path":
                    self.default_state()
                    self.window["output"].update("")  
                    if self.check_file():
                        continue
                    if self.extract_data():
                        continue
                    self.update_fields()

                case "open_file":
                    if self.check_file():
                        continue
                    self.open_file()

                case "Digitalisera betyg":
                    if self.check_file():
                        continue
                    if self.check_fields():
                        continue
                    self.create_archive()   
                    self.default_state()
        self.window.close()
        sys.exit()

    # Kontrollerar att samtliga fält har data
    def check_fields(self):
        for student in range(self.students):
            for category in self.metadata_category:
                if self.values[f"{student}{category}"] == "":
                    self.window[f"{student}{category}"].update(background_color=self.error_color)
                    bool = True
                else:
                    self.window[f"{student}{category}"].update(background_color=sg.theme_input_background_color())

        if "bool" in locals():
            print("Fält utan uppgifter har markerats")  
            return True

    # Kontrollerar att fil har hämtats
    def check_file(self):
        if self.values["file_path"] == "":
            self.window["file_path_text"].update(background_color=self.error_color)
            print("Ingen betygsfil har hämtats.")
            return True

    # Kontrollera ifall betygsinformation redan finns i metadatafilen.
    def check_metadata(self):
        for row in self.metadata:
            if row[:6] == [self.values[f"{self.student}{category}"] for category in self.metadata_category]:
                print(f"Aktuellt betyg för {self.values[f'{self.student}{self.metadata_category[1]}']} är redan digitaliserat.")
                return True
    
    # Digitalisera de hämtade betygen.
    def create_archive(self):
        print("Betyg digitaliseras......")

        with open(os.path.join(self.metadata_folder_path, self.metadata_file), encoding="UTF-8", mode="a") as metadata_file:   
            csvwriter = csv.writer(metadata_file, delimiter=",", lineterminator="\n")
            
            # Skriver in de individuella betygsuppgifterna
            for self.student in range(self.students):

                # Formaterar om personnumret
                self.values[f"{self.student}{self.metadata_category[1]}"] = str(self.values[f"{self.student}{self.metadata_category[1]}"]).replace("-", "")
                if len(self.values[f"{self.student}{self.metadata_category[1]}"]) == 10:
                    if int(self.values[f"{self.student}{self.metadata_category[1]}"][:2]) <= int(str(datetime.now())[2:4]):
                        self.values[f"{self.student}{self.metadata_category[1]}"] = "20" 
                        + self.values[f"{self.student}{self.metadata_category[1]}"]
                    else:
                        self.values[f"{self.student}{self.metadata_category[1]}"] = "19" 
                        + self.values[f"{self.student}{self.metadata_category[1]}"]

                # Kontroll om betyget redan är hanterat.
                if self.check_metadata():
                    self.create_archive_error()
                    continue
                filename = f"{uuid4()}.pdf"

                # För in information i metadatafilen och lokala metadatavariabeln.
                csvwriter.writerow([self.values[f"{self.student}{category}"] for category in self.metadata_category] 
                                    + [self.archive_folder_path, filename])
                self.metadata.append([self.values[f"{self.student}{category}"] for category in self.metadata_category] 
                                    + [self.archive_folder_path, filename])

                # Sparar betygsfilen som egen fil.
                pdfwriter = PdfWriter()      
                pdfwriter.add_page(self.pdfreader.pages[self.student])
                pdfwriter.pdf_header = "%PDF-1.4" # Enligt RA-FS 2009:2 3 kap 4 §
                with open(os.path.join(self.archive_folder_path, filename), "wb") as pdf_file:
                    pdfwriter.write(pdf_file)      
       
        # Tar bort den nu bearbetade betygsfilen.
        send2trash(os.path.abspath(self.values["file_path"]))
        print("Digitalisering av betyg har slutförts.")  
    
    def create_archive_error(self):
        with open (os.path.join(self.error_folder_path, self.error_file), encoding="UTF-8", mode="a") as error_file:   
            csvwriter = csv.writer(error_file, delimiter=",", lineterminator="\n")

            # Skriver in de individuella betygsuppgifterna
            filename = f"{uuid4()}.pdf"
            csvwriter.writerow([self.values[f"{self.student}{category}"] for category in self.metadata_category] 
                + [self.error_folder_path + "\\", filename])
        
        # Sparar betygsfilen som egen fil.
        pdfwriter = PdfWriter()      
        pdfwriter.add_page(self.pdfreader.pages[self.student])
        pdfwriter.pdf_header = "%PDF-1.4" # Enligt RA-FS 2009:2 3 kap 4 §
        with open(os.path.join(self.error_folder_path, filename), "wb") as pdf_file:
            pdfwriter.write(pdf_file) 

   # Återställer fönstret till grund.
    def default_state(self):
        self.window["file_path_text"].update("")
        for student in range(self.students):
            for category in self.metadata_category:
                self.values[f"{student}{category}"] = ""
                self.window[f"{student}{category}"].update(visible=False) 

    # Hämta metadata ur betygen
    def extract_data(self):
        self.students = 0
        self.pdfreader = PdfReader(self.values["file_path"])
        
        # Kontrollerar sidantal.
        if self.pdfreader.get_num_pages() > self.max_students:
            print(f"Betygsfilen innehåller fler än maxantalet {self.max_students} sidor")
            return True  
        
        print("Läser in betygsfilen......")
        for page in self.pdfreader.pages:
            text = page.extract_text()
            
            # Hoppar över försök att hämta data ifall det inte finns någon OCR.
            if text == "":  
                self.students  += 1
                continue
        
            # Försöker hämta personnummer enligt 901010-1111 eller 9010101111.
            if matches := re.search(r"([\d]{6})[\W]?([\d]{4})", text):
                if int(matches[1][0:2]) <= int(str(datetime.now())[2:4]):
                    self.values[f"{self.students}{self.metadata_category[1]}"] = f"20{matches[1]}{matches[2]}"
                else:
                    self.values[f"{self.students}{self.metadata_category[1]}"] = f"19{matches[1]}{matches[2]}"
            
            # Försöker hämta skola.
            for school in self.schools:
                if re.search(school, text):
                    self.values[f"{self.students}{self.metadata_category[2]}"] = school

            # Försöker hämta betygsform.
            for grade in self.gradetypes:
                if re.search(grade, text):
                    self.values[f"{self.students}{self.metadata_category[5]}"] = grade
            
            # Försöker hämta år.
            if matches := re.search(r"([\d]{4})-[\d]{2}-[\d]{2}", text):
                    self.values[f"{self.students}{self.metadata_category[4]}"] = matches[1].strip()

            # Försöker hämta klass.
            if matches := re.search(r"Årskurs ([\w])", text):
                self.values[f"{self.students}{self.metadata_category[3]}"] = matches[1].strip()
            
            self.students  += 1
        print("Försök att hämta data har genomförts och en rad per identifierad elev har lagts in")

    # Öppnar den hämtade betygsfilen i webläsaren
    def open_file(self):
        webbrowser.open(self.values["file_path"])

    # Läser in metadatafilen.
    def read_metadata(self):
        # Läser in metadatafilen i variabel.
        with open(os.path.join(self.metadata_folder_path, self.metadata_file), encoding="UTF-8", mode="r", newline="\n") as metadata_file: 
            csvreader = csv.reader(metadata_file)
            for row in csvreader:
                self.metadata.append(row)
        self.metadata.pop(0)    # Tar bort headern så programmet inte behöver söka på den.

    # Läser in inställningsfilen.
    def read_settings(self):
        self.error_list = []

        # Kontrollerar ifall inställnnigsfilen saknas.
        if not os.path.exists(self.settings_file_path):
            self.error_list += ["Inställningsfilen saknas."]
            return True

        # Hämtar uppgifter från configfilen.
        settings = configparser.ConfigParser(allow_no_value=True)
        settings.read(self.settings_file_path, encoding="UTF-8")

        self.archive_folder_path = settings["DEFAULT"]["archive_folder"] + "\\"
        self.metadata_folder_path = settings["DEFAULT"]["metadata_folder"]
        self.scan_folder_path = settings["DEFAULT"]["scan_folder"]
        self.error_folder_path = settings["DEFAULT"]["error_folder"]
        self.institution = settings["DEFAULT"]["institution"]
        self.schools = settings["DEFAULT"]["schools"].split(",")
        self.gradetypes = settings["DEFAULT"]["gradetypes"].split(",")
        self.max_students = int(settings["DEFAULT"]["max_students"])

        if not os.path.exists(os.path.join(self.metadata_folder_path, self.metadata_file)):
            self.error_list += [
                "Metadatafilen saknas.", 
                "Var god genomför rättelser i inställningsprogrammet för att generera en ny metadatafil."]
            return True

    # Visar så många fält som betygsfilen har antal sidor.
    def update_fields(self):
        self.window["file_path_text"].update(self.values["file_path"], background_color=sg.theme_background_color())  
        for student in range(self.students):
            for category in self.metadata_category:
                self.window[f"{student}{category}"].update(self.values[f"{student}{category}"], visible=True, background_color=sg.theme_input_background_color())
  
if __name__ == "__main__":
    digitalisera_betyg = DigitaliseraBetyg()
    digitalisera_betyg.main()