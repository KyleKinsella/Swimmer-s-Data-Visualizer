#Name: Kyle Kinsella
#Student Number: C00273146


import os
import webbrowser
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Label, Select
import swim_utils
import hfpy_utils

class SwimmersApp(App[str]):

    # Function to generate dropdown options for swimmer selection
    def dropdownlist(self):
        # Path to the swimdata folder
        swimdata_folder_path = 'swimdata/'

        # Set to store unique names
        unique_names = set()

        # Loop through the files in the swimdata folder
        for filename in os.listdir(swimdata_folder_path):
            # Extract the name from the filename (assuming filename is the swimmer's name)
            swimmer_name = os.path.splitext(os.path.basename(filename))[0]

            # Extract the first part of the name (e.g., "Hannah" from "Hannah-13-100m-Free")
            first_name_part = swimmer_name.split('-')[0]

            # Add the first part of the name to the set (this will automatically remove duplicates)
            unique_names.add(first_name_part)

        # Create the dropdown options
        options = [(name, name) for name in unique_names]
        return options





    # Function to list all files for a selected swimmer
    def allSwimmersFiles(self, selected_swimmer):
        # Path to the swimdata folder
        swimdata_folder_path = 'swimdata/'

        # List to store filenames for the selected swimmer
        files_for_selected_swimmer = []

        # Loop through the files in the swimdata folder
        for filename in os.listdir(swimdata_folder_path):
            # Extract the name from the filename (assuming filename is the swimmer's name)
            swimmer_name = os.path.splitext(os.path.basename(filename))[0]

            # Extract the first part of the name (e.g., "Hannah" from "Hannah-13-100m-Free")
            first_name_part = swimmer_name.split('-')[0]

            # Check if this file is for the selected swimmer
            if first_name_part == selected_swimmer:
                # Append a tuple with (value, label) for each file
                files_for_selected_swimmer.append((filename, filename))

        return files_for_selected_swimmer
    
    
    

    def on_load(self):
        self.title = "Swimmer's Data"
        
        

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Click below to view all Swimmer's: ", id="Swimmer")

        # Generate options for the first Select
        options1 = self.dropdownlist()

        # Create the first Select widget
        select_widget1 = Select(
            options=options1,
            prompt="Select a swimmer",
            allow_blank=True,
            value=None,
            name=None,
            id=None,
            classes=None,
            disabled=False
        )

        yield select_widget1
        
        

        yield Label("Click below to go to Selected Swimmers Events: ", id="EventsLabel")

        self.s2 = Select([(None, None)])
        yield self.s2
        
        
        

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        filenamelist = []
        for file_name in os.listdir("swimdata/"):
            if file_name.endswith(".txt"):
                if event.value in file_name:
                    filenamelist.append((file_name, file_name))

        self.s2.set_options(filenamelist)

        # Call makeChart when the second Select is changed and a file is selected
        if self.s2.value:
            selected_file = self.s2.value
            # Modify this according to your data retrieval method
            data = swim_utils.get_swimmers_data(selected_file)
            self.makeChart(data)

            htmlurl = "Calvin.html"

            # Open URL in a new tab, if a browser window is already open.
            webbrowser.open_new_tab(htmlurl)
            
            
            

    def makeChart(self, data):
        # Function to create a chart based on swimmer data
        name, age, distance, stroke, times, values, average = data 

        title = f"Swimmer: {name}"

        body = f"Swimmer: {name} <br> Age: {age} <br> Distance: {distance} <br> Stroke: {stroke}"

        header = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>
                    {title}
                </title>
            </head>
            <body>
                <h3>{body}</h3>
        """
        print(header)

        footer = f""" 
        <h4>Average: {average}</h4>
            </body>
        </html>
        """

        print(footer)

        # Convert values to a suitable range for chart display
        converts = []
        for n in values:
            converts.append(hfpy_utils.convert2range(n, 0, max(values)+50, 0, 400))

        times.reverse()
        converts.reverse()

        body = ""
        for t, c in zip(times, converts):
            svg = f""" 
                        <svg height="30" width="400">
                                <rect height="30" width="{c}" style="fill:rgb( 51, 200, 255 );" />
                        </svg>{t}<br />
                    """
            body = body + svg

        print(body)

        html = header + body + footer

        print(html)

        # Write HTML to a file
        with open("Calvin.html", "w") as df:
            print(html, file=df) 
            
            
if __name__ == '__main__':
    app = SwimmersApp()
    app.run()
