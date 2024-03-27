import cv2
import numpy as np
import os


def circle_detection(img, display=False):

    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                    cv2.HOUGH_GRADIENT, 1,20,
                            param1=50,param2=30, minRadius = 49, maxRadius = 70)
    # Draw circles that are detected.
    image_center_x, image_center_y = int(img.shape[1]/2), int(img.shape[0]/2)
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        
        for pt in detected_circles[0, :][:1]:
            a, b, r = pt[0], pt[1], pt[2]

            offset_x = a-image_center_x
            offset_y = b-image_center_y

            print(f"find a circle in [{a},{b}] with radius={r}, offset_x={offset_x} offset_y={offset_y} ")
            

            font = cv2.FONT_HERSHEY_SIMPLEX
  
            # org           
            org = (a+60, b+60)
            
            # fontScale
            fontScale = 0.5
            
            # Blue color in BGR
            color = (255, 0, 0)
            
            # Line thickness of 2 px
            thickness = 1
            
            # Using cv2.putText() method
            image = cv2.putText(img, str(a)+','+str(b), org, font, 
                                fontScale, color, thickness, cv2.LINE_AA)    

            cv2.circle(img, (a, b), r, (0, 255, 0), 2)
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
            cv2.circle(img, (image_center_x, image_center_y), 1, (0, 0, 255), 3)
            cv2.line(img,(a,b),(image_center_x, image_center_y),(155, 0, ),1)
           
            if display:
                # Draw the circumference of the circle.
                cv2.imshow("Detected Circle", img)
                cv2.waitKey(0)
    else:
        print("error")

    return img
    #return a, b, r, offset_x, offset_y

def main():
    cap = cv2.VideoCapture("moon_timelapse_nuage_1080.mp4")
    #cap = cv2.VideoCapture("videos/Extrait1-Cosmos_Laundromat1(340p).m4v")
    paused = False  
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            img = circle_detection(frame, False)
            cv2.imshow("image", img) 
            key = cv2.waitKey(25)

            # if spacebar is pressed, pause video
            if key == 32: # ASCII value of spacebar is 32
                paused = not paused

            # if video is paused, wait for spacebar to be pressed again to resume
            while paused:
                key = cv2.waitKey(25)
                if key == 32:
                    paused = not paused

            # if 'q' is pressed, exit loop
            if key == ord('q'):
                break
        else:
            break
if __name__=="__main__":
    main()