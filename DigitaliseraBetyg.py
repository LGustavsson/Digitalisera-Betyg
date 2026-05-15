# Standardmoduler.
import csv
import os
import re
import sys
import webbrowser
from datetime import datetime
from uuid import uuid4

# Tredjepartsmoduler.
import FreeSimpleGUI as sg
from pypdf import PdfReader, PdfWriter

# Egna, lokala moduler.
from Data import Data
from DigitaliseraBetygGUI import DigitaliseraBetygGUI


class DigitaliseraBetyg:
    def __init__(self):
        self.students = 0
        self.color_error = Data.color_error()
        self.metadata = Data.metadata_grade()

    def main(self):
        """ Main-loopen för programmet."""
        if self.read_settings():
            DigitaliseraBetygGUI().gui_error(self.error_list)
            sys.exit()
        else:
            self.window = DigitaliseraBetygGUI().gui_main()
            self.read_metadata()

        while True:
            event, self.values = self.window.read()
            match event:
                case sg.WIN_CLOSED | "Avsluta": break
                case "file_path":
                    self.window["output"].update("")
                    self.default_state()
                    if self.error_check(): continue
                    self.extract_data()
                    self.update_fields()
                case "open_file": self.open_file()
                case "Digitalisera betyg":
                    if self.error_check(True): continue
                    self.create_archive()
                    self.default_state(True)
        self.window.close()
        sys.exit()

    def check_metadata(self):
        """Kontrollerar ifall betygsinformationen redan är digitaliserad."""
        for row in self.metadata_local:
            if row == [self.values[f"{self.student}{data}"] for data in self.metadata[1:]]:
                print(f"Betyg för {self.values[f'{self.student}{self.metadata[1]}']} är redan digitaliserat.")
                return True

    def create_archive(self):
        """Sparar inlästa betyg i arkivet tillsammans med dess uppgifter i metadatafiler."""
        print("Betyg digitaliseras.")
        for self.student in range(self.students):
            self.filename = f"{uuid4()}.pdf"

            # Tar bort bindestreckfrån personnumret.
            if "-" in self.values[f"{self.student}{self.metadata[2]}"]:
                self.values[f"{self.student}{self.metadata[2]}"] = str(
                    self.values[f"{self.student}{self.metadata[2]}"]).replace("-", "")
            # Lägger till ledande 19 eller 20 till personnumret.
            if len(self.values[f"{self.student}{self.metadata[2]}"]) == 10:
                if int(self.values[f"{self.student}{self.metadata[2]}"][:2]) <= int(str(datetime.now())[2:4]):
                    self.values[f"{self.student}{self.metadata[2]}"] = (
                        f"20{self.values[f'{self.student}{self.metadata[2]}']}")
                else:
                    self.values[f"{self.student}{self.metadata[2]}"] = (
                        f"19{self.values[f'{self.student}{self.metadata[2]}']}")

            # Kontrollera om betyget redan är hanterat.
            if self.check_metadata():
                self.create_archive_double()
                continue

            # Sparar metadata.
            with open(self.path_metadata, encoding="UTF-8", mode="a") as file:
                csvwriter = csv.writer(file, delimiter=",", lineterminator="\n")
                csvwriter.writerow([self.folder_archive, self.filename] 
                                    + [self.values[f"{self.student}{data}"] for data in self.metadata[1:]])
            self.metadata_local.append([self.values[f"{self.student}{data}"] for data in self.metadata[1:]])
                    
            # Sparar fil.
            pdfwriter = PdfWriter()
            pdfwriter.add_page(self.pdfreader.pages[self.student])
            pdfwriter.pdf_header = "%PDF-1.4"  # Riksarkivets RA-FS 2009:2 3 kap 4 §
            with open(os.path.join(self.folder_archive, self.filename), "wb") as file: pdfwriter.write(file)
        print("Digitalisering av betyg har slutförts.")

    def create_archive_double(self):
        """Spara betyg som antagen dubblett."""
        # Sparar metadata.
        with open(self.path_double, encoding="UTF-8", mode="a") as file:
            csvwriter = csv.writer(file, delimiter=",", lineterminator="\n")
            csvwriter.writerow([self.folder_double, self.filename]
                               + [self.values[f"{self.student}{data}"] for data in self.metadata[1:]])
            
        # Sparar fil.
        pdfwriter = PdfWriter()
        pdfwriter.add_page(self.pdfreader.pages[self.student])
        pdfwriter.pdf_header = "%PDF-1.4"  # Riksarkivets RA-FS 2009:2 3 kap 4 §
        with open(os.path.join(self.folder_double, self.filename), "wb") as file: pdfwriter.write(file)

    def default_state(self, bool=False):
        """Återställer programfönstret till sin grund."""
        for student in range(self.students):
            for data in self.metadata[1:]:
                self.values[f"{student}{data}"] = ""
                self.window[f"{student}{data}"].update(visible=False)
        if bool:
            self.window["file_path"].update("")
            self.values["file_path"] = ""

    def error_check(self, bool=False):
        """Samtliga funktioner som kontrollerar fel som behöver åtgärdas."""
        # Kontrollerar att fil har hämtats.
        if self.values["file_path"] == "":
            print("Ingen betygsfil har hämtats.")
            return True
        
        # Kontrollerar sidantal av hämtad fil.
        self.pdfreader = PdfReader(self.values["file_path"])
        if self.pdfreader.get_num_pages() > self.max_students:
            print(f"Betygsfilen innehåller fler än maxantalet {self.max_students} sidor")
            return True
        
        # Kontrollerar att samtliga fält har data.
        if bool:
            for student in range(self.students):
                for data in self.metadata[1:]:
                    if self.values[f"{student}{data}"] == "":
                        self.window[f"{student}{data}"].update(background_color=self.color_error)
                        state = True
                    else:
                        self.window[f"{student}{data}"].update(background_color=sg.theme_input_background_color())
            if "state" in locals():
                print("Fält utan uppgifter har markerats")
                return True

    def extract_data(self):
        """Hämta metadata ur betygsfilen ifall denna har OCR och för över detta till inmatningsfält."""
        print("Läser in betygsfilen.")
        self.students = 0
        for page in self.pdfreader.pages:   # self.pdfreader-variabeln kommer från error_check-metoden.
            text = page.extract_text()
            # Hoppar över betyg om den saknar OCR.
            if text == "":
                self.students += 1
                continue

            # Hämta personnummer.
            if matches := re.search(r"([\d]{6,8})[-]?([\d]{4})", text):
                self.values[f"{self.students}{self.metadata[2]}"] = f"{matches[1]}{matches[2]}"

            # Hämta år.
            if matches := re.search(r"([\d]{4})-[\d]{2}-[\d]{2}", text):
                self.values[f"{self.students}{self.metadata[3]}"] = matches[1]

            # Hämta klass.
            if matches := re.search(r"Årskurs ([\w]+)[\s]", text):
                self.values[f"{self.students}{self.metadata[4]}"] = matches[1]
            
            # Hämta betygstyp.
            for grade in self.gradetypes:
                if re.search(grade, text):
                    self.values[f"{self.students}{self.metadata[5]}"] = grade
                    break

            # Hämta skola.
            for school in self.schools:
                if re.search(school, text):
                    self.values[f"{self.students}{self.metadata[6]}"] = school
                    break

            # Hämta skolform
            for form in self.forms:
                if re.search(form, text):
                    self.values[f"{self.students}{self.metadata[7]}"] = form
                    break

            self.students += 1 
        print("Försök att hämta data har genomförts och en rad per identifierad elev har lagts in")

    def open_file(self):
        """Öppnar den hämtade betygsfilen i webbläsaren."""
        if self.values["file_path"] != "": webbrowser.open(self.values["file_path"])

    def read_metadata(self):
        """Läser in metadatafilen i lokal variabel."""
        self.metadata_local = []
        with open(self.path_metadata, encoding="UTF-8", mode="r", newline="\n",) as file:
            csvreader = csv.reader(file)
            csvreader.__next__()    # Hoppar över titelraden.
            for row in csvreader:
                self.metadata_local.append(row[2:])

    def read_settings(self):
        """ Läser in inställningsfilen."""
        self.error_list = []
        data = Data()
        # Kontrollerar ifall inställningsfilen saknas.
        if not os.path.exists(Data.path_settings()):
            self.error_list += ["Inställningsfilen saknas.", 
                "Starta Settings-programmet och genomför rättelser där för att generera nödvändiga mappar och filer."]
            return True
        
        # Hämtar uppgifter.
        self.path_metadata = data.path_metadata()
        self.path_double = data.path_double()
        if not os.path.exists(self.path_metadata) or not os.path.exists(self.path_double):
            self.error_list += ["Arkiv-, eller dubblettmapp, eller dess metadatafiler saknas.",
                "Starta Settings-programmet och genomför rättelser där för att generera nödvändiga mappar och filer."]
            return True
        if not os.access(self.path_metadata, os.W_OK) or not os.access(self.path_double, os.W_OK):
            self.error_list += ["Programmet saknar skrivrättigheter till metadatafilerna.", 
                                "Kontakta systemansvarig eller er IT-enhet för att lösa problemet."]
            return True
        self.folder_archive = data.folder_archive()
        self.folder_double = data.folder_double()
        self.schools = data.schools()
        self.gradetypes = data.gradetypes()
        self.forms = data.forms()
        self.max_students = data.max_students()
        del data

    def update_fields(self):
        """Visar så många rader som betygsfilen har antal sidor."""
        for student in range(self.students):
            for data in self.metadata[1:]:
                self.window[f"{student}{data}"].update(self.values[f"{student}{data}"], visible=True,
                                                       background_color=sg.theme_input_background_color())


if __name__ == "__main__":
    digitalisera_betyg = DigitaliseraBetyg()
    digitalisera_betyg.main()
