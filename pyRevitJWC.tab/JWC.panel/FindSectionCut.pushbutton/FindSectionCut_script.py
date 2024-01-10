# Import Libraries
from pyrevit import forms
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import FilteredElementCollector, Grid, BuiltInParameter,XYZ,Line,BuiltInCategory,View,ElementType,Element

#from pyRevit import DB

# Get Revit Document
doc = __revit__.ActiveUIDocument.Document
uiDoc = __revit__.ActiveUIDocument

selectedSectionID = uiDoc.Selection.GetElementIds()[0]

selectedSectionID = doc.GetElement(selectedSectionID).ViewId




selectedSectionName = doc.GetElement(selectedSectionID).Name
detailID = doc.GetElement(selectedSectionID).GetTypeId()


collector = FilteredElementCollector(doc)
allElements = collector.OfCategory(BuiltInCategory.OST_Viewers)

for element in allElements:
	try:
		if element.Name == selectedSectionName:
			
			ownerId = element.OwnerViewId
			ownerView = doc.GetElement(ownerId)
			ownerViewName = ownerView.Name
			print(ownerViewName)	
			
	except AttributeError:
	
		continue


