
#include <bits/stdc++.h>

#define rep(a, b)   for(int a = 0; a < (b); ++a)
#define all(a)      (a).begin(),(a).end()
//#define endl        '\n' //comment this out for interactive problems

using namespace std;
using Graph = vector<vector<int>>;
using ll = long long;


vector<int> merge(vector<int> l,vector<int> r)
{
    vector<int> re;
    int i=0;
    int j=0;
    while(i!=l.size() && j!=r.size())
    {
        if(l[i] == r[j]){
            re.push_back(l[i++]);
            continue;
        }
        bool smaller;
        cout << "? " << l[i]+1 << " " << r[j]+1 << endl;
        cin >> smaller;
        if(smaller)
        {
            re.push_back(l[i++]);
        }
        else
        {
            re.push_back(r[j++]);
        }
    }

    while(i!=l.size())
        re.push_back(l[i++]);

    while(j!=r.size())
        re.push_back(r[j++]);

    return re;
}


vector<int> merge_d(vector<int>&A, int s,int e)
{
    if(s-e==0)
    {
        vector<int> t;
        t.push_back(A[s]);
        return t;
    }

    int m=(s+e)/2;

    vector<int> l;
    vector<int> r;
    l=merge_d(A,s,m);
    r=merge_d(A,m+1,e);

    return merge(l,r);
}


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.precision(10);

    ll num_knights;
    cin >> num_knights;

    vector<int> knights(num_knights);

    rep(i, num_knights) knights[i] = i;

    int prince = 0;
    int counter = 0;

    vector<int> sorted = merge_d(knights, 0, knights.size()-1);

    //stable_sort(all(knights), [&prince](const int& lhs, const int& rhs) {
        //cout << "? " << lhs+1 << " " << rhs+1 << endl;
        //cin >> prince;
        //return prince;
    //    prince++;
    //    return lhs > rhs;
    //});

    cout << "! ";
    //cout << prince;
    //return 0;
    for (auto &knight : sorted) cout << knight+1 << " ";
    cout << endl;

    return 0;
}
