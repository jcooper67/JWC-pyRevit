# Import Libraries
from pyrevit import forms
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import FilteredElementCollector, Grid, BuiltInParameter,XYZ,Line
#from pyRevit import DB

# Get Revit Document
doc = __revit__.ActiveUIDocument.Document
uiDoc = __revit__.ActiveUIDocument

GRIDSX = []
GRIDSY = []

def checkDuplicateGrids(gridOrigin, direction):
    duplicate = False 
    if direction == "X":
        print("X")
        print(gridOrigin)
        print(GRIDSX)
        if gridOrigin in GRIDSX:
            duplicate = True
        else:
            print("Not Duplicate")
            GRIDSX.append(gridOrigin)
            duplicate = False
    
    if direction == "Y":
        print("Y")
        print(gridOrigin)
        print(GRIDSY)
        if gridOrigin in GRIDSY:
            duplicate = True
        else:
            print("Not Duplicate")
            GRIDSY.append(gridOrigin)
            duplicate = False

    

    return duplicate
    
# def getGridOrigin(gridObject):
#     originString = gridObject.Curve.Origin.ToString()
#     originString = originString.replace("(","")
#     originString = originString.replace(")","")
#     subStrings=originString.split(",")
#     return subStrings[0],subStrings[1],subStrings[2]
#Method for Taking XYZ Object and returning its individual coordinates as Floats
def parseXYZ(xyzOBject):
    xyzString = xyzOBject.ToString()
    xyzString = xyzString.replace("(","")
    xyzString = xyzString.replace(")","")
    subStrings=xyzString.split(",")
    x = float(subStrings[0])
    y = float(subStrings[1])
    z = float(subStrings[2])
    return x,y,z
#Creating Grid Method
def createGrid(document,columnLocationXYZ,xyzDestination):
    print(columnLocationXYZ)
    print(xyzDestination)
    with Transaction(document,"Create Grid") as t:
        t.Start()
        line = Line.CreateBound(columnLocationXYZ,xyzDestination)
        Grid.Create(document,line)
        t.Commit()

def moveGrid(document,distance,grid):
    with Transaction(document,"Move Grid") as t:
        t.Start()
        grid.Location.Move(-distance)
        t.Commit()

def moveColumn(document,distance,column):
    with Transaction(document,"Move Grid") as t:
        t.Start()
        column.Location.Move(distance)
        t.Commit()
            
            
#Method for searching through grids, find the appropriate grids and then check the distance between the center of the column and the gridline
def checkAssociatedGrids(column,columnGrids,allGrids):
    print(columnGrids)
    foundGridX = False
    foundGridY = False
    columnLocationXYZ = column.Location.Point
    columnX,columnY,columnZ = parseXYZ(columnLocationXYZ)
    for grid in allGrids:
        gridName = grid.Name
        print("Grid Name")
        print(gridName)
        if gridName in columnGrids:
            gridX,gridY,gridZ = parseXYZ(grid.Curve.Origin)
            distance = grid.Curve.Distance(columnLocationXYZ)
            print("Distance")
            print(distance)
            directionString = grid.Curve.Direction.ToString()
            directionString = directionString.split(",")
            # print("Direction String")
            # print(directionString)
            # print(directionString[1][1])
            # print(directionString[1][2])
            if directionString[0][2] == "1" or directionString[0][1] == "1":
                print("Found X Grid")
                foundGridX = True
                moveDistance = gridY-columnY
                xyz = XYZ(0,moveDistance,0)
            elif directionString[1][2] =="1" or directionString[1][1]=="1":
                print("Found Y Grid")
                foundGridY = True
                moveDistance = gridX-columnX
                xyz = XYZ(moveDistance,0,0)
            if distance>.0001:
                if SELECTEDMOVE == "Grids":
                    print("Moving Grid")
                    #If the distance to the grid exceeds the limit, move the grid by that distance so it is on the centerpoint of the column
                    moveGrid(doc,xyz,grid)
                elif SELECTEDMOVE == "Columns":
                    print("Moving Columns")
                    moveColumn(doc,xyz,column)
    if foundGridX == False:
        print("Creating X Grid")
        x,y,z = parseXYZ(columnLocationXYZ)
        xyzDestination = XYZ(x+10,y,z)
        duplicate = checkDuplicateGrids(y, "X")
        if duplicate == False:
            createGrid(doc,columnLocationXYZ,xyzDestination)
    if foundGridY == False:
        print("Creating Y Grid")
        x,y,z = parseXYZ(columnLocationXYZ)
        xyzDestination = XYZ(x,y+10,z)
        duplicate = checkDuplicateGrids(x, "Y")
        if duplicate == False:
            createGrid(doc,columnLocationXYZ,xyzDestination)
                   

listItems = ["Grids", "Columns"]
SELECTEDMOVE = forms.SelectFromList.show(listItems,button_name = "Select Item To Move")
print("Selected")
print(SELECTEDMOVE)


#Grab Selected Element Ids
selectedIds = uiDoc.Selection.GetElementIds()

#Convert Id List Into A List Of ELements

selectedColumns = []

#If the selected Element is a column, we'll add it to the list, otherwise discard it
for Id in selectedIds:
    element = doc.GetElement(Id)
    if element.Category.Name == "Structural Columns":
        selectedColumns.append(element)
        
#Process Grids Associated With Column Line 

#Get all grids in the model
allGrids = FilteredElementCollector(doc).OfClass(Grid).ToElements()



#Need To Deal With Errors Here if there is No Mark or the Mark is not Valid (It references a distance to the nearest grid)
for column in selectedColumns:
    columnGrids = column.get_Parameter(BuiltInParameter.COLUMN_LOCATION_MARK).AsString()
    columnGrids = columnGrids.split("-")
    i = 0
    while i<len(columnGrids):
        if "(" in columnGrids[i] or ")" in columnGrids[i]:
            columnGrids.remove(columnGrids[i])
        else:
            i+=1
    #Separate Grid String into 2 Grid Names and then store in a dictionary with the object as a key and a list of the grids corresponding to it
    #If the grid names is longer that 2, that means that the column isn't centered on two grids, so we should create one in the other direction
    checkAssociatedGrids(column,columnGrids,allGrids)