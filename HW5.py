import csv
import random
import math
import os

os.chdir('/Users/kristianivanov/Desktop/IS Homeworks/HW5/')

entries = []
data_sets = []

republicans = [[0] * 16 for _ in range(3)]
democrats = [[0] * 16 for _ in range(3)]

rep_counter = 0
dem_counter = 0

def transform_data(data_set):
    global rep_counter, dem_counter, republicans, democrats
    for row in data_set:
        is_republican = row[0] == "republican"
        if is_republican:
            rep_counter += 1
        else:
            dem_counter += 1

        for i in range(1, 17):
            val = row[i]
            if val == "y":
                if is_republican:
                    republicans[0][i - 1] += 1
                else:
                    democrats[0][i - 1] += 1
            elif val == "n":
                if is_republican:
                    republicans[1][i - 1] += 1
                else:
                    democrats[1][i - 1] += 1
            elif val == "?":
                if is_republican:
                    republicans[2][i - 1] += 1
                else:
                    democrats[2][i - 1] += 1

def calculate_accuracy(test_set):
    global rep_counter, dem_counter, republicans, democrats
    lambda_val = 1
    correct = 0

    for row in test_set:
        is_republican = row[0] == "republican"
        p_republican = 0
        p_democrat = 0

        for i in range(1, 17):
            val = row[i]
            if val == "y":
                p_republican += math.log((republicans[0][i - 1] + lambda_val) / (rep_counter + 2 * lambda_val))
                p_democrat += math.log((democrats[0][i - 1] + lambda_val) / (dem_counter + 2 * lambda_val))
            elif val == "n":
                p_republican += math.log((republicans[1][i - 1] + lambda_val) / (rep_counter + 2 * lambda_val))
                p_democrat += math.log((democrats[1][i - 1] + lambda_val) / (dem_counter + 2 * lambda_val))
            elif val == "?":
                p_republican += math.log((republicans[2][i - 1] + lambda_val) / (rep_counter + 2 * lambda_val))
                p_democrat += math.log((democrats[2][i - 1] + lambda_val) / (dem_counter + 2 * lambda_val))

        p_republican += math.log(rep_counter / (rep_counter + dem_counter))
        p_democrat += math.log(dem_counter / (rep_counter + dem_counter))

        if is_republican and p_republican > p_democrat:
            correct += 1
        elif not is_republican and p_democrat > p_republican:
            correct += 1

    accuracy = correct / len(test_set) * 100
    print(f"Correct: {correct}/{len(test_set)} -> {accuracy}%")
    return accuracy

def count_entries(test_set):
    reps = sum(1 for row in test_set if row[0] == "republican")
    print(f"Republicans: {reps}, Democrats: {len(test_set) - reps}")

def main():
    with open('house-votes-84.data', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            entries.append(row)

    chunk_size = len(entries) // 10
    for _ in range(10):
        test_set = []
        for _ in range(chunk_size):
            test_set.append(entries.pop(random.randint(0, len(entries) - 1)))
        data_sets.append(test_set)
        count_entries(test_set)

    test_index = 0
    overall_accuracy = 0

    for _ in range(10):
        for j in range(10):
            if j == test_index:
                continue
            transform_data(data_sets[j])

        overall_accuracy += calculate_accuracy(data_sets[test_index])
        test_index += 1

        republicans = [[0] * 16 for _ in range(3)]
        democrats = [[0] * 16 for _ in range(3)]
        rep_counter = 0
        dem_counter = 0

    print(f"\nOverall accuracy: {overall_accuracy / 10}%")

if __name__ == "__main__":
    main()
