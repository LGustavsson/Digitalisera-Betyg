import FreeSimpleGUI as sg
import os

class DigitaliseraBetygSettingsGUI:
    def __init__(self):
        self.theme = "Green Mono"   # https://user-images.githubusercontent.com/46163555/202543904-e7fefe99-2c02-4e58-9a97-ef0724aa4d8a.png
        self.icon = f"{os.path.dirname(__file__)}/icon.ico"
        self.font = ("arial", "10" ,"normal")
        self.font_bold = ("arial", "10" ,"bold")
        self.error_color = "#f0b6a4"
        self.size_button = (10, 1)
        self.size_title = (15, 2)
        self.size_text = (50, 2)

        self.data_fields = [
            "scan_folder",  #[0]    # Denna är först så den kan hoppas över.
            "archive_folder",   #[1]
            "metadata_folder",  #[2]     
            "error_folder", #[3]
            "institution",  #[4]
            "schools",  #[5]
            "gradetypes",   #[6]
            "max_students", #[7]
            ]   

        self.text_fields = [
            "scan_text",
            "archive_text",
            "metadata_text",
            "error_text",
            "institution",
            "schools",
            "gradetypes",
            "max_students"
            ]

    def main(self):
        sg.theme(self.theme)

        information = [
            [sg.Text("Information", font=self.font_bold)],
            [sg.Text("Här fyller ni i de grundinställningar som behövs för att betygsdigitaliseringen ska kunna genomföras.")],
            [sg.Text("För ytterligare information om programmet och om vad varje individuell inställning syftar till så hänvisas ni till README-filen i programmappen.")]
            ]

        settings = [
            [sg.Button("Spara inställningarna", size=(30, 3), font=self.font_bold)]
            ]
        
        archive = [
            [sg.Text("Arkivmapp", size=self.size_title, font=self.font_bold), sg.Text("I denna mapp kommer de individuella betygen placeras.", size=self.size_text)],
            [sg.FolderBrowse("Välj målmapp", key="archive_folder", size=self.size_button), sg.Text(key="archive_text", size=self.size_text)], 
            ]

        metadata = [    
            [sg.Text("Metadatamapp", size=self.size_title, font=self.font_bold), sg.Text("I denna mapp kommer metadatafilen med betygsuppgifterna placeras.", size=self.size_text)],
            [sg.FolderBrowse("Välj målmapp", key="metadata_folder", size=self.size_button), sg.Text(key="metadata_text", size=self.size_text)],   
            ]
        
        scan =[
            [sg.Text("Skanningsmapp", size=self.size_title, font=self.font_bold), sg.Text("I denna mapp kommer skannade betygsfiler hämtas från. Mappen är frivillig att använda.", size=self.size_text)],
            [sg.FolderBrowse("Välj målmapp", key="scan_folder", size=self.size_button), sg.Button("Töm", key="clear"), sg.Text(key="scan_text", size=(45, 2))],
            ]
        
        error =[
            [sg.Text("Fellistemapp", size=self.size_title, font=self.font_bold), sg.Text("I denna mapp kommer troliga dubbletthanterade betyg hamna.", size=self.size_text)],
            [sg.FolderBrowse("Välj målmapp", key="error_folder", size=self.size_button), sg.Text(key="error_text", size=self.size_text)],
            ]

        institution = [
            [sg.Text("Ansvarig institution", size=self.size_title, font=self.font_bold), sg.Input(size=self.size_text, key="institution")], 
            [sg.Text("Här fyller ni in namnet på den organisation som ska ansvara för programmet.", size=self.size_text)],
            ]
        
        schools =[
            [sg.Text("Skolor", size=self.size_title, font=self.font_bold), sg.Input(size=self.size_text, key="schools") ],
            [sg.Text("Här fyller ni i de skolor som kan vara aktuella. Flera skolor skrivs med kommatecken mellan.", size=self.size_text)],
            ]
        
        gradetypes = [
            [sg.Text("Betygstyper", size=self.size_title, font=self.font_bold), sg.Input("Terminsbetyg,Slutbetyg", size=self.size_text, key="gradetypes") ],
            [sg.Text("Här fyller ni i de betygstyper som kan vara aktuella. Flera betygstyper skrivs med kommatecken mellan.", size=self.size_text)],
            ]
        
        max_students = [
            [sg.Text("Max antal elever", size=self.size_title, font=self.font_bold), sg.Input(size=self.size_text, key="max_students")],
            [sg.Text("Här fyller ni i det maxantal av samtida elever som programmet ska kunna hantera. Maxantalet måste vara en siffra.", size=self.size_text)],
            ]

        layout = [
            [sg.Frame("", information, element_justification="Center", expand_x=True, )],
            [sg.Frame("", archive), sg.Frame("", institution)],
            [sg.Frame("", metadata), sg.Frame("", schools)],
            [sg.Frame("", scan), sg.Frame("", gradetypes)],
            [sg.Frame("", error), sg.Frame("", max_students)],
            [sg.Frame("",settings, expand_x=True, element_justification="Center")]
            ]

        window = sg.Window(
            title="Inställningar till betygsdigitaliseringen", 
            layout=layout,
            font=(self.font), 
            icon=self.icon, 
            finalize=True)
        return window, self.error_color
    
    def get_lists(self):
        return self.text_fields, self.data_fields
    
    def show_popup(self, text):
        match text:
            case "check_fields":
                sg.popup(
                    "Fält utan uppgifter har markerats.",
                    "Fyll i de uppgifterna som behövs innan ni sparar inställningarna igen.",
                    icon=self.icon,
                    title="Felmeddelande",
                    )
                
            case "check_folder":
                sg.popup(
                    "Mappen för arkivet och mappen för fellista kan inte vara samma",
                    icon=self.icon,
                    title="Felmeddelande"
                    )
           
            case "check_value":
                sg.popup(
                    "Max antal studenter måste vara skriven med en siffra",
                    icon=self.icon,
                    title="Felmeddelande"
                    )

            case "create_settings":
                sg.popup(
                    "Inställningarna har sparats.",
                    "Allt är nu klart för att börja digitalisera betygen via programmet 'DigitaliseraBetyg'.",
                    "Programmet kommer stängas efter detta.",
                    icon=self.icon,
                    title="Information"
                    )
                
            case "read_settings":
                sg.popup(
                    "Det finns inställningar i inställningsfilen sedan tidigare.",
                    "Inställningarna har hämtats och visas nu i fönstret.",
                    "Tänk extra på om ni ska ändrar någonting nu.",
                    "Det kan innebära behov av att ni genomföra manuella hanteringar i efterhand.",
                    icon=self.icon,
                    title="Information"
                    )   