print("Tervetuloa Lentosuunnistuspeliin!")

nimi = input("Syötä käyttäjänimesi: ")

print(f"Hei {nimi}! Tehtävänäsi on suunnistaa maailmalla lentokoneellasi käyttäen lentokenttiä rasteina.")
print(f"Ensin syötät lentokokemuksesi määrän, jonka jälkeen annamme sinulle viisi lentokenttää kierrettäväksi.")
print(f"Tavoitteenasi on lentää kuluttaen mahdollisimman vähän lentokilometrejä.")

kokemus = input("Syötä lentokokemuksesi taso (1: alle 1 vuosi, 2: 1-10 vuotta, 3: yli 10 vuotta): ")

print("Nyt syötä, mihin pääilmansuuntaan haluat lentää, ja kuinka monta kilometriä. Esimerkki: 100 km länteen")
lento = input("Lentosuunta: ")