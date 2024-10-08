from geopy import distance
from random import randint, choice
import mysql.connector

# Luo yhteys MySQL-tietokantaan
connection = mysql.connector.connect(
    host='localhost',
    user='narges',
    password='Qam2016',
    database='lentosuunnistuspeli',
    charset='utf8mb4',
    collation='utf8mb4_general_ci'
)


def koordinaatit(id):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE id = {id};"
    kursori = connection.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos[0] if tulos else None


def lentokentan_nimi(id):
    sql = f"SELECT name FROM airport WHERE id = {id};"
    kursori = connection.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos[0][0] if tulos else None


def rastit(lentokokemus):
    lentokentat = []
    # Perustason pelaajille valitaan vain Suomessa olevat lentokentät
    # Keskitasolle vain Euroopassa
    # Korkealle tasolle kaikki lentokentät
    if lentokokemus == 1:
        # Esimerkin vuoksi käytetään vain ensimmäisiä kenttiä Suomessa
        for i in range(5):
            numero = randint(1, 500)  # Oletetaan, että 1-500 ovat Suomessa
            lentokentat.append(numero)
    elif lentokokemus == 2:
        for i in range(5):
            numero = randint(501, 1500)  # Esimerkki Euroopan kentistä
            lentokentat.append(numero)
    else:
        for i in range(5):
            numero = randint(1, 70942)  # Kaikki kentät
            lentokentat.append(numero)
    return lentokentat


def etsi_lentokentta(rasti, suunta, matka, nykyinen_kohde):
    # Oletetaan, että nykyinen_kohde on käyttäjän viimeisin sijainti (alkupiste)
    # Suunta ja matka käsitellään täällä (voisit lisätä matemaattiset laskelmat)
    uusi_kohde = nykyinen_kohde # Tämä olisi laskettu uusi sijainti
    return uusi_kohde  # Tässä on vain yksinkertaistettu paluu


# Aloitus
print("Tervetuloa Lentosuunnistuspeliin!")

nimi = input("Syötä käyttäjänimesi: ")
print(f"Hei {nimi}! Tehtävänäsi on suunnistaa maailmalla lentokoneellasi.")

kokemus = int(input("Syötä lentokokemuksesi taso (1: alle 1 vuosi, 2: 1-10 vuotta, 3: yli 10 vuotta): "))
lista = rastit(kokemus)
nykyinen_kohde = koordinaatit(lista[0])  # Alustetaan ensimmäinen lentokenttä

for i, rasti in enumerate(lista):
    rasti_nimi = lentokentan_nimi(rasti)
    print(f"Ensimmäinen rastisi on {rasti_nimi}!")

    while True:
        suunta = input("Mihin pääilmansuuntaan haluat lentää (pohjoinen, itä, etelä, länsi): ").lower()
        matka = int(input("Syötä, kuinka pitkälle haluat lentää kilometreinä: "))

        # Matkan laskeminen (tätä tulisi kehittää)
        nykyinen_kohde = etsi_lentokentta(rasti, suunta, matka, nykyinen_kohde)

        # Oletetaan, että olet nyt kohdassa nykyinen_kohde
        etaisyys = distance.distance(nykyinen_kohde, koordinaatit(rasti)).km

        if etaisyys < 5:
            print(f"Olet saapunut {rasti_nimi} lentokentälle!")
            break
        else:
            print(f"Olet {etaisyys:.2f} km päässä {rasti_nimi}. Yritä uudelleen.")

# Pelin lopputulos
print("Peli päättyi! Kiitos pelaamisesta!")