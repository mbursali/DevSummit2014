import arcpy
import json
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [JsonToGDB]


class JsonToGDB(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "JSON To GDB"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None

        param0 = arcpy.Parameter(
            displayName="Input Files",
            name="infiles",
            datatype="DETextfile",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        param0.filter.list = ["txt", "json"]

        param1 = arcpy.Parameter(
            displayName="Output File Geodatabase",
            name="gdbName",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Input")

        param1.defaultEnvironmentName="workspace"

        param2 = arcpy.Parameter(
            displayName="Output Feature Class",
            name="fcName",
            datatype="DEFeatureClass",
            parameterType="Derived",
            direction="Output")

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        infiles = parameters[0].valueAsText
        gdbName = parameters[1].valueAsText

        infileList = infiles.split(';')

        fcName = os.path.basename(infileList[0]).split('.')[0].split('_')[0]

        arcpy.env.workspace = gdbName

        if arcpy.Exists(fcName):
            print 'Deleting ' + fcName
            arcpy.Delete_management(fcName)

        fcCreated = False
        cursorCreated = False

        try:
            for infile in infileList:
                with open(infile, 'r') as f:
                    jsonObj = json.load(f)
                    f.close()

                geom = arcpy.AsShape(jsonObj, True)

                if jsonObj.has_key('spatialReference') == False:
                    sr = arcpy.SpatialReference(0)
                    geom = arcpy.FromWKT(geom.WKT)
                else:
                    sr = arcpy.SpatialReference(int(jsonObj['spatialReference']['wkid']))

                if fcCreated == False:
                    if sr.factoryCode > 0:
                        arcpy.CreateFeatureclass_management(gdbName, fcName, geom.type, spatial_reference=sr)
                    else:
                        arcpy.CreateFeatureclass_management(gdbName, fcName, geom.type)

                    arcpy.AddField_management(fcName, "OLD_ID", "SHORT")
                    cursor = arcpy.da.InsertCursor(fcName, ["SHAPE@", "OLD_ID"])
                    cursorCreated = True
                    fcCreated = True

                fileNameSplit = os.path.basename(infile).split('.')[0].split('_')
                if len(fileNameSplit) > 1 and fileNameSplit[1].isdigit():
                    old_id = fileNameSplit[1]
                else:
                    old_id = -1

                id = cursor.insertRow([geom, old_id])

        except Exception as e:
            print e.message
        finally:
            if cursorCreated:
                del cursor

        arcpy.SetParameterAsText(2, os.path.join(gdbName, fcName))

        arcpy.AddMessage("Success creating  {0}/{1}".format(gdbName, fcName))

        return
