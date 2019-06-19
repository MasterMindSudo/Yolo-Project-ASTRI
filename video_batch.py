#import m3u8.ini_download
from shutil import move
#import m3u8
import time

#from m3u8 import *
#from video_each import ini_detect
#from video_each import *
#import video_each.ini_detect
#import video_each.ini_detect
import os
from pydarknet  import Detector, Image
net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
       bytes("cfg/coco.data", encoding="utf-8"))
meta_file = None
if __name__ == "__main__":

    start_time = time.time()
    folder_name = None # source folder
    output_folder = None
    whole_name = None
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".m3u8"):
            print("Found" + filename)
            whole_name = os.path.basename(filename)
            file_name = os.path.splitext(whole_name)[0]
            folder_name = file_name
            output_folder = folder_name + "_output"
            meta_file = open(output_folder + ".txt" , "w+")


            if (os.path.isdir(output_folder)):
                print("Output Folder Exists, Overwriting")
            else:
                print("Output Folder NOT Exist, Building")
                os.mkdir(output_folder)
            from m3u8 import ini_download
            ini_download(whole_name,file_name,output_folder)
            #move(whole_name, folder_name)
            print ("Finished processing this m3u8 (source), moved to source folder", whole_name," to ",folder_name)


    end_time = time.time()
    print("Total time : ", end_time - start_time)


#for filename in os.listdir(folder_name):
#    if filename.endswith(".ts"):
#    	whole_name = os.path.basename(filename)
#    	ini_detect(whole_name,folder_name,output_folder)
        #pre_name = os.path.splitext(base_name)[0]
