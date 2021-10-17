import matplotlib.pyplot as plt
import numpy as np

wielo = (0, -3, -5, 0, 1) # wspolczynniki wielomianu od tylu
der = (-3, -10, 0, 4) # wspolczynniki pochodnej wielomianu od tylu
beta = 0.01 # wspolczynnik uczenia
start = 3 # punkt startowy
limit = 0.001 # limit wielkosci kroku, zeby metoda skonczyla prace, bo znalazla minimum

# liczy wartosc wielomianu w podanym punkcie
def licz_wielo(wielo, x):
	suma = 0
	for i in range(len(wielo)):
		suma += wielo[i] * (x ** i)
	return suma

run = True
now = start
points = [start]
counter = 0
while run:
	counter += 1
	deriv = licz_wielo(der, now)
	add = deriv * beta
	now -= add
	points.append(now)

	# stop
	if abs(add) < limit or counter > 1000:
		run = False

print("Minimum lokalne: ", now)
print("Liczba krokow: ", counter)

x = np.arange(-3, 3.3, 0.1)
y = licz_wielo(wielo, x)

pointsy = []
for i in range(len(points)):
	pointsy.append(licz_wielo(wielo, points[i]))

plt.plot(x, y)
plt.plot(points, pointsy, 'ro-')
plt.show()
