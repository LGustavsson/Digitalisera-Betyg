import FreeSimpleGUI as sg
import os
import sys

from DigitaliseraBetygSettings import DigitaliseraBetygSettings

class DigitaliseraBetygGUI:
    def __init__(self):
        self.theme = "Green Mono"   # https://user-images.githubusercontent.com/46163555/202543904-e7fefe99-2c02-4e58-9a97-ef0724aa4d8a.png
        self.icon = f"{os.path.dirname(__file__)}/icon.ico"
        self.font = ("arial", "12" ,"normal")
        self.font_output = ("arial", "10" ,"normal")    # Output-texten blir lite mindre. 
        self.error_color = "#f0b6a4"
        self.error_list_end = [
            "",
            "Var god fyll i nödvändig information via programmet 'DigitaliseraBetygSettings' som finns i programmappen", 
            "Starta programmet DigitaliseraBetyg igen efter genomförda rättelser."]
        
        self.metadata_category = DigitaliseraBetygSettings().get_metadata_category()

    # Felrättningsfönstret för applikationen.
    def gui_error(self, error_list):
            sg.theme(self.theme)

            window = sg.Window(
                title="Felinformation", 
                layout=[  
                    [sg.Text(f"Följande fel upptäcktes som behöver rättas innan programmet öppnas igen:")],
                    [sg.Output(expand_x=True, size=(None, 10), font=self.font_output)],
                    ], 
                font=(self.font), 
                icon=self.icon, 
                finalize=True)
            
            # Skriver ut vad som är felaktigt i inställningsfilen.
            for row in error_list + self.error_list_end:
                print(row)

            while True:
                event, values = window.read()
                match event:
                    case sg.WIN_CLOSED:
                        break
            window.close()
            sys.exit()

    # Huvudfönstret för applikationen.
    def gui_main(self, max_students, schools, gradetypes, scan_path, institution):
            sg.theme(self.theme)
            
            category = [[
                sg.Text("ID", size=(3)), 
                sg.Text(self.metadata_category[0], size=(20)), 
                sg.Text(self.metadata_category[1], size=(15)), 
                sg.Text(self.metadata_category[2], size=(20)),
                sg.Text(self.metadata_category[3], size=(6)),
                sg.Text(self.metadata_category[4], size=(6)),
                sg.Text("Betygstyp", size=(13)), # "Handlingstyp" i metadatafilen, "betygstyp" i GUI för att vara enkel att förstå.
                ]]
            
            fields= [[
                sg.Text(student+1, size=(3)), 
                sg.Input(key=f"{student}{self.metadata_category[0]}", visible=False, size=(20)), 
                sg.Input(key=f"{student}{self.metadata_category[1]}", visible=False, size=(15)), 
                sg.Combo(schools, key=f"{student}{self.metadata_category[2]}", visible=False, size=(19)),
                sg.Input(key=f"{student}{self.metadata_category[3]}", visible=False, size=(6)), 
                sg.Input(key=f"{student}{self.metadata_category[4]}", visible=False, size=(6)), 
                sg.Combo(gradetypes, key=f"{student}{self.metadata_category[5]}", visible=False, size=(11)), 
                ] for student in range(max_students)]

            layout = [[
                    sg.FileBrowse("Hämta betygsfil", file_types=(("ALL Files", ".pdf"),), initial_folder=scan_path, target="file_path", key="file_path", enable_events=True), 
                    sg.Text(key="file_path_text", size=(50)), 
                    sg.Push(), 
                    sg.Button("Visa betygsfil", key="open_file", enable_events=True), 
                    sg.Button("Hjälp", enable_events=True),
                    ],
                [sg.Column(category)],
                [sg.Column(fields)],
                [sg.Button("Digitalisera betyg"), sg.Push(), sg.Button("Avsluta")],
                [sg.Output(key="output", size=(None, 8), expand_x=True, font=self.font_output)],
                ]    
            
            window = sg.Window(
                title=f"{institution} - Digitalisera betyg", 
                layout=layout, 
                font=(self.font), 
                icon=self.icon, 
                finalize=True
                )
            
            # Löser en bugg där text efter val i combomenyn är dold bakom heltäckande färg. Outlinen av markeringen är dock kvar, menmen.....
            # Lösningen är hämtad från https://stackoverflow.com/a/73225157.
            style = sg.ttk.Style()
            for student in range(max_students):
                style.configure(window[f"{student}{self.metadata_category[2]}"].widget.configure()['style'][-1], selectforeground=sg.theme_input_text_color())
                style.configure(window[f"{student}{self.metadata_category[5]}"].widget.configure()['style'][-1], selectforeground=sg.theme_input_text_color())
            
            return self.error_color, window
    
    # Kort tillvägagångsinformation som skrivs ut i huvudfönstret.
    def help_text(self, max_students):
         return [
            f"1. Skanna så många betyg som ni känner att ni vill hantera samtidigt. Dock inte så att sidantalet i den skannade filen överstiger {max_students} sidor.", 
            "2. Tänk på att betygen måste vara enkelsidiga, programmet kan inte hantera flersidiga individuella betyg.",
            "3. Hämta pdf-filen med inskannade betyg via 'Välj betygsfil'.",
            "4. Programmet kommer försöka hämta information från betygen och placera dessa i rätt fält.", 
            "5. Den hämtade pdf-filen kan visas i webbläsaren via 'Visa betygsfilen'. ID:t för varje elev är samma som sidan i pdf-filen.",
            "6. Fyll i resterande fält med rätt uppgifter, samt säkerställ att de uppgifter som programmet hämtade är korrekta.", 
            "7. När samtliga fält är ifyllda, välj 'Digitalisera betyg'.",
            ]