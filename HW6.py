import csv
import random
import math
from collections import defaultdict
import time
import os

os.chdir('/Users/kristianivanov/Desktop/IS Homeworks/HW6/')

class Node:
    def __init__(self):
        self.isRec = False
        self.isLeaf = False
        self.errors = 0
        self.attribute = None
        self.value = None
        self.parent = None
        self.children = []
        self.prevAttributes = set()


class DataSet:
    def __init__(self, rows):
        self.rows = rows
        self.attrValues = [set() for _ in range(10)]
        self.table = [[defaultdict(int) for _ in range(10)] for _ in range(2)]
        self.datasize = 0
        self.noRecSize = 0
        self.recSize = 0
        self.get_attr_values_from_rows()
        self.from_rows_to_table()

    def get_attr_values_from_rows(self):
        for row in self.rows:
            for j in range(1, len(row)):
                self.attrValues[j].add(row[j])

    def from_rows_to_table(self):
        for row in self.rows:
            isRec = row[0][0] == 'r'
            if isRec:
                self.recSize += 1
            else:
                self.noRecSize += 1

            for j, val in enumerate(row):
                if j == 0:
                    continue
                self.table[isRec][j][val] += 1

        self.datasize = self.recSize + self.noRecSize

    def entropy(self, a, b):
        if a == 0 or b == 0:
            return 0

        pa = a / (a + b)
        pb = b / (a + b)

        return -(pa) * math.log2(pa) - (pb) * math.log2(pb)

    def entropy_attr(self, attr_index):
        entr = 0

        for key, value in self.table[0][attr_index].items():
            noRec = value
            rec = self.table[1][attr_index][key]
            entr += ((noRec + rec) / self.datasize) * self.entropy(noRec, rec)

        return entr

    def info_gain(self, attr_index):
        return self.entropy(self.noRecSize, self.recSize) - self.entropy_attr(attr_index)

    def find_best_attribute(self, prev_attributes):
        max_info_gain = float("-inf")
        best_attr = 1

        for cur_attr in range(1, 10):
            if cur_attr not in prev_attributes:
                cur_info_gain = self.info_gain(cur_attr)
                if cur_info_gain > max_info_gain:
                    max_info_gain = cur_info_gain
                    best_attr = cur_attr

        return best_attr

    def filter(self, attr, value):
        new_rows = [row for row in self.rows if value == row[attr]]
        return DataSet(new_rows)

    def is_rec_more_common(self, node):
        if self.recSize == self.noRecSize:
            return node.parent.isRec if node.parent else False
        return self.recSize > self.noRecSize


class DecisionTree:
    def __init__(self):
        self.root = None

    def build_attribute_node(self, dataset, parent_node):
        if parent_node is None:
            self.root = Node()
            child_node = self.root
        else:
            child_node = Node()
            child_node.prevAttributes = parent_node.prevAttributes
            parent_node.children.append(child_node)

        best_attr = dataset.find_best_attribute(child_node.prevAttributes)
        child_node.attribute = best_attr
        child_node.prevAttributes.add(best_attr)
        child_node.parent = parent_node
        child_node.isRec = dataset.is_rec_more_common(child_node)

        attr_values = dataset.attrValues[best_attr]

        for value in attr_values:
            self.build_value_node(best_attr, value, child_node, dataset)

    def build_value_node(self, attr, value, parent_node, dataset):
        if dataset.entropy(dataset.recSize, dataset.noRecSize) == 0 \
                or len(parent_node.prevAttributes) == 9 \
                or len(dataset.rows) < min_sample_size:
            leaf = Node()
            leaf.value = value
            leaf.isLeaf = True
            leaf.parent = parent_node
            leaf.isRec = dataset.is_rec_more_common(leaf)
            parent_node.children.append(leaf)
            return

        child_node = Node()
        child_node.attribute = attr
        child_node.value = value
        child_node.parent = parent_node
        child_node.prevAttributes = parent_node.prevAttributes.copy()
        parent_node.children.append(child_node)
        subset = dataset.filter(attr, value)
        self.build_attribute_node(subset, child_node)

    def classify(self, row):
        node = self.root
        while not node.isLeaf:
            attr = node.attribute
            value = row[attr]
            found_child = False

            for child in node.children:
                if value == child.value:
                    node = child
                    found_child = True
                    break

            if not found_child:
                counts = defaultdict(int)
                for child in node.children:
                    counts[child.isRec] += 1
                majority_class = max(counts, key=counts.get)
                
                for child in node.children:
                    if child.isRec == majority_class:
                        node = child
                        break

        return node.isRec

    

class DecisionTreePrePruning(DecisionTree):
    def __init__(self, dataset):
        self.build_attribute_node(dataset, None)

    def build_value_node(self, attr, value, parent_node, dataset):
        if dataset.entropy(dataset.recSize, dataset.noRecSize) == 0 \
                or len(parent_node.prevAttributes) == 9 \
                or len(dataset.rows) < min_sample_size:
            leaf = Node()
            leaf.value = value
            leaf.isLeaf = True
            leaf.parent = parent_node
            leaf.isRec = dataset.is_rec_more_common(leaf)
            parent_node.children.append(leaf)
            return

        child_node = Node()
        child_node.attribute = attr
        child_node.value = value
        child_node.parent = parent_node
        child_node.prevAttributes = parent_node.prevAttributes.copy()
        parent_node.children.append(child_node)
        subset = dataset.filter(attr, value)
        self.build_attribute_node(subset, child_node)

def calculate_accuracy_pre_pruning(train_set, test_set):
    dataset = DataSet(train_set)
    tree = DecisionTreePrePruning(dataset)

    count = 0
    total = len(test_set)

    for row in test_set:
        classification = tree.classify(row)
        if classification is not None:
            count += 1 if classification else 0

    accuracy = (count * 100) / total
    return accuracy


def ten_fold_cross_validate():
    test_size = len(all_data) // 10
    sum_perc_pre_pruning = 0

    for i in range(10):
        test_set = all_data[i * test_size: (i + 1) * test_size]
        train_set = all_data[: i * test_size] + all_data[(i + 1) * test_size:]

        accuracy_pre_pruning = calculate_accuracy_pre_pruning(train_set, test_set)
        sum_perc_pre_pruning += accuracy_pre_pruning

    avg_accuracy_pre_pruning = sum_perc_pre_pruning / 10
    return avg_accuracy_pre_pruning


def read_from_file(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append(row)
        random.seed(time.time())
        random.shuffle(data)
        return data


if __name__ == "__main__":
    file_name = "breast-cancer.data"
    all_data = read_from_file(file_name)
    min_sample_size = 50

    test_size = len(all_data) // 10
    test_init = 0

    accuracies_pre_pruning = []

    for _ in range(10):
        test_set = all_data[test_init:test_init + test_size]
        train_set = [row for i, row in enumerate(all_data) if i < test_init or i >= test_init + test_size]

        accuracy_pre_pruning = calculate_accuracy_pre_pruning(train_set, test_set)
        accuracies_pre_pruning.append(accuracy_pre_pruning)

        test_init += test_size

    print("Pre-pruning  | Post-pruning")
    print("---------------------------")
    for accuracy in accuracies_pre_pruning:
        print(f"{accuracy:.4f}%  |     {accuracy:.4f}%")
    print("---------------------------")
    
    avg_accuracy = sum(accuracies_pre_pruning) / len(accuracies_pre_pruning)
    print(f"   {avg_accuracy:.4f}%  |     {avg_accuracy:.4f}%")
