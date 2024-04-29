
#include <bits/stdc++.h>

#define rep(a, b)   for(int a = 0; a < (b); ++a)
#define all(a)      (a).begin(),(a).end()
#define endl        '\n'

using namespace std;
using Graph = vector<vector<int>>;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.precision(10);

    struct puzpie{
        ll tbo;
        ll tbc;
        double ratio;

        bool operator<(const puzpie& other) const {
            if (tbo == 0 && other.tbo != 0) {
                return true;
            } else if (tbo != 0 && other.tbo == 0) {
                return false;
            } else if (tbc == 0 && other.tbc != 0) {
                return false;
            } else if (tbc != 0 && other.tbc == 0) {
                return true;
            } else {
                return ratio < other.ratio;
            }
        }
    };

    ll pieces;
    cin >> pieces;
    ll pieces_check = pieces;
    cin.ignore();
    puzpie cur_piece;
    priority_queue<puzpie> puzzle;
    for (ll i = 0; i < pieces; ++i){
        stack<int> piece;
        cur_piece = {0, 0};
        string input;
        getline(cin, input);
        for (char c : input){
            switch(c){
                case ')':
                    if (!piece.empty()){
                        piece.pop();
                    }
                    else {
                        cur_piece.tbo++;
                    }
                    break;
                case '(':
                    piece.emplace(1);
                    break;
            }
        }
        cur_piece.tbc += piece.size();
        cur_piece.ratio = (cur_piece.tbc == 0)? numeric_limits<double>::max() : static_cast<double>(cur_piece.tbo)/cur_piece.tbc;
        puzzle.push(cur_piece);
    }
//    for (puzpie piece : puzzle){
//        switch(c){
//            case ')':
//                if (!piece.empty()){
//                    piece.pop();
//                }
//                else {
//                    cur_piece.tbo++;
//                }
//                break;
//            case '(':
//                piece.emplace(1);
//                break;
//        }
//    }
    ll total = 0;
    while (!puzzle.empty()) {
        cur_piece = puzzle.top();
        total -= cur_piece.tbc;
        if (total < 0){
            cout << "NO" << endl;
            return 0;
        }
        total += cur_piece.tbo;
        puzzle.pop();
    }
    if (total == 0) cout << "YES" << endl;
    else cout << "NO" << endl;
    return 0;
}