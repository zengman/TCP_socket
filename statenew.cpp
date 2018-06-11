#include <iomanip>
#include <stdlib.h>
#include <math.h>
#include<fstream>
#include<iostream>
using namespace std;

const int k=20;//历元数
double X[k],Y[k],Z[k];//计算所得卫星坐标
const double GM=3986004.418E8;//地球引力常数
const double we=7.2921151467E-5;//地球自转角速度
double dn,a05,t0e,M0,e,w,Cuc,Cus,Crc,Crs,Cic,Cis,IDOT,i0,WMG,WMG0;//定义广播星历参数


//广播星历参数导入
void Input()
{   
	// ifstream f1("广播星历参数.txt");
    ifstream f1("3.nav");
	if(!f1)
	{
		cerr<<"广播星历参数.txt file not open!"<<endl;
		exit(1);
	}	
	f1>>dn;
	f1>>a05;
	f1>>t0e;
	f1>>M0;
	f1>>e;
	f1>>w;
	f1>>Cuc;
	f1>>Cus;
	f1>>Crc;
	f1>>Crs;
	f1>>Cic;
	f1>>Cis;
	f1>>IDOT;
	f1>>i0;
	f1>>WMG;
	f1>>WMG0;
	f1.close();

}

//卫星坐标计算
void Compute(double t,int k)
{
	double n0,n,tk,Mk,E0,Ek,Vk,fk,du,dr,di,uk,rk,ik,xk,yk,Lt;//定义卫星坐标计算过程中间量

//（）计算平均角速度n：

	n0=sqrt(GM/pow(a05,6));
	n=n0+dn;

//（）计算规化时刻tk：

	tk=t-t0e;

//（）计算平近点角Mk：

	Mk=M0+n*tk;

//（）迭代计算偏近点角Ek：

	E0=Mk;
	do
	{
		Ek=Mk+e*sin(E0);
		E0=Ek;
	}while(Mk+e*sin(E0)-E0>=1e-8);

//（）计算真近点角Vk：

	double v1=sqrt(1-e*e)*sin(Ek);
	double v2=cos(Ek)-e;
	Vk=atan2(v1,v2);

//（）计算升交角距fk：

	fk=Vk+w;

//（）摄动改正：

	du=Cuc*cos(2*fk)+Cus*sin(2*fk);//升交角距改正du
	dr=Crc*cos(2*fk)+Crs*sin(2*fk);//轨道向径改正dr
	di=Cic*cos(2*fk)+Cis*sin(2*fk);//轨道倾角改正di
	
	uk=fk+du;//改正后的升交角距uk
	rk=a05*a05*(1-e*cos(Ek))+dr;//改正后的轨道向径rk
	ik=i0+di+IDOT*tk;//改正后的轨道倾角ik

//（）计算卫星在升交点轨道直角坐标系的坐标：

	xk=rk*cos(uk);
	yk=rk*sin(uk);

//（）计算升交点精度：

	Lt=WMG0+(WMG-we)*(t-t0e)-we*t0e;
	
//（）计算卫星空间直角坐标：
	
	X[k]=xk*cos(Lt)-yk*cos(ik)*sin(Lt);
	Y[k]=xk*sin(Lt)+yk*cos(ik)*cos(Lt);
	Z[k]=yk*sin(ik);

}


int main()
{
	Input();
	for(int i=0;i<k;i++)
	{
		double t=t0e+i*60;
		Compute(t,i);
	}
	cout<<" 历元/s  卫星号      X/m             Y/m             Z/m           卫地距离"<<endl;
	for(int i=0;i<k;i++)
	{
		cout.precision(11);
		cout<<t0e+i*60<<"    7    "<<X[i]<<"     "<<Y[i]<<"     "<<Z[i]<<"     "<<sqrt(X[i]*X[i]+Y[i]*Y[i]+Z[i]*Z[i])<<endl;
	}


//输出结果到“卫星坐标计算结果.txt”

    ofstream outfile;
	outfile.open("卫星坐标计算结果.txt");
	if(outfile.is_open ())
	  {
		outfile<<" 历元/s   卫星号       X/m                 Y/m                 Z/m              卫地距离"<<endl;
		
		for(int i=0;i<k;i++)
		 {
			 outfile.precision(11);
			 outfile<<t0e+i*60<<"     7     "<<X[i]<<"        "<<Y[i]<<"        "<<Z[i]<<"        "<<sqrt(X[i]*X[i]+Y[i]*Y[i]+Z[i]*Z[i])<<endl;
		 }
	  }	
	outfile.close();
	return 0;

}
