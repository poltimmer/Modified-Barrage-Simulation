import matplotlib.pyplot as plt
import pandas as pd

select = 0
if select == 0:
    means = [
        [45.7149, 45.4877, 45.7461, 49.8541],
        [44.9846, 44.7645, 45.0311, 48.6717],
        [45.6971, 46.0479, 45.173, 49.5754],
        [44.1077, 43.8225, 44.1603, 48.9137],
        [44.06, 43.6011, 44.298, 49.4272]
    ]
    errors = [
        [0.135, 0.195, 0.194, 0.563],
        [0.137, 0.2, 0.194, 0.607],
        [0.131, 0.184, 0.191, 0.61],
        [0.131, 0.189, 0.188, 0.622],
        [0.139, 0.205, 0.195, 0.61]
    ]
    columns = ['Any', 'General', 'Scout', 'Marshall', 'Spy']
    indices = ['Overall', 'Red wins', 'Blue wins', 'Tie']
    ylabel = "Average number of moves"
else:
    means = [
        [48.94, 48.74, 2.32, 1.52],
        [48.21, 49.54, 2.25, 2.36],
        [49.04, 48.80, 2.16, 1.48],
        [48.24, 49.44, 2.32, 1.74],
        [50.08, 47.76, 2.16, 0.66]
    ]
    errors = [
        [0.50, 0.50, 0.15, 0.12],
        [0.50, 0.50, 0.15, 0.15],
        [0.50, 0.50, 0.15, 0.12],
        [0.50, 0.50, 0.15, 0.13],
        [0.50, 0.50, 0.15, 0.08]
    ]
    columns = ['Any', 'General', 'Scout', 'Marshall', 'Spy']
    indices = ['Red wins', 'Blue wins', 'Tie', 'Both spies survive']
    ylabel = 'Chance (%)'


def reorder(arr):
    return [[row[i] for row in arr] for i in range(4)]


means = reorder(means)
errors = reorder(errors)

df = pd.DataFrame(means)
er = pd.DataFrame(errors)

print(df)
print("=")
print(er)

df.columns = columns
er.columns = columns
df.index = indices
er.index = indices

ax = df.plot(kind="bar", yerr=er)
ax.set_ylabel(ylabel)
plt.xticks(rotation=0)
plt.legend(title="First move with", loc="lower left")
plt.savefig('graph-export.svg')
plt.show()
