import math
import numpy as np
print("@keyframes sine {")
amplitude = 300
offsetX = -150
offsetY = 300
j=0
for i in np.arange(-1000, 2122, 31.21):
    print("%d%% {left:%dpx; top:%fpx;}" % (j, i + offsetX, (math.sin(i)*amplitude)+offsetY))
    j=j+1
print("}")
