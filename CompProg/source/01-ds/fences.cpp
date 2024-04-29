
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

    struct order{
        ll l;
        ll r;
        ll c;
        ll time;
    };

    ll num_colors;
    ll num_orders;
    cin >> num_colors >> num_orders;

    vector<ll> colors(num_colors, 0);
    vector<order> orders(num_orders+1);

    //lambda pq
    auto cmp = [](order x, order y) { return (x.time) < (y.time); };
    priority_queue<order, vector<order>, decltype(cmp)> pq(cmp);

    ll l, r, c;
    for (ll i = 0; i < num_orders; ++i){
        cin >> l >> r >> c;
        orders[i] = order{l, r, c, i};
    }

    orders[num_orders] = {LLONG_MAX, LLONG_MAX, 0, num_orders};
    stable_sort(orders.begin(), orders.end(), [](const order& lhs, const order& rhs) {
        return lhs.l < rhs.l;
    });

    order current_order;
    order new_order;
    ll current_paint;
    if (!orders.empty()) {
        pq.emplace(orders[0]);
        current_paint = orders[0].l;
    }
    for (ll i = 1; i < num_orders+1; ++i){
        new_order = orders[i];
        if (!pq.empty()){
            current_order = pq.top();
            while (!pq.empty() && current_order.r <= new_order.l){
                pq.pop();
                if(current_paint >= current_order.r) {
                    if(!pq.empty()) current_order = pq.top();
                    continue;
                }
                colors[current_order.c] += current_order.r - current_paint;
                current_paint = current_order.r;
                if(!pq.empty()) current_order = pq.top();
            }
            if(!pq.empty()) colors[current_order.c] += new_order.l - current_paint;
        }
        current_paint = new_order.l;
        pq.emplace(new_order);
    }

    for (ll i = 0; i < num_colors; ++i){
        cout << colors[i] << endl;
    }

    return 0;
}
