import Tkinter
import Image, ImageDraw, ImageTk
import scipy
import numpy

class RegionOfInterest:
    def __init__(self,canvas,boundingBox):
        #take bounding box, draw an oval on the image, save boundingBox locally
        self.box = boundingBox
        self.pixels = []
        self.avgInt = 0
        canvas.create_rectangle(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3],outline="white")

    def findPixels(self):
        #Take the pixels in the bounding box and create a list of those pixels
        x_coords = (self.box[0],self.box[2])
        y_coords = (self.box[1],self.box[3])
        for i in range(min(x_coords),max(x_coords)):
            for j in range(min(y_coords),max(y_coords)):
                self.pixels.append(imPix[i,j])

    def calcIntensity(self):
        #find the average intensity of all the pixels in the pixel list
        self.avgInt = scipy.mean(self.pixels)
        print 'Average Intensity is: ',self.avgInt

def drawEllipse(event):
    global region
    mouse_X = event.x
    mouse_Y = event.y
    region.append(mouse_X)
    region.append(mouse_Y)
    if len(region) == 4:
        #draw.ellipse(region,fill=(0,255,0))
        roi = RegionOfInterest(canvas,region)
        canvas.update()
        roi.findPixels()
        roi.calcIntensity()
        region = []

window = Tkinter.Tk()
window.title('Calcium Imaging Software')

mouse_X = 0
mouse_Y = 0
region = []

image = Image.open("test.jpg")
image = image.convert('L')
imPix = image.load()
#draw = ImageDraw.Draw(image)
canvas = Tkinter.Canvas(window, width=image.size[0], height=image.size[1])
canvas.pack()
image_tk = ImageTk.PhotoImage(image)
canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

canvas.bind("<Button-1>", drawEllipse)
Tkinter.mainloop()
