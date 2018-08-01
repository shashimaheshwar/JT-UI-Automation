import csv


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    for row in reader:
        print(" ".join(row))


if __name__ == "__main__":
    csv_path = "InputData/TestData.csv"
    with open(csv_path, "rb") as f_obj:
        reader=csv.reader(fi)