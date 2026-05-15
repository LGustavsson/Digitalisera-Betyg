# Digitalisera Betyg
Digitalisera skannade betyg via lättanvänt gränsnitt.

<img width="1210" height="686" alt="image" src="https://github.com/user-attachments/assets/204dda44-ff67-4b75-8ee5-e21d1bdd321d" />

Via användarifyllda uppgifter genereras ett arkiv med metadatafil och samtliga hantera betyg.

<img width="342" height="145" alt="image" src="https://github.com/user-attachments/assets/117fc521-eb72-4a8f-969d-dd8691d5096e" />

Där metadatafilen kan användas för databearbetning, sökning för utlämnande, och som ostrukturerad data vid leverans till e-arkiv. 

<img width="1587" height="47" alt="image" src="https://github.com/user-attachments/assets/281688c4-9b05-423e-9e95-f3642538032c" />

# Beskrivning
Detta programstöd har framarbetats i huvudsakligt syfte att kunna erbjuda arbetstränande ett jobb att genomföra via er lokala arbetsmarknadsenhet.
Programmet utgår därmed från att vara så enkelt som möjligt, att kunna hjälpa till så mycket som möjligt med att hämta data, samt att kunna erbjuda en valfrihet i arbetsbelastning.
Programmet har därmed inte som huvudsaklig användare arkivpersonal eller andra kunniga inom området, utan är tänkt att fungera för en som är oinsatt, ooh är av samma anledning inte framarbetad i syfte att kunna masshantera snabbt. 

För de arkivorganisationer som inte har behov av detta programstöd, som riktar sig till de som behöver extra hjälp, 
så kan jag tipsa om Andrew Tutt-Wixners framtagna programstöd "DigiBetyg" som kan häntas här: [DigiBetyg](https://archivetools.itch.io/digiarchive).

Programmet fungerar så att ett antal betyg skannas in till en pdf-fil. Betygen måste vara ensidiga då programmet inte kan hantera att enskilda betygsdokument är flersidiga. Programmet hämtar den skannade filen, slår ut sidorna till en sida per betyg. Den information som matas in sparas i en metadatafil tillsammans med den enskilda betygsdokumentet. 

# Förberedelser
1. Ladda ner den senaste releasen av Digitalisera-Betyg.
2. Packa upp zip-filen på den dator som ska hantera och använda applikationen.
3. Fyll i nödvändig information i programmet "DigitaliseraBetygSettings".

# Hur programmet används
1. Skanna så många betyg som ni känner att ni vill hantera på samma gång. Dock inte så att sidantalet i det enskilda betyget är fler än en, samt att den skannade filen inte överstiger sedan tidigare överenskomna maxantalet sidor.
2. Starta Digitalisera-Betyg med "DigitaliseraBetyg.exe".
3. Hämta pdf-fil med inskannade betyg via "Hämta betygsfil".Den hämtade pdf-filen kan visas i webbläsaren via "Visa betygsfil".
4. Programmet kommer försöka hämta information från betygen och placera dessa i rätt fält. Var vaksam ifall informationen som hämtats är korrekt eller ej. 
5. Fyll i samtliga fält med rätt uppgifter och kontrollera att uppgifterna är korrekta.
6. Välj "Digitalisera betyg" för att spara alla uppgifter i metadatafilen samt spara betygen som enskilda filer.

# Credits
Programmet har framarbetats av Linus Gustavsson, linus.gustavsson.1@gmail.com.

Ikonen är hämtad från [https://icon-icons.com/icon/archive/125380](https://icon-icons.com/icon/archive/125380)

# Creative Commons License
Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
