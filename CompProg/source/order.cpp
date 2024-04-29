
#include <bits/stdc++.h>

#define rep(a, b)   for(int a = 0; a < (b); ++a)
#define all(a)      (a).begin(),(a).end()
#define endl        '\n' //comment this out for interactive problems

using namespace std;
using Graph = vector<vector<int>>;
using ll = long long;

struct problem {
    ll l;
    ll r;
    ll pos;

    bool operator<(const problem& other) const {
        return r > other.r;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.precision(10);

    ll testcases;
    cin >> testcases;

    vector<problem> problems(testcases);
    priority_queue<problem> pq;
    rep(i, testcases){
        cin >> problems[i].l;
        cin >> problems[i].r;
        problems[i].pos = i;
    }
    stable_sort(all(problems), [](const problem& lhs, const problem& rhs) {
        return lhs.l < rhs.l;
    });

    ll problems_it = 0;
    rep(i, testcases){
        while(problems_it < testcases && problems[problems_it].l-1 == i){
            pq.emplace(problems[problems_it]);
            problems_it++;
        }
        cout << pq.top().pos + 1 << " ";
        pq.pop();
    }

    return 0;
}
