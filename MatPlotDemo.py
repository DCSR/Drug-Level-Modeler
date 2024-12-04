"""

Objectives
1. To illustrate how to use an Object-Oriented approach with MatplotLib
2. To illustrate how to us the tk backend without pyplot
3. And include a plt.show() window as well

This needs alot of documentation.


"""
import tkinter as tk            # tk is used for the root application
import tkinter.ttk as ttk       # ttk has better widgets
from tkinter import *
import sys
from datetime import datetime, date, time

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.lines as lines
import matplotlib.pyplot as plt

from matplotlib.ticker import (MultipleLocator, MaxNLocator, FormatStrFormatter, AutoMinorLocator)

import numpy as np
from scipy.optimize import curve_fit

def main(argv=None):
    if argv is None:
        argv = sys.argv
    gui = GuiClass()
    gui.go()
    return 0

class GuiClass(object):
    def __init__(self):

        self.root = tk.Tk()
        self.root.wm_title("MatPlotDemo.py")

        # buttonFrame       
        self.buttonFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.buttonFrame.grid(column = 0, row = 0, sticky = 'N')
        Button1 = ttk.Button(self.buttonFrame,text="clearFigure()",command=lambda: self.clearFigure())
        Button1.grid(column = 0, row = 0)
        Button2 = ttk.Button(self.buttonFrame,text="figureAndAxes()",command=lambda: self.figureAndAxes())
        Button2.grid(column = 0, row = 1)
        Button3 = ttk.Button(self.buttonFrame,text="patchesAndLines()",command=lambda: self.patchesAndLines())
        Button3.grid(column = 0, row = 2)
        Button4 = ttk.Button(self.buttonFrame,text="drawSomeLInes()",command=lambda arg = 1: self.drawSomeLines())
        Button4.grid(column = 0, row = 3)
        
        Button5 = ttk.Button(self.buttonFrame,text="drawSinePlot",command=lambda: self.drawSinePlot())
        Button5.grid(column = 0, row = 4)
        Button6 = ttk.Button(self.buttonFrame,text="curveFitLinear()",command=lambda: self.curveFitLinear())
        Button6.grid(column = 0, row = 5)        
        Button7 = ttk.Button(self.buttonFrame,text="curveFitExp(0)",command=lambda arg = 0: self.curveFitExp(arg))
        Button7.grid(column = 0, row = 6)
        Button8 = ttk.Button(self.buttonFrame,text="curveFitExp(1)",command=lambda arg = 1: self.curveFitExp(arg))
        Button8.grid(column = 0, row = 7)
        Button9 = ttk.Button(self.buttonFrame,text="drawDoublePlot()",command=lambda arg = 0: self.drawDoublePlot(arg))
        Button9.grid(column = 0, row = 8)
        Button10 = ttk.Button(self.buttonFrame,text="twinxCurves",command=lambda arg = 0: self.twinxCurves())
        Button10.grid(column = 0, row = 9)
        Button11 = ttk.Button(self.buttonFrame,text="Report",command=lambda arg = 0: self.report())
        Button11.grid(column = 0, row = 10)
        Button12 = ttk.Button(self.buttonFrame,text="PlayGround",command=lambda arg = 0: self.playGround())
        Button12.grid(column = 0, row = 11)
        
        self.radioButtonFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.radioButtonFrame.grid(column = 0, row = 1, sticky = 'N')

        # add button for drawSomeLInes()
        
        self.showOn_tkCanvas = BooleanVar(value = True)
        """
        pyplotButton = Checkbutton(self.radioButtonFrame, text = "Show on Canvas", variable = self.showOn_tkCanvas, onvalue = True, offvalue = False)
        pyplotButton.grid(row = 1, column = 0)
        """
        
        canvasButton = Radiobutton(self.radioButtonFrame, text = "tk Canvas", variable = self.showOn_tkCanvas, value = 1).grid(row = 0, column = 0, sticky = W)
        pyplotButton = Radiobutton(self.radioButtonFrame, text = "pyplot ", variable = self.showOn_tkCanvas, value = 0).grid(row = 0, column = 1, sticky = W)
        
        # Create a ttk Frame to hold the MatplotLib Figure
        self.canvasFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.canvasFrame.grid(column = 1, row = 0)
        #self.canvasFrame.grid(column = 1, row = 0, rowspan = 5)

        # Create a matplotLib Figure - a matplotlib container for plots (axes) and patches 
        self.matPlotFigure = Figure(figsize=(6,6), dpi=80, constrained_layout = False) # Creates a 480 x 480 pixel figure.
        self.matPlotFigure.set_facecolor("white")        

        # Create the matplotlib canvas that the TkAgg backend renders on.
        # And this is the thing that gets redrawn after things are changed.
        self.matPlotCanvas = FigureCanvasTkAgg(self.matPlotFigure, master=self.canvasFrame)
        self.matPlotCanvas.get_tk_widget().grid(row=1,column=0)
      
        # Date Time Frame 
        self.dateTimeFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.dateTimeFrame.grid(column = 0, row = 1, columnspan = 2)
        self.timeStringVar = tk.StringVar()
        timeLabel = ttk.Label(self.dateTimeFrame, textvariable = self.timeStringVar)
        timeLabel.grid(column = 0, row = 0)

    def clearFigure(self):
        print("clearFigure")
        self.matPlotFigure.clf()
        self.matPlotCanvas.draw()

    def figureAndAxes(self):       
        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = False)  # Newly instantaited pyplot figure
                       
        print(fig) # - outputs:  "Figure(400x400)"
        print(fig.axes)     #  returns : []
        
        # Figure stuff       
        fig.patch.set_facecolor("azure") # or "none"
        fig.patch.set_linewidth(5.0)     # 0.5 would be very thin
        fig.patch.set_edgecolor("black") # or "none"
        fig.suptitle("Figure Title", fontsize = 16, x = 0.2, y = 0.94)

        # Axes stuff
        ax1 = fig.add_subplot(111)  
        print("ax1", ax1)
        ax1.set_title("aGraph Title \n Second Row", pad = 25.0)
        ax1.set_position([0.2, 0.2, 0.6, 0.6])
        ax1.patch.set_facecolor("green")  # or "none"
        ax1.patch.set_alpha(0.2)          # Here we make it 80% transparent to tone down the green.

        # X Axis        
        ax1.set_xlim(0,100)
        ax1.xaxis.set_major_locator(MaxNLocator(5))       # Four major intervals
        ax1.xaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval

        ax1.set_xlabel('X axis label: fontsize = 14', fontsize = 14, color = 'blue')
        ax1.xaxis.labelpad = 25          # Move label up or down

        # Y Axis
        ax1.set_ylim(0, 5)
        ax1.yaxis.set_major_locator(MultipleLocator(1.0))  # Pick interval
        ax1.yaxis.set_minor_locator(AutoMinorLocator(5))  # 5 ticks per interval
        ax1.set_ylabel('Y axis label: fontsize = 14', fontsize = 14)
        ax1.yaxis.labelpad = 25          # Move label left or right

        ax1.spines['top'].set_color('blue')
        ax1.spines['top'].set_position(('axes', 1.02))    # Offset the axis 0.02 to left of zero
        ax1.spines['bottom'].set_color('blue')
        ax1.spines['bottom'].set_position(('axes', -0.02))  # Offset X axis down 0.02 
        ax1.spines['left'].set_color('blue')
        ax1.spines['left'].set_position(('axes', -0.02))    # Offset the axis 0.02 to left of zero
        ax1.spines['right'].set_color('blue')
        ax1.spines['right'].set_position(('axes', 1.02))    # Offset to the right

        ax1.set_aspect(15.0)        # This pegs the aspect ratio and guarantees that
                                    # the tk and pyplot are the same ratio
        print('Aspect Ratio:', ax1.get_aspect())  

        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()

    def patchesAndLines(self):
        
        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()                   # Clear Figure
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = False)  # Newly instantaited pyplot figure
                       
        print(fig) # - outputs:  "Figure(400x400)"
        print(fig.axes)     #  returns : []

        def myArrow(x,y,l, aTransform, aColor = 'k'):
            """
            Creates a horizontal Arrow that points at [x,y] with length = l
            A positive l will point to the right
            A negative l will point to the left

            Annoyingly, the patches.Arrow starts at [x,y] and points away.
            """
            p = patches.Arrow(x+l, y, -l, 0.0, width = 0.05, clip_on = False, color = aColor, \
            transform = aTransform)
            # The tail of the arrow is at X1, Y1,
            # (X1,Y1, head offset from X1, head offset from Y1, width...)
            #p = patches.Arrow(0.5, 0.6, 0.0, -0.1, width = 0.05, clip_on = False, color = 'r')
            return p
 
        # Figure stuff       
        fig.patch.set_facecolor("azure") # or "none"
        fig.patch.set_linewidth(5.0)     # 0.5 would be very thin
        fig.patch.set_edgecolor("black") # or "none"

        # Axes stuff
        ax1 = fig.add_subplot(111)  
        ax1.set_position([0.2, 0.2, 0.6, 0.6])
        ax1.patch.set_facecolor("green")  # or eg. "none"
        ax1.patch.set_alpha(0.2)          # Here we make it 80% transparent to tone down the green.

        # X Axis        
        # Y Axis

        for position in ax1.spines:         #'top', 'bottom', 'left', right'
            ax1.spines[position].set_color('blue')

        ax1.set_aspect(1.0)                     # This pegs the aspect ratio and guarantees that
                                            # the tk and pyplot are the same ratio
        print('Aspect Ratio:', ax1.get_aspect())  

        # Pathches are 2D shapes that are rendered onto the Figure or Axes.

        circ1 = patches.Circle((0.0, 0.8), 0.1, color='r', alpha=0.3, transform = ax1.transAxes, \
                              clip_on = True)
        circ2 = patches.Circle((0.0, 0.2), 0.1, color='b', alpha=0.3, transform = ax1.transAxes, \
                              clip_on = False)
        rect = patches.Rectangle((0.8,0.7), 0.2, 0.2, color='cyan', alpha=0.4, transform = fig.transFigure, \
                              clip_on = False)

        poly_coords = [(0.25, 0.75), (0.75, 0.75), (0.75, 0.3), (0.25, 0.75) ] # draw a triangle
        ax1.add_patch(plt.Polygon(poly_coords, color ='forestgreen', alpha = 0.5))

        ax1.add_patch(circ1)
        ax1.add_patch(circ2)
        ax1.add_patch(rect)    

        ax1.text(0.5, 0.7, '[0.5,0.7] align right', ha = 'right', transform=ax1.transAxes)
        ax1.text(0.5, 0.5, '[0.5,0.5] centered', ha = 'center', va = 'center', transform=ax1.transAxes)
        ax1.text(0.5, 0.3, '[0.5,0.3] align left', ha = 'left', transform=ax1.transAxes)
        ax1.text(0.5, 0.1, '[0.5,0.1] vertical', ha = 'center', rotation= 'vertical', transform=ax1.transAxes)
        ax1.text(0.5, 1.1, '[0.5,1.1]', ha = 'center', transform=ax1.transAxes, \
                 fontsize=20, color='red')
        # ha = horizontalalignment, va = verticalalignment, 'center', 'right' or 'left'

        # https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Arrow.html
        # class matplotlib.patches.Arrow(x, y, dx, dy, *, width=1.0, **kwargs)

        arrow1 =  patches.Arrow(0.2, 0.5, -0.1, -0.2, width = 0.05, clip_on = False, color = 'r')

        # arrow1 = myArrow(0.0,0.5, 0.15, ax1.transData, aColor = 'r')
        arrow2 = myArrow(0.0, 0.5, -0.1,  ax1.transAxes)   # uses myArrow

        ax1.add_patch(arrow1)
        ax1.add_patch(arrow2)

        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()


    def drawSomeLines(self):
        """
        Line2D args:        https://matplotlib.org/api/_as_gen/matplotlib.lines.Line2D.html
        Marker styles: https://matplotlib.org/api/markers_api.html#module-matplotlib.markers

        """     
        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = True)  # Newly instantaited pyplot figure
  
        ax1 = fig.add_subplot(111)   # Create a new subplot
        ax1.set_title('Another Graph \n Second line')
        ax1.set_xlabel('X axis label: fontsize = 12', fontsize = 12)      
        ax1.set_ylabel('Y axis label: fontsize = 10', fontsize = 10)       
        ax1.set_xscale("linear")
        ax1.set_yscale("linear")
        ax1.set_xlim(0, 22)  
        ax1.set_ylim(0, 22)

        x = [2,6,10,14,18]
        y1 = [16,18,18,18,16] 
        line1 = Line2D(x,y1, color = 'red', ls = 'solid', marker = 'o')       # circle
        ax1.add_line(line1)

        x = [2,6,10,14,18]
        y2 = [14,16,16,16,14]
        line2 = Line2D(x,y2, color = 'blue', ls = "dashed", marker = 's')      # square
        ax1.add_line(line2)

        x = [2,6,10,14,18]
        y3 = [12,14,14,14,12]
        line3 = Line2D(x,y3, color = 'green', ls = 'dotted', marker = 'D', markersize = 3.5)      # diamond
        ax1.add_line(line3)

        ax1.legend(handles=(line1, line2, line3), labels=('label1', 'label2', 'label3'),loc='upper right')

        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()
            
    def drawSinePlot(self):
        """
        Simple example of drawing a graph using Line2D
        """
        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = True)  # Newly instantaited pyplot figure
 
        ax1 = fig.add_subplot(111)   # Create a new subplot
        ax1.set_position([0.2, 0.2, 0.6, 0.6])
        ax1.set_xlim(0,1)
        ax1.set_ylim(-1, 1)
        ax1.set_title('First line of title\n Second line')
        ax1.set_xlabel('X axis label: fontsize = 14', fontsize = 14)
        ax1.xaxis.labelpad = 25 
        ax1.set_ylabel('Y axis label: fontsize = 14', fontsize = 14)
        ax1.yaxis.labelpad = 25 

        x = np.arange(0.0,1.0,0.01)   # Using numpy, generate an array of x values from 0 to 1 in 0.01 intervals
        y = np.sin(3*np.pi*x)         # Generate a corresponding array of y using the numpy sine function        
        aLine   = Line2D(x,y, color = 'black')  
        ax1.add_line(aLine)

        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()

    def curveFitLinear(self):
        """
        curve_fit() example.
        Might be a little easier to understand using y = ax + b as function

        This genenerate a noisy dataset using parameters. It then submits this dataset
        to curve_fit() which returns its best guess at a and b.

        The scatter plot is generated with the best fit line (plus and minus some measure of varaince).
              
        """
        def fitFunc(x,a,b):
            y = (a * x) + b
            return y

        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = True)  # Newly instantaited pyplot figure
 
        ax1 = fig.add_subplot(111)   # Create a new subplot

        # Generate a dataset using known parameters (temp) and add some noise (noisyDataset)               
        x = np.arange(0,10,0.1)         # Using numpy, generate an array of x from 0 to 10 in interavsl of 0.1    
        y = fitFunc(x, 2.5, 10)         # Generate a corresponding array of y values using fitFunc()
        noisyDataset = y + 5*np.random.normal(size=len(y))
 
        fitParams, fitCovariances = curve_fit(fitFunc, x, noisyDataset)
        print (fitParams)
        print (fitCovariances)
        
        ax1.set_ylabel('Y Label', fontsize = 16)
        ax1.set_xlabel('X Label', fontsize = 16)
        ax1.set_xlim(0,10)

        sigma = [fitCovariances[0,0], \
                 fitCovariances[1,1]]
        ax1.plot(x, fitFunc(x, fitParams[0], fitParams[1]),\
                 x, fitFunc(x, fitParams[0] + sigma[0], fitParams[1] - sigma[1]),\
                 x, fitFunc(x, fitParams[0] - sigma[0], fitParams[1] + sigma[1]))
        ax1.scatter(x, noisyDataset) 
                
        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()

    def curveFitExp(self,arg):
        """
        Example using  curve_fit to solve for three parameters in an exponential function.
        The equation is given in fitFunc()
        - curve_fit uses fitFunc() and arrays of x and y data: 
        - curve_fit() returns fitParams and fitCovariances
        - fitParams is an array corresponding to a,b anc c in the fitFunc().
        - fitCovariances reflect the varainaces around those parameters.
        - aGraph plots the best fit curve plus/minus the varaince.

        arg == 1 - plots using log scales
        arg == 0 - plots using linear scales

        ToDo: It might be easier to understand if the lines are plotted with Line2D
              Plot the fitline in blue and the 
         
        """

        def fitFunc(x, a, b, c):
            y = a * np.exp(-b*x) + c
            return y

        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = True)  # Newly instantaited pyplot figure
 
        ax1 = fig.add_subplot(111)   # Create a new subplot

        # Generate a dataset using known parameters (temp) and add some noise (noisyDataset)
        x = np.linspace(0.1,4,50)             # Generate an array with 50 points, starting at 0.1 and ending at 4
        temp = fitFunc(x, 2.5, 1.3, 0.5)      # Generate a corresponding array of y using fitFunc
        noisyDataset = temp + 0.5 * np.random.normal(size=len(temp))   # Add some noise to the dataset

        # Try curve fitting - 
        fitParams, fitCovariances = curve_fit(fitFunc, x, noisyDataset)
        #print (fitParams)
        #print (fitCovariances)

        ax1.set_ylabel('Y Axis Label', fontsize = 16)
        ax1.set_xlabel('X Axis Label', fontsize = 16)

        if (arg == 0):
            ax1.set_xscale("log")
            ax1.set_yscale("log")
            ax1.set_xlim(0.03, 10)        
            ax1.set_ylim(0.1, 10)
        else:
            ax1.set_xscale("linear")
            ax1.set_yscale("linear")
            ax1.set_xlim(0, 4)        
            ax1.set_ylim(0, 4)
            
                  # .0001 to 10
        sigma = [fitCovariances[0,0], \
                 fitCovariances[1,1], \
                 fitCovariances[2,2] \
                 ]
        ax1.plot(x, fitFunc(x, fitParams[0], fitParams[1], fitParams[2]),\
                 x, fitFunc(x, fitParams[0] + sigma[0], fitParams[1] - sigma[1], fitParams[2] + sigma[2]),\
                 x, fitFunc(x, fitParams[0] - sigma[0], fitParams[1] + sigma[1], fitParams[2] - sigma[2]))

        ax1.scatter(x, noisyDataset)
        
        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()

    def drawDoublePlot(self,arg):

        """
        For positioning graphs see:
        https://matplotlib.org/tutorials/intermediate/gridspec.html?highlight=gridspec

        Use GridSpec to define how the figures fit into the space.
        Here we define a 3x3 space. The top figure uses a 2x3 space
        and the bottom uses a 1x3 space. 

        uses numpy two dimensional indexing for a 3x3 array
        >>> x = np.arange(10)
        >>> x
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> x[0:2]
        array([0, 1])
        >>> x[0:3]
        array([0, 1, 2])
        """
        from matplotlib import gridspec

        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = False)  # Newly instantaited pyplot figure
 
        gs = gridspec.GridSpec(nrows = 3, ncols= 3, figure = fig)


        ax1 = fig.add_subplot(gs[0:2,0:3]) # Create a new subplot 2 rows, 3 columns
        
        # The program is expecting to fill 3 rows and 3 columns.
        # [0:2,0:3] tells it that this subplot will use two rows (from 0 up to, but not including, 2)
        # and 3 columns (from 0 up to, but not including,  3)
               
        #aCumRecGraph.set_title('Another Graph \n Second line')
        ax1.set_xlabel('X axis label: fontsize = 12', fontsize = 12)      
        ax1.set_ylabel('Y axis label: fontsize = 10', fontsize = 10)       
        ax1.set_xscale("linear")
        ax1.set_yscale("linear")
        ax1.set_xlim(0, 21)  
        ax1.set_ylim(0, 21)
        x = [0,2,3,4,20]
        y = [4,4.1,4.7,2.0,2.5]
        aLine = Line2D(x,y, color = 'black', ls = 'solid', drawstyle = 'steps')
        ax1.add_line(aLine)

        bins = 20
        ax2 = fig.add_subplot(gs[2,0:3])       # row [2] and col [0,1,2]
        ax2.set_xlim(0, bins+1)  
        ax2.set_ylim(0, 6)
        
        barHeights = [0.5,1.0,1.5,2.0,2.5, 3.0,3.5,4.0,4.5,5.0, \
                     5.0,4.5,4.0,3.5,3.0, 2.5,2.0,1.5,1.0,0.5]


        index = np.arange(bins)       
        bar_width = 0.35
        ax2.bar(index,barHeights,bar_width)

        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()


    def twinxCurves(self):
        """
        Example of a graph with two axes.
        The main graph is a loglog line and a scatter plot
        """

        x =  [2.53, 4.49, 8.0, 14.23, 25.32, 42.55, 80.0, 142.86, 258.06, 444.44, 800.0, 1428.57]
        y1 = [0.864, 0.690, 0.486, 0.286, 0.134, 0.048, 0.012, 0.003, 0.00069, 0.000262, 0.000171, 0.0001607]
        y2 = [1.58, 0.69, 1.13, 1.75, 1.50, 0.98, 0.804, 0.891, 0.325, 0.064, 0.09, 0.01]
        y3 = [4, 3, 9, 25, 38, 44, 64, 127, 100, 50, 20, 20]

        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = True)  # Newly instantaited pyplot figure

        ax1 = fig.add_subplot(111)
        ax1.set_title('Demand Curve\n Second line of title')
        ax1.set_xlabel('X axis label: fontsize = 16', fontsize = 16)      
        ax1.set_ylabel('Y axis label: fontsize = 14', fontsize = 14)
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.set_xlim(1e0, 1e4)                   # 1 to 10,000
        ax1.set_ylim(1e-4, 1e1)                  # .0001 to 10
        ax1.loglog(x, y1, color ='red')          # Draw a loglog line 
        ax1.scatter(x, y2)                       # and a scatter plot
        ax2 = ax1.twinx()                        # create a 2nd axes that shares the same x-axis
        ax2.set_ylabel('Responses', fontsize = 16)
        ax2.set_ylim(0,250)                      # Y axis from 0 to 250
        ax2.plot(x,y3, color = 'black')
        #    OR
        #responseLine = Line2D(x,y3, color = 'black')
        #secondAxisPlot.add_line(responseLine)

        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()
        
    def report(self):
        print("Report:")
        axes = self.matPlotFigure.gca()
        print("Current Axes", axes)
        figure = self.matPlotFigure.get_figure()
        print("Current Figure", figure)
        #print("graph1:", self.graph1)
        #print("line1:", self.line1)
        print("Axes:", self.matPlotFigure.axes)
        print("DPI:", self.matPlotFigure.get_dpi())
        print("size in inches:", self.matPlotFigure.get_size_inches())

    def playGround(self):
        """
        Template to generate graph for discussion with Jones Lab
        
        """


        
        Qzero = 10.0  # arbitrary
        k = 2.0       # arbitrary - Highest to lowest is 10, so k should be 1. But 2 looks better. 

        def demandFunction(x,alpha):
            """
            Demand function described by Hursh
            y = np.e**(np.log10(Qzero)+k*(np.exp(-alpha*Qzero*x)-1))            
            """
            y = 10**(np.log10(Qzero)+k*(np.exp(-alpha*Qzero*x)-1))                       
            return y

        from matplotlib import gridspec
        gs = gridspec.GridSpec(nrows = 4, ncols= 3)

        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = False)  # Newly instantaited pyplot figure

        # Data
        responseList = [9.9, 19, 37, 72, 140, 200, 150, 50, 10, 10, 10, 10]       
        consumptionList = [0,0,0,0,0,0,0,0,0,0,0,0]

        # Each times is half of the previous
        TH_PumpTimes = [8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625,0.0312,0.0156,0.0078,0.0039]

        dosePerResponse = []

        priceList = []
        for i in range(12):
            binDose = TH_PumpTimes[i] * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
            dosePerResponse.append(round(binDose,5))           
            price = round(1/binDose,2)
            priceList.append(price)

        print("Doses =",dosePerResponse)
        print("Prices =",priceList)
        
        for i in range(12):
            consumptionList[i] = round(responseList[i] * dosePerResponse[i],4)

        print("Consumption =",consumptionList)
 
        ax1 = fig.add_subplot(gs[0:2,0:3])   # Create a new subplot, 2 rows and 3 columns 
        ax1.set_ylabel('Intake (mg per 2h session)', fontsize = 16)
        ax1.set_xlabel('Price (responses/mg)', fontsize = 16)
        ax1.set_xscale("log")
        ax1.set_yscale("linear")
        ax1.set_xlim(0.75, 1000)        
        ax1.set_ylim(0.0, 12)

        # Fit the curve. i.e.
 
        param_bounds=([0.0001],[0.02])
        fitParams, fitCovariances = curve_fit(demandFunction, priceList, consumptionList, bounds=param_bounds)
        alpha = fitParams[0]
        alphaString = "alpha (curve fit) = {0:7.5f}".format(alpha)
        print(alphaString)

        fitLine = []      
        for x in priceList:
            y = demandFunction(x,alpha)
            fitLine.append(y)

        ax1.scatter(priceList, consumptionList)
        ax1.plot(priceList,fitLine, color='red')


        ax2 = fig.add_subplot(gs[3,0:3])       # fourth row and col [0,1,2]

        ax2.set_xscale("log")
        ax2.set_xlim(1.5, 0.001)
        ax2.set_xlabel('Dose (mg/injection)', fontsize = 16)
        ax2.set_yscale("linear")
        ax2.set_ylim(0,300) 
        ax2.set_ylabel('Responses', fontsize = 16)
        #line1 = Line2D(priceList,responseList, color = 'red', ls = 'solid', marker = 'o')       # circle
        #ax2.add_line(line1)
        ax2.plot(dosePerResponse,responseList, marker = 'o', color = 'black')

        # Draw ellipse
        from matplotlib.patches import Ellipse
        mean = [0.25 , 0.80]
        width = 0.55
        height = 0.3
        myEllipse = Ellipse(xy=mean, width=width, color = 'blue', height=height, fill = False, transform = ax1.transAxes)
        ax1.add_patch(myEllipse)
        
        if (self.showOn_tkCanvas.get()):
            self.matPlotCanvas.draw()
        else:
            plt.show()

    def periodic_check(self):
        # http://docs.python.org/dev/library/datetime.html#strftime-strptime-behavior
        time = datetime.now()
        self.timeStringVar.set(time.strftime("%B %d -- %H:%M:%S"))        
        self.root.after(100, self.periodic_check)

    def go(self):
        self.root.after(100, self.periodic_check)
        self.root.mainloop()

if __name__ == "__main__":
    sys.exit(main())  
