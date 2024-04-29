
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

    char cur_hat;

    rep(cur_case, testcases){
        ll chars;
        cin >> chars;
        vector<bool> hats(chars);
        vector<ll> spells;
        bool possible = true;
        rep(cur_char, chars){
            cin >> cur_hat;
            hats[cur_char] = cur_hat == 'W';
        }

        for (int cur_char = 0; cur_char < chars-2; cur_char++){
            if (hats[cur_char] != hats[cur_char+1]){
                hats[cur_char+1] = !hats[cur_char+1];
                hats[cur_char+2] = !hats[cur_char+2];
                spells.push_back(cur_char+1);
            }
        }
        for (int cur_char = chars-1; cur_char > 1; --cur_char){
            if (hats[cur_char] != hats[cur_char-1]){
                hats[cur_char-1] = !hats[cur_char-1];
                hats[cur_char-2] = !hats[cur_char-2];
                spells.push_back(cur_char-2);
            }
        }

        for (int cur_char = 0; cur_char < chars-1; cur_char++){
            if (hats[cur_char] != hats[cur_char+1]){
                possible = false;
                break;
            }
        }

        if (possible){
            cout << "YES" << endl;
            cout << spells.size() << endl;
            for (auto &cur_spell : spells) cout << cur_spell+1 << " ";
            cout << endl;
        }
        else{
            cout << "NO" << endl;
        }

    }


    return 0;
}
