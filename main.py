import os
import sqlite3
import random
import json
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# create data directory if not exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# list of example products
products = [
    'Milk', 'Bread', 'Eggs', 'Butter', 'Cheese', 'Apples', 'Bananas',
    'Chicken', 'Beef', 'Fish', 'Rice', 'Pasta', 'Tomatoes', 'Onions', 'Lettuce'
]

# generate random transactions
num_transactions = 200 
transactions = []
for i in range(num_transactions):
    # each transaction has between 1 and 5 random items
    num_items = random.randint(1, 5)
    transaction = random.sample(products, num_items)
    transactions.append(transaction)

db_path = os.path.join(DATA_DIR, "transactions.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# create table
cursor.execute("DROP TABLE IF EXISTS transactions")
cursor.execute("""
    CREATE TABLE transactions (
        transaction_id INTEGER,
        product TEXT
    )
""")

# insert each transaction as multiple rows
transaction_rows = []
for t_id, transaction in enumerate(transactions, 1):
    for product in transaction:
        transaction_rows.append((t_id, product))

cursor.executemany("INSERT INTO transactions (transaction_id, product) VALUES (?, ?)", transaction_rows)
conn.commit()

# retrieve data using SQL
query = "SELECT transaction_id, product FROM transactions ORDER BY transaction_id"
df_sql = pd.read_sql_query(query, conn)
conn.close()

# group by transaction_id to reconstruct transactions
grouped = df_sql.groupby('transaction_id')['product'].apply(list)
transactions_from_db = grouped.tolist()

# convert transactions to one-hot encoded df
te = TransactionEncoder()
te_array = te.fit(transactions_from_db).transform(transactions_from_db)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)

# apply Apriori algorithm with a minimum support threshold
min_support = 0.05 
frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)

# generate association rules
min_confidence = 0.3 
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

# prepare data for D3.js visualization
filtered_rules = rules[(rules['antecedents'].apply(lambda x: len(x)) == 1) & 
                       (rules['consequents'].apply(lambda x: len(x)) == 1)]

# prepare nodes and links for network graph
nodes = set()
links = []

for idx, row in filtered_rules.iterrows():
    antecedent = next(iter(row['antecedents']))
    consequent = next(iter(row['consequents']))
    nodes.add(antecedent)
    nodes.add(consequent)
    link = {
        "source": antecedent,
        "target": consequent,
        "confidence": row['confidence'],
        "lift": row['lift']
    }
    links.append(link)

nodes_list = [{"id": node} for node in nodes]
graph = {"nodes": nodes_list, "links": links}

# save the network graph as JSON for D3.js
json_path = os.path.join(DATA_DIR, "associations.json")
with open(json_path, "w") as f:
    json.dump(graph, f, indent=4)

print(f"Association graph JSON saved to {json_path}")