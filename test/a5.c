#include <bits/stdc++.h>
using namespace std;

int calc(int node,int node_from,vector<vector<int>> &tree,vector<int> &xsum,vector<int64_t> &psum);

int main()
{
	int n,q;
	cin >> n >> q;
	vector<int> a(n),b(n);
	vector<int> p(q+1),x(q+1);
	for (int i=1;i<n;++i)
	{
		cin >> a[i] >> b[i];
	}
	for (int i=1;i<=q;++i)
	{
		cin >> p[i] >> x[i];
	}

	vector<vector<int>> tree(n+1,vector<int>());
	for (int i=1;i<n;++i)
	{
		tree[a[i]].push_back(b[i]);
		tree[b[i]].push_back(a[i]);
	}

	vector<int> xsum(n+1);
	for (int i=1;i<=q;++i)
	{
		xsum[p[i]]+=x[i];
	}

	vector<int64_t> psum(n+1);
	psum[0]=0;
	calc(1,0,tree,xsum,psum);

	bool initial=true;
	for (int i=1;i<=n;++i)
	{
		if (initial!=false)
		{
			initial=false;
		}
		else
		{
			cout << " ";
		}
		cout << psum[i];
	}
	cout << endl;


}

int calc(int node,int node_from,vector<vector<int>> &tree,vector<int> &xsum,vector<int64_t> &psum)
{
	psum[node]=psum[node_from]+xsum[node];
	for (int i=0;i<tree[node].size();++i)
	{
		if (tree[node][i]==node_from)
		{
			continue;
		}
		calc(tree[node][i],node,tree,xsum,psum);
	}
	return 0;
}







