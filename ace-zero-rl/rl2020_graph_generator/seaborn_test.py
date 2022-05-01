import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

#sns.set_theme(style="whitegrid")
tips = sns.load_dataset("tips")
ax = sns.boxplot(x="day", y="total_bill", hue="smoker",
                 data=tips, palette="Set3")
print(type(tips))

plt.show()
