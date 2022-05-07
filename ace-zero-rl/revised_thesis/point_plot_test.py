import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset('tips')
print(tips)
sns.pointplot('sex', 'tip', hue='smoker',
    data=tips, dodge=True, join=False)
plt.show()