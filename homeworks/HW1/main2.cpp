#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <climits>

const int FOUND = -24;

std::vector<int> tiles;
int boardSize;
int sideSize;
int currIdxOfZero;
int goalIdxOfZero;

std::vector<std::string> path;

namespace moves {
    bool up() {
        if (currIdxOfZero / sideSize < 1)
            return false;

        std::swap(tiles[currIdxOfZero], tiles[currIdxOfZero - sideSize]);
        currIdxOfZero -= sideSize;
        return true;
    }

    bool down() {
        if (currIdxOfZero / sideSize >= sideSize - 1)
            return false;

        std::swap(tiles[currIdxOfZero], tiles[currIdxOfZero + sideSize]);
        currIdxOfZero += sideSize;
        return true;
    }

    bool left() {
        if (currIdxOfZero % sideSize == sideSize - 1)
            return false;

        std::swap(tiles[currIdxOfZero], tiles[currIdxOfZero + 1]);
        currIdxOfZero += 1;
        return true;
    }

    bool right() {
        if (currIdxOfZero % sideSize == 0)
            return false;

        std::swap(tiles[currIdxOfZero], tiles[currIdxOfZero - 1]);
        currIdxOfZero -= 1;
        return true;
    }
}

int manhattan() {
    int sum = 0;
    int positionsBeforeZeroLeft = goalIdxOfZero;
    int cur;
    int x;
    for (int i = 0; i < sideSize; i++) {
        for (int j = 0; j < sideSize; j++) {
            x = j + i * sideSize;
            cur = tiles[x];
            if (cur == 0) {
                continue;
            }

            if (positionsBeforeZeroLeft > 0) {
                sum += std::abs((cur - 1) / sideSize - i) + std::abs((cur - 1) % sideSize - j);
                --positionsBeforeZeroLeft;
            } else {
                sum += std::abs(cur / sideSize - i) + std::abs(cur % sideSize - j);
            }
        }
    }
    return sum;
}

bool isGoal() {
    return manhattan() == 0;
}

int search(int g, int threshold) {
    int f = g + manhattan();

    if (f > threshold) {
        return f;
    }

    if (isGoal()) {
        std::cout << path.size() - 1 << std::endl;
        for (int i = 1; i < path.size(); i++) {
            std::cout << path[i] << std::endl;
        }
        return FOUND;
    }

    int min = INT_MAX;
    int temp;

    if (path.empty() || path.back() != "down" && moves::down()) {
        path.push_back("down");
        temp = search(g + 1, threshold);
        if (temp == FOUND) {
            return FOUND;
        }
        if (temp < min) {
            min = temp;
        }
        path.pop_back();
        moves::up();
    }
    if (path.empty() || path.back() != "up" && moves::up()) {
        path.push_back("up");
        temp = search(g + 1, threshold);
        if (temp == FOUND) {
            return FOUND;
        }
        if (temp < min) {
            min = temp;
        }
        path.pop_back();
        moves::down();
    }
    if (path.empty() || path.back() != "right" && moves::right()) {
        path.push_back("right");
        temp = search(g + 1, threshold);
        if (temp == FOUND) {
            return FOUND;
        }
        if (temp < min) {
            min = temp;
        }
        path.pop_back();
        moves::left();
    }
    if (path.empty() || path.back() != "left" && moves::left()) {
        path.push_back("left");
        temp = search(g + 1, threshold);
        if (temp == FOUND) {
            return FOUND;
        }
        if (temp < min) {
            min = temp;
        }
        path.pop_back();
        moves::right();
    }

    return min;
}

bool idastar() {
    int threshold = manhattan();
    path.push_back("init");
    int temp;

    while (true) {
        temp = search(0, threshold);
        if (temp == FOUND) {
            return true;
        }
        if (temp > threshold) {
            return false;
        }
        threshold = temp;
    }
}

void solve() {
    if (idastar()) {
        std::cout << path.size() - 1 << std::endl;
        for (int i = 1; i < path.size(); i++) {
            std::cout << path[i] << std::endl;
        }
    } else {
        std::cout << -1 << std::endl;
    }
}

void input() {
    std::cin >> boardSize;
    std::cin >> goalIdxOfZero;

    int temp;
    for (int i = 0; i < boardSize; i++) {
        std::cin >> temp;

        if (temp == 0)
            currIdxOfZero = i;

        tiles.push_back(temp);
    }

    if (goalIdxOfZero == -1)
        goalIdxOfZero = boardSize;

    sideSize = std::sqrt(boardSize + 1);
}

int main() {
    input();
    solve();
}
