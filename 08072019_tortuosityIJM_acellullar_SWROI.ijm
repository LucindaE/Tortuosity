#Written by Alessandro Felder & Lucinda Evans
#Please acknowledge its use in any publications or presentations 
#Skeletonises images from a directory with minimal branches - writes results to a file for tortuosity analysis

run("Close All");
//directory = "F:\Mouse A I13 scan\Tortuosity_100VoxSW_childvolumeROItest\";
directory = getDirectory("Choose a Directory");
fileList = getFileList(directory)
print(fileList.length)
for(i=0; i<fileList.length; i++) 
{
	if(!endsWith(fileList[i], ".bmp")) {
		continue;
	}
	name = fileList[i];
	open(name);
	
	
	setAutoThreshold("Default dark");
	setThreshold(1, 255);
	setOption("BlackBackground", true);
	run("Convert to Mask");
	
	run("Find Edges");
	
	setForegroundColor(0, 0, 0);
	lines = getNumber("Please enter number of lines needed from this image (max 2): ", 1);

	for(line=1;line<=lines;line++)
	{
		waitForUser("Line "+line+". Please remove lower line, and any other lines not needed right now, then click OK");	
		run("Select None");
		run("Dilate");
		run("Purify", "labelling=Mapped chunk=4");
		run("Invert LUT");
		run("Dilate");
		run("Dilate");
		run("Dilate");
		run("Dilate");
		run("Dilate");
		run("Dilate");
		if(line==1){
			open(fileList[i]);
	
			setAutoThreshold("Default dark");
			setThreshold(1, 255);
			setOption("BlackBackground", true);
			run("Convert to Mask");
			
			run("Find Edges");
			
			setForegroundColor(0, 0, 0);
		}
	}
	if(lines>1){
		imageCalculator("Add create", name,replace(name, ".bmp", "-1.bmp"));
		selectWindow("Result of "+name);
	}
	else {
		selectWindow(name);
	}
	saveAs(directory+"Articular_surface/"+replace(name, ".bmp", "")+"_articular-surface.tif");
	run("Close All");
}
