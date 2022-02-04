import numpy as np
from matplotlib import pyplot as plt
from glob import glob


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


paths = glob("cantrbry/*")
# path = paths[0]
# path = "large/world192.txt"

for path in paths:
    data = file_to_array(path)
    H1 = entropy_combined(data, 1)
    H2 = entropy_combined(data, 2)
    H3 = entropy_combined(data, 3)
    print(path, H1, H2, H3, sep="\t")
