#!/usr/bin/env python

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
import graphviz



def toSet(l):
    s = set()
    for item in l:
        s.add(item)
    return s

class Likes:
	#possibly put back in method

	#jsonarr = None
	#def __init__ (self,jsonarr):
	#	self.jsonarr = jsonarr
	def findDocus(self,visUUID,jsonarr):
		documents=[]
		for item in jsonarr:
			try:
				if item["visitor_uuid"] == visUUID:
					documents.append(item["subject_doc_id"])
			except KeyError:
				pass
		if documents == []:
			print ("Error: please check that visitor UUID is correct")
		return documents

	def findVisitors(self,docUUID, jsonarr):
		visitors = []
		for item in jsonarr:
			try:
				if item["subject_doc_id"] == docUUID:
					visitors.append(item["visitor_uuid"])
			except KeyError:
				pass
		return visitors


	def alsoLikes(self, docUUID,jsonarr,visUUID=None):
		#print(findVisitors(docUUID))
		alsoreads = toSet(self.findVisitors(docUUID,jsonarr))
		#for visitor in self.findVisitors(docUUID):
		#	self.alsoreads.add(visitor)
		#print(self.alsoreads)
		for reader in alsoreads:
			read = self.findDocus(reader,jsonarr)
		#print(r)
			for doc in read:
				alsodocs.append(doc)

		counter = collections.Counter(alsodocs)
		return counter

	def top10(self,dictionary):
		sort = sorted(dictionary)
		top10 = []
		if len(sort) < 10:
			for i in range(len(sort)):
				top10.append(sort[i])
		else:
			for i in range(10):
				top10.append(sort[i])
		return top10

	def graphLikes(self,docuuid,top10, jsonarr, visitoruuid = None):
		top10readers = set()
		#populate top 10 readers
		output = open("graph.dot" , "w+")
		#allreaders of the top 10 documents
		for doc in top10:
			for reader in toSet(self.findVisitors(doc, jsonarr)):
				top10readers.add(reader)

		#dot = Digraph(ranksep=.75, ratio=compress, size = "15,22", orientation=landscape, rotate=180)
		output.write("""digraph also_likes {
			ranksep=.75; ratio=compress; size = "15,22"; orientation=landscape; rotate=180;
			{
				node [shape=plaintext, fontsize=16];

				Readers -> Documents
			[label="Size: 1m"];\n""")
		#documents
		output.write("""	"{0}"[label="{0}",shape="box",style=filled,color=".3 .9 .7"];\n""" .format(self.shorten(docuuid)) )
		for i,doc in enumerate(top10):
			if i == 0:
				output.write("""	"{0}"[label="{0}",shape="box",style=filled,color=".0 .9 .9"];\n""" .format(self.shorten(doc)) )
			output.write("""	"{0}"[label="{0}",shape="box"];\n""" .format(self.shorten(doc)) )
		#readers
		for reader in top10readers:
			if self.isReader(docuuid,reader,jsonarr):
				output.write("""	"{0}" [label="{0}",shape="circle"];\n""".format(self.shorten(reader)))

		output.write("""{ rank = same; "Readers";\n""")

		for reader in top10readers:
			if self.isReader(docuuid,reader,jsonarr):
				output.write("""	"{0}";\n""".format(self.shorten(reader)))

		output.write("""};{ rank = same; "Documents";\n""")

		for doc in top10:
			output.write("""	"{0}";\n""".format(self.shorten(doc)))
		output.write("""	"{0}";\n""".format(self.shorten(docuuid)))
		output.write("};")

		for doc in top10:
			#print(doc)
			#print(toSet(self.findVisitors(doc)))
			for reader in toSet(self.findVisitors(doc, jsonarr)):

				if self.isReader(docuuid,reader,jsonarr):
					output.write("""	"{0}" -> "{1}";\n""".format(self.shorten(reader),self.shorten(doc)))
		for reader in toSet(self.findVisitors(docuuid,jsonarr)):
			if reader in top10readers:
				output.write("""	"{0}" -> "{1}";\n""".format(self.shorten(reader),self.shorten(docuuid)))
		output.write("""	};
		}""")

	def isReader(self,doc,visitor,jsonarr):
		isreader = False
		if visitor in self.findVisitors(doc, jsonarr):
			isreader = True
		return isreader

	def shorten(self,uuid):
		"""shortens a UUID down to its last 4 hex-digits"""
		return uuid[-4:]

	def printList(self, l):
		"""iteratively prints list with its corresponding number """
		for i,no in enumerate(l):
			print(i+1,no)
			print("\n")
