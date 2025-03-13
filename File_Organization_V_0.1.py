#########################################################################################################################################################################################################################################################################################
# Jim Clothier
# https://www.github.com/Jim-Clothier2
# https://www.linkedin.com/in/jimclothier97
# Jim.Clothier.97@gmail.com 
# 03/08/2025
# File Organization V 0.1
# Python 3.9
# This program will organize files in a directory by file type. It will create a new directory for each file type and move the files to the appropriate directory.
#########################################################################################################################################################################################################################################################################################

#Importing the necessary libraries
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime 
import json

#Current time to pass to other functions
currentTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

#Dictionary to map file extensions to their respective directories for other modules to use
fileExtensions = {

    # Microsoft Office files
    "doc": "Word",
    "docx": "Word",
    "xls": "Excel",
    "xlsx": "Excel",
    "ppt": "PowerPoint",
    "pptx": "PowerPoint",

    # LibreOffice files
    "odt": "Writer",
    "ods": "Calc",
    "odp": "Impress",

    # Adobe Files (including additional commonly found extensions)
    "ai": "Illustrator",
    "psd": "Photoshop",
    "aep": "After Effects",
    "indd": "InDesign",
    "indt": "InDesign",
    "idml": "InDesign",
    "eps": "EPS",
    "prproj": "Premiere Pro",

    # Documents and PDFs
    "pdf": "PDF",
    "txt": "Text",
    "rtf": "RTF",
    "docm": "Word Macro-Enabled",
    "dotx": "Word Template",
    "md": "Markdown",

    # Font files
    "ttf": "TrueType Font",
    "otf": "OpenType Font",
    "woff": "Web Open Font Format",
    "woff2": "Web Open Font Format 2",
    "eot": "Embedded OpenType",

    # Images
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "bmp": "BMP",
    "tiff": "TIFF",
    "svg": "SVG",

    # Videos (expanded)
    "mp4": "MP4",
    "avi": "AVI",
    "mkv": "MKV",
    "mov": "MOV",
    "wmv": "WMV",
    "flv": "FLV",
    "webm": "WebM",

    # Audio (expanded)
    "mp3": "MP3",
    "wav": "WAV",
    "aac": "AAC",
    "flac": "FLAC",
    "ogg": "OGG",
    "m4a": "M4A",
    "wma": "WMA",

    # 3D and modeling files
    "blend": "Blender",
    "obj": "OBJ",
    "fbx": "FBX",
    "stl": "STL",
    "dae": "COLLADA",

    # Compressed files
    "zip": "Zip",
    "rar": "RAR",
    "7z": "7-Zip",
    "tar": "Tar",
    "gz": "GZ",
    "bz2": "Bzip2",
    "xz": "XZ",

    # Code / script files
    "py": "Python",
    "js": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "java": "Java",
    "c": "C",
    "cpp": "C++",
    "cs": "C#",
    "rb": "Ruby",
    "php": "PHP",
    "go": "Go",
    "swift": "Swift",
    "ts": "TypeScript",

    # Backup and temporary files
    "bak": "Backup",
    "tmp": "Temporary",
    "old": "Old",
    "sav": "Save"
}

##########################################################################################################################################################################################################################################################################################

#Browse for the directory to organize
def browseFolder():

  try:
  #Opens file explorer dialog to select a folder. Once selected, the folder is visible within the widget
    folderPath = filedialog.askdirectory(title="Select a Folder to Organize")
    if folderPath:

        #Clears the current text in the entry widget
        folderEntry.delete(0, tk.END)
       
        #Inserts the selected folder path into the entry widget
        folderEntry.insert(0, folderPath)

  #Error handling for selecting a folder
  except Exception as e:
      messagebox.showerror("Error", f"Error selecting folder: {e}")

#########################################################################################################################################################################################################################################################################################

# Logs the current state of the target directory prior to making any changes.
def log_initialState(folderPath):

    # Allows for optional undo functionality
    # Create a Logs folder inside the target directory
   try:
    logsDir = os.path.join(folderPath, "Logs")
    if not os.path.exists(logsDir):
        os.makedirs(logsDir)

    # Use the global timestamp in the log file name
    logFile_initialState = f"logFile_initialState_{currentTime}.txt"
    logPath = os.path.join(logsDir, logFile_initialState)
    with open(logPath, 'w') as logFile:
        logFile.write(f"Initial State of {folderPath}:\n\n")

        # Recursively traverses folder
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                if file.startswith('logFile_initialState'):
                    continue
                fileFullPath = os.path.join(root, file)
                logFile.write(f"{fileFullPath}\n")

    # Output print statement
    print(f"Initial state of {folderPath} has been logged to {logPath}")

   #Error handling for logging initial state
   except (OSError, IOError) as e:
        messagebox.showerror("Log Error", f"Error logging initial state: {e}")

#########################################################################################################################################################################################################################################################################################

#Funciton to obtain most recent log file
def getMostRecentOperationLog(folderPath):

   try:
    # Create the Logs folder path
    logsDir = os.path.join(folderPath, "Logs")
    if not os.path.exists(logsDir):
        return None

    # Gathers Log Files
    logFiles = [f for f in os.listdir(logsDir) if f.startswith("operation_log_") and f.endswith(".json")]
    if not logFiles:
        return None

    logFiles.sort()  
    return os.path.join(logsDir, logFiles[-1])

   except Exception as e:
       messagebox.showerror("Error", f"Error retrieving log files: {e}")
       return None

#########################################################################################################################################################################################################################################################################################

#Function to organize files in the directory
def organizeFiles(folderPath):

  try:
    # Create a Logs folder inside the target directory
    logsDir = os.path.join(folderPath, "Logs")
    if not os.path.exists(logsDir):
        os.makedirs(logsDir)
    logFile_operationPath = os.path.join(logsDir, f"operation_log_{currentTime}.json")

    # Load existing operation log if it exists
    # Otherwise, the program starts a new one
    if os.path.exists(logFile_operationPath):
        with open(logFile_operationPath, "r") as logFile:
            opLog = json.load(logFile)
    else:
        opLog = {}

    # Process each item in the folder 
    for item in os.listdir(folderPath):
        itemPath = os.path.join(folderPath, item)
        if os.path.isfile(itemPath):

            # Extract the file extension 
            _, ext = os.path.splitext(item)
            ext = ext.lower()[1:]

            # Use the global fileExtensions dictionary to determine the target folder
            targetFolder = fileExtensions.get(ext, "Other Files")
            destinationDirectory = os.path.join(folderPath, targetFolder)
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            destinationFilePath = os.path.join(destinationDirectory, item)

            # Log the move:
            opLog[destinationFilePath] = itemPath

            # Move the file
            shutil.move(itemPath, destinationFilePath)
            print(f"Moved '{item}' to '{destinationDirectory}'")

    # Save the operation log to a JSON file
    with open(logFile_operationPath, "w") as logFile:
        json.dump(opLog, logFile, indent=4)

    # Output print statement
    print(f"Operation log saved to {logFile_operationPath}")

  #Error handling for file organization
  except (OSError, IOError) as e:
       messagebox.showerror("File Organization Error", f"Error during file organization: {e}")

  #Error handling for unexpected errors
  except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

#########################################################################################################################################################################################################################################################################################

#Undo Function
def undoChanges(folderPath):
   try: 
    #Confimation message for undo
    if not messagebox.askokcancel("Confirm Undo", "Do you want to undo the last operation?"):
        return

    # Retrieve the most recent operation log file
    logFile_operationPath = getMostRecentOperationLog(folderPath)
    if not logFile_operationPath or not os.path.exists(logFile_operationPath):
        messagebox.showerror("Undo Error", "No operation log found. Cannot undo changes.")
        print("No operation log found. Cannot undo changes.")
        return

    # Load the operation log
    with open(logFile_operationPath, "r") as logFile:
        opLog = json.load(logFile)

    # Process each logged move and move the file back to its original location
    for destinationFilePath, originalFilePath in opLog.items():

        if os.path.exists(destinationFilePath):

            originalDir = os.path.dirname(originalFilePath)
            if not os.path.exists(originalDir):
                os.makedirs(originalDir)
            shutil.move(destinationFilePath, originalFilePath)
            print(f"Moved '{destinationFilePath}' back to '{originalFilePath}'")

        else:
            print(f"File '{destinationFilePath}' not found; cannot undo its move.")

    # Remove the operation log file after undoing the changes
    os.remove(logFile_operationPath)
    print("Undo complete; operation log removed.")

    # Show a dialog box after undo is complete
    messagebox.showinfo("Undo Complete", "Undo complete; operation log removed.")

   #Error handling for undo
   except Exception as e:
        messagebox.showerror("Undo Error", f"An unexpected error occurred during undo: {e}")

   # After undoing changes, remove empty target folders (created by our program)
   targetFolders = set(fileExtensions.values())
   targetFolders.add("Other Files")

   for folderName in targetFolders:
        folderPathToCheck = os.path.join(folderPath, folderName)
        if os.path.exists(folderPathToCheck) and os.path.isdir(folderPathToCheck):
           
           # Check if the folder is empty
            if not os.listdir(folderPathToCheck):

                try:
                    os.rmdir(folderPathToCheck)
                    print(f"Removed empty folder: {folderPathToCheck}")

                except Exception as e:
                    messagebox.showerror("Folder Removal Error", f"Could not remove folder {folderPathToCheck}: {e}")

#########################################################################################################################################################################################################################################################################################

def main():
   try:
    # Retrieves the folder path from the entry widget
    folder = folderEntry.get()
    print(f"Selected folder: {folder}")

    if not folder:
        # Show an error dialog if no folder is selected and exit the function
        messagebox.showerror("No Folder Selected", "Please select a folder before clicking Organize.")

    #Confirmation message for file organization
    if not messagebox.askokcancel("Confirm Operation", "Do you want to proceed with file organization?"):
        return
     

    # Proceed if a folder is selected
    log_initialState(folder)
    organizeFiles(folder)

    # Show a dialog box after organization is complete
    messagebox.showinfo("Operation Complete", "File organization complete. You may now choose to undo changes or close the program.")

   #Error handling for main operation
   except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred in the main operation: {e}")

#Creates Main Window
root = tk.Tk()
root.title("File Organization")

#Creates an entry widget and a button widget
folderEntry = tk.Entry(root, width=50)
folderEntry.pack(side=tk.LEFT, padx=(10, 0), pady=10)
browseButton = tk.Button(root, text="...", command=browseFolder)
browseButton.pack(side=tk.LEFT, padx=(0, 10), pady=10)

#Add an "Organize" button that triggers main()
organizeButton = tk.Button(root, text="Organize", command=main)
organizeButton.pack(side=tk.LEFT, padx=(0, 10), pady=10)

#Add an "Undo" button that triggers undoChanges with the folder path from the entry widget
undoButton = tk.Button(root, text="Undo", command=lambda: undoChanges(folderEntry.get()))
undoButton.pack(side=tk.LEFT, padx=(0, 10), pady=10)
root.mainloop()

#########################################################################################################################################################################################################################################################################################
