import numpy as np
from matplotlib import pyplot as plt
from glob import glob
import pandas as pd
import os


def file_to_array(path):
    with open(path, "rb") as f:
        return np.array(list(f.read()))


def entropy(x, size):
    hist = np.histogram(x, size, (-0.5, size - 0.5))[0] / len(x)
    # plt.plot(hist)
    return -np.sum(hist * np.log2(hist, where=hist > 0))


def combine_tuples(x, num):
    out = np.zeros(x.size - num + 1)
    for i in range(num):
        out += (data[num - i - 1 : -i] if i else data[num - i - 1 :]) * 256**i
    return out


def entropy_combined(x, num, size=256):
    out = np.zeros(x.size - num + 1)
    for i in range(num):
        out += (data[num - i - 1 : -i] if i else data[num - i - 1 :]) * 256**i
    return entropy(out, size**num)


paths = glob("cantrbry/*") + glob("large/*")
# path = paths[0]
# path = "large/world192.txt"

filenames = []
H0s = []
H1s = []
H2s = []

for path in paths:
    data = file_to_array(path)
    H1 = entropy_combined(data, 1)
    H2 = entropy_combined(data, 2)
    H3 = entropy_combined(data, 3)
    filenames.append(os.path.basename(path))
    H0s.append(H1)
    H1s.append(H2 - H1)
    H2s.append(H3 - H2)

    print(
        *([path] + list(map("{:.2f}".format, [H1, H2, H3, H2 - H1, H3 - H2]))), sep="&"
    )

H0s = np.array(H0s)
H1s = np.array(H1s)
H2s = np.array(H2s)

# normalized visualization
# H2s /= H0s
# H1s /= H0s
# H0s /= H0s
plt.subplot(1, 1, 1)
plt.subplots_adjust(bottom=0.25)

bot = plt.bar(filenames, H2s, label="$H(X_i|X_{i-1},X_{i-2})$")
bot = plt.bar(filenames, H1s - H2s, bottom=H2s, label="$H(X_i|X_{i-1})$")
bot = plt.bar(filenames, H0s - H1s, bottom=H1s, label="$H(X_i)$")

plt.tick_params(labelrotation=90)
plt.ylabel("Entropy in bits/symbol")
plt.title("Comparison of Memory")
plt.legend()
plt.show()
