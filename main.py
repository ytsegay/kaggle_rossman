__author__ = 'ytsegay'

import csv

def main():
    # read training file and match it to the stores file
    with open("data/store.csv", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            print row


if __name__ == "__main__":
    main()
