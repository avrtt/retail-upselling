This project is a part of my work on association rule mining; it demonstrates a pipeline for market basket analysis aimed at identifying product associations to optimize retail promotions and bundle deals. Although the project was designed using a real company's dataset, the provided example uses simulated data.

Tools:
- **Python** with `mlxtend` for association rule mining; `pandas`, `json`, `random`
- **SQLite** to simulate a real-world database storing transactional data
- **D3.js** for network graph visualization of the product associations

## Structure

```
.
├── README.md
├── main.py
├── d3_visualization.html
└── data
    └── (generated SQLite DB and JSON output files)
```

- **main.py** contains the Python code to generate example transaction data, store it in an SQLite database, apply the Apriori algorithm to extract frequent itemsets and association rules, and generate a JSON file for network visualization
- **d3_visualization.html**: a D3.js based HTML file that loads the generated JSON data and displays a network graph of product associations
- **data/**: directory where the SQLite database (`transactions.db`) and the JSON file (`associations.json`) are saved

## Features

1. **Data generation and SQL storage**
   - simulated transactional data is created with random transactions and a list of example products
   - the transactions are stored in an SQLite database to mimic a real-world scenario
   - a SQL query retrieves the transactions to feed the association rule mining process

2. **Association rule mining part**
   - the Apriori algorithm (from the mlxtend package) is applied on one-hot encoded transaction data
   - association rules are extracted based on defined support, confidence and lift thresholds

3. **Visualization part**
   - the extracted rules (with single-item antecedents and consequents) are converted into a network graph JSON format
   - the D3.js visualization uses force-directed graph techniques to display nodes (products) and edges (associations), allowing interactive exploration of the results

## How to run

1. Ensure you have Python3 and install the required packages:
     ```bash
     pip install pandas mlxtend
     ```

2. Execute:
    ```bash
    python main.py
    ```

3. To view the visualization, open `d3_visualization.html` in your browser. Ensure the JSON file `associations.json` is in the same directory or adjust the file path in the HTML file accordingly.

## Notes

- The simulated data in this project is for demonstration purposes only
- Parameters for the Apriori algorithm (such as support and confidence thresholds) can be adjusted in `main.py` to fine-tune the association rule mining process.

## License
MIT