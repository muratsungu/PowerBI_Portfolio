import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

os.makedirs("data", exist_ok=True)

# === Yardımcı Fonksiyonlar ===
def random_dates(start, end, n):
    return [start + timedelta(days=random.randint(0, (end - start).days)) for _ in range(n)]

def create_dim_date(start="2023-01-01", end="2025-12-31"):
    dates = pd.date_range(start, end)
    df = pd.DataFrame({
        "DateKey": range(1, len(dates)+1),
        "Date": dates,
        "Year": dates.year,
        "Month": dates.month,
        "MonthName": dates.strftime("%B"),
        "Quarter": dates.quarter,
        "Weekday": dates.strftime("%A")
    })
    return df

# === DIM TABLOLAR ===
# Dim Branch
branches = [
    {"BranchKey":1, "BranchName":"Istanbul", "City":"Istanbul", "Region":"Marmara"},
    {"BranchKey":2, "BranchName":"Ankara", "City":"Ankara", "Region":"Central Anatolia"},
    {"BranchKey":3, "BranchName":"Izmir", "City":"Izmir", "Region":"Aegean"},
    {"BranchKey":4, "BranchName":"Bursa", "City":"Bursa", "Region":"Marmara"},
    {"BranchKey":5, "BranchName":"Antalya", "City":"Antalya", "Region":"Mediterranean"},
    {"BranchKey":6, "BranchName":"Adana", "City":"Adana", "Region":"Mediterranean"},
    {"BranchKey":7, "BranchName":"Gaziantep", "City":"Gaziantep", "Region":"Southeast Anatolia"},
    {"BranchKey":8, "BranchName":"Trabzon", "City":"Trabzon", "Region":"Black Sea"}
]
dimBranch = pd.DataFrame(branches)

# Dim Product
products = [
    {"ProductKey":1, "ProductName":"Credit Card", "ProductCategory":"Retail Banking"},
    {"ProductKey":2, "ProductName":"Loan", "ProductCategory":"Retail Banking"},
    {"ProductKey":3, "ProductName":"Deposit", "ProductCategory":"Retail Banking"},
    {"ProductKey":4, "ProductName":"Insurance", "ProductCategory":"Wealth"},
    {"ProductKey":5, "ProductName":"Investment", "ProductCategory":"Wealth"},
    {"ProductKey":6, "ProductName":"Corporate Loan", "ProductCategory":"Corporate Banking"}
]
dimProduct = pd.DataFrame(products)

# Dim Customer
n_customers = 3000
dimCustomer = pd.DataFrame({
    "CustomerID": range(1, n_customers+1),
    "CustomerName": [f"Customer_{i}" for i in range(1, n_customers+1)],
    "City": np.random.choice(dimBranch["City"], n_customers),
    "RiskLevel": np.random.choice(["Low","Medium","High"], n_customers, p=[0.6,0.3,0.1]),
    "CustomerSegment": np.random.choice(["Individual","Corporate"], n_customers, p=[0.85,0.15])
})

# Dim Date
dimDate = create_dim_date()

# === FACT TABLOLAR ===

# 1️⃣ Financials (≈ 10,000 satır)
n_fin = 10000
factFinancials = pd.DataFrame({
    "TransactionID": range(1, n_fin+1),
    "DateKey": np.random.randint(1, len(dimDate)+1, n_fin),
    "BranchKey": np.random.randint(1, len(dimBranch)+1, n_fin),
    "ProductKey": np.random.randint(1, len(dimProduct)+1, n_fin),
    "Revenue": np.random.randint(1000, 50000, n_fin),
    "Expense": np.random.randint(500, 30000, n_fin),
    "TransactionCount": np.random.randint(10, 500, n_fin)
})

# 2️⃣ Transactions (≈ 20,000 satır)
n_trans = 20000
factTransactions = pd.DataFrame({
    "TransactionID": range(1, n_trans+1),
    "CustomerID": np.random.randint(1, n_customers+1, n_trans),
    "DateKey": np.random.randint(1, len(dimDate)+1, n_trans),
    "Amount": np.random.randint(10, 100000, n_trans),
    "Channel": np.random.choice(["Online","POS","ATM"], n_trans),
    "TransactionType": np.random.choice(["Payment","Transfer","Deposit","Withdrawal"], n_trans),
    "IsFlagged": np.random.choice([0,1], n_trans, p=[0.94,0.06])
})

# 3️⃣ Data Quality Loads (≈ 5,000 satır)
n_loads = 5000
tables = ["Customer","Account","Transaction","Branch","Product","Loan","Card"]
factDataLoad = pd.DataFrame({
    "LoadID": range(1, n_loads+1),
    "DateKey": np.random.randint(1, len(dimDate)+1, n_loads),
    "TableName": np.random.choice(tables, n_loads),
    "RecordCount": np.random.randint(1000, 200000, n_loads),
    "MissingValues": np.random.randint(0, 5000, n_loads),
    "ErrorCount": np.random.randint(0, 500, n_loads),
    "LoadDurationSeconds": np.random.randint(20, 800, n_loads),
    "LoadStatus": np.random.choice(["Success","Fail"], n_loads, p=[0.9,0.1])
})

# === KAYDET ===
dimDate.to_csv("data/dimDate.csv", index=False)
dimBranch.to_csv("data/dimBranch.csv", index=False)
dimProduct.to_csv("data/dimProduct.csv", index=False)
dimCustomer.to_csv("data/dimCustomer.csv", index=False)

factFinancials.to_csv("data/factFinancials.csv", index=False)
factTransactions.to_csv("data/factTransactions.csv", index=False)
factDataLoad.to_csv("data/factDataLoad.csv", index=False)

print("✅ Tüm mock veri setleri üretildi! 'data/' klasörüne bak:")
print("• dimDate.csv")
print("• dimBranch.csv")
print("• dimProduct.csv")
print("• dimCustomer.csv")
print("• factFinancials.csv")
print("• factTransactions.csv")
print("• factDataLoad.csv")
