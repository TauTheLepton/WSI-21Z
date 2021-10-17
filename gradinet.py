import matplotlib.pyplot as plt
import numpy as np

# odwrotnie
wielo = (1, -8, 3)
der = (-8, 6)
# 0.1 jest ok, 0.3 zygzakuje
beta = 0.1
start = 10
limit = 0.001

def licz_wielo(wielo, x):
	suma = 0
	for i in range(len(wielo)):
		suma += wielo[i] * (x ** i)
	return suma

run = True
now = start
points = []
counter = 0
while run:
	counter += 1
	deriv = licz_wielo(der, now)
	add = deriv * beta
	now -= add
	points.append(now)

	# stop
	if abs(add) < limit or counter > 100:
		run = False

print("Minimum lokalne: ", now)
print("Liczba krokow: ", counter)

x = np.arange(-10, 10, 1)
y = licz_wielo(wielo, x)

pointsy = []
for i in range(len(points)):
	pointsy.append(licz_wielo(wielo, points[i]))

plt.plot(x, y)
plt.plot(points, pointsy, 'ro-')
plt.show()
