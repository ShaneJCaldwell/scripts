
## Test script for movie functions ##

import movie_functions as mv

#update viewport
#cmd.viewport(300,300)

## Load molecule
cmd.load ("1gll.pdb")

cmd.hide()							#hide default crap
cmd.show("cartoon")					
cmd.show("sticks", "organic")		
cmd.show("spheres", "inorganic")	#draw single atoms
cmd.set_color("start_color", [0., 0., 1.])
cmd.color("start_color", "elem C")
cmd.bg_color("white")

mv.ray = 0
mv.filename = "test"

#mv.images_skip(10)

mv.images_spin(18, 90., "x")
mv.images_ghost(20, "all", 1, 0.8)
mv.images_chameleon(40, "elem C", [0., 0., 1.], [1.,0.,0.])
mv.images_slide(20, 10.0, "y")
mv.images_slide_3D(20, [10.0, 5., 20.])
mv.images_screw(40, -20., 180., "x")
mv.images_spin3_slide3(50, [-10.0, -5., 20.], [180., 72., 18])
mv.images_refocus(40, "chain Y and resn ACP")
mv.images_spin(36, 180., "x")
mv.images_spin_3ax(64, [360., 144., 36.])
mv.images_refocus(40, "chain O and resn ACP")
mv.images_freeze(10)

# Write into a gif file
mv.gif_linux()
#mv.clean()

cmd.quit()
