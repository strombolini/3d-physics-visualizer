1. Install Python
2. Install the dependencies by running this in cmd.exe:

`python pip install requests json pyglet openai`

3. Download physics-visualizer.py from the main github page
4. If you are not running Windows, replace this line of Windows code in physics-visualizer.py with your corresponding platform's line of code.

`##Windows:`
`os.startfile(glb_file_path)`

`##MacOS:`
`os.system("open " + glb_file_path)`

`##Linux:`
`os.system("xdg-open " + glb_file_path)`

5. Cd into the downloaded directory and run the code with 

`python physics-visualizer.py`

6. Enter the physics problem and wait a long time. It will render and display on your computer, no action on your part is required. Just make sure you have an internet connection.
