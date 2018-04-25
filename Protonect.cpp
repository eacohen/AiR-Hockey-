/*
 * This file is part of the OpenKinect Project. http://www.openkinect.org
 *
 * Copyright (c) 2011 individual OpenKinect contributors. See the CONTRIB file
 * for details.
 *
 * This code is licensed to you under the terms of the Apache License, version
 * 2.0, or, at your option, the terms of the GNU General Public License,
 * version 2.0. See the APACHE20 and GPL2 files for the text of the licenses,
 * or the following URLs:
 * http://www.apache.org/licenses/LICENSE-2.0
 * http://www.gnu.org/licenses/gpl-2.0.txt
 *
 * If you redistribute this file in source form, modified or unmodified, you
 * may:
 *   1) Leave this header intact and distribute it under the same terms,
 *      accompanying it with the APACHE20 and GPL20 files, or
 *   2) Delete the Apache 2.0 clause and accompany it with the GPL2 file, or
 *   3) Delete the GPL v2 clause and accompany it with the APACHE20 file
 * In all cases you must keep the copyright notice intact and include a copy
 * of the CONTRIB file.
 *
 * Binary distributions must follow the binary distribution requirements of
 * either License.
 */


#include <iostream>
#include <signal.h>
#include <stdio.h>
#include <ctime>
#include <stdlib.h>
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <math.h>

#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include <opencv2/opencv.hpp>
#include <opencv2/contrib/contrib.hpp>

#include <libfreenect2/libfreenect2.hpp>
#include <libfreenect2/frame_listener_impl.h>
#include <libfreenect2/threading.h>

#define COORD_MASK 0xfff 
#define COORD_BITS 12
#define XCOORD_OFFSET 12
#define PID_OFFSET 24

bool protonect_shutdown = false;



using namespace cv;
using namespace std;

void sigint_handler(int s)
{
  protonect_shutdown = true;
}

  double timing_acc;
  double timing_acc_n;

  double timing_current_start;


 void startTiming()
  {
    timing_current_start = cv::getTickCount();
  }

  void stopTiming()
  {
    timing_acc += (cv::getTickCount() - timing_current_start) / cv::getTickFrequency();
    timing_acc_n += 1.0;

    if(timing_acc_n >= 100.0)
    {
      double avg = (timing_acc / timing_acc_n);
      std::cout << "Protonect while loop: [FPS] avg. time: " << (avg * 1000) << "ms -> ~" << (1.0/avg) << "Hz" << std::endl;
      timing_acc = 0.0;
      timing_acc_n = 0.0;
    }
  }


int main(int argc, char *argv[])
{
  std::string program_path(argv[0]);
  size_t executable_name_idx = program_path.rfind("Protonect");

  std::string binpath = "/";

  if(executable_name_idx != std::string::npos)
  {
    binpath = program_path.substr(0, executable_name_idx);

  }



  libfreenect2::Freenect2 freenect2;
  libfreenect2::Freenect2Device *dev = freenect2.openDefaultDevice();

  if(dev == 0)
  {
    std::cout << "no device connected or failure opening the default one!" << std::endl;
    return -1;
  }

    timing_acc = 0.0;
    timing_acc_n = 0.0;
    timing_current_start = 0.0;

  signal(SIGINT,sigint_handler);
  protonect_shutdown = false;

  libfreenect2::SyncMultiFrameListener listener(libfreenect2::Frame::Color);
  libfreenect2::FrameMap frames;

  // Setup the color image window
  int window_height = 1080;
  int window_width = 1920;
  cv::namedWindow("Color Image",CV_WINDOW_NORMAL) ;
  cv::resizeWindow("Color Image",window_width/2,window_height/2) ;
  cv::moveWindow("Color Image",window_width/2,32) ;

  //cv::namedWindow("left", CV_WINDOW_NORMAL);
  //cv::resizeWindow("left", 960/2, 1080/2);

  //cv::namedWindow("right", CV_WINDOW_NORMAL);
  //cv::resizeWindow("right", 960/2, 1080/2);
  
  //cv::namedWindow("thresholded image", CV_WINDOW_NORMAL);
  //cv::resizeWindow("thresholded image", 1920/2, 1080/2);
 

  dev->setColorFrameListener(&listener);
  dev->start();


  // setup named fifos
  int fd;
  char *fifo = "/tmp/fifo";
  mkfifo(fifo, 0666);
  int p1Data = -1;
  int p2Data = -1;


  std::cout << "device serial: " << dev->getSerialNumber() << std::endl;
  std::cout << "device firmware: " << dev->getFirmwareVersion() << std::endl;
  cv::Mat colorMapImage;
  cv::Mat depthConverted ;
  cv::Mat leftImage;
  cv::Mat rightImage;
  int colorMapType = cv::COLORMAP_JET ;
  
  int prevXLeft = -1;
  int prevYLeft = -1;
  int prevXRight = -1;
  int prevYRight = -1;
  cv::Mat imgLines = cv::Mat::zeros(window_height, window_width, CV_8UC3);

  while(!protonect_shutdown)
  {
    clock_t start = clock();
    //startTiming() ;
    listener.waitForNewFrame(frames);
    libfreenect2::Frame *rgb = frames[libfreenect2::Frame::Color];

#ifndef LIBFREENECT2_WITH_TEGRA_JPEG_SUPPORT
    cv::imshow("Color Image", cv::Mat(rgb->height, rgb->width, CV_8UC3, rgb->data));
   printf("IFNDEF TAKEN!\n");
#else
    unsigned char **pprgba = reinterpret_cast<unsigned char **>(rgb->data);
    cv::Mat rgba(window_height, window_width, CV_8UC4, pprgba[0]);
    cv::Mat rgbmat(window_height, window_width, CV_8UC3);
    cv::cvtColor(rgba, rgbmat, cv::COLOR_RGBA2RGB);
    cv::Mat hsv(window_height, window_width, CV_8UC3);
    cv::cvtColor(rgbmat, hsv, cv::COLOR_RGB2HSV);
    cv::Mat mask_hsv, result_hsv;
    cv::Mat lower_red, upper_red;
   // cv::inRange(hsv, cv::Scalar(0, 100, 100), cv::Scalar(10, 255, 255), lower_red);
   cv::inRange(hsv, cv::Scalar(160, 100, 100), cv::Scalar(179, 255, 255), upper_red);
    //cv::addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0, mask_hsv);
    cv::bitwise_and(hsv, hsv, result_hsv, upper_red);
    cv::Mat bgr(window_height, window_width, CV_8UC3);
    cv::cvtColor(rgbmat, bgr, cv::COLOR_RGB2BGR);

    //cv::imshow("Color Image", bgr);

    /* Calcualting position of paddles */
    //vector<vector<Point>> contours;
    //vector<Vec4i> hierarchy;
    
    //cv::findContours(upper_red, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
    
    leftImage = upper_red(cv::Rect(0,0,window_width/2,window_height));
    rightImage = upper_red(cv::Rect(window_width/2,0,window_width/2,window_height));
    cv::Moments momLeft, momRight;
    //mom = cv::moments(upper_red);
    momLeft = cv::moments(leftImage);
    momRight = cv::moments(rightImage);

    double leftM01 = momLeft.m01;
    double leftM10 = momLeft.m10;
    double leftArea = momLeft.m00;

    double rightM01 = momRight.m01;
    double rightM10 = momRight.m10;
    double rightArea = momRight.m00;

    p1Data = (1 << PID_OFFSET) | (COORD_MASK << XCOORD_OFFSET) | (COORD_MASK); 
    p2Data = (2 << PID_OFFSET) | (COORD_MASK << XCOORD_OFFSET) | (COORD_MASK);

    if (leftArea > 10000) {
        
        int posX = leftM10 / leftArea;
        int posY = leftM01 / leftArea;
        //printf("Paddle at (%d, %d)\n", posX, posY);    
        if (prevXLeft >= 0 && prevYLeft >=0 && posX >=0 && posY >=0) {
            //printf("Paddle  at (%d, %d)\n", posX, posY);
            cv::line(imgLines, Point(posX, posY), Point(prevXLeft, prevYLeft), Scalar(255,0,255), 4);
        }
        prevXLeft = posX;
        prevYLeft = posY;
        //update transmitted data (player#, x coord, y coord)
        p1Data = (1 << PID_OFFSET) ((posX & COORD_MASK) << XCOORD_OFFSET) |(posY & COORD_MASK);
    }

    if (rightArea > 10000) {
        
        int posX = rightM10 / rightArea;
        int posY = rightM01 / rightArea;
        if (prevXRight >= 0 && prevYRight >=0 && posX >=0 && posY >=0) {
            //printf("Paddle  at (%d, %d)\n", posX, posY);
            cv::line(imgLines, Point(posX+window_width/2, posY), Point(prevXRight+window_width/2, prevYRight), Scalar(255,0,255), 4);
        }
        prevXRight = posX;
        prevYRight = posY;
        //update transmitted data (player#, x coord, y coord)
        p2Data = (2 << PID_OFFSET) ((posX & COORD_MASK) << XCOORD_OFFSET) |(posY & COORD_MASK);
    }

    //send data to game
    write(fd, &p1Data, 4);
    write(fd, &p2Data, 4);
    
    bgr = imgLines + bgr;
    //result_hsv = result_hsv + imgLines;
    //cv::imshow("thresholded image", result_hsv);
    cv::imshow("Color Image", bgr);
    //cv::imshow("left", leftImage);
    //cv::imshow("right", rightImage);
   //printf("ELSE TAKEN\n");
#endif
    
    // Colorize the depth image; - it's only 8 bit, but seems better than gray
    // cv::imshow("depth", cv::Mat(depth->height, depth->width, CV_32FC1, depth->data) / 4500.0f);
    int key = cv::waitKey(1);
    if (key != -1) {
	std::cout << "Key pressed: " << key << std::endl;
    }
    switch (key) {
        case 48: {
           colorMapType = 11; 
         }
         break ;
	case 49:
        case 50:
        case 51:
        case 52:
        case 53:
        case 54:
        case 55:
        case 56:
        case 57: {
	     colorMapType = key-49 ;
		}
	  break ;
        default:
 	  break ;
    } ;
    protonect_shutdown = protonect_shutdown || (key > 0 && ((key & 0xFF) == 27)); // shutdown on escape

    listener.release(frames);
    //stopTiming() ;
    clock_t end = clock();

    double duration = (end - start) / ((double)CLOCKS_PER_SEC);
    duration *= 1000.0;
    printf("Protonect while loop took: %f ms\n", duration);  
    //libfreenect2::this_thread::sleep_for(libfreenect2::chrono::milliseconds(100));
  }

  // TODO: restarting ir stream doesn't work!
  // TODO: bad things will happen, if frame listeners are freed before dev->stop() :(
  dev->stop();
  dev->close();
  
  return 0;
}

