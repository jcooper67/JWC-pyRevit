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


#print(selectedSectionID)

selectedSectionName = doc.GetElement(selectedSectionID).Name
detailID = doc.GetElement(selectedSectionID).GetTypeId()
#print(detailID)
# print(selectedSectionName)

collector = FilteredElementCollector(doc)
#allElements = collector.OfCategory(detailID)
#allElements = collector.OfClass(View)
allElements = collector.OfCategory(BuiltInCategory.OST_Viewers)
#print(allElements)

for element in allElements:
	#print(element.Name)

	try:
		if element.Name == selectedSectionName:
			print("Searching for: ")
			print(selectedSectionName)
			print("Match Found: ")
			print(element.Name)
			print(element.Id)

			
			ownerId = element.OwnerViewId
			ownerView = doc.GetElement(ownerId)
			ownerViewName = ownerView.Name
			print(ownerViewName)
			
			
	except AttributeError:
	
		continue


