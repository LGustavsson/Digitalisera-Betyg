# Digitalisera Betyg
Skapa arkiv med tillhörande metadatafil av digitaliserade betygsdokument.

Programmet kan hanera valfritt samtida ensidiga betyg upp till en vafri maxgräns
<img width="1081" height="700" alt="image" src="https://github.com/user-attachments/assets/eabfe738-778a-45ae-beb5-80101168e9fb" />

Detta genererar ett arkiv med metadatafil och samtliga hantera betyg
<img width="592" height="88" alt="image" src="https://github.com/user-attachments/assets/1d7a531b-d7e0-4d7b-91cc-1f219f1adb07" />

Där metadatafilen kan användas för databearbetning, sökning för utlämnande, och som ostrukturerad data vid leverans till e-arkiv. 
<img width="1305" height="78" alt="image" src="https://github.com/user-attachments/assets/255b224c-6576-49c3-9703-241ff24ab74d" />

# Beskrivning
Detta programstöd har framarbetats i huvudsakligt syfte att kunna erbjuda arbetstränande ett jobb att genomföra via er lokala arbetsmarknadsenhet.
Programmet utgår därmed från att vara så enkelt som möjligt, att kunna hjälpa till så mycket som möjligt med att hämta data, samt att kunna erbjuda en valfrihet i arbetsbelastning.
Programmet har därmed inte som huvudsaklig användare arkivpersonal eller andra kunniga inom området, utan är tänkt att fungera för en som är oinsatt. 

För de arkivorganisationer som inte har behov av detta programstöd som riktar sig till de som behöver extra hjälp, 
så kan jag tipsa om Andrew Tutt-Wixners framtagna programstöd "DigiBetyg" som kan häntas här: [DigiBetyg](https://archivetools.itch.io/digiarchive).

Programmet fungerar så att ett antal betyg skannas in till en pdf-fil. Betygen måste vara ensidiga då programmet inte kan hantera att enskilda betygsdokument är flersidiga. Programmet hämtar den skannade filen, slår ut sidorna till en sida per betyg och elev. Den information som matas in sparas i en metadatafil tillsammans med den enskilda betygsdokumentet. 

# Förberedelser
1. Ladda ner den senaste releasen av Digitalisera-Betyg.
2. Packa upp zip-filen på den dator som ska hantera och använda applikationen.
3. Fyll i nödvändig information i programmet "DigitaliseraBetygSettings".

# Hur programmet används
1. Starta Digitalisera-Betyg med "DigitaliseraBetyg.exe".
2. Skanna så många betyg som ni känner att ni vill hantera på samma gång. Dock inte så att sidantalet i det enskilda betyget är fler än en, samt att den skannade filen inte överstiger sedan tidigare överenskomna maxantalet sidor. 
4. Hämta pdf-fil med inskannade betyg via "Hämta betygsfil".
5. Programmet kommer försöka hämta information från betygen och placera dessa i rätt fält. Var vaksam ifall informationen som hämtats är korrekt eller ej. 
6. Fyll i samtliga fält med rätt uppgifter. 
7. Den hämtade pdf-filen kan visas i webbläsaren via "Visa betygsfil".
8. När samtliga fällt är ifyllda, kontrollera att de är korrekta, därefter välj "Digitalisera betyg".

# Credits
Programmet har framarbetats av Linus Gustavsson, linus.gustavsson.1@gmail.com.
Ikonen är hämtad från - [https://icon-icons.com/icon/archive/125380](https://icon-icons.com/icon/archive/125380)

# Creative Commons License
![image](https://github.com/user-attachments/assets/22d24ea9-5ecc-4e4f-be3a-0e51860bfb22)
This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).  
