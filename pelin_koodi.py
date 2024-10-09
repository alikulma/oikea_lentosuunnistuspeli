import mysql.connector
from geopy.distance import geodesic
from tabulate import tabulate
from turtle import *

# Yhteys tietokantaan
connection = mysql.connector.connect(
    host='127.0.0.1',  # localhost
    port=3306,
    database='lentosuunnistuspeli',  # Tietokannan nimi
    user='käyttäjä',
    password='salasana',  # Tietokannan salasana
    autocommit=True,  # Automaattinen commit-toiminto
)

# Luodaan yksi kursori
cursor = connection.cursor()


# Lentokentän koordinaatit haetaan ID:n perusteella
def koordinaatit(id):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE id = '{id}';"
    cursor.execute(sql)
    return cursor.fetchone()


# Lentokentän nimi haetaan ID:n perusteella
def lentokentan_nimi(id):
    sql = f"SELECT name FROM airport WHERE id = '{id}';"
    cursor.execute(sql)
    tulos = cursor.fetchone()
    return tulos[0] if tulos else None


# Kahden lentokentän välinen etäisyys lasketaan
def laske_etaisyys(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km


# Kokemustason perusteella lentokentät haetaan
def arvo_lentokentat(experience):
    if experience == "1":
        sql = "SELECT id FROM airport WHERE iso_country = 'FI' ORDER BY RAND() LIMIT 5"
    elif experience == "2":
        sql = "SELECT id FROM airport WHERE iso_country IN (SELECT iso_country FROM country WHERE continent = 'EU') ORDER BY RAND() LIMIT 5"
    else:
        sql = "SELECT id FROM airport ORDER BY RAND() LIMIT 5"
    cursor.execute(sql)
    return [lentokentta[0] for lentokentta in cursor.fetchall()]


# Score tallennetaan tietokantaan
def tallenna_score(nimi, kokonaismatka):
    sql = f"INSERT INTO highscore (username, highscore) VALUES ('{nimi}', '{kokonaismatka}');"
    cursor.execute(sql)
    connection.commit()


# Parhaat tulokset tulostetaan
def nayta_top():
    sql = "SELECT username, highscore FROM highscore ORDER BY highscore ASC"
    cursor.execute(sql)
    top = cursor.fetchall()
    head = ["Käyttäjä", "Kilometrit"]
    print("Parhaat tulokset:")
    print(tabulate(top, headers=head, tablefmt="fancy_grid"))

# Piirtää sydämen turtlella
def sydan():
    speed(2)
    bgcolor("black")
    color("red")
    pensize(3)
    begin_fill()
    left(50)
    forward(133)
    circle(50, 200)
    right(140)
    circle(50, 200)
    forward(133)
    end_fill()
    done()

# Peli alkaa
def peli():
    print("Tervetuloa Lentosuunnistuspeliin!")
    nimi = input("Syötä käyttäjänimesi: ")
    print(f"Hei {nimi}, tehtäväsi on lentää viidelle lentokentälle mahdollisimman lyhyillä lentomatkoilla!")

    # Lentokokemuksen taso
    kokemus = input("Syötä lentokokemustaso (1: Perustaso, 2: Keskitaso, 3: Korkea taso): ")

    # Lentokentät haetaan
    lista = arvo_lentokentat(kokemus)
    if not lista:
        print("Lentokenttiä ei löytynyt.")
        return

    kokonaismatka = 0

    # Käyttäjä lentää lentokenttien välillä
    for i in range(len(lista) - 1):
        lentokentan_id_nyt = lista[i]
        sijainti_nyt = koordinaatit(lentokentan_id_nyt)
        leveys_nyt = sijainti_nyt[0]
        pituus_nyt = sijainti_nyt[1]
        lentokentan_nimi_nyt = lentokentan_nimi(lentokentan_id_nyt)

        if not sijainti_nyt:
            print("Virhe lentokentän tiedoissa.")
            continue

        # Seuraava lentokenttä
        lentokentan_id_seuraava = lista[i + 1]
        sijainti_seuraava = koordinaatit(lentokentan_id_seuraava)
        leveys_seuraava = sijainti_seuraava[0]
        pituus_seuraava = sijainti_seuraava[1]
        lentokentan_nimi_seuraava = lentokentan_nimi(lentokentan_id_seuraava)

        # Etäisyyden laskeminen
        etaisyys = laske_etaisyys(leveys_nyt, pituus_nyt, leveys_seuraava, pituus_seuraava)

        print(f"Olet tällä hetkellä lentokentällä {lentokentan_nimi_nyt}.")
        print(f"Seuraava rastisi on {lentokentan_nimi_seuraava}.")
        print(f"Etäisyys rastille on {etaisyys:.2f} kilometriä.")
        print("")

        # Suunta ja matka kysytään käyttäjältä
        while True:
            suunta = input("Syötä, mihin pääilmansuuntaan haluat lentää (pohjoinen, itä, etelä, länsi): ").lower()
            while suunta not in ["pohjoinen", "itä", "etelä", "länsi", "luovutan"]:
                print("Virheellinen suunta. Syötä vain pohjoinen, itä, etelä tai länsi.")
                suunta = input("Mihin suuntaan haluat lentää? (pohjoinen, itä, etelä, länsi): ").lower()

            try:
                matka = float(input("Syötä, kuinka pitkälle haluat lentää kilometreinä (esim. 100): "))
            except ValueError:
                print("Virheellinen syöte. Syötä vain numero.")
                continue

            kokonaismatka += matka

            # sijainnin muutos
            if suunta == "pohjoinen":
                leveys_nyt = leveys_nyt + (matka / 110.574)
            elif suunta == "etelä":
                leveys_nyt = leveys_nyt - (matka / 110.574)
            elif suunta == "länsi":
                pituus_nyt = pituus_nyt - (matka / 111.320)
            elif suunta == "itä":
                pituus_nyt = pituus_nyt + (matka / 111.320)

            # pelaajan uusi etäisyys
            etaisyys = laske_etaisyys(leveys_nyt, pituus_nyt, leveys_seuraava, pituus_seuraava)

            # rasti löytyy tai ei löydy
            if etaisyys < 10:
                print("Löysit lentokentän!")
                break
            else:
                print("Et ole löytänyt lentokenttää.")
                print(f"Etäisyys rastille on {etaisyys:.2f} kilometriä.")
                ero1 = (leveys_nyt - leveys_seuraava) * 110.574
                ero2 = (pituus_nyt - pituus_seuraava) * 111.320

                # suuntavinkki, jos lentokenttää ei löydy
                if abs(ero1) > abs(ero2):
                    if ero1 > 5:
                        print("Vinkki: Kokeile lentää etelään.")
                        print("")
                    elif ero1 < -5:
                        print("Vinkki: Kokeile lentää pohjoiseen.")
                        print("")
                elif abs(ero2) > abs(ero1):
                    if ero2 < -5:
                        print("Vinkki: Kokeile lentää itään.")
                        print("")
                    elif ero2 > 5:
                        print("Vinkki: Kokeile lentää länteen.")
                        print("")

    # Highscore tallennetaan
    tallenna_score(nimi, kokonaismatka)

    print(f"Onnittelut! Olet päässyt maaliin. Lensit {kokonaismatka:.2f} kilometriä.")

    # Eniten pisteitä saaneet käyttäjät näytetään
    nayta_top()

    # Piirtää sydämen :)
    sydan()

# suorittaa pelin
if __name__ == "__main__":
    peli()

# Yhteys tietokantaan suljetaan
cursor.close()
connection.close()