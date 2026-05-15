import configparser
import os


class Data:
    """Samlar standardiserad data för hämtning mellan olika kodfiler."""
    def __init__(self):
        self.settings = configparser.ConfigParser(allow_no_value=True)
        self.settings.read(Data.path_settings(), encoding="UTF-8")

    def version():
        """Programversionen."""
        return "V2" 
    
    def metadata_grade_size():
        """Storleken på GUI-fälten för aktuella datamängder. Ska vara exakt lika med "metadata_grade"."""
        return [
            3,  #0 ID
            20, #1 Namn
            13, #2 Personnummer
            6, #3 År
            6,  #4 Klass
            12,  #5 Betygstyp  
            15,  #6 Skola
            15, #7 Skolform
            ]

    def metadata_grade():
        """Både GUI-fält och uppgifter i metadatafilen."""
        return [
            "ID",   #0
            "Namn", #1
            "Personnummer", #2
            "År",   #3
            "Klass",    #4
            #Combofält
            "Betygstyp",    #5
            "Skola",    #6
            "Skolform", #7
            ]
    
    def metadata_system():
        """De första kolumnerna i metadatafilen."""
        return [
            "Mappsökväg",
            "Filnamn",
            ]
    
    def metadata_settings():
        """Datamängderna i Settings-programmet."""
        return [
            # Mappar
            "folder_scan",     #0 Denna är först så den kan hoppas över.
            "folder_archive",  #1
            "folder_double",    #2
            # Inputfält.
            "institution",     #3
            "max_students",    #4
            # Inputfält listor
            "schools",         #5
            "gradetypes",      #6
            "forms",           #7
            ]   

    def file_metadata():
        """Filnamnet på metadatafilen."""
        return f"_Digitaliserade_Betyg_{Data.version()}_Metadata.csv"

    def file_double():
        """Filnamnet på metadatafilen för dubbletter."""
        return f"_Digitaliserade_Betyg_{Data.version()}_DubbletterMetadata.csv"   
    
    def folder_settings():
        """Mappsökväg till Settings-filen."""
        return rf"{os.path.dirname(__file__)}\Settings"
    
    def folder_archive(self):
        """Mappsökväg till arkivmappen."""
        return self.settings["DEFAULT"]["folder_archive"].replace("/", os.path.sep)
    
    def folder_scan(self):
        """Mappsökväg till skanningsmappen."""
        return self.settings["DEFAULT"]["folder_scan"]
    
    def folder_double(self):
        """Mapp sökväg till dubblettmappen."""
        return self.settings["DEFAULT"]["folder_double"].replace("/", os.path.sep)
    
    def path_settings():
        """Direkt sökväg till Settings-filen."""
        return os.path.join(Data.folder_settings(), "Settings.ini")
    
    def path_metadata(self):
        """Direkt sökväg till metadata-filen."""
        return os.path.join(self.folder_archive(), Data.file_metadata())
    
    def path_double(self):
        """Direkt sökväg till metadata-filen för dubbletter."""
        return os.path.join(self.folder_double(), Data.file_double())
    
    def path_icon():
        """Direkt sökväg till programikonen."""
        return os.path.join(f"{os.path.dirname(__file__)}", "icon.ico")

    def institution(self):
        """Ansvarig institution för programmet."""
        return self.settings["DEFAULT"]["institution"]
    
    def max_students(self):
        """Max antal samtida elever, vilket är lika med max antal samtida visade rader i programmet."""
        return int(self.settings["DEFAULT"]["max_students"])
    
    def gradetypes(self):
        """Lista med valbara betygstyper."""
        return self.settings["DEFAULT"]["gradetypes"].split(",")
    
    def schools(self):
        """Lista med valbara skolor."""
        return self.settings["DEFAULT"]["schools"].split(",")
    
    def forms(self):
        """Lista med valbara skolformer."""
        return self.settings["DEFAULT"]["forms"].split(",")
    
    def color_error():
        """Hexkod för färg som visas på fält som behöver rättas i programmet."""
        return "#f0b6a4"
    
    def theme():
        """Färgtemat för programmet."""
        #https://user-images.githubusercontent.com/46163555/202543904-e7fefe99-2c02-4e58-9a97-ef0724aa4d8a.png
        return "SandyBeach"
    
    def font(destination):
        """Standardfonten för programmet."""
        match destination:
            case "grade":
                return ("arial", "12" ,"normal")
            case "output":
                return ("arial", "10", "normal")
            case "settings":
                return ("arial", "10", "normal")
            case "settings_bold":
                return ("arial", "10", "bold")
    

if __name__ == "__main__":
    pass