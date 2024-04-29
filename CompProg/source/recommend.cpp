
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


    ll num_problems, diff;
    cin >> num_problems >> diff;

    vector<ll> problems(num_problems);
    for (auto &cur_prob : problems) cin >> cur_prob;

    stable_sort(all(problems), greater<>());

    num_problems = 1;
    ll sum = 0;

    for (auto &cur_prob : problems){
        if ( (sum + cur_prob)/num_problems < diff ) break;
        sum += cur_prob;
        num_problems++;
    }

    cout << num_problems-1 << endl;

    return 0;
}
