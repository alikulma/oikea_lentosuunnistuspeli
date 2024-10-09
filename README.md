## ✈️ Tarina ✈️
Olet lentäjä, jonka tehtävänä on suunnistaa maailmalla käyttäen lentokenttiä rasteinasi, samalla kuluttaen mahdollisimman vähän lentokilometrejä. Jos olet aloitteleva lentäjä, voit lentää Suomessa. Jos olet saanut jonkin verran kokemusta, ovat rastit Euroopassa, ja taidokkaimmille lentäjille koko maailma on avoin. Annettuasi nimesi ja lentokokemuksesi määrän saat ensimmäisen rastisi. Sitten pystyt liikkumaan neljään pääilmansuuntaan valitsemasi määrän kilometrejä, kunnes saavut rastille, jolloin saat seuraavan lentokenttäsi. Jos rastin löytämisessä on vaikeuksia, saat suuntavihjeen. Kun vihdoin saavut viimeiselle rastille, saat tietää kuluttamasi lentokilometrit, ja myös miten pärjäsit verrattuna edellisiin suunnistuksiin.

## 🩷 Tietokannan luominen 🩷
Peli käyttää Tietokannat-kurssin flight_game-tietokantaa.
  1. Luo uusi tietokanta "lentosuunnistuspeli": `CREATE DATABASE lentosuunnistuspeli;`
  2. Vaihda tähän tietokantaan: `USE lentosuunnistuspeli;`
  3. Käytä samaa `lp.sql` tiedostoa, jota käytit Tietokannat-kurssilla: `source` ja polku tiedostoon omalla koneella
  4. Käytä taulukoita `airport` ja `country`, poista muut:
      - `SET FOREIGN_KEY_CHECKS = 0;`
      - `DROP TABLE game;`
      - `DROP TABLE goal;`
      - `DROP TABLE goal_reached;`
      - `SET FOREIGN_KEY_CHECKS = 1;`
  5. Luo seuraava taulukko:
     ```
       create table highscore
     (
      id           int auto_increment
          primary key,
      username  varchar(40) null,
      highscore int         null
     )
     charset = latin1;
     ```
  6. Tarkista, että sinulla on tarvittavat taulukot: `SHOW TABLES;`
       - Tuloksen tulisi näyttää tältä:
```
+-------------------------------+
| Tables_in_lentosuunnistuspeli |
+-------------------------------+
| airport                       |
| country                       |
| highscore                     |
+-------------------------------+
```
