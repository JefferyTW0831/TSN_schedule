import matplotlib.pyplot as plt
import numpy as np

# Define the data
data = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
 
]

rows = ['(D6, SW4)']
columns = [ 'T1', 'T2', 'T3', 'T4', 'T5', 'T15', 'T16', 'T23', 'T24', 'T25', 'T26']

# Create the plot
fig, ax = plt.subplots(figsize=(8, 8))

# Hide axes
ax.axis('off')

# Create table
table = ax.table(cellText=data,
                 rowLabels=rows,
                 colLabels=columns,
                 cellLoc='center',
                 loc='center')

# Set font size
table.set_fontsize(10)
table.scale(1, 1.5)

# Color the cells
for i in range(len(rows)):
    for j in range(len(columns)):
        cell = table[i+1, j]
        if data[i][j] == 'F1':
            cell.set_facecolor('orange')
        elif data[i][j] == 'F2':
            cell.set_facecolor('lightgreen')
        elif data[i][j] == 'F3':
            cell.set_facecolor('yellow')

# Add deadline labels
ax.text(0.5, 1.05, 'Deadline = F2', transform=ax.transAxes, ha='center')
ax.text(0.85, 1.05, 'Deadline = F1, F3', transform=ax.transAxes, ha='center')

plt.title('Task Schedule', fontsize=16)
plt.tight_layout()
plt.show()