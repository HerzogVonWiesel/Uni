
#include <bits/stdc++.h>

#define rep(a, b)   for(int a = 0; a < (b); ++a)
#define all(a)      (a).begin(),(a).end()
#define endl        '\n' //comment this out for interactive problems

using namespace std;
using Graph = vector<vector<int>>;
using ll = long long;

ll op(ll a,ll b,ll i){
    switch(i){
        case 0:
            return a+b;
        case 1:
            return a-b;
        case 2:
            return a*b;
    }
    return 0;
}

void generatePermutatioN(const vector<ll>& input, ll k, ll permutationNumber, vector<ll>& permutation) {
    ll n = input.size();
    for (ll i = 0; i < k; ++i) {
        permutation[i] = input[permutationNumber % n];
        permutationNumber /= n;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.precision(10);

    ll testcases;
    cin >> testcases;

    vector<ll> num(5);
    vector<ll> ops {0, 1, 2};
    vector<ll> current_ops(4);
    ll current_perm = 0;
    ll total_perms = 1;
    for (ll i = 0; i < current_ops.size(); ++i) {
        total_perms *= ops.size();
    }

    rep(cur_case, testcases){
        for (auto &cur_num : num) cin >> cur_num;
        for (current_perm = 0; current_perm < total_perms; ++current_perm){
            generatePermutatioN(ops, current_ops.size(), current_perm, current_ops);
            do {
                ll prev_op = num[0];

                for (ll x = 1; x < 5; ++x){
                    prev_op = op(prev_op, num[x], current_ops[x-1]);
                }
                if (prev_op == 23){
                    cout << "Possible" << endl;
                    goto next_case;
                }
            } while (next_permutation(all(num)));
        }
        cout << "Impossible" << endl;
        next_case: ;
    }

    return 0;
}
