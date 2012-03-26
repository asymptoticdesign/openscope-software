import Tkinter
import Image, ImageDraw, ImageTk
import scipy, numpy
import os, sys

class Sequence:
    def __init__(self,filename,extension):
        self.fileList = []
        #takes the current directory
        listing = os.listdir(os.getcwd())
        #and makes a list of all items in that directory that contains the filename and extension
        for item in listing:
            if filename and extension in item:
                self.fileList.append(item)
        #and then sorts them into order
        self.fileList.sort()

    def nextImage(self):
        #returns a string with the name of the next image
        return self.fileList.pop(0)

class RegionOfInterest:
    def __init__(self,canvas,boundingBox):
        #take bounding box, draw an oval on the image, save boundingBox locally
        self.box = boundingBox
        self.avgInt = 0
        canvas.create_rectangle(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3],outline="white")

    def redraw(self):
        canvas.create_rectangle(self.box[0],self.box[1],self.box[2],self.box[3],outline="white")  

    def findPixels(self):
        self.pixels = []
        #Take the pixels in the bounding box and create a list of those pixels
        x_coords = (self.box[0],self.box[2])
        y_coords = (self.box[1],self.box[3])
        for i in range(min(x_coords),max(x_coords)):
            for j in range(min(y_coords),max(y_coords)):
                self.pixels.append(imPix[i,j])

    def calcIntensity(self):
        #find the average intensity of all the pixels in the pixel list
        self.avgInt = scipy.mean(self.pixels)
        print "Intensity: ",self.avgInt
        
def draw(event):
    global region
    global listOfRegions
    mouse_X = event.x
    mouse_Y = event.y
    region.append(mouse_X)
    region.append(mouse_Y)
    if len(region) == 4:
        roi = RegionOfInterest(canvas,region)
        listOfRegions.append(roi)
        canvas.update()
        roi.findPixels()
        roi.calcIntensity()
        region = []

def nextFrame(sequence_object,event=None):
    global image_tk
    global imPix
    global listOfRegions
    nextImage = sequence_object.nextImage()
    image = Image.open(nextImage)
    image = image.convert('L')
    imPix = image.load()
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)
    for i in listOfRegions:
        i.redraw()
        i.findPixels()
        i.calcIntensity()
    canvas.update()
    
"""
The following is run once before the the Tkinter mainloop() takes over
"""
window = Tkinter.Tk()
window.title('OpenScope Image Analysis Software')

if len(sys.argv) > 2:
    sequence = Sequence(sys.argv[1],sys.argv[2])
    imageFile = sequence.nextImage()
if len(sys.argv) == 2:
    imageFile = sys.argv[1]

mouse_X = 0
mouse_Y = 0
region = []
listOfRegions = []

image = Image.open(imageFile)
image = image.convert('L')
imPix = image.load()
canvas = Tkinter.Canvas(window, width=image.size[0], height=image.size[1])
canvas.pack()
image_tk = ImageTk.PhotoImage(image)
canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

window.bind("<Button-1>", draw)
window.bind("<Control-space>", lambda e: nextFrame(sequence_object=sequence,event=e))
Tkinter.mainloop()
