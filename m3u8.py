# -*- coding: utf-8 -*-
import datetime
import requests
import argparse
import imutils
import os
from shutil import rmtree

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--input", required=True,
#   help="path to input video")
#args = vars(ap.parse_args())

#if __name__ == "__main__":
def ini_download(whole_name,file_name,output_folder): #whole name include suffix, file name include only prefix

    def get_ts_urls(m3u8_path,base_url):
        urls = []
        with open(m3u8_path,"r") as file:
            print ("get links")
            lines = file.readlines()
            print (lines)
            for line in lines:

                if line.find(".ts") != -1:
                    print (line)
                    tempstr = line
                    y = tempstr.replace('-', '/',2)
                    print(y)
                    urls.append(base_url + y.strip("\n"))
        print(urls)
        return urls
    from video_each import ini_detect
    def download(ts_urls,download_path):
        print ("down mod")
        print (len(ts_urls))
        for i in range(len(ts_urls)):
            ts_url = ts_urls[i]
            file_name = ts_url.split("/")[-1]
            print("Start Download: %s" %file_name)
            #meta_file_name = output_folder+ ".txt"
            #meta_file =open(meta_file_name,"w+")

            start = datetime.datetime.now().replace(microsecond=0)
            try:
                response = requests.get(ts_url,stream=True,verify=False)
            except Exception as e:
                print("Error：%s"  %e.args)
                return

            ts_path = download_path+"/{0}.ts".format(i)
            with open(ts_path,"wb+") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            end = datetime.datetime.now().replace(microsecond=0)

            print("Elasped：%s"%(end-start))

            ini_detect(file_name,ts_path,output_folder)


    if (os.path.isdir(file_name)):
        print("Deleting existing folder")
        rmtree(file_name)

    os.mkdir(file_name)
    print("Going to down mod")

    download(get_ts_urls(whole_name,"http://183.60.119.106:5141/dn/adv/file/"),file_name)
    #m_input = input_name
    #base_name = os.path.basename(m_input)
    #file_name = os.path.splitext(base_name)[0]
    #print (file_name)






#download(get_ts_urls("192-168-1-4-2019_05_13_17.m3u8","http://183.60.119.106:5141/dn/adv/file/"),file_name)
