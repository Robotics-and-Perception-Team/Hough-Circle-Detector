import cv2
import numpy as np

capture = cv2.VideoCapture(0)
print
capture.get(cv2.CAP_PROP_FPS)
check=0
t = 100
w= 640.0
distance=100 #according to lidar data
last = 0
while True:
    ret, image = capture.read()

    img_height, img_width, depth = image.shape

    scale_percent = 100  # percent of original size
    width_i = int(img_width * scale_percent / 100)
    height_i = int(img_height * scale_percent / 100)
    dim = (width_i, height_i)

    scale = w // img_width
    h = img_height * scale
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    print(image.shape)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,140,0])
    upper_red = np.array([15,255,184])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(image, image, mask=mask)
    red_sayi=1
    x_sum=0
    y_sum=0
    red_middle_x=0
    red_middle_y=0

    # Apply filters
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blured = cv2.medianBlur(grey, 15)

    sc = 1
    md = 30
    at = 40
    try:
        circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, 1, 20, param1=75, param2=40, minRadius=10,maxRadius=120)
        circles = np.uint16(np.around(circles))
    except:
        circles = None


    if circles is not None:
        # We care only about the first circle found.
        circle = circles[0][0]

        x, y = int(circle[0]), int(circle[1])
        if(x>479 or y >639):
            continue
        dot_y=int(h/2)
        print(x , y)
        if hsv[x][y][0]<179 and hsv[x][y][0]>0 and hsv[x][y][1]<207 and hsv[x][y][1]>81 and hsv[x][y][2]>18 and hsv[x][y][2]<152:
            cv2.circle(image, (x, y), 1, (130, 112, 107), 10)

            cv2.circle(image, (red_middle_x, red_middle_x), 1, (0, 255, 0), 10)
            cv2.circle(image, (320, dot_y), 1, (0, 0, 0), 10)
            cv2.line(image, (x, y), (320, dot_y), (120, 150, 30), 5)
            text1 = "circle center:"
            text_x = str(x)
            text_y = str(y)
            difference_x = str(x - 320)
            difference_y = str(dot_y - y)
            cv2.putText(image, text1 + text_x + "," + text_y, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255),
                        2)
            cv2.putText(image, "distance from middle x:" + difference_x, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (209, 80, 0, 255), 2)
            cv2.putText(image, "distance from middle y:" + difference_y, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (209, 80, 0, 255), 2)


        # Draw dot in the center
        #print(image[x][y])

    cv2.imshow('Image with detected circle', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break