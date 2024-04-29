
#include <bits/stdc++.h>

#define rep(a, b)   for(int a = 0; a < (b); ++a)
#define all(a)      (a).begin(),(a).end()
#define endl        '\n' //comment this out for interactive problems

using namespace std;
using Graph = vector<vector<int>>;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.precision(10);

    ll testcases;
    cin >> testcases;

    ll cur_max = 0, prev_max = 0, prev_prev_max = 0, monster;
    rep(i, testcases){
        cin >> monster;
        prev_prev_max = prev_max;
        prev_max = cur_max;
        cur_max = max(prev_max, prev_prev_max + monster);
    }

    cout << cur_max << endl;

    return 0;
}
