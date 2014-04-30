# NYC restaurant inspection
Data mining on [NYC restaurant open data](https://data.cityofnewyork.us/data?browseSearch=restaurants)
You can find the accompany article [here](https://docs.google.com/document/d/1t_e0_LnwI5pwWqIuYvJerRd5Fakc-2aPShvKat11ots/edit)
A more detailed description is in the [NYC restaurant data inspection](*)

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

Open *output.txt* you should see the following:
==Frequent itemsets (min_sup=0.7)
frozenset(['pen']) support: 1.0
frozenset(['ink']) support: 0.75
frozenset(['diary']) support: 0.75
frozenset(['pen', 'diary']) support: 0.75
frozenset(['pen', 'ink']) support: 0.75


==High-confidence association rules (min_conf=0.8)
frozenset(['ink'])-->frozenset(['pen']) support: 0.75 confidence: 1.0
frozenset(['diary'])-->frozenset(['pen']) support: 0.75 confidence: 1.0

## INTEGRATED-DATASET Retrieval and association rules Retrieval
Please see [NYC restaurant data inspection](*)

## Design


