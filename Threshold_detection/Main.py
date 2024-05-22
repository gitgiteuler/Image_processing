from PIL import Image
from PIL import ImageTk
import tkinter as tk
from tkinter import Button, Label, filedialog
import cv2
from cv2 import threshold
import matplotlib.pyplot as plt
import matplotlib.image as image
import numpy as np
from scipy import signal as sig
from scipy import ndimage as ndi

list = []

def select_image():
    global frame1 
    path = filedialog.askopenfilename()
    list.append(path)
    if len(path)>0:
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 
        image = cv2.resize(image,(400,300))
        #convert the images to PIL format
        image = Image.fromarray(image)
        #convert the PIL format to ImageTk format
        image = ImageTk.PhotoImage(image)
        frame1 = Label(image = image)
        frame1.image = image 
        frame1.pack(side="left",fill=tk.BOTH, expand=True)

def input_delete():
    list.clear()
    frame1.destroy()

def harris_detection(): #Option6 a)
    img=cv2.imread(list[0])
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  
    kernel_x = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    kernel_y = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    derivative_x = sig.convolve2d(gray,kernel_x,mode='same')
    derivative_y = sig.convolve2d(gray,kernel_y,mode='same')
    #1)compute products of derivatives 
    Ixx = ndi.gaussian_filter(derivative_x**2,sigma=1)
    Ixy = ndi.gaussian_filter(derivative_x*derivative_y,sigma=1)
    Iyy = ndi.gaussian_filter(derivative_y**2,sigma=1)
    Ixx_array = np.asarray(Ixx)
    Ixy_array = np.asarray(Ixy)
    Iyy_array = np.asarray(Iyy)
    #1)visualize them in (R,G,B)
    print(Ixx_array)
    print(Ixy_array)
    print(Iyy_array)
    detA = Ixx * Iyy - Ixy**2
    traceA = Ixx + Iyy
    k = float(entry1.get()) #0.2
    #2)calculate corner response 
    corner_response = detA - k * traceA**2
    print(f'Min = {corner_response.min()}, Max={corner_response.max()}')
    corner_response_range = corner_response.max() - corner_response.min()
    scaled_response =(corner_response / corner_response_range)*255
    corners = np.copy(img)
    edges=np.copy(img)
    h_max = corner_response.max()
    h_min = corner_response.min()
    #3)applying the thresholding
    THRESHOLD_CORNER = 0.01
    THRESHOLD_EDGE=0.01
    for y, row in enumerate(corner_response):
        for x, pixel in enumerate(row):
            if pixel >= h_max*THRESHOLD_CORNER:
                corners = cv2.circle(corners,(x,y),1,(0,0,255),5) #If you can't see the corner pixel clearly, you can see them by getting pixel size larger
            elif pixel <= h_min*THRESHOLD_EDGE:
                edges = cv2.circle(edges,(x,y),1,(0,255,0),1)
    #4)use distancde transform
    #corners_n=cv2.distanceTransform(corners,cv2.DIST_L2,3)

    fig,axs = plt.subplots(2,2)
    axs[0,0].imshow(img),plt.title('Original Image')
    axs[0,1].imshow(gray,cmap='gray'),plt.title('Greyscale Image')
    axs[1,0].imshow(corner_response,cmap='gray'),plt.title('Corner response') #2)display corner response
    axs[1,1].imshow(corners,cmap='gray'),plt.title('Corner detected Image) #3)display thresholding
   
    plt.show()
    
window = tk.Tk()
window.geometry("900x400")     
window.title("Hough Transform")
frame1 = None
frame2 = None
# Menu for manupilating
frame3 = tk.LabelFrame(window,bd=2,relief="ridge",text="Menu")
frame3.pack(fill="x")
lbl1= tk.Label(frame3, text = "parameter k:")
lbl1.pack(side=tk.LEFT)
entry1 = tk.Entry(frame3,width=5)
entry1.pack(side="left")
btn1 = tk.Button(frame3,text = "Harris corner detection",command = harris_detection)
btn1.pack(side="left")
btn4 = tk.Button(frame3,text = "Delete Input image",command = input_delete)
btn4.pack(side="left")
btn5 = tk.Button(window, text="Select an image", command=select_image)
btn5.pack(side = "bottom", fill = "both", expand = "yes", padx = "5", pady = "5")
window.mainloop()