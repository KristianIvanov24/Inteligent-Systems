#include <iostream>
#include <vector>
#include <cmath>

//Globals
std::vector<int> titles;
int boardSize;
int sideSize;
int currIdxOfZero;
int goalIdxOfZero;

bool moveUp(){
    if(currIdxOfZero / sideSize < 1)
        return false;

    std::swap(titles[currIdxOfZero], titles[currIdxOfZero+sideSize]);
    currIdxOfZero += sideSize;
    return true;
}

bool moveDown(){
    if(currIdxOfZero / sideSize > sideSize - 1)
        return false;

    std::swap(titles[currIdxOfZero], titles[currIdxOfZero-sideSize]);
    currIdxOfZero -= sideSize;
    return true;
}

bool moveLeft(){
    if(currIdxOfZero % sideSize == sideSize - 1)
        return false;

    std::swap(titles[currIdxOfZero], titles[currIdxOfZero+1]);
    currIdxOfZero += 1;
    return true;
}

bool moveRight(){
    if(currIdxOfZero % sideSize == 0)
        return false;

    std::swap(titles[currIdxOfZero], titles[currIdxOfZero-1]);
    currIdxOfZero -= 1;
    return true;
}

void printBoard(){
    for(int i = 0; i <= boardSize; i++){
        if(i % sideSize == 0)
            std::cout << std::endl;
        std::cout << titles[i] << ' ';
    }
    std::cout << std::endl;
}

void input(){
    std::cin >> boardSize;
    std::cin >> goalIdxOfZero;

    int temp;
    for(int i = 0; i <= boardSize; i++){
        std::cin >> temp;

        if(temp == 0)
            currIdxOfZero = i;

        titles.push_back(temp);
    }

    if(goalIdxOfZero == -1)
        goalIdxOfZero = boardSize;

    sideSize = sqrt(boardSize+1);
}

void playGame(){
    input();

    while(1){
        char cmd[10];
        std::cin >> cmd;

        if(strcmp(cmd, "up") == 0){
            moveUp();
            printBoard();
        }
        else if(strcmp(cmd, "down") == 0){
            moveDown();
            printBoard();
        }
        else if(strcmp(cmd, "left") == 0){
            moveLeft();
            printBoard();
        }
        else if(strcmp(cmd, "right") == 0){
            moveRight();
            printBoard();
        }
        else {
            printBoard();
            break;
        }
    }
}

int main(){
    playGame();
}
