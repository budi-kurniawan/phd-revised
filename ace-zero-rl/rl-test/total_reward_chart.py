import matplotlib.pyplot as plt
import csv

x = []
y = []

scenario = 'ac2d5A-008.json'
with open('../rl_results/' + scenario + '/viper-all-scores.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(float(row[1]) + 0.5)

plt.plot(x,y, label='Total rewards')
plt.xlabel('Episode')
plt.ylabel('Total reward')
plt.title('Total rewards  for ' + scenario)
#plt.legend()
plt.show()