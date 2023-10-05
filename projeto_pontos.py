import cv2
import numpy as np
import json

suffix = '_cin'

json_file_path = f'Pontos/points{suffix}.json'
json_file = open(json_file_path, "r")
data = json.load(json_file)
points = data.get("points", [])

colors = []
colors.append((255, 0, 0))
colors.append((0, 255, 0))
colors.append((0, 0, 255))
colors.append((255, 255, 0))
colors.append((255, 0, 255))
colors.append((0, 255, 255))
colors.append((255, 165, 0))
colors.append((128, 0, 128))
colors.append((255, 192, 203))
colors.append((139, 69, 19))
colors.append((0, 128, 128))
colors.append((230, 230, 250))

image1 = cv2.imread(f"Imagens/image1{suffix}.png")
image2 = cv2.imread(f"Imagens/image2{suffix}.png")

points1 = []
points2 = []
for i in range(len(points)):
    points1.append(points[i][0])
    points2.append(points[i][1])
    
points1 = np.array(points1)


points2 = np.array(points2)

pts1 = points1
pts2 = points2

F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_8POINT)#FM_LMEDS
print(F)


cv2.namedWindow("Epipolar Lines", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Epipolar Lines", image1.shape[1] * 2, image1.shape[0])
counter = 0

def draw_epipolar_line(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global counter

        height = image1.shape[0]
        width = image1.shape[1]
        lines1 = []
        if x > width:        
            x = x % width    
            point1 = np.array([x, y, 1])
            print(point1)
            lines1 = cv2.computeCorrespondEpilines(np.array([[x,y]]), 1, F)
            lines2 = cv2.computeCorrespondEpilines(np.array([[x,y]]), 2, F)

            x1_, y1_ = map(int, [0, -lines2[0][0][2] / lines2[0][0][1]])
            x2_, y2_ = map(int, [image2.shape[1], -(lines2[0][0][0] * image2.shape[1] + lines2[0][0][2]) / lines2[0][0][1]])   
            cv2.line(image1, (x1_, y1_), (x2_, y2_), colors[counter], 2)     

            cv2.circle(image2, (x,y), 2, colors[counter], thickness=2)
            
        else:
            x = x % width   
            point1 = np.array([x, y, 1])            
            lines1 = cv2.computeCorrespondEpilines(np.array([[x,y]]), 1, F)
            lines2 = cv2.computeCorrespondEpilines(np.array([[x,y]]), 2, F)
            
            
            x1, y1 = map(int, [0, -lines1[0][0][2] / lines1[0][0][1]])
            x2, y2 = map(int, [image2.shape[1], -(lines1[0][0][0] * image2.shape[1] + lines1[0][0][2]) / lines1[0][0][1]])
            cv2.line(image2, (x1, y1), (x2, y2), colors[counter], 2)

            cv2.circle(image1, (x,y), 2, colors[counter], thickness=2)

            print('lines1')
            print(lines1)
    
        counter = (counter+1) % len(colors)
        cv2.imshow("Epipolar Lines", np.hstack((image1, image2)))

cv2.setMouseCallback("Epipolar Lines", draw_epipolar_line)

while True:
    cv2.imshow("Epipolar Lines", np.hstack((image1, image2)))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()