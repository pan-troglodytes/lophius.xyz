import math
import numpy as np
radius = 400
x = []
y = []
offsetX = 860
offsetY = 440
for i in np.arange(0, 361, 3.6):
    x.append(radius * math.cos(i * math.pi / 180))
    y.append(radius * math.sin(i * math.pi / 180))
print("@keyframes circle {")
for i in range(len(x)):
    print("%d%% {left: %fpx; top: %fpx;}" % (i, x[i]+offsetX, y[i]+offsetY))
print("}")
