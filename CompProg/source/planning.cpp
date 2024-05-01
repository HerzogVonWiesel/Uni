
#include <bits/stdc++.h>

#define rep(a, b)   for(int a = 0; a < (b); ++a)
#define all(a)      (a).begin(),(a).end()
#define endl        '\n' //comment this out for interactive problems

using namespace std;
using Graph = vector<vector<int>>;
using ll = long long;

struct problem{
    ll down;
    ll up;
    ll difficulty;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.precision(10);

    ll testcases;
    cin >> testcases;

    ll difficulty;
    ll down_max;
    ll up_max;
    vector<problem> problems(testcases);
    rep(i, testcases){
        cin >> difficulty;
        down_max = 1;
        up_max = 1;
        rep(j, i){
            if (problems[j].difficulty < difficulty && problems[j].up + 1 > up_max) up_max = problems[j].up + 1;
            if (problems[j].difficulty > difficulty && problems[j].down + 1 > down_max) down_max = max(problems[j].down + 1, problems[j].up + 1);
        }
        problems[i].difficulty = difficulty;
        problems[i].down = down_max;
        problems[i].up = up_max;
    }
    down_max = 1;
    for (auto &cur_prob : problems) down_max = max(down_max, max(cur_prob.up, cur_prob.down));

    cout << down_max;

    return 0;
}
