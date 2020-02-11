#include <iostream>
#include <vector>
#include <stack>
#include <cstring>
using namespace std;



/*  the chr struct holds information about each input character:
 *
 *  c    | the character itself
 *  idx  | the first index in the output string (compute later)
 *  mult | if a bracket, multipler associated with segment
 *  len  | if a bracket, the length of the segment. else the type of char
 */

typedef struct {
    char c;
    int idx;
    int mult;
    int len;
} chr;

#define CHR_CHR (-8)
#define CHR_INT (-9)

void read_input(vector<chr> &input) {
    input.push_back({'1'});
    input.push_back({'['});
    while (cin >> c) {
        input.push_back({c});
    }
    input.push_back({']'});
}



int main() {

    char c;
    int i = 0;
    stack<chr*> stk;
    vector<chr> input;

    // reads in characters and stores in a list of chr structs
    read_input(input);


    for (int j = 0; j < input.size(); j++) {
        chr &c = input[j];

        if (isdigit(c.c)) {
            c.len   = CHR_INT;    // mark digit
            chr &c2 = input[++j]; // find the opening bracket (skip it as well)
            c2.idx  = i;          // store running counter as index for bracket
            c2.mult = c.c-'0';    // store multiplier
            stk.push(&c2);        // push opening bracket on stack

        } else if (c.c==']') {
            chr *top = stk.top();    // find opening bracket
            top->len = i - top->idx; // compute length of segment

            // open and close bracket hold the same info (same segment)
            c.mult = top->mult;
            c.len  = top->len;
            c.idx  = top->idx;
            stk.pop();

            // increase the counter with expanded segment
            i += top->len * (top->mult-1);

        } else {
            c.idx = i;       // keep track of char
            c.len = CHR_CHR; // mark char
            i++;

        }
    }


    char * output = new char[i+1];
    memset(output, 0, i+1);

    for (chr c : input) {
        if (c.c == ']') {
            for (int j = 1; j < c.mult; j++) {
                int dest_idx = c.idx + (j*c.len);
                memcpy(output+dest_idx, output+c.idx, c.len);
            }
        }
        else if (c.len == CHR_CHR) {
            output[c.idx] = c.c;
        }
    }

    printf("%s\n", output);
    delete[] output;

}
