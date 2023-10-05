import numpy as np
import cv2
import json
from matplotlib import pyplot as plt

suffix = '_cin'

json_file_path = f'Pontos/points{suffix}.json'
json_file = open(json_file_path, "r")
data = json.load(json_file)
points = data.get("points", [])

img1 = cv2.imread(f"Imagens/image1{suffix}.png", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(f"Imagens/image2{suffix}.png", cv2.IMREAD_GRAYSCALE)

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

def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r,c = img1.shape
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    counter = 0
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), colors[counter],1)
        img1 = cv2.circle(img1,tuple(pt1),5,colors[counter],-1)
        img2 = cv2.circle(img2,tuple(pt2),5,colors[counter],-1)
        counter = (counter+1) % len(colors)
    return img1,img2

lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2,F)
lines1 = lines1.reshape(-1,3)
img5,img6 = drawlines(img1,img2,lines1,pts1,pts2)

lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1,F)
lines2 = lines2.reshape(-1,3)
img3,img4 = drawlines(img2,img1,lines2,pts2,pts1)
plt.subplot(121),plt.imshow(img5)
plt.subplot(122),plt.imshow(img3)
plt.show()