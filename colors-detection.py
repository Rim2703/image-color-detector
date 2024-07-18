import cv2
import pandas as pd

img_path = r"colorpic.jpg" 
img = cv2.imread(img_path)

clicked = False
r = g = b = x_pos = y_pos = 0 

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("colors.csv", names=index, header=None)

def getColorName(R, G, B):
    min_distance = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"])) 
        if d <= min_distance:
            min_distance = d
            closest_color = csv.loc[i, "color_name"]
    return closest_color

def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global clicked, r, g, b, x_pos, y_pos
        clicked = True
        x_pos = x 
        y_pos = y 
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)
        print(f"Clicked: RGB({r}, {g}, {b})")

cv2.namedWindow('Color detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Color detection', img.shape[1], img.shape[0])
cv2.setMouseCallback('Color detection', draw_function)

while True:
    cv2.imshow('Color detection', img)
    if clicked:
        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1) 
        
        # Creating text string to display( Color name and RGB values )
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        
        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
       
        # For very light colours we will display text in black colour
        if r+g+b>=600:
            cv2.putText(img,text,(50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False

     # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xff == 27:
        break

cv2.destroyAllWindows()
