# -------------------------------
# 1. IMPORT LIBRARIES
# -------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import os   # ✅ Needed for folder handling

# -------------------------------
# 2. CREATE REQUIRED FOLDERS
# -------------------------------
os.makedirs("visualizations", exist_ok=True)  
# ✅ Fixes your previous error (folder not found)

# -------------------------------
# 3. LOAD DATA (ERROR HANDLING)
# -------------------------------
try:
    df = pd.read_csv("sales_data.csv")
    print("✅ Data loaded successfully!")
except FileNotFoundError:
    print("❌ File not found. Check file path.")
    exit()

# -------------------------------
# 4. DATA CLEANING
# -------------------------------
print("\n🔍 Missing Values:\n", df.isnull().sum())

df.dropna(inplace=True)  # ✅ remove null values

# Convert Date column properly
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop invalid dates (if any)
df.dropna(subset=['Date'], inplace=True)

# -------------------------------
# 5. FEATURE ENGINEERING
# -------------------------------
df['Month'] = df['Date'].dt.month  # ✅ Needed for trend analysis

# -------------------------------
# 6. DATA ANALYSIS
# -------------------------------
product_sales = df.groupby('Product')['Total_Sales'].sum()
region_sales = df.groupby('Region')['Total_Sales'].sum()
monthly_sales = df.groupby('Month')['Total_Sales'].sum()

# Debug check (VERY IMPORTANT)
print("\n📊 DEBUG DATA:")
print("Product Sales:\n", product_sales)
print("Region Sales:\n", region_sales)
print("Monthly Sales:\n", monthly_sales)

# -------------------------------
# 7. INSIGHTS (PLACED BEFORE PLOTS)
# -------------------------------
print("\n📌 KEY INSIGHTS:")

try:
    if not product_sales.empty:
        print(f"✔ Top selling product: {product_sales.idxmax()}")

    if not region_sales.empty:
        print(f"✔ Region with highest sales: {region_sales.idxmax()}")

    if not monthly_sales.empty:
        print(f"✔ Month with highest sales: {monthly_sales.idxmax()}")

except Exception as e:
    print("❌ Error in insights:", e)

# -------------------------------
# 8. VISUALIZATION
# -------------------------------

# 🔵 Bar Chart - Product Sales
plt.figure()
product_sales.plot(kind='bar')
plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/product_sales.png")
plt.show()

# 🟢 Line Chart - Monthly Trend
plt.figure()
monthly_sales.plot(kind='line', marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.grid()
plt.tight_layout()
plt.savefig("visualizations/monthly_sales.png")
plt.show()

# 🟡 Pie Chart - Region Sales (FIXED VERSION)
plt.figure()

if not region_sales.empty:
    plt.pie(region_sales.values,
            labels=region_sales.index,
            autopct='%1.1f%%',
            startangle=90)
    
    plt.title("Sales Distribution by Region")
    plt.axis('equal')  # ✅ makes perfect circle

    plt.savefig("visualizations/region_sales.png")
    plt.show()
    print("✅ Pie chart generated successfully!")
else:
    print("❌ No data available for pie chart")

# -------------------------------
# 9. FINAL MESSAGE
# -------------------------------
print("\n🎯 Project completed successfully!")