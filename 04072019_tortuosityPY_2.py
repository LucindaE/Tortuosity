#Written by Alessandro Felder & Lucinda Evans
#Please acknowledge its use in any publications or presentations 
#Produces .csv file with euclidean distances of endpoints and branch lengths from skeletonised images in a directory (if no branches are present)

# @CommandService cs
# @DisplayService ds

import os
import csv
from ij import IJ

def getTortuosity(directory, imageName):
	print(imageName)
	image = IJ.openImage(directory+imageName)
	
	skeletoniseWrapper = cs.run("org.bonej.wrapperPlugins.SkeletoniseWrapper", False, ["inputImage",image])
	skeletonInstance = skeletoniseWrapper.get()
	skeleton = skeletonInstance.getOutput("skeleton")
	IJ.save(skeleton, directory+"Skeletons/"+imageName.replace(".tif","")+"-skeleton")
	
	wrapper = cs.run("org.bonej.wrapperPlugins.AnalyseSkeletonWrapper", False, ["inputImage",image,"verbose",True])
	wrapperInstance = wrapper.get()
	
	table = wrapperInstance.getOutput("verboseTable")
	print(table[0])
	nskeletons = max(table[0])
	print(nskeletons)
	branchLength = table[2]
	euclideanDistance = table[9]
	if(len(branchLength)>nskeletons):
		print("multiple branches in skeleton: returning zero tortuosity")
		return [0,0,0]
	avgBL = sum(branchLength) / float(nskeletons)
	avgED = sum(euclideanDistance)/float(nskeletons)
	print("branch length: ", avgBL)
	print("euclidean distance: ", avgED)
	tortuosity = avgED/avgBL
	return [avgBL, avgED, tortuosity]


directory = "F:/Mouse A I13 scan/Tortuosity_100VoxSW_childvolumeROItest/Articular_surface/"
os.chdir(directory)
outputFile = open("tortuosity.csv",'w')
outputWriter = csv.writer(outputFile, delimiter=',')
outputWriter.writerow(["name","branchLength","euclideanDistance","tortuosity"])
for fileName in os.listdir(directory):
    if fileName.endswith(".tif"):
    	t = getTortuosity(directory,fileName)
    	print(t)
    	print(type(t))
    	row = [fileName,t[0],t[1],t[2]]
    	outputWriter.writerow(row)
    	IJ.run("Close All")
outputFile.close()
