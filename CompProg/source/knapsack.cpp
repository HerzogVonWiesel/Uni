
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


    ll items; cin >> items;
    ll capacity; cin >> capacity;
    ll capacitwo = capacity;

    ll one = 0; ll two = 0; ll three = 0;
    ll current_weight;
    rep(i, items){
        cin >> current_weight;
        switch(current_weight){
            case 1:
                one++;
                break;
            case 2:
                two++;
                break;
            case 3:
                three++;
                break;
        }
    }

    rep(i, three){
        if (capacitwo - 3 < 0) break;
        capacitwo -= 3;
    }
    ll capacithree = capacitwo + 3;
    if (three < 1 || capacity <= 3) capacithree = capacitwo;
    rep(i, two){
        if (capacithree -2 < 0) break;
        capacitwo -= 2;
        capacithree -= 2;
    }
    if (capacitwo <= -1) capacitwo = (capacitwo % 2)* (-1);
    capacitwo = min(capacitwo, capacithree);
    rep(i, one){
        if (capacitwo - 1 < 0) break;
        capacitwo -= 1;
    }

    cout << capacity - capacitwo << endl;


    return 0;
}
