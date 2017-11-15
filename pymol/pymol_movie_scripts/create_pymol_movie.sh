#!/bin/bash

#create the python file
touch make_movie.py

echo "## Test script for movie functions ##" >> make_movie.py

echo "import movie_functions as mv" >> make_movie.py

echo "#update viewport" >> make_movie.py
echo "#cmd.viewport(300,300)" >> make_movie.py

echo "## Load molecule" >> make_movie.py
echo '''cmd.load ("1gll.pdb")''' >> make_movie.py

echo "cmd.hide()							#hide default crap" >> make_movie.py
echo '''cmd.show("cartoon")					''' >> make_movie.py
echo '''cmd.show("sticks", "organic")		''' >> make_movie.py
echo '''cmd.show("spheres", "inorganic")	#draw single atoms''' >> make_movie.py
echo '''cmd.set_color("start_color", [0., 0., 1.])''' >> make_movie.py
echo '''cmd.color("start_color", "elem C")''' >> make_movie.py
echo '''cmd.bg_color("white")''' >> make_movie.py
echo '''mv.ray = 0''' >> make_movie.py
echo '''mv.filename = "test"''' >> make_movie.py

echo '''#mv.images_skip(10)''' >> make_movie.py

echo '''mv.images_spin(18, 90., "x")''' >> make_movie.py
echo '''mv.images_ghost(20, "all", 1, 0.8)''' >> make_movie.py
echo '''mv.images_chameleon(40, "elem C", [0., 0., 1.], [1.,0.,0.])''' >> make_movie.py
echo '''mv.images_slide(20, 10.0, "y")''' >> make_movie.py
echo '''mv.images_slide_3D(20, [10.0, 5., 20.])''' >> make_movie.py
echo '''mv.images_screw(40, -20., 180., "x")''' >> make_movie.py
echo '''mv.images_spin3_slide3(50, [-10.0, -5., 20.], [180., 72., 18])''' >> make_movie.py
echo '''mv.images_refocus(40, "chain Y and resn ACP")''' >> make_movie.py
echo '''mv.images_spin(36, 180., "x")''' >> make_movie.py
echo '''mv.images_spin_3ax(64, [360., 144., 36.])''' >> make_movie.py
echo '''mv.images_refocus(40, "chain O and resn ACP")''' >> make_movie.py
echo '''mv.images_freeze(10)''' >> make_movie.py

echo '''# Write into a gif file''' >> make_movie.py
echo '''mv.gif_linux()''' >> make_movie.py
echo '''mv.clean()''' >> make_movie.py

echo '''cmd.quit()''' >> make_movie.py

#bash pymol make_movie.py

#delete python file
#rm make_movie.py
