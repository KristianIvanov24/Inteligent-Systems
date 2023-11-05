#include <iostream>
#include <vector>
#include <cmath>

//Globals

const int FOUND = -24;

std::vector<int> tiles;
int boardSize;
int sideSize;
int currIdxOfZero;
int goalIdxOfZero;

std::vector<std::string> path;

namespace moves{
    bool up(){
        if(currIdxOfZero / sideSize < 1)
            return false;

        std::swap(tiles[currIdxOfZero], tiles[currIdxOfZero+sideSize]);
        currIdxOfZero += sideSize;
        return true;
    }

    bool down(){
        if(currIdxOfZero / sideSize > sideSize - 1)
            return false;

        std::swap(tiles[currIdxOfZero], tiles[currIdxOfZero-sideSize]);
        currIdxOfZero -= sideSize;
        return true;
    }

    bool left(){
        if(currIdxOfZero % sideSize == sideSize - 1)
            return false;

        std::swap(tiles[currIdxOfZero], tiles[currIdxOfZero+1]);
        currIdxOfZero += 1;
        return true;
    }

    bool right(){
        if(currIdxOfZero % sideSize == 0)
            return false;

        std::swap(tiles[currIdxOfZero], tiles[currIdxOfZero-1]);
        currIdxOfZero -= 1;
        return true;
    }
}

/*void printBoard(){
    for(int i = 0; i <= boardSize; i++){
        if(i % sideSize == 0)
            std::cout << std::endl;
        std::cout << titles[i] << ' ';
    }
    std::cout << std::endl;
}*/

int manhattan()
{
    int sum = 0;
    int positionsBeforeZeroLeft = goalIdxOfZero;
    int cur;
    int x;
    for (int i = 0; i < sideSize; i++)
    {
        for (int j = 0; j < sideSize; j++)
        {
            x = j + i * sideSize;
            cur = tiles[x];
            if (cur == 0)
            {
                continue;
            }

            if (positionsBeforeZeroLeft > 0) {
                sum += abs((cur - 1) / sideSize - i) + abs((cur - 1) % sideSize - j);
                --positionsBeforeZeroLeft;
            }
            else {
                sum += abs(cur / sideSize - i) + abs(cur % sideSize - j);
            }
        }
    }
    return sum;
}

// is this board the goal board?
bool isGoal()
{
    return manhattan() == 0;
}

int search(int g, int threshold)
{
    int f = g + manhattan();

    //greater f encountered
    if (f > threshold)
    {
        return f;
    }

    //Goal node found
    if (isGoal())
    {
        std::cout << path.size() - 1 << std::endl;
        for (int i = 1; i < path.size(); i++) {
            std::cout << path[i] << std::endl;
        }
        return FOUND;
    }

    int min = INT_MAX;
    int temp;

    if (path.back() != "up" && moves::down())
    {
        path.push_back("down");
        temp = search(g + 1, threshold);
        if (temp == FOUND)
        {
            return FOUND;
        }
        if (temp < min)
        {
            min = temp;
        }
        path.pop_back();
        moves::up();
    }
    if (path.back() != "down" && moves::up())
    {
        path.push_back("up");
        temp = search(g + 1, threshold);
        if (temp == FOUND)
        {
            return FOUND;
        }
        if (temp < min)
        {
            min = temp;
        }
        path.pop_back();
        moves::down();
    }
    if (path.back() != "left" && moves::right())
    {
        path.push_back("right");
        temp = search(g + 1, threshold);
        if (temp == FOUND)
        {
            return FOUND;
        }
        if (temp < min)
        {
            min = temp;
        }
        path.pop_back();
        moves::left();
    }
    if (path.back() != "right" && moves::left())
    {
        path.push_back("left");
        temp = search(g + 1, threshold);
        if (temp == FOUND)
        {
            return FOUND;
        }
        if (temp < min)
        {
            min = temp;
        }
        path.pop_back();
        moves::right();
    }

    //return the minimum 'f' encountered greater than threshold
    return min;
}

bool idastar() {
    int threshold = manhattan();
    path.push_back("init");
    int temp;

    while (true)
    {
        temp = search(0, threshold);
        if (temp == FOUND)
        {
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

void input(){
    std::cin >> boardSize;
    std::cin >> goalIdxOfZero;

    int temp;
    for(int i = 0; i <= boardSize; i++){
        std::cin >> temp;

        if(temp == 0)
            currIdxOfZero = i;

        tiles.push_back(temp);
    }

    if(goalIdxOfZero == -1)
        goalIdxOfZero = boardSize;

    sideSize = sqrt(boardSize+1);
}

int main(){
    input();
    solve();
}
