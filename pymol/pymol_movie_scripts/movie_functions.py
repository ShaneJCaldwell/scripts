##########################################

##      Pymol Movie Transformations     ##

## Shane Caldwell June 2015             ##
## Last updated 2015.12.03              ##

##########################################


#This file contains functions to do transformation, write png files, 
#and increment imagecounter, naming pngs based on imagecounter

#currently not as robust as I would like, especially the for loops
#input checking would really help things out
#global ray trace function can be turned on or off, invoking 

# png function is weird, if you give values to height and width, 
#imagemagick can make gif from png, but the files are corrupt and can't open in image viewer

#ximage, yimage should be global variables that let us set the size of the image, but for the bug above

from pymol import cmd
import numpy as np
import os

ray = 0
imagecount = 1
filename = "molecule"
ximage = 300
yimage = 300

# Turn camera along defined cardinal axis - basic function
# images: Number of frames written
# sweep: angular turn around specified axis
# axis: cardinal axis, x, y, or z

def images_spin(images, sweep, axis):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images - 1)
	print "Writing %s images turning about %s axis by %s degrees per image" % \
			(images, axis, sweep/images)

	#cycle over images
	for i in range (0, images):

		#move camera
		cmd.turn(axis, sweep/images) # turn each image the fraction of the total spin
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		print "cycle %s, image %s" % (i + 1, imagecount)
		imagecount = imagecount + 1
		cmd.refresh()


# Morph between two states

# Morph between different states of the molecule, generated from server
# images: Number of frames written. must be same as number of states

def images_morph(images):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images - 1)
	print "Writing %s images morphing froms state %s to state %s" % \
			(images, 1, images)
	
	#cycle over images
	for i in range (0, images):
		
		#change state
		cmd.set("state", i+1)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()
			


# Morph in reverse order between two states

# Morph between different states of the molecule, generated from server
# images: Number of frames written. must be same as number of states

def images_morphback(images):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images - 1)
	print "Writing %s images morphing froms state %s to state %s" % \
			(images, images, 1)
	
	#cycle over images
	for i in range (0, images):
		
		#change state
		cmd.set("state", images-i)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()




# Turn the camera in 3 axes
# rotations aren't independent, need to do some work to figure out how to implement
# independent angles. But as it is, this creates some cool 3-axis-ish rotations
# images: Number of frames written
# sweep: turns in degrees on the x, y, and z axes, sequentially


def images_spin_3ax(images, sweep):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images turning about:" % images
	print "     x axis by %s degrees," % (sweep[0]/images)
	print "     y axis by %s degrees, and" % (sweep[1]/images)
	print "     z axis by %s degrees per image" % (sweep[2]/images)


	#cycle over number of images
	for i in range (0, images):

		# transformations
		cmd.turn("x", sweep[0]/images)
		cmd.turn("y", sweep[1]/images)
		cmd.turn("z", sweep[2]/images)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()
			

# Move the camera along one axis. basic operation
# images: Number of frames written
# distance: total distance to shift camera
# axis: axis along which to shift

def images_slide(images, distance, axis):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images moving along %s axis by %s Angstrom per image" % \
			(images, axis, distance/images)

	#cycle for number of images
	for i in range (0, images):

		# transformations
		cmd.move(axis, distance/images)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()



# Move the camera in 3D 

def images_slide_3D(images, distance):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage


	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images moving along:" % images
	print "     x axis by %s Angstrom," % (distance[0]/images)
	print "     y axis by %s Angstrom, and" % (distance[1]/images)
	print "     z axis by %s Angstrom per image" % (distance[2]/images)


	for i in range (0, images): #cycle for number of images

		# transformations
		cmd.move("x", distance[0]/images)
		cmd.move("y", distance[1]/images)
		cmd.move("z", distance[2]/images)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()



# Spiral screw movement on cardinal axis (arbitrary axis is MUCH harder)

def images_screw(images, distance, sweep, axis):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images moving along %s axis by %s Angstrom" % \
			(images, axis, distance/images)
	print "     and rotating %s degrees per image" % (sweep/images)

	for i in range (0, images): #cycle for number of images

		# transformations
		cmd.move(axis, distance/images)
		cmd.turn(axis, sweep/images)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()



# Move in 3-dimensions at the same time as rotating on three axes
def images_spin3_slide3(images, distance, sweep):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images turning about:" % images
	print "     x axis by %s degrees, then" % (sweep[0]/images)
	print "     y axis by %s degrees, and" % (sweep[1]/images)
	print "     z axis by %s degrees per image," % (sweep[2]/images)
	print "   while moving along:"
	print "     x axis by %s Angstrom," % (distance[0]/images)
	print "     y axis by %s Angstrom, and" % (distance[1]/images)
	print "     z axis by %s Angstrom per image" % (distance[2]/images)


	for i in range (0, images): #cycle for number of images

		# transformations
		cmd.turn("x", sweep[0]/images)
		cmd.turn("y", sweep[1]/images)
		cmd.turn("z", sweep[2]/images)
		cmd.move("x", distance[0]/images)
		cmd.move("y", distance[1]/images)
		cmd.move("z", distance[2]/images)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()



# Zoom in to the target of interest. uses the get-view and set_view to extract matrices
# and then interpolate the transformation in between them
# to do: zoom with a buffer

def images_refocus(images, target):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images zooming to selection:" % images
	print "  %s" % target

	current_view = cmd.get_view()	#get the starting view
	temporary_view = current_view	#make variabe to track interpolation
	cmd.zoom(target)				#zoom to the target selection
	end_view = cmd.get_view()		#get the ending view
			
	#get the difference between the start and ending views, divide per step
	views_difference = tuple(np.subtract(end_view, temporary_view))
	diff_per_image = tuple(i/images for i in views_difference)
		
	for i in range (0, images): #cycle for number of images
		
		#update the interpolating view
		temporary_view = tuple(np.add(temporary_view, diff_per_image))
				
		cmd.set_view(temporary_view)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()



# Change colour from a defined start colour to a defined end colour.
# to do: extract current colour to be the start colour

def images_chameleon(images, target, start_color, end_color):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images changing colour of %s from %s to %s:" \
			% (images, target, start_color, end_color)

	temp_color = start_color	#set list for interpolation of colour
	color_diff = [0., 0., 0.]	#initialize difference to zero


	#there's likely a more elegant way to rewrite the next couple steps:
	for i in range (0, 3):
		color_diff[i] = end_color[i] - start_color[i] # set difference variables for rgb values

	for i in range (0, images):
		
		for j in range (0, 3):

			#update interpolated colour
			temp_color[j] = temp_color[j] + (color_diff[j]/images) 

			# round to avoid number format problems with color input
			temp_color[j] = round(temp_color[j], 6) 

		cmd.set_color("temp_colour", temp_color) 	# set the interpolated colour
		cmd.color("temp_colour", target)			# update
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()


# change transparency of selected object. Modes necessary because pymol uses different functions
# for different types of object
#mode 0= surface 1 = cartoon 2 = sticks 3 = spheres

def images_ghost(images, target, mode, transparency, initial_transparency = 0):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images changing transparency of %s to %s:" % (images, target, transparency)


	temporary_transparency = initial_transparency			#set initial transparency
	transparency_diff = transparency - initial_transparency	#determine difference to iterate over

	for i in range (0, images):

		temporary_transparency = temporary_transparency + (transparency_diff/images) #interpolate

		if mode == 0:
			cmd.set("transparency", temporary_transparency, target) #surface transparency

		elif mode == 1:
			cmd.set("cartoon_transparency", temporary_transparency, target)

		elif mode == 2:
			cmd.set("stick_transparency", temporary_transparency, target)

		elif mode == 3:
			cmd.set("sphere_transparency", temporary_transparency, target)
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()




#Clunky, but in case of inserting special images, add a function to increment the imagecounter. necc?
def images_skip(images):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s will be skipped" % (imagecount, imagecount + images -1)

	imagecount = imagecount + images



# write out images with no change. may not be needed if restructure code
def images_freeze(images):

	global imagecount
	global ray
	global filename
	global ximage
	global yimage

	print "... Images %s - %s:" % (imagecount, imagecount + images -1)
	print "Writing %s images without moving" % images

	for i in range (0, images):
			
		#print image
		cmd.png("images/%s_%04d" % (filename, imagecount), ray = ray)

		#increment imagecounter
		imagecount = imagecount + 1
		cmd.refresh()



def gif_linux():

	global filename

	os.system("convert -delay 4 -verbose -dispose previous 'images/%s'_*.png 'images/%s'.gif" %(filename, filename))

def clean():

	global filename

	os.system("rm images/%s*.png" %(filename))

