
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

    int test_cases;
    ll n;
    ll max_turnout = 0;
    ll prev_set_size, cur_set_size;
    cin >> test_cases;

    for (int i = 0; i < test_cases; ++i){
        cin >> n;
        vector<ll> flakes(n);
        for (ll j = 0; j < n; ++j){
            cin >> flakes[j];
        }
        max_turnout = 0;
        ll k = 0;
        ll j = 0;
        cur_set_size = 0;
        set<ll> longest;
        bool inserted;
        for (j = 0; j < n; ++j){
            prev_set_size = cur_set_size;
            inserted = longest.insert(flakes[j]).second;
            if (!inserted){
                if (j-k > max_turnout) max_turnout = j-k;
                while(flakes[j] != flakes[k]){
                    longest.erase(flakes[k]);
                    k++;
                }
                k++;
            }
        }
        if (j-k > max_turnout) max_turnout = j-k;
        cout << max_turnout << endl;
    }


    return 0;
}
