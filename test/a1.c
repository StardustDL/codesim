#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for(int i = 0; i < n; i++)
typedef long long ll;

int main(){
    int n; cin >> n;
    vector<int> v(n);
    rep(i, n){
        cin >> v.at(i);
    }
    int m = 10000000;
    int count = 0;
    rep(i, n){
        if(m < v.at(i)) continue;
        count++;
        m = min(m, v.at(i));
    }
    cout << count << endl;
    return 0;
}
