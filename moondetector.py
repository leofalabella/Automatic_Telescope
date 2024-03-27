import cv2
import numpy as np
import os


def circle_detection(image_path, display=False):
    
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #-------------------------------------------------
    #threshold
    thres_value = 100
    #_, gray = cv2.threshold(gray, thres_value, 255, cv2.THRESH_BINARY)
    #cv2.imshow("Threshold"+str(thres_value), gray)
    #cv2.waitKey(0)
    #----------------

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
                param2 = 50, minRadius = 50, maxRadius = 120)
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
            
            if display:
                # Draw the circumference of the circle.
                cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                cv2.circle(img, (image_center_x, image_center_y), 1, (0, 0, 255), 3)
                cv2.line(img,(a,b),(image_center_x, image_center_y),(155, 0, ),1)
                #cv2.namedWindow('finalImg', cv2.WINDOW_NORMAL)
                cv2.waitKey(0)
    else:
        print("error")
    
    return a, b, r, offset_x, offset_y

def main():

    directory_name = './images'
    for file_name in os.listdir(directory_name):
        print(file_name)
        circle_detection(directory_name+'/'+ file_name, True)
        
if __name__=="__main__":
    main()