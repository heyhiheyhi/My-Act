#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>

t_add(void *a){
	int num;
	int max=0;
	num=*((int*)a);
	for(; num<=10000000; num++)
	{
		max+=num;
	}
	return max;
}

main(){
	pthread_t p_thread[2];
	int i=0;
	int j=5000000;
	int err;
	int status;

	if((err = pthread_create(&p_thread[0],NULL,t_add,(void*)&i)) < 0)
	{
		perror("thread create error : ");

		exit(1);
	}
	if((err = pthread_create(&p_thread[1],NULL,t_add,(void*)&j)) < 0)
	{	perror("thread create error2 : ");

		exit(1);
	}
	pthread_join(p_thread[0],(void **)&status);
	printf("thread join : %d\n", status);
	pthread_join(p_thread[1],(void **)&status);
	printf("thread join : %d\n", status);
return 0;
}
	

