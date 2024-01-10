# Import Libraries
from pyrevit import forms
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import FilteredElementCollector, Grid, BuiltInParameter,XYZ,Line
#from pyRevit import DB

# Get Revit Document
doc = __revit__.ActiveUIDocument.Document
uiDoc = __revit__.ActiveUIDocument

selectedSectionID = uiDoc.Selection.GetElementIds()

element = doc.GetElement(selectedSectionID)

print(element)