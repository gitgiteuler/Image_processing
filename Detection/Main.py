from PIL import Image
from PIL import ImageTk
import tkinter as tk
from tkinter import Button, Label, filedialog
import cv2
from cv2 import threshold
import matplotlib.pyplot as plt
import numpy as np

list = []

def select_image():
    global frame1 
    if len(list) != 0:
        input_delete()
    path = filedialog.askopenfilename()
    list.append(path)
    if len(path)>0:
        image_input = cv2.imread(path)
        gray = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)
        image_rgb = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)
        #convert the images to PIL format
        image_pil = Image.fromarray(image_rgb)
        #convert the PIL format to ImageTk format
        image = ImageTk.PhotoImage(image_pil)
        frame1 = Label(image = image)
        frame1.image = image 
        frame1.pack(side="left",fill=tk.BOTH, expand=True)

def input_delete():
    list.clear()
    frame1.destroy()

def line_detection():
    image = cv2.imread(list[0])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,int(entry1.get()),int(entry2.get()), apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        # Stores the value of cos(theta) in a
        a = np.cos(theta)
        # Stores the value of sin(theta) in b
        b = np.sin(theta)
        # x0 stores the value rcos(theta)
        x0 = a*r
        # y0 stores the value rsin(theta)
        y0 = b*r
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000*(-b))
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000*(a))
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000*(-b))
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000*(a))
        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imshow("Hough Lines", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    list.clear()
    frame1.destroy()
 
def circle_detection():
    image	= cv2.imread(list[0])
    gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(gray_img,	5)
    cimg = cv2.cvtColor(img_blur,cv2.COLOR_GRAY2BGR)
    #center
    circles	= cv2.HoughCircles(
        img_blur,cv2.HOUGH_GRADIENT,1,120
        ,param1=int(entry2.get()),param2=int(entry1.get()) #Need to type the appropriate values such as (param1=30,param2=20)
        ,minRadius=int(entry3.get()),maxRadius=0
        )
    circles	= np.uint16(np.around(circles))
    for	i in circles[0,:]:
        #draw the outer circle
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),3)
        #draw the center of the circle
        cv2.circle(image,(i[0],i[1]),1,(0,0,255),3)
    cv2.imshow("Hough Cirlces", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    list.clear()
    frame1.destroy()

def edge_detection():
    image = cv2.imread(list[0], cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image,100,200)
    plt.subplot(121),plt.imshow(image,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()
    list.clear()
    frame1.destroy()

window = tk.Tk()
window.geometry("900x400")     
window.title("Hough Transform")
frame1 = None
frame2 = None
# Menu for manupilating
frame3 = tk.LabelFrame(window,bd=2,relief="ridge",text="Menu")
frame3.pack(fill="x")
lbl1= tk.Label(frame3, text = "Threshold(Min):")
lbl1.pack(side=tk.LEFT)
entry1 = tk.Entry(frame3,width=5)
entry1.pack(side="left")
lbl2= tk.Label(frame3, text = "Threshold(Max):")
lbl2.pack(side=tk.LEFT)
entry2 = tk.Entry(frame3,width=5)
entry2.pack(side="left")
btn1 = tk.Button(frame3,text = "Straight-line",command=line_detection)
btn1.pack(side="left")
lbl3= tk.Label(frame3, text = "Search radius:")
lbl3.pack(side=tk.LEFT)
entry3 = tk.Entry(frame3,width=5)
entry3.pack(side="left")
btn2 = tk.Button(frame3,text = "Circle",command = circle_detection)
btn2.pack(side="left")
btn3 = tk.Button(frame3,text = "Edge",command = edge_detection)
btn3.pack(side="left")
btn4 = tk.Button(window, text="Select an image", command=select_image)
btn4.pack(side = "bottom", fill = "both", expand = "yes", padx = "5", pady = "5")
window.mainloop()