#include<iostream>
#include<algorithm>
#include<cstring>
#include<cstdio>
#include<vector>
#include<queue>
#include<stack>
#include<bitset>
using namespace std;
const int INF=0x3f3f3f3f,MAXN=1000*1000;
struct edge{
	int u,v,w,c,f;
	edge(int u,int v,int w,int c,int f):u(u),v(v),w(w),c(c),f(f){} 
};
vector<edge> es;
vector<int> g[MAXN+3];
int d[MAXN+3],cur[MAXN+3],S,T;
queue<int> q;
bitset<MAXN+3> vis;
void addedge(int u,int v,int w,int c){
	es.push_back(edge(u,v,w,c,0));
	es.push_back(edge(v,u,-w,0,0));
	g[u].push_back(es.size()-2);
	g[v].push_back(es.size()-1);
}
bool bfs(){
	vis=0;
	while(!q.empty())q.pop();
	memset(d,-1,sizeof(d));
	q.push(S);vis[S]=1;d[S]=1;
	while(!q.empty()){
		int u=q.front();q.pop();
		for(int i=0;i<g[u].size();i++){
			edge &e=es[g[u][i]];
			if(vis[e.v]||e.c-e.f<=0)continue;
			vis[e.v]=1;
			d[e.v]=d[u]+1;
			q.push(e.v);
		}
	}
	return vis[T];
}
int dfs(int u,int a){
	if(u==T||a==0)return a;
	int rel=0,f;
	for(int &i=cur[u];i<g[u].size();i++){
		edge &e=es[g[u][i]];
		if(d[e.v]==d[u]+1 && (f=dfs(e.v,min(a,e.c-e.f)))>0){
			e.f+=f;
			es[g[u][i]^1].f-=f;
			rel+=f;
			a-=f;
			if(!a)break;
		}
	}
	return rel;
}
int maxflow(int s,int t){
	S=s;T=t;
	int ans=0;
	while(bfs()){
		memset(cur,0,sizeof(cur));
		ans+=dfs(s,INF);
	}
	return ans;
}
int n,m;
inline int id(int x,int y){
	return (x-1)*m+y;
}
int main(){
	scanf("%d%d",&n,&m);int k;
	for(int i=1;i<=n;i++){
		for(int j=1;j<m;j++){
			scanf("%d",&k);
			addedge(id(i,j),id(i,j+1),0,k);
			addedge(id(i,j+1),id(i,j),0,k);
		}
	}
	for(int i=1;i<n;i++){
		for(int j=1;j<=m;j++){
			scanf("%d",&k);
			addedge(id(i,j),id(i+1,j),0,k);
			addedge(id(i+1,j),id(i,j),0,k);
		}
	}
	for(int i=1;i<n;i++){
		for(int j=1;j<m;j++){
			scanf("%d",&k);
			addedge(id(i,j),id(i+1,j+1),0,k);
			addedge(id(i+1,j+1),id(i,j),0,k);
		}
	}
	printf("%d\n",maxflow(id(1,1),id(n,m)));

	
	constexpr auto lamb = [](int n)
	{ return n * n; };
	static_assert(lamb(3) == 9, "a");
	return 0;
}