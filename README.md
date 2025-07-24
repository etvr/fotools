# FOTools is a set of blender utilities aimed at forensic 3d-analysis.

This program is distributed in the hope that it will be useful,https://github.com/etvr/fotools/blob/master/README.md
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 

## WARNING, assume that all results of these tools are WRONG! 
these tools make large rounding errors and the calculations are questionable at best.
YOU as the analyst make your own findings based on your knowledge and insight, not the tool.
these tools might assist you but their results are anything but conclusive so use at your own risk.
We accept no responsibility whatsoever for any results, successes, mistakes, damages or harm in any form that might result in your use of this code.

 ### it contains a utilities for:

#### - drawing an equilateral triangle
  the top corner angle and radius are defined by the user
  this can be used to illustrate or analyse a field of view (FOV)
  
  ![blender_In0mdvSHWO](https://github.com/etvr/fotools/assets/858190/8547fae7-f7c7-4db5-8892-504f967805fe)


#### - drawing a frustum with a given horizontal and vertical angle,
   - this can be used to represent a simple camera frustum

   ![blender_JsXYgdstCx](https://github.com/etvr/fotools/assets/858190/03c24f7c-7f3b-4eae-bbc6-915a1cad3741)
   
#### - a line of sight colorisation tool
   - this tool creates a pointlight with a set color and almost no falloff.
   - put the pointlight in a position where you want to colorize the possible sightlines from this position
   - warning, this function will adjust your rendersettings! BEWARE!!
   - 
  ![blender_c8aogUNRO8](https://github.com/etvr/fotools/assets/858190/f0b752e6-4bce-4d29-95ed-f21c571bbf66)

#### - a tool that aims a cone along the axis between two selected objects
  the angle, length are user defined
  also the cone can be split into 3 seperatye objects wich are defiend by the minimum and maximum size of the middel segment
  this tool can be used to illustrate or analyse gunshot trajectory
  
   ![blender_vV9a68e5Pj](https://github.com/etvr/fotools/assets/858190/94669524-f3ac-4965-b459-daaeff9fb17f)

#### - a PLY-pointcloud to geometry nodes converter
    - import a binary encoded pointcloud, rgb color is suported
    - keep the pointcloud small, 1 to 5 million points depending on the systems specs
    - once loaded, click the conversion buton.
    - switch to viewport shading to render in color

#### - Angle Measurement Tool
  - Measures the angle between three selected objects.
  - The active object is used as the vertex of the angle.
  - Creates a visual representation of the angle with lines and a text label showing the degrees.
  - To use: Select three objects, make sure the intended vertex is the active object, and click "Measure Angle" in the FOTools panel.

  ![blender_angle_measurement](https://github.com/etvr/fotools/assets/858190/placeholder_for_angle_measurement.png)

## How to Install the add-on
 - save the code as a zipfile
 - open blender, goto menu "EDIT" > "PREFERENCES"
 - in the preferences screen in the left sidebar click on "Add-ons"
 - click on "Install" in the top right
 - navigate to the previously saved zipfile and clikc on "Install Add-on"

   the addon will show op in the 3d-view as a "N-pannel" called FOTools

   
