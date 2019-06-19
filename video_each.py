import time
import imutils
from pydarknet  import Image
import cv2
#import m3u8
#if __name__ == "__main__":
import argparse
import os
from video_batch import net

#net = video_batch.net

#parser = argparse.ArgumentParser(description='Process a video.')
#parser.add_argument('path', metavar='video_path', type=str,
#                    help='Path to source video')
#f = open("0"+ ".txt", "w+")
#f.write("Frame          Object \n")
#args = parser.parse_args()
#print("Source Path:", args.path)

#name = video name for each , folder_name = source folder name , output_folder = output folder name
def ini_detect(name,folder_name,output_folder):
    count = 0
    video_name = name
    f_name = folder_name
    prefix_name = os.path.splitext(video_name)[0]
    o_folder = output_folder
    print(folder_name)
    cap = cv2.VideoCapture(folder_name)
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = 540
    width = 720
    average_time = 0


    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #writer = cv2.VideoWriter("output.mp4", fourcc,30,(height,width))
    print (prefix_name)
    output_file_name = o_folder + "/" + prefix_name + ".mp4"
    print (output_file_name)
    print ('%s' '%d' % ("Total Frame = ", int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    writer = cv2.VideoWriter(output_file_name, fourcc,frame_rate,(width,height),True)
    meta_file_name = output_folder+".txt"
    meta_file = open(meta_file_name,"a+")
    meta_file.write('%s' '%s' '%s \n'  % ("Clip: ", prefix_name, ".ts"))
    meta_file.write("Frame   		Object \n")
    while True:
        r, frame = cap.read()
        #frame = imutils.resize(frame, width = 720)

        if r:

            start_time = time.time()
            count += 1
            print(count)
            # Only measure the time taken by YOLO and API Call overhead
            inter_frame = cv2.resize(frame,(width,height),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)

            dark_frame = Image(inter_frame)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            average_time = average_time * 0.8 + (end_time-start_time) * 0.2

            print("Total Time:", end_time-start_time, ":", average_time)

            for cat, score, bounds in results:
                if score  > 0.6:
                    x, y, w, h = bounds
                    new_score = "%.2f" % score
                    cv2.rectangle(inter_frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(0,0,255))
                    #cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0))
                    append_text = str(cat.decode("utf-8")) + " "+ str(new_score)
                    meta_file.write('%d ' ' %d ' ' %d ' ' %d ' ' %d ' ' %s \n'  % (count, int(x-w/2),int(y-h/2),int(x+w/2),int(y+h/2), str(cat.decode("utf-8"))))
                    #meta_text = .format(count) + .format(x) + .format(y) + append_text
                    #meta_file.write(meta_text)
                    cv2.putText(inter_frame, append_text, (int(x-w/2),int(y-h/2)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255),2)


                    #print('%d ' ' %d ' ' %d ' ' %d ' ' %d ' ' %s \n'  % (count, x,y,x+w, y+h, str(cat.decode("utf-8"))))
            #if writer is None:
                #writer = cv2.VideoWriter(f_name + "/" + video_name + "mp4", fourcc,30,(width,height),True)


            # cv2.imshow("preview", frame)
            writer.write(inter_frame)
        else:
            break
    writer.release()
    cap.release()
