# Import Libraries
from pyrevit import forms
from Autodesk.Revit.DB import Transaction, ModelPathUtils
from Autodesk.Revit.ApplicationServices import Application
from Autodesk.Revit.DB import FilteredElementCollector, Grid, BuiltInParameter,XYZ,Line
import os.path
# Get Revit Document
doc = __revit__.ActiveUIDocument.Document
uiDoc = __revit__.ActiveUIDocument

def adjustPath(path):
    split = path.split("\\")
    split = split[0:-1]
    #print(split)
    newPath = "\\".join(split)
    return newPath
            
def getCentralPath(doc):
    if doc.IsWorkshared:
        modelPath = doc.GetWorksharingCentralModelPath()
        centralPath = ModelPathUtils.ConvertModelPathToUserVisiblePath(modelPath)
    else: 
        centralPath = doc.PathName
    return centralPath

def writeToDoList(path,task):
    filePath = path + "\\ToDoList.txt"
    toDoList = open (filePath,"a")
    toDoList.write(task)
    toDoList.write("\n")
    toDoList.close()
    #userName = doc.userName
    #print(userName)

def readToDoList(path):
    filePath = path + "\\ToDoList.txt"
    validity = os.path.isfile(filePath)
    if validity :
        toDoList = open(filePath,"r")
        tasks = toDoList.readlines()
    else:
        toDoList = open (filePath,"a")
        toDoList.close()
        tasks = []
    
    return tasks

def removeTask(path,selectedTasks):
    filePath = path + "\\ToDoList.txt"
    with open(filePath,"r") as file:
        lines = file.readlines()
    with open(filePath,"w") as file:
        for line in lines:
            match = False
            #print("Line: ")
            #print(line)
            for task in selectedTasks:
                #print("Task: ")
                #print(task)
                if line == task:
                    match = True
            if match == False:
                file.write(line)

def launchApp(doc):

    #Figure out a way to get active user
    
    currentUser = os.path.expanduser('~')
    #print(currentUser)
    centralPath = getCentralPath(doc)

    path = adjustPath(centralPath)

    options = ["Add Task", "View Tasks"]
    command = forms.CommandSwitchWindow.show(options, message = "Select Option")
    #print(command)

    if command == "Add Task":
        taskAdd = forms.ask_for_string(prompt = "Task To Be Added", title = "Add Task")
        if taskAdd is not None:
            writeToDoList(path,taskAdd)
        ##Test Added
        launchApp(doc)
        ##
    elif command == "View Tasks":
        tasks = readToDoList(path)
        selectedTask = forms.SelectFromList.show(tasks,button_name = "Select Task To Mark As Completed",multiselect = True, title = "Project Task List")
        #print(selectedTask)
        if selectedTask != None:
            removeTask(path,selectedTask)
            ##Test Added
            tasks = readToDoList(path)
            selectedTask = forms.SelectFromList.show(tasks,button_name = "Select Task To Mark As Completed",multiselect = True)
            ##

launchApp(doc)

#jsloan@m2structural.com








