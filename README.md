# FOTools is a set of blender utilities aimed at forensic 3d-visualisation.

This program is distributed in the hope that it will be useful,https://github.com/etvr/fotools/blob/master/README.md
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 

## WARNING, assume that all results of these tools are WRONG! 
these tools make large rounding errors and the calculations are questionable at best.
YOU as the analyst make your own findings based on your knowledge and insight, not the tool.
these tools might assist you but their results are anything but conclusive so use at your own risk.
We accept no responsibility whatsoever for any results, successes, mistakes, damages or harm in any form that might result in usage of this code.

 ### it contains a utilities for:

#### - drawing an equilateral triangle
  the top corner angle and radius are defined by the user
  this can be used to illustrate or analyse a field of view (FOV)
  
  ![blender_In0mdvSHWO](https://github.com/etvr/fotools/assets/858190/8547fae7-f7c7-4db5-8892-504f967805fe)


#### - drawing a frustum with a given horizontal and vertical angle,
   - this can be used to represent a simple camera frustum

   ![blender_JsXYgdstCx](https://github.com/etvr/fotools/assets/858190/03c24f7c-7f3b-4eae-bbc6-915a1cad3741)
   
#### - Line of sight colorisation tool
   - this tool creates a pointlight with a set color and almost no falloff.
   - put the pointlight in a position where you want to colorize the possible sightlines from this position
   - warning, this function will adjust your rendersettings! BEWARE!!
   - 
  ![blender_c8aogUNRO8](https://github.com/etvr/fotools/assets/858190/f0b752e6-4bce-4d29-95ed-f21c571bbf66)

#### - Gunshot trajectory illusstration. a tool that aims a cone along the axis between two selected objects 
  - the angle, length are user defined
  - the cone can be split into 3 seperatye objects wich are defiend by the minimum and maximum size of the middel segment

  
   ![blender_vV9a68e5Pj](https://github.com/etvr/fotools/assets/858190/94669524-f3ac-4965-b459-daaeff9fb17f)

#### - PLY-pointcloud to geometry nodes converter
    - import a binary encoded PLY-file pointcloud, rgb color is suported
    - keep the pointcloud small, 1 to 5 million points depending on the systems specs
    - once loaded, click the conversion buton.
    - switch to viewport shading to render in color

#### - Concentric circle grid generator (circulair distance grid)
  - Creates a grid of concentric circles with customizable radius, number of circles, and resolution.
  - Useful for visualizing distances and areas of interest around a central point.

  ![blender_concentric_circles](https://github.com/etvr/fotools/assets/858190/placeholder_for_circles.png)

#### - Primitive Fitting Tools
  - A set of tools to fit geometric primitives to a selection of vertices (in Edit Mode) ~~~or objects (in Object Mode)~~
  - To use, select the target geometry, then click the desired fitting button.
  - The fitting algirithm will report an rms value in the console
  - Supported primitives include:
    - **Fit Line**: Fits a straight line through the selected points.
    - **Fit Plane**: Fits a flat plane to the selected points.
    - **Fit Circle**: Fits a circle to three selected points, the circle can be fittend in the xy plane or in the best fit plane.
    - **Fit Cylinder**: Fits a cylinder to the selected points.
    - **Fit Sphere**: Fits a sphere to the selected points.

  ![blender_fitting_tools](https://github.com/etvr/fotools/assets/858190/placeholder_for_fitting.png)

## How to Install the add-on
 - save the code as a zipfile
 - open blender, goto menu "EDIT" > "PREFERENCES"
 - in the preferences screen in the left sidebar click on "Add-ons"
 - click on "Install" in the top right
 - navigate to the previously saved zipfile and click on "Install Add-on"

   the addon will show op in the 3d-view as a "N-pannel" called FOTools

   
