#include <bits/stdc++.h>
using namespace std;
using ll=long long;
#define rep(i,n) for(int i=0;i<(int)(n);i++)
#define inf 1001001001001001001
#define mod 1000000007
#define mod2 998244353
#define pi acos(-1)
#define all(v) v.begin(),v.end()

int main(){
    int tmp;
    set<int>s;
    rep(i,2){
        cin>>tmp;
        s.insert(tmp);
    }
    for(int i=1;i<=3;i++){
        if(!s.count(i)){
            cout<<i<<endl;
            return 0;
        }
    }
}