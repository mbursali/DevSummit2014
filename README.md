DevSummit2014
=============

Understanding and Using Geometry, Projections and Spatial Reference Systems in ArcGIS

This repository contains the slideshow and demos from a presentation given at the Esri Developer Summit 2014 in Palm Springs, CA. The name of the presentation is "Understanding and Using Geometry, Projections and Spatial Reference Systems in ArcGIS", and it was given by Rob Juergens, Melita Kennedy and Annette Locke. 

To see the slideshow, open "Understanding and Using Geometry, Projections and Spatial Reference Systems in ArcGIS.pdf". 

To use the ArcMap demos that were shown during the presentation, go to the Demos folder. There are two file geodatabases and some ArcMap documents. 

DevSummit2014.gdb contains data for the following ArcMap demos:
  - Projection between different GCSs (Project.mxd)
  - Merge polygons (MergePolygons.mxd)
  - What is simple here may not be simple there (OneSimplePolygon.mxd)
  
QM.gdb contains data for the ArcMap demo 
  - Where on the map do I put the geometry? (QM.mxd)
  
There is also a Python toolbox, MyPythonToolbox.pyt, containing a tool called "JSON to GDB". The tool was used in the QM.mxd demo to convert the JSON file, QM.txt, to a feature class in the file geodatabase QM.gdb. 
You can use this tool on any valid JSON file representing a geometry by accessing the .pyt file through the Catalog window in ArcMap. 

For the javascript demos, go to the JavaScript folder. 
The javascript demos are:
  - Why do we care if geometries are simple? (SimplifyPolygon.html)
  - Buffer and Spatial Reference (GeodesicBufferWebMercator.html and GeodesicBufferOther.html)
  

