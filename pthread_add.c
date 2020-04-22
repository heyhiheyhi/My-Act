#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>

t_add(void *a){
	int num;
	int max=0;
	num=*((int*)a);
	for(num=0; num<=10000000; num++)
	{
		max+=num;
	}
	return max;
}

main(){
	pthread_t p_thread;
	int i=0;
	int err;
	int status;

	if((err = pthread_create(&p_thread,NULL,t_add,(void*)&i)) < 0)
	{
		perror("thread create error : ");

		exit(1);
	}
	pthread_join(p_thread,(void **)&status);
	printf("thread join : %d\n", status);
	return 0;
}
	

