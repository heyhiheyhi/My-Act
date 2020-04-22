#include<stdio.h>
#include<sys/stat.h>

main(){
	char* a="12345";
	mkdir("aaaa",0777);
	mkdir(a,0777);
	mkdir("../abc",0777);		
}

//
