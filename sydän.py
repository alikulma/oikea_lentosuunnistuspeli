from turtle import *

# Asetukset
speed(2)  # Piirtämisen nopeus
bgcolor("black")  # Taustaväri
color("red")  # Sydämen väri
pensize(3)  # Viivan paksuus

# Piirretään sydän
begin_fill()  # Alkaa täyttää sydäntä
left(50)  # Käännetään vasemmalle 50 astetta
forward(133)  # Piirretään ensimmäinen viiva

circle(50, 200)  # Piirretään ympyrän kaari
right(140)  # Käännytään oikealle
circle(50, 200)  # Piirretään toinen ympyrän kaari

forward(133)  # Piirretään viimeinen viiva
end_fill()  # Sydän täytetään

# Lopetetaan piirto
done()