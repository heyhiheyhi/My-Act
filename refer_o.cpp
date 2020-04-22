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
#include<iostream>
#include<sys/stat.h>
#include<ctime>
#include<string.h>
#include<stdlib.h>

using namespace cv;
using namespace std;


int capture_width = 640 ;
int capture_height = 480 ;
double framerate = 30.0 ;
int flip_method = 0 ;

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

char* getTime_dir(){
	struct tm* tm;
        time_t UTCtime = time(0);
        tm = localtime(&UTCtime);

        char* name;
        name=(char*)malloc(sizeof(name));
        strftime(name, 15, "%Y%m%d_%H", tm);
        return name;
	
}


char* getTime_f(){
 	struct tm* tm;
        time_t UTCtime = time(0);
        tm = localtime(&UTCtime);

        char* name;
        name=(char*)malloc(sizeof(name));
        strftime(name, 18, "%Y%m%d_%H%M%S", tm);
        return name;
}


int main()
{
 	char* dir_name;
	char* f_name;

	int i=0;
	int j=0;
	
//	f_name = getTime_f();
//	mkdir((char*)dir_name,0777);

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
	writer.open(f_name , fourcc, framerate, size, true);
	if(!writer.isOpened()){

	cout<<" Error : writer.isOpened" <<endl; 
	}

	cv::namedWindow("CSI Camera", cv::WINDOW_AUTOSIZE);
	cout << "Hit ESC to exit" << "\n" ;

	int frameCnt=0;
	while(true)

	{
		dir_name=getTime_dir();
		if (!cap.read(img))
		{
			cout<<"Capture read error"<<std::endl;
			break;
		}
		writer.write(img);
		frameCnt++;
        
		if(frameCnt==90)
		{
			writer.release();
			frameCnt=0;
			cout<<"Record is Done!" <<endl;

			f_name = getTime_f();
 		    	writer.open(f_name , fourcc, framerate, size, true);
			mkdir((char*)dir_name,0777);
			frameCnt=0;
		}
	
		cv::imshow("CSI Camera",img);
		if (waitKey(5) == 27)
			break ;
	}
	cap.release();
	cv::destroyAllWindows() ;
	printf("%s\n",dir_name);
	printf("%s\n",f_name);
	return 0;
}
