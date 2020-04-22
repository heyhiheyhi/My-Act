// simple_camera.cpp
// MIT License
// Copyright (c) 2019 JetsonHacks
// See LICENSE for OpenCV license and additional information
// Using a CSI camera (such as the Raspberry Pi Version 2) connected to a 
// NVIDIA Jetson Nano Developer Kit using OpenCV
// Drivers for the camera and OpenCV are included in the base image

// #include <iostream>
#include <stdio.h>
#include <opencv2/opencv.hpp>
// #include <opencv2/videoio.hpp>
// #include <opencv2/highgui.hpp>
#include <iostream>
#include <time.h>
#include <dirent.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>


using namespace cv;
using namespace std;


int capture_width = 640 ;
int capture_height = 480 ;
double framerate = 30.0 ;
int flip_method = 0 ;

time_t t;

struct stat sb;
struct tm *pt;

#define FILE_NAME_LENGTH 100
#define FOLDER_NAME_LENGTH 100

#define TIME_DIR 0
#define TIME_FILE 1

#define PATH_NAME "/home/user/coding/"

#define LIMIT 1024*1024*2
/*
string gstreamer_pipeline (int capture_width, int capture_height, int display_width, int display_height, int framerate, int flip_method) {
    return "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)" + to_string(capture_width) + ", height=(int)" +
           to_string(capture_height) + ", format=(string)NV12, framerate=(fraction)" + to_string(framerate) +
           "/1 ! nvvidconv flip-method=" + to_string(flip_method) + " ! video/x-raw, width=(int)" + to_string(display_width) + ", height=(int)" +
           to_string(display_height) + ", format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink";
}
*/

string gstreamer_pipeline (int capture_width, int capture_height, int framerate) {
    return "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)" + to_string(capture_width) + ", height=(int)" + 
	    to_string(capture_height) + ", format=(string)NV12, framerate=(fraction)" + to_string(framerate) + 
	    "/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink";
}

void ttime(int types, char *buf)
{

	if(types == TIME_DIR)
       	{
		strftime(buf, FOLDER_NAME_LENGTH,"%Y%m%d_%H", localtime(&t));
	}
	else if
	{
		strftime(buf, FILE_NAME_LENGTH,"%Y%m%d_%H%M%S" localtime(&t));
	}
}


int main()
{
	

    	string pipeline = gstreamer_pipeline(capture_width, capture_height, framerate);

    	cout << "Using pipeline: \n\t" << pipeline << "\n";

    	fflush(stdout);

    	VideoCapture cap(pipeline, cv::CAP_GSTREAMER);
    	if(!cap.isOpened())
    	{
        	cout<<"Failed to open camera."<<std::endl;
		return (-1);
    	}
	
	
	
    	Mat img;
    	int fourcc = VideoWriter::fourcc('D', 'I', 'V', 'X');
    	Size size = Size(capture_width, capture_height);
    	VideoWriter writer;

	// 파일 이름 생성
	char *mkdirName;
	char *mkfileName;
    	int frameCnt=0;
	char temp[100];
	
	mkfileName =(char *) malloc(FILE_NAME_LENGTH);
	mkdirName  =(char *) malloc(FOLDER_NAME_LENGTH);

	
	while(true) {
		ttime(TIME_DIR, mkdirName);
		strcat(PATH_NAME, mkdirName);
		
		if(sb.st_size >= LIMIT) 
		{
			sprintf(temp, "rf -rf %s", PATH_NAME);
			system(temp);
		}
		else if 
		{
			//시간이름을 가진 폴더 생성/같은 이름 가진 폴더가 있으면 에러
			if(mkdir(PATH_NAME, 0777)<0)
				perror("mkdir error\n");
			//없으면 폴더 생성 및 그 안에  파일까지 생성
			else if 
			{
				mkdir(PATH_NAME, 0777);
				strcat(PATH_NAME, mkfileName);
				frameCnt++; //if문 반복시 Cnt증가
				//프레임 1800당 파일생성
				if(frameCnt == 1800) 
				{
					ttime(TIME_FILE, mkfileName);
					strcat(PATH_NAME, mkfileName);
					strcat(PATH_NAME, ".avi");
					writer.open(PATH_NAME, fourcc, framerate, size, true);
				}
			}
		}
		
	
	}

	if(!writer.isOpened()){
        	cout<<" Error : writer.isOpened" <<endl; 
    	}
	
    	cv::namedWindow("CSI Camera", cv::WINDOW_AUTOSIZE);

    	cout << "Hit ESC to exit" << "\n" ;

    	while(true)
    	{
        	if (!cap.read(img))
        	{
            		cout<<"Capture read error"<<std::endl;
           		 break;
		}

		writer.write(img);
		frameCnt++;
        
		if(frameCnt==1800)
		{
			break;
		}
	
		cv::imshow("CSI Camera",img);
		if (waitKey(5) == 27)
			break ;
    	}	

    	cap.release();
    	cv::destroyAllWindows() ;

    	return 0;
}

