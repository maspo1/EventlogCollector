import pandas as pd
import matplotlib.pyplot as plt
import random

# Generate random product data
products = [f'Product {i}' for i in range(1, 51)]
optimal_stock = [random.randint(30, 120) for _ in range(50)]
current_stock = [random.randint(10, int(optimal * 0.5)) for optimal in optimal_stock]

# Create a data frame
data = {
    'Product': products,
    'Optimal Stock Level': optimal_stock,
    'Current Stock': current_stock
}
df = pd.DataFrame(data)

# Extract 5 data points with current stock level < 50% of optimal stock level
condition = df['Current Stock'] < (df['Optimal Stock Level'] * 0.5)
selected_data = df[condition].sample(n=5)

# Create the graph
plt.figure(figsize=(10, 6))
ax = selected_data.plot(kind='bar', x='Product', y=['Optimal Stock Level', 'Current Stock'], color=['b', 'r'], alpha=0.7)
selected_data.plot(kind='bar', x='Product', y='Current Stock', color='r', alpha=0.8, ax=ax)
plt.xlabel('Product')
plt.ylabel('Stock Quantity')
plt.title('Optimal Stock Levels and Current Stock Quantities by Product (Selected Data)')
plt.xticks(rotation=45)
plt.legend(['Optimal Stock Level', 'Current Stock'])
plt.tight_layout()

# Highlight x-axis labels for selected data
for tick in ax.get_xticklabels():
    if tick.get_text() in selected_data['Product'].tolist():
        tick.set_weight("bold")

# Show the graph
plt.show()
