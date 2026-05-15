# Tredjepartsmoduler.
import FreeSimpleGUI as sg

# Egna, lokala moduler.
from Data import Data


class DigitaliseraBetygSettingsGUI:
    def __init__(self):
        sg.theme(Data.theme())
        self.icon = Data.path_icon()
        self.font_bold = Data.font("settings_bold")
        self.size_title = (15, 1)
        self.size_text = (50, 1)

    def main(self):
        metadata = Data.metadata_settings()
        settings = [
            [sg.Text("Skanningsmapp", size=self.size_title, font=self.font_bold, pad=10),
                sg.FolderBrowse("Välj målmapp", key=metadata[0], target=f"text{metadata[0]}"), 
                sg.Button("Töm", key="folder_scan_clear"), sg.Text(key=f"text{metadata[0]}", expand_x=True)],
            [sg.Text("Arkivmapp", size=self.size_title, font=self.font_bold, pad=10),
                sg.FolderBrowse("Välj målmapp", key=metadata[1], target=f"text{metadata[1]}"), 
                sg.Text(key=f"text{metadata[1]}", expand_x=True)], 
            [sg.Text("Dubblettmapp", size=self.size_title, font=self.font_bold, pad=10),
                sg.FolderBrowse("Välj målmapp", key=metadata[2], target=f"text{metadata[2]}"), 
                sg.Text(key=f"text{metadata[2]}", expand_x=True)],
            [sg.Text("Ansvarig institution", size=self.size_title, font=self.font_bold, pad=10), 
                sg.Input("Kommunarkivet", size=(30), key=metadata[3]), 
                sg.Text("Max antal elever", size=self.size_title, font=self.font_bold, pad=10), 
                sg.Input("10", size=(5), key=metadata[4])],
            [sg.Text("Skolor", size=self.size_title, font=self.font_bold, pad=10), 
                sg.Input("Abbaskolan,Bebbe Carlskolan", size=self.size_text, key=metadata[5])],
            [sg.Text("Betygstyper", size=self.size_title, font=self.font_bold, pad=10), 
                sg.Input("Terminsbetyg,Slutbetyg", size=self.size_text, key=metadata[6])],
            [sg.Text("Skolformer", size=self.size_title, font=self.font_bold, pad=10), 
                sg.Input("Grundskola,Gymnasieskola,Komvux", size=self.size_text, key=metadata[7])],
            [sg.Push(), sg.Button("Spara inställningarna", size=(20, 2), font=self.font_bold), sg.Push()]
            ]   
        help = [
            [sg.Text("Här fyller ni i de inställningar som ska användas av huvudprogrammet DigitaliseraBetyg.",)],
            [sg.Text("Arkivmapp", font=self.font_bold), 
                sg.Text("är den plats där betygsfilerna med tillhörande metadatafil kommer placeras.")],
            [sg.Text("Dubblettmapp", font=self.font_bold), 
                sg.Text("är den plats där antagna dubbletter av betyg med tillhörande metadatafil kommer placeras.")],
            [sg.Text("Skanningsmapp", font=self.font_bold), 
                sg.Text("är den standardmapp som programmet startar i när användaren hämtar skannade betyg.")],
            [sg.Text("  Skanningsmappen kan vara tom.")],
            [sg.Text("Ansvarig institution", font=self.font_bold), 
                sg.Text("är den verksamhet som nyttjar systemet.")],
            [sg.Text("  Exempelvis Abbakommunens kommunarkiv.")],
            [sg.Text("Max antal elever", font=self.font_bold), 
                sg.Text("är det maxantal rader som programmet simultant kan hantera.")],
            [sg.Text("  Testa er fram för finna lämpligt antal för den skärm som kommer att användas.")],
            [sg.Text("  Max antal elever måste vara en siffra.")],
            [sg.Text("Skolor, Betygstyper, Skolfomer", font=self.font_bold), 
                sg.Text("kan vara en eller flera föremål som är aktuella för er kommun.")],
            [sg.Text("  Vid flera föremål ska dessa separeras med ett kommatecken, exempelvis:")],
            [sg.Text("      Abbaskolan,Bebbe Carlskolan,Dahlskolan")],
            ]
        layout = [[sg.TabGroup([[sg.Tab("Inställningar", settings), sg.Tab("Hjälp", help)]])]]
        window = sg.Window(title="Inställningar till DigitaliseraBetyg", layout=layout, font=Data.font("settings"),
                           icon=self.icon, finalize=True)
        return window
    
    def show_popup(self, text):
        match text:
            case "check_fields":
                sg.popup(
                    "Fält utan uppgifter har markerats.",
                    icon=self.icon, title="Felmeddelande")
                
            case "check_folder":
                sg.popup(
                    "Mappen för arkivet och mappen för dubbletter kan inte vara samma.",
                    icon=self.icon, title="Felmeddelande")
           
            case "check_value":
                sg.popup(
                    "Max antal studenter måste vara en siffra",
                    icon=self.icon, title="Felmeddelande")

            case "create_settings":
                sg.popup(
                    "Inställningarna har sparats.",
                    "Allt är nu klart för att börja digitalisera betygen via programmet 'DigitaliseraBetyg'.",
                    "Programmet kommer stängas efter detta.",
                    icon=self.icon, title="Information")
                
            case "read_settings":
                sg.popup(
                    "Det finns inställningar i befintlig inställningsfil, vilka har hämtats och visas nu i fönstret.",
                    "Tänk extra noga om ni ska ändrar någonting nu, vilket kan innebära behov av manuella rättelser.",
                    icon=self.icon, title="Information")   
                
            case "OSError":
                sg.popup(
                    "Programmet saknar skrivrättigheter till någon av de mappar ni har valt.",
                    "Kontakta systemansvarig eller er IT-enhet för undersökning av felet.",
                    icon=self.icon, title="Felmeddelande")   
                
                
if __name__ == "__main__":
    pass
