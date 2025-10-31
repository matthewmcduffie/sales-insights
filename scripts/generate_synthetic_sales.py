"""
Synthetic Sales Dataset Generator
Author: Matthew McDuffie
Generates a realistic sales dataset with intentional errors and missing values.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Parameters ---
num_rows = 5000
output_file = "../data/synthetic_sales.csv"

# --- Seed for reproducibility ---
random.seed(42)
np.random.seed(42)

# --- Base categories ---
regions = ["East", "West", "North", "South"]
categories = {
    "Office Supplies": ["Binders", "Paper", "Labels", "Storage", "Art"],
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Technology": ["Phones", "Accessories", "Machines", "Copiers"]
}
segments = ["Consumer", "Corporate", "Home Office"]
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

# --- Helper: random date between 2020–2024 ---
def random_date():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# --- Generate rows ---
data = []
for i in range(num_rows):
    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])
    region = random.choice(regions)
    segment = random.choice(segments)
    shipmode = random.choice(ship_modes)
    order_id = f"ORD-{i+10000}"
    order_date = random_date()
    sales = round(np.random.gamma(2, 200), 2)  # skewed toward smaller sales
    quantity = random.randint(1, 10)
    discount = round(random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5]), 2)
    margin = random.uniform(0.05, 0.3)
    profit = round((sales - discount * sales) * margin, 2)
    returned = random.choice(["Yes"] * 1 + ["No"] * 9)
    comment = random.choice(
        [None, "Delayed shipment", "Customer requested refund", "Damaged box", None, "Expedited delivery"]
    )

    data.append(
        [order_id, order_date, region, category, subcategory, f"{subcategory} {i}", sales,
         quantity, discount, profit, segment, returned, shipmode, comment]
    )

columns = [
    "OrderID", "OrderDate", "Region", "Category", "SubCategory", "ProductName",
    "Sales", "Quantity", "Discount", "Profit", "CustomerSegment",
    "Returned", "ShipMode", "Comments"
]

df = pd.DataFrame(data, columns=columns)

# --- Add intentional errors and missing data ---
# Randomly blank out some numeric values
for col in ["Sales", "Profit"]:
    df.loc[df.sample(frac=0.05).index, col] = np.nan

# Break some dates
broken_indices = df.sample(frac=0.03).index
df.loc[broken_indices, "OrderDate"] = "NotADate"

# Randomly lowercase some regions
df.loc[df.sample(frac=0.1).index, "Region"] = df["Region"].str.lower()

# Shuffle the rows
df = df.sample(frac=1).reset_index(drop=True)

# --- Save ---
df.to_csv(output_file, index=False)
print(f"✅ Synthetic dataset created with {len(df)} rows at {output_file}")
