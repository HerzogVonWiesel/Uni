
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

    ll num_cases;
    ll h, p;
    ll xi;

    struct household {
        ll ponies;
        ll pies;
        ll ratio;
        household(ll ponies, ll pies): ponies(ponies), pies(pies) {
            ratio = static_cast<ll>(ceil(ponies / static_cast<double>(pies)));
        }

        bool operator<(const household& other) const {
            return ratio < other.ratio;
        }
    };

    cin >> num_cases;
    for (ll i = 0; i < num_cases; ++i) {
        cin >> h >> p;
        p = p-h;
        priority_queue<household> households;
        for (ll j = 0; j < h; ++j) {
            cin >> xi;
            households.emplace(xi, 1);
        }
        household x(1, 1);
        for (ll j = 0; j < p; ++j){
            x = households.top();
            households.pop();
            households.emplace(x.ponies, x.pies+1);
        }
        cout << households.top().ratio << endl;
    }

    return 0;
}
