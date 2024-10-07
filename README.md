## Tarina
Olet lentäjä, jonka tehtävänä on suunnistaa maailmalla käyttäen lentokenttiä rasteinasi, samalla kuluttaen mahdollisimman vähän lentokilometrejä.
## Tietokannan luominen
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
