import configparser

def create_settings_file(path, settings):
    # Initiera config-filen.
    config = configparser.ConfigParser(allow_no_value=True)
    config["DEFAULT"] = {} 
    
    # Skriver in inställningsnamnen och den ifyllda datan. 
    for key, value in settings.items():
        config["DEFAULT"][key] = value

    # Sparar inställningsfilen.
    with open(path, mode='w', encoding="UTF-8") as config_file:
        config.write(config_file)