#!/usr/bin/env python2
""" Image Processing with PIL and cImage

    Originated from assignments in interactivepython.org (Iteration Chapter).
    Applies different filters/algorithms to an image file, displays the changes
    and writes a new file.
    Both PIL and the supplied cImage libraries must be present on your system.

    Available filters/methods:
    invert - Inverts all pixels in the given image.
    greyscale - Turns picture into a grey version by averaging each pixels RBG values.
    blackwhite - Creates a black and white version of the given image.
    removecolor - Removes one color (currently only red) from the picture.
    sepia - Applies the sepia filter to the given image.
    double - Doubles the size of the image.
    average - Smoothes out the image by averaging the 8 neighbors of a pixel.
    median - Same thing as average but using a median. Likely gives better results.
    
    TODO:
    1. Use colorsys to add HLS, HSV, YIQ compatibility and customization (satu-
    ration, intensity, lightness)
    2. Write testcases
    3. Add file type conversion
    4. Add command line arguments
    5. Add resizing and thumbnail methods
    6. Use gaussian kernel for average() instead of averaging.
        Also source out the neighborhood stuff to a separate method.
"""


import cImage as image
from os.path import splitext

class ImageFilter(object):

    def __init__(self, img_file):
        "Initialize image, clone it, get its size and create a canvas"
        self.img_file = img_file
        self.oldimg = image.Image(self.img_file)
        self.newimg = self.oldimg.copy()
        self.width = self.oldimg.getWidth()
        self.height = self.oldimg.getHeight()
        self.win = image.ImageWin(self.img_file, self.width, self.height)

    def write(self, func_name="_"):
        "Draw and save a processed image"
        # This order will only save if the window gets clicked on.
        self.newimg.draw(self.win)
        self.win.exitonclick()
        img_name, img_ext = self.strip_name()
        self.newimg.save(img_name+func_name+img_ext)

    def strip_name(self):
        "Strips the name of a file into (pathname, extension)"
        return splitext(self.img_file)

    def invert(self):
        "Invert the colors of the image"
        for col in range(self.width):
            for row in range(self.height):
                pixel = self.newimg.getPixel(col,row)
                pixel.red = 255 - pixel.red
                pixel.green = 255 - pixel.green
                pixel.blue = 255 - pixel.blue
                self.newimg.setPixel(col,row,pixel)
        self.write("_inv")

    def greyscale(self):
        "Convert image to greyscale"        
        for col in range(self.width):
            for row in range(self.height):
                pixel = self.newimg.getPixel(col,row)
                avg = (pixel[0]+pixel[1]+pixel[2])/3
                pixel.red = pixel.green = pixel.blue = avg
                self.newimg.setPixel(col,row,pixel)
        self.write("_grey")

    def blackwhite(self):
        "Convert image to black and white"
        for col in range(self.width):
            for row in range(self.height):
                pixel = self.newimg.getPixel(col,row)
                avg = (pixel[0]+pixel[1]+pixel[2])/3
                if avg >= 128:
                    avg = 255
                else:
                    avg = 0
                pixel.red = pixel.green = pixel.blue = avg
                self.newimg.setPixel(col,row,pixel)
        self.write("_bw")

    def removecolor(self, color="R"):
        "Remove either (R)ed, (G)reen, (B)lue or a combination of those"
        # TODO: Add options for different colors.
        for col in range(self.width):
            for row in range(self.height):
                p = newimg.getPixel(col,row)
                p.red = 0
                newimg.setPixel(col,row,p)
        self.write("_rc")
        
    def sepia(self):
        "Apply the sepia filter to the image"
        for col in range(self.width):
            for row in range(self.height):
                try:
                    p = self.newimg.getPixel(col,row)
                    p.red = int(p.red * 0.393 + p.green * 0.769 + p.blue * 0.189)
                    p.green = int(p.red * 0.349 + p.green * 0.686 + p.blue * 0.168)
                    p.blue = int(p.red * 0.272 + p.green * 0.534 + p.blue * 0.131)
                    self.newimg.setPixel(col,row,p)
                except:
                    continue
        self.write("_sepia")

    def double(self):
        "Double the size of the image"
        self.newimg = image.EmptyImage(self.width*2, self.height*2)
        self.win = image.ImageWin(self.img_file, self.width*2, self.height*2)
    
        for row in range(self.height):
            for col in range(self.width):    
                self.oldpixel = self.oldimg.getPixel(col,row)
                self.newimg.setPixel(2*col,2*row, self.oldpixel)
                self.newimg.setPixel(2*col+1, 2*row, self.oldpixel)
                self.newimg.setPixel(2*col, 2*row+1, self.oldpixel)
                self.newimg.setPixel(2*col+1, 2*row+1, self.oldpixel)
        self.write("_double")

    def average(self):
        """Average

        Apply average of surrounding 8 pixels to the current pixel.
        This should probably be updated to use Gaussian instead."""
        
        for row in range(self.height):
            for col in range(self.width):    
                p = self.newimg.getPixel(col, row)
                neighbors = []
                for i in range(col-1, col+2):
                    for j in range(row-1, row+2):
                        try:
                            neighbor = self.newimg.getPixel(i, j)
                            neighbors.append(neighbor)
                        except:
                            continue
                nlen = len(neighbors)
                # Average out the RBG values
                if nlen:
                # Uncommented, the following line would leave most of the white 
                # untouched which works a little better for real photographs, imo.
                #~ if nlen and p[0]+p[1]+p[2] < 690:
                    p.red = sum([neighbors[i][0] for i in range(nlen)])/nlen
                    p.green = sum([neighbors[i][1] for i in range(nlen)])/nlen
                    p.blue = sum([neighbors[i][2] for i in range(nlen)])/nlen
                    self.newimg.setPixel(col,row,p)
        self.write("_avg")

    def median(self):
        """Median

        Apply median of surrounding 8 pixels to current pixel
        This usually gives better results than average()"""
        for row in range(self.height):
            for col in range(self.width):
                p = self.newimg.getPixel(col, row)
                neighbors = []
                for i in range(col-1, col+2):
                    for j in range(row-1, row+2):
                        try:
                            neighbor = self.newimg.getPixel(i, j)
                            neighbors.append(neighbor)
                        except:
                            continue
                nlen = len(neighbors)
                # Making sure the list of pixels is not empty
                if nlen:
                    red = [neighbors[i][0] for i in range(nlen)]
                    green = [neighbors[i][1] for i in range(nlen)]
                    blue = [neighbors[i][2] for i in range(nlen)]
                    # Sort the lists so we 
                    for i in [red, green, blue]:
                        i.sort()
                    # If the list has an odd number of items in it.
                    if nlen % 2:
                        p.red = red[len(red)/2]
                        p.green = green[len(green)/2]
                        p.blue = blue[len(blue)/2]
                    else:
                        p.red = (red[len(red)/2] + red[len(red)/2-1])/2
                        p.green = (green[len(green)/2] + green[len(green)/2-1])/2
                        p.blue = (blue[len(blue)/2] + blue[len(blue)/2-1])/2
                    self.newimg.setPixel(col,row,p)
        self.write("_median")


if __name__ == "__main__":
    #~ img = Image("cy.png")
    #~ img.double()
    img2 = ImageFilter("cyd.png")
    img2.median()