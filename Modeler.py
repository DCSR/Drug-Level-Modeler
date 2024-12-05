
"""
Dec 1, 2024
Modeler.py started as a stripped down version of Analysis.py.

        Using the Pan equation for alpha as follows
        alpha := 0.5*((k12+k21+kel)+SQRT((k12+k21+kel)*(k12+k21+kel)-(4*k21*kel)));
        beta  := 0.5*((k12+k21+kel)-SQRT((k12+k21+kel)*(k12+k21+kel)-(4*k21*kel)));
        results in the alpha used by Nicola and Deadwyler
        alpha : real = 0.641901;   // per min
        beta : real = 0.097099;    // per min
    
    dv1 = 0.112444;   # blood
    dv2 = 0.044379;   # brain
    k12 = 0.233;      # rate constant for transfer from blood to brain      0.2 max 
    k21 = 0.212;      # rate contant for transfer from brain to blood
    kel = 0.294       # rate constant for elimination from blood by metabolism and excretion          
    alpha = 0.641901               # per min
    beta = 0.097099                # per min



Done: mostly cleaned up. Draw buttons seem functional and useful.

To Do:

Standardize dataRecord with one four second injection at 110000 as per Nicks file

1 min 60,000
2 min 120,000

5 min 300,000
30 min 1,800,000



   Should it include Drug ("cocaine"), drug concentration etc.




   Prototype Draw using Pan et al. before organizing buttons etc

    try adding stuff (alpha and beta) to canvas: aCanvas.create_text(300, 20, text="graphLibTest")


Conclusions: dv1 seems to be 100% irrelevant in these calculations!
I don't understand what parameter affects rise time (onset duration) - is it assume


"""

from tkinter import *
from tkinter.ttk import Notebook
from tkinter import filedialog
from datetime import datetime
import tkinter as tk
import math
import os
import GraphLib
import numpy as np
import sys
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.lines as lines
from matplotlib import gridspec
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, MaxNLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.ticker as ticker

"""
Models, Views and Controllers (MCV) design: keep the representation of the data separate
from the parts of the program that the user interacts with.

Models: store and retrieve data from databases and files.

View: displays information to the user (Graphical User Interface (tkinter and graphs)

Controllers: convert user input into calls on functions that manipulate data
"""

def main(argv=None):
    if argv is None:
        argv = sys.argv
    gui = myGUI()
    gui.go()
    return 0


class myGUI(object):
    def __init__(self):
        """
        This object controls all aspects of the Graphical User Interface:
        It uses the Tk tookkit imported from tkinter.
        "root" is the base level; all other frames and widgets are in relation to "root".

        Note that widgets can be called from Tk or ttk. Here the default is to Tk widgets. 

        """
        self.version = "Modeler"
        self.root = Tk()
        self.root.title(self.version)
        canvas_width = 800
        canvas_height = 600
        self.initialDir = ""
        if (os.name == "posix"):
            self.initialDir = "/Users/daveroberts/Documents"
        else:
            self.initialDir = "C:/"
        print("Initial Directory:", self.initialDir)

        # **********************************************************************
        # *********   Variables and Lists associated with the View     *********
        # **********************************************************************
        
        #Construct ten empty dataRecords
        self.record0 = self.DataRecord([],"empty")   #Data Record defined in DataModel.py      
        self.record1 = self.DataRecord([],"empty")
        self.record2 = self.DataRecord([],"empty")
        self.record3 = self.DataRecord([],"empty")
        self.record4 = self.DataRecord([],"empty")
        self.record5 = self.DataRecord([],"empty")
        self.record6 = self.DataRecord([],"empty")
        self.record7 = self.DataRecord([],"empty")
        self.record8 = self.DataRecord([],"empty")
        self.record9 = self.DataRecord([],"empty")
        
        # Create a list of these dataRecords so that one can be "selected" with self.fileChoice.get()
        self.recordList = [self.record0,self.record1,self.record2,self.record3,self.record4, \
                           self.record5,self.record6,self.record7,self.record8,self.record9]

        # Header row
        self.showOn_tkCanvas = BooleanVar(value = True) # Either tk Canvas or pyplot
        self.clockTimeStringVar = StringVar(value="0:00:00")
        
        self.fileChoice = IntVar(value=0)
        self.fileName0 = StringVar(value = self.recordList[0].fileName)
        self.fileName1 = StringVar(value = self.recordList[1].fileName)
        self.fileName2 = StringVar(value = self.recordList[2].fileName)
        self.fileName3 = StringVar(value = self.recordList[3].fileName)
        self.fileName4 = StringVar(value = self.recordList[4].fileName)
        self.fileName5 = StringVar(value = self.recordList[5].fileName)
        self.fileName6 = StringVar(value = self.recordList[6].fileName)
        self.fileName7 = StringVar(value = self.recordList[7].fileName)
        self.fileName8 = StringVar(value = self.recordList[8].fileName)
        self.fileName9 = StringVar(value = self.recordList[9].fileName)
        
        self.fileNameList = [self.fileName0,self.fileName1,self.fileName2,self.fileName3,self.fileName4,\
                             self.fileName5,self.fileName6,self.fileName7,self.fileName8,self.fileName9]

        # Graphs Tab
        self.max_x_scale = IntVar(value=360)  # Should eventually be coupled to a radiobutton selection
        self.max_y_scale = IntVar(value=500)  # Should eventually be coupled to a radiobutton selection

        # *******  Model parameters **********
        # Global varaibles which could change. Initial placeholder values are cocaine defaults.
        # These are variables that could change!
        # Set desired values in setCocaineDefaults(), setHeroinDefaults() and setTestDefaults()

        self.dv1 = 0.112444
        self.dv2 = 0.044379
        self.k12 = 0.233
        self.k21 = 0.212
        self.kel = 0.294
        self.alpha = 0.641901
        self.beta = 0.097099
        

        # ******************************************************************************
        # **************************         Root Frame            *********************
        # ******************************************************************************
        
        self.rootFrame = Frame(self.root, borderwidth=2, relief="sunken")
        self.rootFrame.grid(column = 0, row = 0)
        headerFrame= Frame(self.root,borderwidth=2, relief="sunken")
        headerFrame.grid(row=0,column=0,sticky=EW)
        fileSelectorFrame = Frame(self.root, borderwidth=2, relief="sunken")
        fileSelectorFrame.grid(row=1,column=0,sticky=NSEW)        
        noteBookFrame = Frame(self.root, borderwidth=2, relief="sunken")
        noteBookFrame.grid(row=2,column=0)

        # ******* Add Tabs ********
        myNotebook = Notebook(noteBookFrame)
        self.graphTab = Frame(myNotebook)
        myNotebook.add(self.graphTab,text = "Graphs")
        self.spareTab = Frame(myNotebook)
        myNotebook.add(self.spareTab,text = "Spare Tab") 
        myNotebook.grid(row=0,column=0)

        # *************  Header Row ******************      
        openFilesButton = Button(headerFrame, text="Open Files", command= lambda: \
                               self.openFiles("Open Selected Files")).grid(row=0,column=0, sticky=W)        
        spacer1Label = Label(headerFrame, text="               ").grid(row=0,column=1)
        clockTimeLabel = Label(headerFrame, textvariable = self.clockTimeStringVar).grid(row = 0, column=2)
        spacer2Label = Label(headerFrame, text="               ").grid(row=0,column=3)
        loadTestButton1 = Button(headerFrame, text="Test1.txt", command= lambda: \
                              self.openFiles("Test1.txt")).grid(row=0,column=4,sticky=N, padx = 20)
        loadTestButton2 = Button(headerFrame, text="Test2.txt", command= lambda: \
                              self.openFiles("Test2.txt")).grid(row=0,column=5,sticky=N, padx = 20)
        loadTestButton3 = Button(headerFrame, text="Test3.txt", command= lambda: \
                              self.openFiles("Test3.txt")).grid(row=0,column=6,sticky=N, padx = 20)
        loadTestButton4 = Button(headerFrame, text="Test4.txt", command= lambda: \
                              self.openFiles("Test4.txt")).grid(row=0,column=7,sticky=N, padx = 20)
        
        spacer2Label = Label(headerFrame, text="                    ").grid(row = 0,column = 8)
        canvasButton = Radiobutton(headerFrame, text = "tk Canvas", variable = self.showOn_tkCanvas, value = 1).grid(row = 0, column = 9, sticky = E)
        pyplotButton = Radiobutton(headerFrame, text = "pyplot ", variable = self.showOn_tkCanvas, value = 0).grid(row = 0, column = 10, sticky = E)

        #*************** FileSelectorFrame stuff ****************
        padding = 20
        radiobutton1 = Radiobutton(fileSelectorFrame, textvariable = self.fileName0, variable = self.fileChoice, \
                                   value = 0, command =lambda: self.selectList()).grid(column=0, row=2, padx=padding)
        radiobutton2 = Radiobutton(fileSelectorFrame, textvariable = self.fileName1, variable = self.fileChoice, \
                                   value = 1, command =lambda: self.selectList()).grid(column=1, row=2,padx=padding)
        radiobutton3 = Radiobutton(fileSelectorFrame, textvariable = self.fileName2, variable = self.fileChoice, \
                                   value = 2, command =lambda: self.selectList()).grid(column=2, row=2,padx=padding)
        radiobutton4 = Radiobutton(fileSelectorFrame, textvariable = self.fileName3, variable = self.fileChoice, \
                                   value = 3, command =lambda: self.selectList()).grid(column=3, row=2,padx=padding)
        radiobutton5 = Radiobutton(fileSelectorFrame, textvariable = self.fileName4, variable = self.fileChoice, \
                                   value = 4, command =lambda: self.selectList()).grid(column=4, row=2,padx=padding)
        radiobutton6 = Radiobutton(fileSelectorFrame, textvariable = self.fileName5, variable = self.fileChoice, \
                                   value = 5, command =lambda: self.selectList()).grid(column=0, row=3,padx=padding)
        radiobutton7 = Radiobutton(fileSelectorFrame, textvariable = self.fileName6, variable = self.fileChoice, \
                                   value = 6, command =lambda: self.selectList()).grid(column=1, row=3,padx=padding)
        radiobutton8 = Radiobutton(fileSelectorFrame, textvariable = self.fileName7, variable = self.fileChoice, \
                                   value = 7, command =lambda: self.selectList()).grid(column=2, row=3,padx=padding)
        radiobutton9 = Radiobutton(fileSelectorFrame, textvariable = self.fileName8, variable = self.fileChoice, \
                                   value = 8, command =lambda: self.selectList()).grid(column=3, row=3,padx=padding)
        radiobutton10 = Radiobutton(fileSelectorFrame, textvariable = self.fileName9, variable = self.fileChoice, \
                                   value = 9, command =lambda: self.selectList()).grid(column=4, row=3,padx=padding)


        """
        Don't know what this was. There is already a self.fileNameList
        self.defaultsList = [self.fileName0,self.fileName1,self.fileName2,self.fileName3,self.fileName4,\
                             self.fileName5,self.fileName6,self.fileName7,self.fileName8,self.fileName9]

        """


        # *************************************************************
        # **************        Graph Tab     *************************
        # *************************************************************

        # ****** Create Frames *******
        """
        Screen is divided into a graphCanvasFrame on the right and the leftColumnFrame
        The leftColumnFrame contains buttonFrame, drugFrame, sliderFrame, parameterFrame and axesFrame
        """
          
        self.graphCanvasFrame = Frame(self.graphTab, borderwidth=2, relief="sunken")
        self.graphCanvasFrame.grid(column = 1, row = 0)
        self.graphCanvas = Canvas(self.graphCanvasFrame, width = canvas_width, height = canvas_height)
        self.graphCanvas.grid(row=0,column=0)
        self.graphCanvas.create_text(100,10,text = "Graph Canvas")
        
        self.leftColumnFrame = Frame(self.graphTab, borderwidth=2, relief="sunken")
        self.leftColumnFrame.grid(row = 0, column = 0, sticky=N)

        self.parameterFrame = Frame(self.leftColumnFrame, borderwidth=2, relief="sunken")
        self.parameterFrame.grid(row = 0, column = 0, sticky=EW)
        
        self.buttonFrame = Frame(self.leftColumnFrame, borderwidth=2, relief="sunken")
        self.buttonFrame.grid(row = 1, column = 0, sticky=EW)

        self.sliderFrame = Frame(self.leftColumnFrame, borderwidth=2, relief="sunken")
        self.sliderFrame.grid(row = 2, column = 0, sticky=W)

        self.axesFrame = Frame(self.leftColumnFrame, borderwidth=2, relief="sunken")
        self.axesFrame.grid(row = 3, column = 0, sticky=W)


        # ********  Add widgets to specific Frames *******

        # ******** buttonFrame ******************
        
        clearCanvasButton = Button(self.buttonFrame, text="Clear Graph", command= lambda: \
                            #self.clearGraphCanvas()).grid(row=1,column=0,sticky=W)
                            self.clearGraphTabCanvas()).grid(row=1,column=0,sticky=W)

        drawModel_button = Button(self.buttonFrame, text="drawCocDefault()", command= lambda: \
                self.drawCocDefault()).grid(column=0, row=2, sticky=W)

        drawModel_button = Button(self.buttonFrame, text="drawTestParams1()", command= lambda: \
                self.drawTestParams1()).grid(column=0, row=3, sticky=W)

        drawModel_button = Button(self.buttonFrame, text="drawTestParams2()", command= lambda: \
                self.drawTestParams2()).grid(column=0, row=4, sticky=W)
    
          
        # ********** sliderFrame ********************

        drawModel_button = Button(self.sliderFrame, text="drawUsingSliders()", command= lambda: \
                self.drawUsingSliders()).grid(row=0, column=0, sticky=W)

        #dv1
        dv1_Label = Label(self.sliderFrame, text = "dv1").grid(row=1,column=0,sticky=W)
        self.scale_dv1 = Scale(self.sliderFrame, orient=HORIZONTAL, length=150, resolution = 0.1, \
                                 from_= 0.05, to = 5.0, variable = self.dv1)
        self.scale_dv1.grid(row=1, column=1, columnspan = 3)
        self.scale_dv1.set(0.112)


        #dv2
        dv2_Label = Label(self.sliderFrame, text = "dv2").grid(row=2,column=0,sticky=W)
        self.scale_dv2 = Scale(self.sliderFrame, orient=HORIZONTAL, length=150, resolution = 0.000001, \
                                 from_= 0.01, to = 0.06, variable = self.dv2)
        self.scale_dv2.grid(row=2,column=1, columnspan = 3)
        self.scale_dv2.set(0.044)

        #k12
        k12_Label = Label(self.sliderFrame, text = "k12").grid(row=3,column=0,sticky=W)
        self.scale_k12 = Scale(self.sliderFrame, orient=HORIZONTAL, length=150, resolution = 0.001, \
                                 from_= 0.05, to = 0.25, variable = self.k12)
        self.scale_k12.grid(row=3,column=1, columnspan = 3)
        self.scale_k12.set(0.233)

        #k21
        k21_Label = Label(self.sliderFrame, text = "k21").grid(row=4,column=0,sticky=W)
        self.scale_k21 = Scale(self.sliderFrame, orient=HORIZONTAL, length=150, resolution = 0.000001, \
                                 from_= 0.10, to = 0.4, variable = self.k21)
        self.scale_k21.grid(row=4,column=1, columnspan = 3)
        self.scale_k21.set(0.212)
            
        #kel
        kel_Label = Label(self.sliderFrame, text = "kel").grid(row=5,column=0,sticky=W)
        self.scale_kel = Scale(self.sliderFrame, orient=HORIZONTAL, length=150, resolution = 0.000001, \
                                 from_= 0.20, to = 0.4, variable = self.kel)
        self.scale_kel.grid(row=5,column=1, columnspan = 3)
        self.scale_kel.set(0.294)

        

        """



        # ******* Y axis frame *********
        self.graph_YaxisRadioButtonFrame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_YaxisRadioButtonFrame.grid(column = 0, row = 4)
        y_axisButtonLabel = Label(self.graph_YaxisRadioButtonFrame, text = "Y axis").grid(row = 0, column=0)
        y_scaleRadiobutton250 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="250", variable=self.max_y_scale, value=250)
        y_scaleRadiobutton250.grid(column = 0, row = 1)
        y_scaleRadiobutton500 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="500", variable=self.max_y_scale, value=500)
        y_scaleRadiobutton500.grid(column = 0, row = 2)
        y_scaleRadiobutton1000 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="1000", variable=self.max_y_scale, value=1000)
        y_scaleRadiobutton1000.grid(column = 0, row = 3)
        y_scaleRadiobutton1500 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="1500", variable=self.max_y_scale, value=1500)
        y_scaleRadiobutton1500.grid(column = 0, row = 4)

        self.graphCanvasFrame = Frame(self.graphTab, borderwidth=2, relief="sunken")
        self.graphCanvasFrame.grid(column = 1, row = 0)
        self.graphCanvas = Canvas(self.graphCanvasFrame, width = canvas_width, height = canvas_height)
        self.graphCanvas.grid(row=0,column=0)
        self.graphCanvas.create_text(100,10,text = "Graph Canvas")

        """

        self.updateParamLabels()
        
    # ***************   End of __init__(self)  *************************

    
   
    class DataRecord:
        def __init__(self, datalist, fileName):
            self.fileName = fileName
            self.datalist = datalist
            self.numberOfL1Responses = 0
            self.numberOfL2Responses = 0
            self.numberOfInfusions = 0
            self.totalPumpDuration = 0        
            self.drugConc = 0.0
            self.pumpSpeed = 0.0
            self.averagePumpTime = 0.0
            self.TH_PumpTimes = []
            self.priceList = []
            self.consumptionList = []
            self.responseList = []
            self.deltaList = []
            self.notes = "test"
            self.iniLine = ""

        def __str__(self):
            """
                Returns a string of values inside object that is used when the print command is called
            """
            consumptionStr = ""
            for i in range(0,len(self.consumptionList)):
                consumptionStr = consumptionStr + "{:.3f}, ".format(self.consumptionList[i])

            priceStr = ""
            for i in range(0,len(self.priceList)):
                priceStr = priceStr + "{:.2f}, ".format(self.priceList[i])

            responseStr = ""
            for i in range(0,len(self.responseList)):
                responseStr = responseStr + "{}, ".format(self.responseList[i])
                    
            s = "Filename: "+self.fileName+ \
            "\nNotes: "+self.notes+ \
            "\nLever 1 Responses: "+str(self.numberOfL1Responses)+ \
            "\nLever 2 Responses: "+str(self.numberOfL2Responses)+ \
            "\nInfusions: "+str(self.numberOfInfusions)+ \
            "\nTotal Pump Time (mSec): "+str(self.totalPumpDuration)+ \
            "\nAverage Pump Time (mSec): "+str(round(self.averagePumpTime,4))+ \
            "\nPump Speed (ml/sec): "+str(self.pumpSpeed)+" ml/Sec\n"
            
            """
            "\nPumpTimes = "+str(self.TH_PumpTimes) + \
            "\nPriceList = " + priceStr + \
            "\nConsumptionList = " + consumptionStr + \
            "\nResponseList = " + responseStr +"\n"
            "\nDelta List: "+str(self.deltaList)+
            """
            #"\n============================\n"
            
            return s

        def extractStatsFromList(self):
            self.numberOfL1Responses = 0
            self.numberOfL2Responses = 0
            self.numberOfInfusions = 0
            self.totalPumpDuration = 0
            leverOut = True
            pumpOn = False
            lastTime = 0
            self.deltaList = []
            delta = 0
            for pairs in self.datalist:                   
                if pairs[1] == 'L':
                    self.numberOfL1Responses = self.numberOfL1Responses + 1
                if pairs[1] == 'J':
                    self.numberOfL2Responses = self.numberOfL2Responses + 1               
                if ((pairs[1] == 'P') and (leverOut == True)) :
                    self.numberOfInfusions = self.numberOfInfusions + 1
                    pumpStartTime = pairs[0]
                    delta = pumpStartTime - lastTime
                    self.deltaList.append(round(delta/(1000*60)))
                    lastTime = pumpStartTime
                    pumpOn = True
                if pairs[1] == 'p':
                    if pumpOn:
                        duration = pairs[0]-pumpStartTime
                        pumpOn = False
                        self.totalPumpDuration = self.totalPumpDuration + duration
                if self.numberOfInfusions > 0:
                    self.averagePumpTime = round(self.totalPumpDuration / self.numberOfInfusions,2)

    # ************** End Record Class *********************************



    
    """

    def drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "black"):
]
        # Draws an X (horizontal) axis using the following parameters:
        # aCanvas:  Here the main canvas is self.graphCanvas, but a different canvas might be added,
        #           for example, in a new Tab.
        # x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions

        aCanvas.create_line(x_zero, y_zero, x_zero + x_pixel_width, y_zero, fill=color)
        for divisions in range(x_divisions + 1):          
            x = x_zero + (divisions * (x_pixel_width // x_divisions))
            aCanvas.create_line(x, y_zero, x, y_zero + 5, fill=color)
            aCanvas.create_text(x, y_zero + 20, text=str(int((max_x_scale/x_divisions)*divisions)), fill=color)

    def drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, labelLeft, format_int = False, color = "black"):
        # Draws an Y (verticle) axis using the following parameters:
        # (aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions,  labelLeft, color):

        #labelLeft = True places labels and tick marks on the left of the axis
        #Adjust x_zero to move the axis left or right.
        #    eg. x_zero = x_zero + x_pixel_width will push it all the way to the right edge. 
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

    """


    def updateParamLabels(self):
        """
        Needs some explanation 
        """        
        dv1_Value_label = Label(self.parameterFrame, text = "dv1 ="+str(self.dv1)).grid(row=3,column=0,sticky=W)   
        dv2_Value_label = Label(self.parameterFrame, text = "dv2 ="+str(self.dv2)).grid(row=4,column=0,sticky=W)
        k12_Value_label = Label(self.parameterFrame, text = "k12 ="+str(self.k12)).grid(row=5,column=0,sticky=W)
        k21_Value_label = Label(self.parameterFrame, text = "k21 ="+str(self.k21)).grid(row=6,column=0,sticky=W)
        kel_Value_label = Label(self.parameterFrame, text = "kel ="+str(self.kel)).grid(row=7,column=0,sticky=W)
        alpha_Value_label = Label(self.parameterFrame,text = "alpha ="+str(round(self.alpha,5))).grid(row=8,column=0,sticky=W)
        beta_Value_label = Label(self.parameterFrame, text = "beta ="+str(round(self.beta,5))).grid(row=9,column=0,sticky=W)
        if True:                # Make conditional at some point
            self.scale_dv1.set(self.dv1)
            self.scale_dv2.set(self.dv2)
            self.scale_k12.set(self.k12)
            self.scale_k21.set(self.k21)
            self.scale_kel.set(self.kel)    

    def eventRecord(self, aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, dataList, charList, aLabel, t_zero = 0):
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

    def  calculateConcentration (self,D, T, resolution):
        """ dose, time, resolution >> concentration
            Returns the concentration of cocaine at time T given dose (D) at time zero.
            Using the Pan equation for alpha and beta as follows:
            alpha := 0.5*((k12+k21+kel)+SQRT((k12+k21+kel)*(k12+k21+kel)-(4*k21*kel)));
            beta  := 0.5*((k12+k21+kel)-SQRT((k12+k21+kel)*(k12+k21+kel)-(4*k21*kel)));
            results in alpha and beta used by Nicola and Deadwyler
            alpha = 0.641901
            beta = 0.097099
        """
        # local variables take on global values
        dv1 = self.dv1 
        dv2 = self.dv2   
        k12 = self.k12
        k21 = self.k21
        alpha = self.alpha
        beta = self.beta

        concentration = ((D*k12)/(dv2*(alpha-beta)))*((math.exp(-beta*(T*(resolution/60)))-math.exp(-alpha*(T*(resolution/60)))));

        return concentration

    def calculateDrugConc(self,aList, drugConc, pumpSpeed, resolution, bodyWeight = 0.330):
        """ dataList, drugConc, pumpSpeed, respultion >> list of cocaine concentrations
            Returns timestamp pairs corresponding to every 5 sec bin of a 6 hr session (4320 bins)
            resolution in seconds
        """
        
        # drugConc   Wake cocaine default = 5.0 mg/ml   
        # pumpSpeed Wake = 0.025 ml/mSec
        pumpSpeed = pumpSpeed/1000    # convert to ml/mSec
        duration = 0
        dose = 0.0

        lastBin = int((60/resolution) * 360)       # ie. 5 sec = (60/5)* 360 = 4320 bins for 6 hours session
        pumpOn = False
        pumpOnTime = 0    

        modelList = []
        """"
        for i in range(lastBin+1):
            modelList.append([i*resolution*1000,0])
        for pairs in aList:
            if pairs[1] == "P":
                pumpOn = True
                pumpOnTime = pairs[0]
            elif pairs[1] == "p":
                if pumpOn:
                    pumpOn = False
                    duration = pairs[0]-pumpOnTime
                    dose =  (duration * drugConc * pumpSpeed)/bodyWeight;
                    # eg. 4000 mSec * 5 mg/ml *0.000025 mls/mSec / 0.330 kg = 1.5 mg/kg
                    i = int(pairs[0]/(resolution*1000)+1)  # calculate which bin
                    # print(i)
                    if i < lastBin:
                        for t in range(lastBin-i):     # t would normally be every 5 sec
                            modelList[i+t][1] = modelList[i+t][1] + self.calculateConcentration(dose,t,resolution)
        """
        for i in range(lastBin+1):
            modelList.append([i*resolution*1000,0])
        for pairs in aList:
            duration = pairs[1]-pairs[0]
            print("duration =", duration)
            dose =  (duration * drugConc * pumpSpeed)/bodyWeight;    # eg. 4000 mSec * 5 mg/ml *0.000025 mls/mSec / 0.330 kg = 1.5 mg/kg
            i = int(pairs[0]/(resolution*1000)+1)  # calculate which bin
            # print(i)
            if i < lastBin:
                for t in range(lastBin-i):     # t would normally be every 5 sec
                    modelList[i+t][1] = modelList[i+t][1] + self.calculateConcentration(dose,t,resolution)

        print(modelList[30])
        return modelList
    
    def clearGraphTabCanvas(self):
        self.graphCanvas.delete('all')
        

    def openFiles(self,filename):
        """
            This is stub for later use with first row buttons
        """       
        print(filename)
 

        # **********************  The Controllers  ***********************************
        # Controllers converts user input into calls to functions that manipulate data
        # ****************************************************************************

    def pyPlotEventRecord(self):
        injNum = 0
        injTimeList = []
        
        aRecord = self.recordList[self.fileChoice.get()]
        for pairs in aRecord.datalist:
            injNum = injNum + 1
            injTimeList.append(pairs[0]/60000)  # Min

        plt.figure(figsize=(9,3))
        plt.subplot(111)
        plt.axis([-0.1,185,0.0,1.0])
        plt.eventplot(injTimeList,lineoffsets = 0, linelengths=1.5)
        plt.show()       

    def clearFigure(self):
        self.matPlotFigure.clf()
        self.threshold_matPlot_Canvas.draw()

    def testStuff2(self):
        print("testStuff2")
        aRecord = self.recordList[self.fileChoice.get()]
        print(aRecord.datalist[0])

    def testStuff3(self):
        print("testStuff3")

 
    def drawModel(self, aColor):
        """
        This compares the same dose over 3 different time periods 5,25 and 50 sec
        It does this by changing the concentration, but perhpas it would be
        better to change the pump speed.

        eg. 5000 mSec * 4 mg/ml *0.000025 mls/mSec / 0.330 kg = 1.5 mg/kg
        # model.calculateDrugConc defaults to bodyweight 0.330 

        """        
        # testRecord1  4 sec infusion
        testRecord1 = self.DataRecord([],"TestRecord1")

        
        # testRecord1.datalist = [[600000, 'P'],[605000, 'p'],[1200000, 'P'],[1205000,'p'],[12000000, 'P'],[12005000,'p']]

        testRecord1.datalist = [(110000,114000)]
        testRecord1.pumpSpeed = 0.025   # Wake default 0.1 mls/4 sec = 0.025 / sec
        testRecord1.drugConc = 4.0
        testRecord1.extractStatsFromList()
        duration = testRecord1.totalPumpDuration
        dose = (testRecord1.totalPumpDuration * testRecord1.drugConc * (testRecord1.pumpSpeed/1000)/0.330)
        print("testRecord1 Duration = {0}; Total Dose = {1:2.1f}".format(duration,dose))

        # ************** later, need to pass aRecord -> drawModel(self,aRecord) *******
        # but for now it just uses only the parameters in testRecord1 above
        # *****************************************************************************

        aCanvas = self.graphCanvas
        aRecord = testRecord1
        print(aRecord.datalist)
        print(aRecord.drugConc)
        print(aRecord.pumpSpeed)
        
        
        x_zero = 75
        y_zero = 350
        x_pixel_width = 500 #700
        y_pixel_height = 150 #200
        x_divisions = 12
        y_divisions = 4
        max_x_scale = 360    # could use elf.max_x_scale.get()
        max_y_scale = 20
        resolution = 60
        # aColor = "blue"      # could pass different colors -> drawModel(self,aRecord,aColor)
        if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
        self.eventRecord(aCanvas, x_zero+5, 185, x_pixel_width, max_x_scale, aRecord.datalist, ["P"], "")
        GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
        GraphLib.drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True)
        x_scaler = x_pixel_width / (max_x_scale*60*1000)
        y_scaler = y_pixel_height / max_y_scale

        # calculateDrugConc(self,aList, drugConc, pumpSpeed, resolution, bodyWeight = 0.330):
        
        drugConcXYList = self.calculateDrugConc(aRecord.datalist,aRecord.drugConc,aRecord.pumpSpeed,resolution)

        # print(drugConcXYList)
        x = x_zero
        y = y_zero
        totalConc = 0
        totalRecords = 0
        startAverageTime = 10 * 60000    # 10 min
        endAverageTime = 180 * 60000     # 120 min
        for pairs in drugConcXYList:
            if pairs[0] >= startAverageTime:
                if pairs[0] < endAverageTime:
                    totalRecords = totalRecords + 1
                    totalConc = totalConc + pairs[1]
            concentration = round(pairs[1],2)
            newX = x_zero + pairs[0] * x_scaler // 1
            newY = y_zero - concentration * y_scaler // 1
            aCanvas.create_line(x, y, newX, newY, fill= aColor)
            # aCanvas.create_oval(newX-2, newY-2, newX+2, newY+2, fill=aColor)
            x = newX
            y = newY
        aCanvas.create_text(300, 400, fill = "blue", text = aRecord.fileName)

        """
        # ************
        
        dose = 2.8*aRecord.drugConc * aRecord.pumpSpeed
        tempStr = "Duration (2.8 sec) * Pump Speed ("+str(aRecord.pumpSpeed)+" ml/sec) * drugConc ("+str(aRecord.drugConc)+" mg/ml) = Unit Dose "+ str(round(dose,3))+" mg/inj"
        aCanvas.create_text(300, 450, fill = "blue", text = tempStr)
        averageConc = round((totalConc/totalRecords),3)
        # draw average line
        X1 = x_zero + (startAverageTime * x_scaler) // 1
        Y  = y_zero-((averageConc) * y_scaler) // 1
        X2 = x_zero + (endAverageTime * x_scaler) // 1
        # aCanvas.create_line(X1, Y, X2, Y, fill= "red")
        # tempStr = "Average Conc (10-180 min): "+str(averageConc)
        # aCanvas.create_text(500, Y, fill = "red", text = tempStr)
        """


    def drawCocDefault(self):
        self.dv1 = 0.112444
        self.dv2 = 0.044379
        self.k12 = 0.233
        self.k21 = 0.212
        self.kel = 0.294
        self.alpha = 0.5*((self.k12+self.k21+self.kel)+math.sqrt((self.k12+self.k21+self.kel)*\
                            (self.k12+self.k21+self.kel)-(4*self.k21*self.kel)));
        self.beta = 0.5*((self.k12+self.k21+self.kel)-math.sqrt((self.k12+self.k21+self.kel)*\
                            (self.k12+self.k21+self.kel)-(4*self.k21*self.kel)));       
        self.updateParamLabels()
        self.drawModel("red")


    def drawTestParams1(self):
        self.dv1 = 0.112444
        self.dv2 = 0.044379
        self.k12 = 0.233
        self.k21 = 0.212
        self.kel = 0.200
        self.alpha = 0.5*((self.k12+self.k21+self.kel)+math.sqrt((self.k12+self.k21+self.kel)*\
                            (self.k12+self.k21+self.kel)-(4*self.k21*self.kel)));
        self.beta = 0.5*((self.k12+self.k21+self.kel)-math.sqrt((self.k12+self.k21+self.kel)*\
                            (self.k12+self.k21+self.kel)-(4*self.k21*self.kel)));
        self.updateParamLabels()
        self.drawModel("blue")

    def drawTestParams2(self):
        self.dv1 = 0.112444
        self.dv2 = 0.044379
        self.k12 = 0.233
        self.k21 = 0.212
        self.kel = 0.400
        self.alpha = 0.5*((self.k12+self.k21+self.kel)+math.sqrt((self.k12+self.k21+self.kel)*\
                            (self.k12+self.k21+self.kel)-(4*self.k21*self.kel)))
        self.beta = 0.5*((self.k12+self.k21+self.kel)-math.sqrt((self.k12+self.k21+self.kel)*\
                            (self.k12+self.k21+self.kel)-(4*self.k21*self.kel)))     
        self.updateParamLabels()
        self.drawModel("green")


    def drawUsingSliders(self):
        self.dv1 = self.scale_dv1.get()
        self.dv2 = self.scale_dv2.get()
        self.k12 = self.scale_k12.get()
        self.k21 = self.scale_k21.get()
        self.kel = self.scale_kel.get()
        self.alpha = 0.5*((self.k12+self.k21+self.kel)+math.sqrt((self.k12+self.k21+self.kel)*\
                            (self.k12+self.k21+self.kel)-(4*self.k21*self.kel)))
        self.beta = 0.5*((self.k12+self.k21+self.kel)-math.sqrt((self.k12+self.k21+self.kel)*\
                            (self.k12+self.k21+self.kel)-(4*self.k21*self.kel)))
        self.updateParamLabels()
        self.drawModel("orange")
        

    def clearText(self):
        self.textBox.delete("1.0",END)


    def periodic_check(self):
        thisTime = datetime.now()
        self.clockTimeStringVar.set(thisTime.strftime("%H:%M:%S"))        
        self.root.after(100, self.periodic_check)               

    def go(self):
        self.root.after(100, self.periodic_check)
        self.root.mainloop()
        

if __name__ == "__main__":
    sys.exit(main())

