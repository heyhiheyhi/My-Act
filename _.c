#include<stdio.h>
#include<unistd.h>

int main()
{
	printf("Good afternoon?");
	_exit(0);	 //곧바로 커널로 복귀
//	exit(0);	//기타 루티 수행후 복귀
}
