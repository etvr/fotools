FOTools is a set of blender utilities aimed at forensic 3d-analysis.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

WARNING, assume that all results of these tools are WRONG! 
these tools make large rounding errors and the calculations are questionable at best.
YOU as the analyst make your own findings based on your knoledge and insight in your specific field of expertise, not the tool.
these tools might assist you but their results are annything but conclusive. 
use at your own risk, we accept no responibillity whatsoever for any results, sucesses, mistakes, damages or harm in any form that result in your use of this code.

 it contains a utilities for:

- drawing an equilateral triangle
  the top corner angle and radius are defined by the user
  this can be used to illustrate or analyse a field of view (FOV)
  
  ![blender_In0mdvSHWO](https://github.com/etvr/fotools/assets/858190/8547fae7-f7c7-4db5-8892-504f967805fe)



- drawing a piramid with a given horizontal and vertical angle,
    this can be used to represent a simple camera frustum

    ![blender_JsXYgdstCx](https://github.com/etvr/fotools/assets/858190/03c24f7c-7f3b-4eae-bbc6-915a1cad3741)


  
- a tool that aims a cone along the axis between two selected objects
  the angle, length are user defined
  also the cone can be split into 3 seperatye objects wich are defiend by the minimum and maximum size of the middel segment
  this tool can be used to illustrate or analyse gunshot trajectory
  
   ![blender_vV9a68e5Pj](https://github.com/etvr/fotools/assets/858190/94669524-f3ac-4965-b459-daaeff9fb17f)

