#!/usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt
import string
import collections
import re
import sys
import argparse
import os
from tkinter import *
from Likes import Likes
from Extract import Extract

import pycountry_convert
#from GUI import Gui
#import pycountry as pc
#import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument("-u" , help = "set the user UUID")
parser.add_argument("-d", help = "set the document UUID")
parser.add_argument("-t", help = "sets the task to be ran either 2a, 2b, 3a, 3b, 4d, 5 or 6")
parser.add_argument("-f", help = "name of json file to be used")
args = parser.parse_args()
file = args.f
doc_uuid = args.d
visitor_uuid = args.u
task = args.t
jsonarr = []
def extractJSON(file):
    arr =[]
    for line in (open(file, "r")):
        arr.append(json.loads(line))
    return arr



class Gui:
    l = Likes()
    e = Extract()
    doc_uuid = None
    master = None
    def __init__(self, master, docuuid):
            self.master = master
            self.doc_uuid = docuuid
    def task6(self):
            w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            self.master.geometry("%dx%d+0+0" % (w, h))
            frame = Frame(self.master)
            frame.pack(fill=BOTH, expand=1)

            # have to use lambda here so the function doesnt get called until clicked on
            self.main_title = Label(frame , text = "Welcome, please select a task from the list below", font = 24)
            self.main_title.pack(fill=BOTH, expand=1)

            self.but2a = Button(frame, text = "Task 2a", command = lambda:self.task2a(frame))
            self.but2a.pack(fill=BOTH, expand=1)
            self.but2b = Button(frame, text = "Task 2b", command = lambda:self.task2b(frame) )
            self.but2b.pack(fill=BOTH, expand=1)
            self.but3a = Button(frame, text = "Task 3a", command = lambda:self.task3a(frame))
            self.but3a.pack(fill=BOTH, expand=1)
            self.but3b = Button(frame, text = "Task 3b", command = lambda:self.task3b(frame))
            self.but3b.pack(fill=BOTH, expand=1)
            self.but4d = Button(frame, text = "Task 4d", command = lambda:self.task4d(frame))
            self.but4d.pack(fill=BOTH, expand=1)
            self.but5 = Button(frame, text = "Task 5", command = lambda:self.task5(frame))
            self.but5.pack(fill=BOTH, expand=1)
            #self.but6 = Button(frame, text = "Task 6", command = lambda:self.task6())
            #self.but6.pack()


    def task2a(self,master = None):

            window = self.create_window(master)

            create_graph= Button(window, text = "Create graph", command = lambda:e.display(e.findCountries(self.doc_entry.get(),extractJSON(self.file_entry.get()))))
            create_graph.pack(side = BOTTOM )

            self.creat_gui(window,"2a", """ Task Description:
	           "We want to analyse, for a given document, from which countries and continents the document
               has been viewed. The data should be displayed as a histogram of countries,i.e. counting
               the number of occurrences for each country in the input file."



	You can see the graph displayed by inputting the JSON file and the document UUID in the fields below and clicking the "Create Graph" button which will display a graph of all the countries that accessed this document and how many times """)




    def task2b(self,master = None):
            window = self.create_window(master)

            create_graph= Button(window, text = "Create graph", command = lambda:e.display(e.findCountries(self.doc_entry.get(),extractJSON(self.file_entry.get())),e.findContinents(e.findCountries(self.doc_entry.get(),extractJSON(self.file_entry.get())))))
            create_graph.pack(side = BOTTOM )

            self.creat_gui(window,"2b", """Task Description:
                "Use  the  data  you  have  collected  in  the  previous  task (task 2a),  group  the  countries  by
                continent,  andgenerate a histogram of the continents of the viewers".


            By inputting the document UUID and JSON file name below and then clicking the "Create Graph" button you will see a similar graph created to that of the precious task, except this time it is grouped by continet where each entry in
            the chart has a colour which is related to which continent its country is from""")


    def task3a(self,master = None):
            window = self.create_window(master)

            create_graph= Button(window, text = "Create graph", command = lambda:e.display(e.findBrowser(self.doc_entry.get(),extractJSON(self.file_entry.get()))))
            create_graph.pack(side = BOTTOM )

            self.creat_gui(window,"3a", """Task Description:
                "In  this  task  we  want  to  identify  the  most  popular  browser..... The application should
                return and display a histogram of all browser identifiers of the viewers."


            Inputting a document UUID and JSON file name below and then clicking the "Create Graph" button will display a graph of the browser identifiers of each of the viewers without edit """)


    def task3b(self,master = None):
            window = self.create_window(master)

            create_graph= Button(window, text = "Create graph", command = lambda:e.display(e.refinedBrowsers(e.findBrowser(self.doc_entry.get(),extractJSON(self.file_entry.get())))))
            create_graph.pack(side = BOTTOM )

            self.creat_gui(window,"3b", """Task Description:
                "In  the  previous  task(task 3a),  you  will  see  that  the  browser  strings  are  very  verbose,  distinguishing
                browser  by  e.g.  version  and  OS  used. Process  the  input  of  the  previous  task (task 3a),  so  that  only  the main
                browser name is used to distinguish them (e.g.Mozilla), and again display the result as a histogram. "


            Input a document UUID and JSON file below and then click the "Create Graph" button to see a graph of the cut-down versions of the previously verbose strings, it should now be much clearer which browsers are present """)

    def task4d(self,master = None):
            window = self.create_window(master)

            print= Button(window, text = "Print Top 10", command = lambda:l.printList(l.top10(l.alsoLikes(self.doc_entry.get(),extractJSON(self.file_entry.get())))))
            print.pack(side = BOTTOM )

            self.creat_gui(window,"4d", """Task Description:
                "implement a function to implement the “also like” functionality, which takes as parameters the above document UUID and
                (optionally) visitor UUID.The function should return a list of “liked” documents, sorted by the sorting function...
                Provide a document UUID and visitor UUID asinput and produce a list of top 10 document UUIDs as a result"


            Inputting the JSON file and a Document UUID present in that file and the clicking the "Print Top 10" button will print an ordered list of documents that readers of the originall document have also read with number one being the most read etc. """)


    def task5(self,master = None):
            window = self.create_window(master)

            create_graph= Button(window, text = "Create graph", command = lambda:self.runTask5())
            create_graph.pack(side = BOTTOM )

            self.creat_gui(window,"""Task Description:
                "For the above “also like” functionality, generate a graph that displays the re-lationship between the input document and
                all documents that have been found as “also like” docu-ments (and only these documents). Highlight the input document and
                user by shading in that graph,and use arrows to capture the “has-read” relationship (i.e. arrow from reader to document).
                In thegraph shorten all visitor UUIDs and document UUIDs to the last 4 hex-digits."

            Inputting the JSON file and a Document UUID present in that file and the clicking the "Create Graph" button will create a .dot graph showing the which reader has read which document. It shows the number 1 document in red and the original document in green""")


    def create_window(self, master):
            if master == None:
                    window = self.master
            else:
                    window = Toplevel(master)
            w, h = window.winfo_screenwidth(), window.winfo_screenheight()
            window.geometry("%dx%d+0+0" % (w, h))
            return window

    def creat_gui(self,master,task,description):
            self.title = Label(master, text= "Task {0}".format(task))
            self.title.pack()

            self.des_label = Label(master, text = description, relief = "ridge")
            self.des_label.pack(fill=BOTH, expand=1)

            self.doc_entry = Entry(master, width = 100)
            self.doc_entry.insert(0, doc_uuid)
            self.doc_entry.pack(side = BOTTOM)

            self.doc_label = Label(master, text= "Enter Document UUID")
            self.doc_label.pack(side = BOTTOM)

            self.file_entry = Entry(master, width = 100)
            self.file_entry.insert(0,file)
            self.file_entry.pack(side = BOTTOM)

            self.file_label = Label(master, text= "Enter File Name")
            self.file_label.pack( side = BOTTOM  )

    def runTask5(self):
            l.graphLikes(self.doc_entry.get(),l.top10(l.alsoLikes(self.doc_entry.get(),extractJSON(self.file_entry.get()))),extractJSON(self.file_entry.get()))
            os.system("dot -Tps -o graph.ps graph.dot")
            os.system("evince graph.ps")

#982a1b10c34efa22
#"130313161023-ee03f65a89c7406fa097abe281341b42" -good example

root = Tk()
e = Extract()
l = Likes()
gui = Gui(root, doc_uuid)
if task == "2a":
    gui.task2a()

if task == "2b":
    gui.task2b()

if task == "3a":
    gui.task3a()

if task == "3b":
    gui.task3b()

if task == "4d":
    gui.task4d()

if task == "5":
    gui.task5()

if (task == "6" or (args.u == None and args.d == None and args.t == None and args.f == None)):

    gui.task6()



else:
    print("ERROR: No/wrong task specified")
root.mainloop()
