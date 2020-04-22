#include<sys/stat.h>
#include<stdio.h>
#include<string.h>
#include<ctime>
#include<iostream>
#include<string>

int main(void)
{
	struct tm* tm;
	time_t UTCtime = time(0);
	tm = localtime(&UTCtime);

	char dir_name[100];

	strftime(dir_name, 100, "%Y%m%d_%H", tm);

	printf("%s\n", dir_name);
}

