import random
import time


def put_queens(n, queens, r, d1, d2):
    col = 1
    for row in range(n):
        queens[col] = row
        r[row] += 1
        d1[col - row + n - 1] += 1
        d2[col + row] += 1

        col += 2
        if col >= n:
            col = 0        


def col_with_queen_with_max_conf(n, queens, r, d1, d2):
    max_conf = -1
    cols_with_max_conf = []

    for cur_col in range(n):
        cur_row = queens[cur_col]
        cur_conf = r[cur_row] + d1[cur_col - cur_row + n - 1] + d2[cur_col + cur_row] - 3
        if cur_conf == max_conf:
            cols_with_max_conf.append(cur_col)
        elif cur_conf > max_conf:
            max_conf = cur_conf
            cols_with_max_conf = [cur_col]

    if max_conf == 0:
        return None
    return random.choice(cols_with_max_conf)


def row_with_min_conf(col, n, queens, r, d1, d2):
    min_conf = n + 1
    rows_with_min_conf = []

    for cur_row in range(n):
        if queens[col] == cur_row:
            cur_conf = r[cur_row] + d1[col - cur_row + n - 1] + d2[col + cur_row] - 3
        else:
            cur_conf = r[cur_row] + d1[col - cur_row + n - 1] + d2[col + cur_row]

        if cur_conf == min_conf:
            rows_with_min_conf.append(cur_row)
        elif cur_conf < min_conf:
            min_conf = cur_conf
            rows_with_min_conf = [cur_row]

    return random.choice(rows_with_min_conf)


def update_state(n, row, col, queens, r, d1, d2):
    prev_row = queens[col]
    r[prev_row] -= 1
    d1[col - prev_row + n - 1] -= 1
    d2[col + prev_row] -= 1

    queens[col] = row
    r[row] += 1
    d1[col - row + n - 1] += 1
    d2[col + row] += 1


def print_queens(n, queens):
    for i in range(n):
        for j in range(n):
            print("* " if queens[j] == i else "_ ", end="")
        print()


def solve(n, queens, r, d1, d2):
    iter_count = 0
    k = 1
    col, row = 0, 0

    while iter_count <= k * n:
        col = col_with_queen_with_max_conf(n, queens, r, d1, d2)
        if col is None:
            break
        row = row_with_min_conf(col, n, queens, r, d1, d2)
        update_state(n, row, col, queens, r, d1, d2)
        iter_count += 1

    if iter_count > k * n: #this check is new, because of cases where there is no solution like n=2
        return -1
    else:
        return 0


def main():
    n = int(input())
    queens = [0] * n
    r = [0] * n
    d1 = [0] * (2 * n - 1)
    d2 = [0] * (2 * n - 1)

    start_time = time.perf_counter()

    put_queens(n, queens, r, d1, d2)

    if solve(n, queens, r, d1, d2) == -1:
        print("-1")

    end_time = time.perf_counter()

    if n < 50:
        print_queens(n, queens)

    print("Time:", end_time - start_time)


if __name__ == "__main__":
    main()
