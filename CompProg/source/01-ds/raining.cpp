
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

    ll test_cases;
    ll water;
    char c;
    cin >> test_cases;
    cin.ignore();
    for (ll i = 0; i < test_cases; ++i){
        stack<ll> geography;
        water = 0;
        string input;
        getline(cin, input);
        for (ll i = 0; i < input.length(); ++i){
            c = input[i];
            switch(c){
                case '/':
                    if (!geography.empty()){
                        water += i-geography.top();
                        geography.pop();
                    }
                    break;
                case '\\':
                    geography.emplace(i);
                    break;
                case '_':
                    break;
            }
        }
        cout << water << endl;
    }

    return 0;
}
