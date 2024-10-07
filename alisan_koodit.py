from geopy import distance
from random import randint
import mysql.connector

yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='lentosuunnistuspeli',
    user='käyttäjänimi',
    password='salasana',
    autocommit=True
)

def koordinaatit(id):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE id = '{id}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def lentokentan_nimi(id):
    sql = f"SELECT name FROM airport WHERE id = '{id}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def rastit():
    lentokentat = []
    for i in range(5):
        numero = randint(1, 70942)
        lentokentat.append(numero)
    return lentokentat


print("Tervetuloa Lentosuunnistuspeliin!")

nimi = input("Syötä käyttäjänimesi: ")

print(f"Hei {nimi}! Tehtävänäsi on suunnistaa maailmalla lentokoneellasi käyttäen lentokenttiä rasteina.")
print(f"Ensin syötät lentokokemuksesi määrän, jonka jälkeen annamme sinulle viisi lentokenttää kierrettäväksi.")
print(f"Tavoitteenasi on lentää kuluttaen mahdollisimman vähän lentokilometrejä.")

kokemus = input("Syötä lentokokemuksesi taso (1: alle 1 vuosi, 2: 1-10 vuotta, 3: yli 10 vuotta): ")

lista = rastit()
rasti = str(lentokentan_nimi(lista[0]))
print(f"Ensimmäinen rastisi on {rasti}!")

print("Nyt syötä, mihin pääilmansuuntaan haluat lentää (pohjoinen, itä, etelä, länsi).")
suunta = input("Lentosuunta: ")
print("Syötä, kuinka pitkälle haluat lentää kilometreinä (esim. 100).")
matka = input("Matka: ")