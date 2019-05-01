from matplotlib import pyplot as plt

plt.switch_backend('agg')
fig = plt.figure(figsize=(10,6))
x = [1,2,3]

plt.plot(x, x)
plt.show()
fig.savefig("filename.png")
