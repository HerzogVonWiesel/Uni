
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

    ll value;

    cout << "? insert 3" << endl;
    cout.flush();
    cout << "? insert 1" << endl;
    cout.flush();
    cout << "? insert 1" << endl;
    cout.flush();
    cout << "? insert 4" << endl;
    cout.flush();

    cout << "? remove" << endl;
    cout.flush();

    cin >> value;
    if (value == -1) return 1;

    if (value == 3){
        cout << "! queue" << endl;
        cout.flush();
    }
    else if (value == 4){
        cout << "! stack" << endl;
        cout.flush();
    }
    else if (value == 1){
        cout << "? remove" << endl;
        cout.flush();
        cin >> value;
        if (value == 1){
            cout << "! pq" << endl;
            cout.flush();
        }
        else{
            cout << "! set" << endl;
            cout.flush();
        }
    }


    return 0;
}
