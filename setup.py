from cx_Freeze import setup, Executable

# Define the base options for the setup
options = {
    "build_exe": {
        "include_files": ["NpasInSvcByLocRpt.csv", "help_utils.py", "areaCodes.py", "dedupe.py", "badnumdel.py", "my_google.py", "chars.py", "numberScraper.py"],
        "packages": ["os", "sys", "keyboard", "threading"],
        "includes": ["csv", "ctypes", "re", "pyperclip", "tkinter", "webbrowser", "requests"],
        "excludes": []
    }
}

# List of executables
executables = [
    Executable(
        r"C:\Users\Bryan Edman\Documents\NumberManipulator_GUI\NumberManipulator_GUI\NumberManipulatorGUI.py ", 
         # Replace with the name of your main script
        base=None,  # Set this to None if you don't want a console window
        #targetName="NumberManipulator.exe",  # Name of the generated executable
    )
]

# Setup the project
setup(
    name="Number Crusher",
    version="1.1",
    description="SDR Number Manipulator tool",
    options=options,
    executables=executables
)
