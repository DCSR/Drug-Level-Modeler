
import math
import numpy as np
from scipy.optimize import curve_fit
"""
GraphLib.py is used both by SelfAdminXXX.py and Analysis101x.py
SelfAdmin defines two 600x300 canvases
X_ZERO = 50
Y_ZERO = 275

Analysis101.py defines two 800x600 canvases


def cumRecord(aCanvas, dataList, max_x_scale, max_y_scale):
def cumRecord(aCanvas, dataList, max_x_scale, x_divisions, x_pixel_width,
                                  max_y_scale, y_divisions, y_pixel_height):

XlogScaler = 3.5
YlogScaler = 2
"""

def drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "black"):
    """
    Draws an X (horizontal) axis using the following parameters:
    aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions
    """
    # aCanvas.create_text(300, 20, text="graphLibTest")
    aCanvas.create_line(x_zero, y_zero, x_zero + x_pixel_width, y_zero, fill=color)
    for divisions in range(x_divisions + 1):          
        x = x_zero + (divisions * (x_pixel_width // x_divisions))
        aCanvas.create_line(x, y_zero, x, y_zero + 5, fill=color)
        aCanvas.create_text(x, y_zero + 20, text=str(int((max_x_scale/x_divisions)*divisions)), fill=color)

def drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, labelLeft, format_int = False, color = "black"):
    """
    Draws an Y (verticle) axis using the following parameters:
    (aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions,  labelLeft, color):

    labelLeft = True places labels and tick marks on the left of the axis
    Adjust x_zero to move the axis left or right.
        eg. x_zero = x_zero + x_pixel_width will push it all the way to the right edge. 
    """
    aCanvas.create_line(x_zero, y_zero, x_zero, y_zero-y_pixel_height, fill=color)
    for divisions in range(y_divisions+1):          
        y = y_zero - (divisions * (y_pixel_height // y_divisions))
        if labelLeft: offsetDirection = -1   # create_text and hash marks on left side of the axis          
        else: offsetDirection = 1            # create_text and hash marks on right side of the axis
        aCanvas.create_line(x_zero, y, x_zero+(5*offsetDirection), y, fill=color)
        if format_int:
            label = "{:.0f}".format((max_y_scale / y_divisions)*divisions)
        else:     # format with one significant 
            label = "{:.1f}".format((max_y_scale / y_divisions)*divisions)
        # print("label", label)
        aCanvas.create_text(x_zero+(20*offsetDirection), y, fill = color, text=label)

def get_logY_PixelValue(y_zero, y_value, y_scaler, y_startValue):
        y = y_zero-(((math.log(y_value,10)* y_scaler) - (math.log(y_startValue,10) * y_scaler)) // 1)
        return y

def get_logX_PixelValue(x_zero, x_value, x_scaler, x_startValue):
        x = x_zero+(((math.log(x_value,10)* x_scaler) - (math.log(x_startValue,10) * x_scaler)) // 1)
        return x   


def drawLog_X_Axis(aCanvas,x_zero,y_zero,x_pixel_width,x_startValue,x_logRange,caption, test = False):

        logList = []
        increment = x_startValue
        for a in range (0, x_logRange):
            for i in range(1, 10):
                logList.append(increment * i)
            increment = increment * 10
        logList.append(increment)   # add the last value

        tickLabelList = []
        increment = x_startValue
        digits = 4
        for a in range (0, x_logRange):
            #tickLabel = round(increment,digits)
            tickLabelList.append(round(increment,digits))
            #tickLabel = round(increment*3,digits)
            tickLabelList.append(round(increment*3,digits))               
            increment = increment * 10
            if digits > 0: digits = digits - 1
        tickLabelList.append(round(increment,digits)) # add the last value
        #print(tickLabelList)
        
        x_scaler = x_pixel_width / x_logRange        
        aCanvas.create_line(x_zero, y_zero, x_zero+x_pixel_width, y_zero, fill="blue")
        for i in logList:               # add tick marks
            x = get_logX_PixelValue(x_zero, i, x_scaler, x_startValue)
            aCanvas.create_line(x, y_zero, x, y_zero+5,fill="blue")
        for i in tickLabelList:         # add a label
            x = get_logX_PixelValue(x_zero, i, x_scaler, x_startValue)
            aCanvas.create_text(x, y_zero+20, fill="blue", text=str(i))
        # Show caption
        x = x_zero + (x_pixel_width //  2)
        aCanvas.create_text(x, y_zero+40, fill="blue", text= caption)
        # Test will put a red and green dot at 1 and 10 (respectively)
        if test:       
            x = get_logX_PixelValue(x_zero, 1, x_scaler, x_startValue)
            y = y_zero - 10
            symbol = aCanvas.create_oval(x-4,y-4,x+4,y+4, fill="red") 
            x = get_logX_PixelValue(x_zero, 10, x_scaler, x_startValue)
            symbol = aCanvas.create_oval(x-4,y-4,x+4,y+4, fill="green")
    

def drawLog_Y_Axis(aCanvas,x_zero,y_zero,y_pixel_height,y_startValue,logRange,caption,leftLabel=True, test = False):
        """
        y_startValue is a float starting with 1: i.e. .001, 0.01, 1, 10, 100 etc.
        logRange is an integer represent orders of magnitude:
        eg. 1-100, 0.1-100 represents 2 and 3 orders of magnitude respectively

        At some point, logRange might support a float: eg. 2.5 ` two and a holf log units
        """

        if leftLabel: offsetDirection = -1          
        else: offsetDirection = 1
        logList = []
        increment = y_startValue
        for a in range (0, logRange):
            for i in range(1, 10):
                logList.append(increment * i)
            increment = increment * 10
        logList.append(increment)   # add the last value
        tickLabelList = []
        increment = y_startValue
        digits = 4
        for a in range (0, logRange):
            #tickLabel = round(increment,digits)
            tickLabelList.append(round(increment,digits))
            #tickLabel = round(increment*3,digits)
            tickLabelList.append(round(increment*3,digits))               
            increment = increment * 10
            if digits > 0: digits = digits - 1
        tickLabelList.append(round(increment,digits)) # add the last value

        #print(tickLabelList)
        y_scaler = y_pixel_height / logRange        
        aCanvas.create_line(x_zero, y_zero, x_zero, y_zero-y_pixel_height, fill="blue")
        for i in logList:               # add tick marks
            y = get_logY_PixelValue(y_zero, i, y_scaler, y_startValue)
            aCanvas.create_line(x_zero, y, x_zero+(5*offsetDirection), y,fill="blue")
        for i in tickLabelList:         # add a label
            y = get_logY_PixelValue(y_zero, i, y_scaler, y_startValue)
            aCanvas.create_text(x_zero+(20*offsetDirection), y, fill="blue", text=str(i))
        # Caption not presently implemented:
        #   Don't know how to rotate text.
        # test = True will put a red and green dot at 1 and 10 (respectively)
        if test:
            x = x_zero + (10*(-1)*offsetDirection)       
            y = get_logY_PixelValue(y_zero, 1, y_scaler, y_startValue)
            symbol = aCanvas.create_oval(x-4,y-4,x+4,y+4, fill="red") 
            y = get_logY_PixelValue(y_zero, 10, y_scaler, y_startValue)
            symbol = aCanvas.create_oval(x-4,y-4,x+4,y+4, fill="green") 

def betaTestCurve(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, \
                  x_startValue, y_startValue, x_logRange, y_logRange, max_x_scale, max_y_scale, \
                  xList, yList, logX = False, logY = False, drawSymbol = True, drawLine = True, color="black"):


    
        """
        Draws a log-log plot using a list of x and y values. 

        x, new_x, y and new_y refer to pixel values on the canvas
        x_value and y_value refer to data points to be plotted  
        """
        if logX: x_scaler = x_pixel_width / x_logRange           
        else: x_scaler = (x_pixel_width / max_x_scale)
        if logY: y_scaler = y_pixel_height / y_logRange 
        else: y_scaler = (y_pixel_height / max_y_scale)           
        x = x_zero-25
        y = y_zero
        for t in range(len(xList)):
            pointInRange = True
            x_value = xList[t]
            if logX: new_x = get_logX_PixelValue(x_zero, x_value, x_scaler, x_startValue)
            else: new_x = (x_zero + (xList[t] * x_scaler)) // 1
            y_value = yList[t]
            if logY:
                if y_value > 0:
                    new_y = get_logY_PixelValue(y_zero, y_value, y_scaler, y_startValue)
                else:
                    new_y = y_zero
                    pointInRange = False                   
            else: new_y = (y_zero - (yList[t] * y_scaler)) // 1
            if pointInRange:
                if drawSymbol:
                    symbol = aCanvas.create_oval(new_x-4,new_y-4,new_x+4,new_y+4, fill=color)
                if drawLine:
                    if t > 0:
                        aCanvas.create_line(x,y,new_x,new_y,fill=color)
            else: aCanvas.create_text(600, y_zero + 50, text="Point(s) out of range")
            x = new_x
            y = new_y
            
def eventRecord(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, dataList, charList, aLabel, t_zero = 0):
    """
    t_zero is the millis() at start time. Most timestamps are saved as session time, but error timetsamps
    are saved as raw millis() and therefore need to have session start time subtracted
    """
    x = x_zero
    y = y_zero
    x_scaler = x_pixel_width / (max_x_scale*60*1000)
    aCanvas.create_text(x_zero-30, y_zero-5, fill="blue", text = aLabel) 
    for pairs in dataList:
        if pairs[1] in charList:
            newX = (x_zero + ((pairs[0]-t_zero) * x_scaler) // 1)
            aCanvas.create_line(x, y, newX, y)
            if (len(charList) == 1):           #eg. charList = ["P"]
                aCanvas.create_line(newX, y, newX, y-10)
            else:                              #eg. charlist = ["B","b"]
                if pairs[1] == charList[0]:
                    newY = y_zero -10
                else:
                    newY = y_zero                
                aCanvas.create_line(newX, y, newX, newY)
                y = newY                        
            x = newX
            # aCanvas.create_text(x, y_zero+10, fill="blue", text = pairs[1])  # show char underneath 

def cumRecord(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, dataList, showBP, aTitle, leverChar = 'L'):
    aCanvas.create_text(100, 20, fill="blue", text = aTitle)
    lastX = x_zero
    lastY = y_zero
    resets = 0
    x_scaler = x_pixel_width / (max_x_scale*60*1000)
    y_scaler = y_pixel_height / max_y_scale
    respTotal = 0
    # stuff for calculating breakpoint
    BP_not_found = True
    pumpStartTime = 0
    lastTime = 0
    BP_time = 0
    numberOfInfusions = 0
    breakpoint = 0
    delta = 0
    BP_X = x_zero
    BP_Y = y_zero
    for pairs in dataList:
        if pairs[1] == leverChar:
            respTotal = respTotal + 1
            adjustedRespTotal = respTotal - (resets * max_y_scale)
            newX = x_zero + (pairs[0] * x_scaler) // 1
            aCanvas.create_line(lastX, lastY, newX, lastY)
            newY = y_zero - (adjustedRespTotal * y_scaler // 1)
            if newY < (y_zero - y_pixel_height):
                aCanvas.create_line(newX, lastY, newX, (y_zero-y_pixel_height))    #Line to max
                aCanvas.create_line(newX, y_zero-y_pixel_height, newX, y_zero)   #line to Y_ZERO
                resets = resets + 1
                adjustedRespTotal = respTotal - (resets * max_y_scale)
                newY = y_zero - (adjustedRespTotal * y_scaler // 1)
            aCanvas.create_line(newX, lastY, newX, newY)
            lastX = newX
            lastY = newY
        if pairs[1] == 'P':
                aCanvas.create_line(lastX, lastY, lastX+5, lastY+5)
                # Look for breakpoint:
                numberOfInfusions = numberOfInfusions + 1
                pumpStartTime = pairs[0]
                delta = round((pumpStartTime - lastTime)/(1000*60))   # delta in minutes
                if (delta < 60) and BP_not_found:   
                    breakpoint = breakpoint + 1
                    BP_X = lastX
                    BP_Y = lastY
                else:
                    BP_not_found = False
                lastTime = pumpStartTime
    if showBP: 
        aCanvas.create_text(300, 20, fill="red", text = "Infusions = "+str(numberOfInfusions))
        aCanvas.create_text(500, 20, fill="red", text = "breakpoint = "+str(breakpoint))
        aCanvas.create_oval(BP_X-8,BP_Y-8,BP_X+8,BP_Y+8, outline = "red")


def plotXYCurve(aCanvas,x_zero,y_zero,x_pixel_width,y_pixel_height,max_x_scale,max_y_scale,xList,yList):
        """
        Draws a black line with black symbols using responseList
        which is composed of pairs: price and total responses in each block
        """
        # maxYScale = threshRecYMax.get()
        resp_x = x_zero-25
        resp_y = y_zero
        x_scaler = (x_pixel_width / max_x_scale)
        y_scaler = (y_pixel_height / max_y_scale)
        for t in range(len(xList)):    # 0..11
            new_x = (x_zero + (xList[t] * x_scaler)) // 1
            new_y = (y_zero - (yList[t] * y_scaler)) // 1
            symbol = aCanvas.create_oval(new_x-4,new_y-4,new_x+4,new_y+4,fill="black")
            if t > 0:
                aCanvas.create_line(resp_x, resp_y, new_x, new_y,fill="black")
            resp_x = new_x
            resp_y = new_y

def plotLogXYCurve(aCanvas,x_zero,y_zero,x_pixel_width,y_pixel_height, \
                   max_y_scale,xList,yList):
        """
        Draws a black line with black symbols using responseList
        which is composed of pairs: price and total responses in each block
        """
        # maxYScale = threshRecYMax.get()
        XlogScaler = 3.5
        resp_x = x_zero-25
        resp_y = y_zero
        y_scaler = (y_pixel_height / max_y_scale)
        x_scaler = x_pixel_width / XlogScaler
        for t in range(len(xList)):    # 0..11
            price = xList[t]
            new_x = (x_zero + (math.log(price,10)*x_scaler)) // 1
            new_y = (y_zero - (yList[t] * y_scaler)) // 1
            symbol = aCanvas.create_oval(new_x-4,new_y-4,new_x+4,new_y+4,fill="black")
            if t > 0:
                aCanvas.create_line(resp_x, resp_y, new_x, new_y,fill="black")
            resp_x = new_x
            resp_y = new_y

def logLogPlot(aCanvas,x_zero,y_zero,x_pixel_width,y_pixel_height, \
               xLogScaler,yLogScaler,xList,yList,drawSymbol,drawLine,color):
        """
        Draws a log-log plot using a list of x and y values.
        Parmeters:
        aCanvas : 

        x, new_x, y and new_y refer to pixel values on the canvas
        x_value and y_value refer data points to be plotted  
        """
        #print(len(xList))
        #print(len(yList))       
        x_scaler = x_pixel_width / xLogScaler
        y_scaler = y_pixel_height / yLogScaler       
        x = x_zero-25
        y = y_zero
        for t in range(len(xList)):    # 0..11
            x_value = xList[t]
            new_x = (x_zero + (math.log(x_value,10)*x_scaler)) // 1
            y_value = yList[t]
            # print(x_value,y_value)
            if y_value > 0.01:
                new_y = ((y_zero-(math.log(100,10)* y_scaler)) - ((math.log(y_value,10))* y_scaler)) // 1
            else:
                new_y = y_zero
            # new_y = (y_zero - (pairs[1] * y_scaler)) // 1
            if drawSymbol:
                symbol = aCanvas.create_oval(new_x-4,new_y-4,new_x+4,new_y+4, fill=color)
            if drawLine:
                if t > 0:
                    aCanvas.create_line(x,y,new_x,new_y,fill=color)
            x = new_x
            y = new_y

def histogram(aCanvas, aList, x_zero = 75,  max_x_scale = 300,  x_divisions = 5, x_pixel_width = 600, \
                              y_zero = 100, max_y_scale = 4000, y_divisions = 1, y_pixel_height = 400, clear = True):
        """
        (LIst) -> None

        Draws a histogram using a list of numbers. 
        The procedure was written specifically for graphing data from IntA, but
        it could be used for a variety of things. It expects a list of cummulative pump
        times in 60 five second bins (12 bins/min * 5 min)

        """
        if clear:
            aCanvas.delete('all')

        def draw_filled_bar(aCanvas,x,y,pixel_height,width, color = "black"):
            x1 = x
            y1 = y
            x2 = x
            y2 = y - pixel_height
            x3 = x + width
            y3 = y - pixel_height
            x4 = x + width
            y4 = y
            aCanvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, fill = 'red')

        def draw_bar(aCanvas,x,y, pixel_height, width, color = "black"):
            aCanvas.create_line(x, y, x, y-pixel_height, fill=color)
            aCanvas.create_line(x, y-pixel_height, x+width, y - pixel_height, fill=color)
            aCanvas.create_line(x+width, y-pixel_height, x+width, y, fill=color)
        
        labelLeft = True
        aCanvas.create_line(x_zero, y_zero, x_zero + x_pixel_width, y_zero, fill="blue")
        #drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "black")
        #drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, labelLeft, \
        #             format_int = True, color = "black")

        #unitPixelHeight = int(y_pixel_height/y_divisions)
        width = int(x_pixel_width/(len(aList)))           
        for i in range(len(aList)):           
            x = x_zero + (i*width)
            pixel_height = int(aList[i]*(y_pixel_height/max_y_scale))
            #drawBar(aCanvas,x,y_zero,pixel_height,width)
            draw_filled_bar(aCanvas,x,y_zero,pixel_height,width)

              
        

    

    

    
