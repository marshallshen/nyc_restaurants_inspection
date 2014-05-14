# NYC restaurant inspection
Data mining upon NYC restaurant open data

## What are inlcuded:
1. Apriori algoithm in Python
2. INTEGRATED-DATASET under folder "datasets"
3. Original datasets from NYC open data website
3. "example_run.txt" that includes a sample result
4. A detailed report that explains how data is processed, algorithm is applied, and analysis of some interesting association rules.
5. [Blogpost](BLOG.md) on how the analysis of the NYC restaurant data

## Usage

Run apriori algorithm on INTEGRATED-DATASET.csv
------------------------------------------------
Inside the directory, run the following command: (support is 0.7, confident is 0.8)
```
python apriori.py -f "datasets/INTEGRATED-DATASET.csv" -s 0.7 -c 0.8
```

Then the output should be saved inside *output.txt*


Run apriori algorithm on test.txt
-------------------------------------------------
To test the correctness of the alogrithm using simpler cases, given the test file: "datasets/test.txt"
```
python apriori.py -f "datasets/test.txt" -s 0.7 -c 0.8
```

==Frequent itemsets (min_sup=0.7)

	['pen'] support: 1.0
	['ink'] support: 0.75
	['diary'] support: 0.75
	['pen', 'diary'] support: 0.75
	['pen', 'ink'] support: 0.75


==High-confidence association rules (min_conf=0.8)

	['ink']-->['pen'] support: 0.75 confidence: 1.0
	['diary']-->['pen'] support: 0.75 confidence: 1.0

## INTEGRATED-DATASET Retrieval and association rules Retrieval
Please see "NYC_Restaurant_Data_Inspection" for details

