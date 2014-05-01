pip install numpy --user
pip install optparse --user
# Run test file
python apriori.py -f "datasets/test.txt" -s 0.7 -c 0.8
# Run on INTEGRATED DATASET
python apriori.py -f "datasets/INTEGRATED-DATASET.csv" -s 0.7 -c 0.8