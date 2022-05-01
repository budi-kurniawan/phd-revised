import matplotlib.pyplot as plt
import numpy as np
import csv

### Plots relative speeds and distances

t = []
my_speed = []
enemy_speed = []
dx = []

with open("../rl_results/archive/eligibility_traces8.json/independent-tests/test-result-4.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    line_no = 1
    for row in reader:
        line_no += 1
        if line_no > 9: #and line_no < 1000:
            if len(row) == 0:
                break
            t.append(float(row[0]))
            dx.append(float(row[1]))
            my_speed.append(float(row[4]))
            enemy_speed.append(float(row[5]))

print(len(t))
print(len(my_speed))
print(len(enemy_speed))
plt.subplot(2, 1, 1)
plt.plot(t, my_speed, 'b', t, enemy_speed, 'r')
#plt.plot(t, my_speed, enemy_speed, label=['my speed', 'enemy speed'])
plt.xlabel('t')
plt.ylabel('my_speed')
plt.title('Viper and Cobra Speed comparison')
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(t, dx, 'g')
plt.xlabel('t')
plt.ylabel('dx')
plt.title('relative distance')
plt.show()
