# Standardmoduler.
import sys

# Tredjepartsmoduler.
import FreeSimpleGUI as sg

# Egna, lokala moduler.
from Data import Data
from DigitaliseraBetygSettings import DigitaliseraBetygSettings


class DigitaliseraBetygGUI:
    def __init__(self):
        sg.theme(Data.theme())
    
    def gui_error(self, error_list):
            """Felrättningsfönstret för programmet."""
            layout = [[sg.Text("Följande fel upptäcktes som behöver rättas innan programmet öppnas igen:")]]
            for row in error_list:
                 layout.append([sg.Text(row)])
            window = sg.Window(title="Felinformation", layout=layout, font=Data.font("grade"), icon=Data.path_icon())
            while True:
                event, values = window.read()
                match event:
                    case sg.WIN_CLOSED: break
            window.close()
            sys.exit()

    def gui_main(self):
            """Huvudfönstret för programmet"""
            metadata = Data.metadata_grade()
            metadata_size = Data.metadata_grade_size()
            data = Data()
            schools = data.schools()
            gradetypes = data.gradetypes()
            forms = data.forms()
            max_students = data.max_students()
            folder_scan = data.folder_scan()
            institution = data.institution()
            del data

            category = [[sg.Text(data, size=size) for data, size in zip(metadata, metadata_size)]]
            fields= [[
                sg.Text(student+1, size=(3)), 
                sg.Input(key=f"{student}{metadata[1]}", visible=False, size=metadata_size[1]), 
                sg.Input(key=f"{student}{metadata[2]}", visible=False, size=metadata_size[2]), 
                sg.Input(key=f"{student}{metadata[3]}", visible=False, size=metadata_size[3]),
                sg.Input(key=f"{student}{metadata[4]}", visible=False, size=metadata_size[4]), 
                sg.Combo(gradetypes, key=f"{student}{metadata[5]}", visible=False, size=metadata_size[5]-1), 
                sg.Combo(schools, key=f"{student}{metadata[6]}", visible=False, size=metadata_size[6]-1), 
                sg.Combo(forms, key=f"{student}{metadata[7]}", visible=False, size=metadata_size[7]-1), 
                ] for student in range(max_students)]
            layout_grade = [
                [sg.FileBrowse("Hämta betygsfil", file_types=(("", ".pdf"),), initial_folder=folder_scan, 
                                target="file_path", enable_events=True), 
                    sg.Input(key="file_path", font=Data.font("output"), expand_x=True, enable_events=True, readonly=True, 
                             disabled_readonly_background_color=sg.theme_background_color()), 
                    sg.Button("Visa betygsfil", key="open_file", enable_events=True)],
                [sg.Column(category)],
                [sg.Column(fields)],
                [sg.Button("Digitalisera betyg"), sg.Push(), sg.Button("Avsluta")],
                [sg.Output(key="output", size=(None, 5), expand_x=True, font=Data.font("output"))],
                ]  
              
            layout_help = [
                [sg.Text("1. Skanna så många betyg som ni känner att ni vill hantera samtidigt. " \
                 f"Dock inte så att sidantalet i den skannade filen överstiger {max_students} sidor.")], 
                [sg.Text("2. Tänk på att betygen måste vara en sida vardera, " \
                "programmet kan inte hantera flersidiga individuella betyg.")],
                [sg.Text("3. Hämta pdf-filen med inskannade betyg via 'Hämta betygsfil'.")],
                [sg.Text("4. Programmet kommer försöka hämta information från betygen och placera dessa i rätt fält.")], 
                [sg.Text("5. Den hämtade pdf-filen kan visas i webbläsaren via 'Visa betygsfilen'. " \
                "ID:t för varje elev är samma som sidan i pdf-filen.")],
                [sg.Text("6. Fyll i resterande fält med rätt uppgifter, " \
                "samt säkerställ att de uppgifter som programmet hämtade är korrekta.")], 
                [sg.Text("7. När samtliga fält är ifyllda, välj 'Digitalisera betyg'.")],
                ]
            
            layout = [[sg.TabGroup([[sg.Tab("Digitalisera betyg", layout_grade), sg.Tab("Hjälp", layout_help)]])]]  
            window = sg.Window(title=f"{institution} - Digitalisera betyg", layout=layout, font=Data.font("grade"), 
                               icon=Data.path_icon(), finalize=True)
            
            # Löser en bugg där text efter val i combomenyn är dold bakom heltäckande färg. 
            # Outlinen av markeringen är dock kvar.
            # Lösningen är hämtad från https://stackoverflow.com/a/73225157.
            style = sg.ttk.Style()
            for student in range(max_students):
                for data in metadata[5:]:
                    style.configure(window[f"{student}{data}"].widget.configure()['style'][-1], 
                                    selectforeground=sg.theme_input_text_color())

            return window


if __name__ == "__main__":
     pass
