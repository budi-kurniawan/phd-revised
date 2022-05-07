import matplotlib.pyplot as plt
import numpy as np

x_ticks = ("Thing 1", "Thing 2", "Other thing", "Yet another thing")

x_1 = np.arange(1, 5)
x_2 = x_1 + 0.1

y_1 = np.random.choice(np.arange(1, 7, 0.1), 4)
y_2 = np.random.choice(np.arange(1, 7, 0.1), 4)

err_1 = np.random.choice(np.arange(0.5, 3, 0.1), 4)
print(err_1)

err_1 = []
for i in range(4):
    err_1.append([[1]*1,[2]*1])
err_1 = np.array([(0.25,1), (0.5,1), (1, 1), (1, 2)]).T
err_2 = err_1 
# err_2 = np.random.choice(np.arange(0.5, 3, 0.1), 4)

print('x_1:', x_1, ", y_1:", y_1, ', err_1:', err_1)

plt.errorbar(x=x_1, y=y_1, yerr=err_1, color="black", capsize=3,
             linestyle="None",
             marker="s", markersize=7, mfc="black", mec="black", label="agent1")

plt.errorbar(x=x_2, y=y_2, yerr=err_2, color="green", capsize=3,
             linestyle="None",
             marker="s", markersize=7, mfc="orange", mec="yellow")

print("x_1:", x_1, ", x_ticks:", x_ticks)
plt.xticks(x_1, x_ticks, rotation=90)

plt.legend(loc='lower right')
plt.tight_layout()
plt.show()