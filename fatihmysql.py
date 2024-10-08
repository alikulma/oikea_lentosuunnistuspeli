import mysql.connector
from geopy.distance import geodesic
from random import randint, choice

# Yhteys tietokantaan
connection = mysql.connector.connect(
    host='127.0.0.1',  # localhost
    port=3306,
    database='mpeli',  # Tietokannan nimi
    user='root',
    password='123', # Tietokannan salasana
    autocommit=True,  # Automaattinen commit-toiminto
    collation='utf8mb4_general_ci'  # Merkkien käsittely
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
def get_airports_by_experience(experience):
    if experience == "1":
        sql = "SELECT id FROM airport WHERE iso_country = 'FI' ORDER BY RAND() LIMIT 5"
    elif experience == "2":
        sql = "SELECT id FROM airport WHERE iso_country IN (SELECT iso_country FROM country WHERE continent = 'EU') ORDER BY RAND() LIMIT 5"
    else:
        sql = "SELECT id FROM airport ORDER BY RAND() LIMIT 5"

    cursor.execute(sql)
    return [lentokentta[0] for lentokentta in cursor.fetchall()]


# Onnistuuko käyttäjä, max 50 km virhe sallitaan
def onko_onnistunut(etaisyys, matka):
    return abs(etaisyys - matka) <= 50


# Epäonnistumisen jälkeen käyttäjälle annetaan vinkkejä
def anna_tavsiye(etaisyys, matka):
    ero = etaisyys - matka
    if ero > 0:
        print(f"Olet lentänyt liian vähän, sinun pitäisi lentää noin {abs(ero):.2f} km lisää.")
    else:
        print(f"Olet lentänyt liikaa, sinun pitäisi lentää noin {abs(ero):.2f} km vähemmän.")
    print("Voisit kokeilla pohjoiseen tai itään seuraavaksi!")


# Pisteet tallennetaan tietokantaan
def tallenna_skor(total_km):
    sql = "INSERT INTO highscore (score) VALUES (%s)"
    cursor.execute(sql, (total_km,))
    connection.commit()


# Eniten pisteitä saaneet 3 käyttäjää näytetään
def nayta_top3():
    sql = "SELECT score FROM highscore ORDER BY score ASC LIMIT 3"
    cursor.execute(sql)
    top3 = cursor.fetchall()
    print("\nParhaat 3 tulosta:")
    for idx, score in enumerate(top3, 1):
        print(f"{idx}. {score[0]:.2f} km")


# Peli alkaa
def peli():
    print("Tervetuloa Lentosuunnistuspeliin!")
    nimi = input("Syötä käyttäjänimesi: ")
    print(f"Hei {nimi}, tehtäväsi on lentää viidelle lentokentälle mahdollisimman lyhyillä lentomatkoilla!")

    # Lentokokemuksen taso
    kokemus = input("Syötä lentokokemustaso (1: Perustaso, 2: Keskitaso, 3: Korkea taso): ")

    # Lentokentät haetaan
    lista = get_airports_by_experience(kokemus)
    if not lista:
        print("Lentokenttiä ei löytynyt.")
        return

    total_km = 0  # Kokonaismatka
    attempts_left = 3  # Käyttäjän yritykset

    # Käyttäjä lentää lentokenttien välillä
    for i in range(len(lista) - 1):
        current_airport_id = lista[i]

        current_coords = koordinaatit(current_airport_id)
        current_airport_name = lentokentan_nimi(current_airport_id)

        if not current_coords:
            print("Virhe lentokentän tiedoissa.")
            continue

        print(f"\nNykyinen lentokenttä: {current_airport_name}")

        # Suunta ja matka kysytään käyttäjältä
        while True:
            suunta = input("Mihin suuntaan haluat lentää? (pohjoinen, itä, etelä, länsi): ").lower()
            while suunta not in ["pohjoinen", "itä", "etelä", "länsi"]:
                print("Virheellinen suunta. Syötä vain pohjoinen, itä, etelä tai länsi.")
                suunta = input("Mihin suuntaan haluat lentää? (pohjoinen, itä, etelä, länsi): ").lower()

            try:
                matka = float(input("Kuinka monta kilometriä haluat lentää?: "))
            except ValueError:
                print("Virheellinen syöte. Syötä vain numero.")
                continue

            # Seuraava lentokenttä
            next_airport_id = lista[i + 1]
            next_coords = koordinaatit(next_airport_id)
            next_airport_name = lentokentan_nimi(next_airport_id)

            # Etäisyyden laskeminen
            etaisyys = laske_etaisyys(current_coords[0], current_coords[1], next_coords[0], next_coords[1])

            # Onnistuuko käyttäjä
            if onko_onnistunut(etaisyys, matka):
                print(f"Onnistuit! Olet saapunut lähelle {next_airport_name}, joka on {etaisyys:.2f} km päässä.")
                total_km += matka
                break
            else:
                attempts_left -= 1
                print(f"Epäonnistuit! Sinulla on {attempts_left} yritystä jäljellä.")
                anna_tavsiye(etaisyys, matka)  # Vinkkejä käyttäjälle

                if attempts_left == 0:
                    print("Valitettavasti yrityksesi loppuivat. Älä luovuta, harjoittelu tekee mestarin!")
                    return  # Peli päättyy

    # Skor tallennetaan tietokantaan
    tallenna_skor(total_km)

    print(f"\nOnnittelut! Pääsit kaikille lentokentille. Kokonaismatka: {total_km:.2f} km.")

    # Eniten pisteitä saaneet 3 käyttäjää näytetään
    nayta_top3()


if __name__ == "__main__":
    peli()
# Yhteys tietokantaan suljetaan
cursor.close()
connection.close()
