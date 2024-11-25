## OFIQ GUI Project Overview and Instructions

### Purpose of This GUI
The OFIQ GUI is a graphical interface created to simplify the use of the [OFIQ](https://github.com/BSI-OFIQ/OFIQ-Project) (Objective Facial Image Quality) assessment tool. OFIQ is a specialized software for assessing the quality of facial image properties and identifying potential defects. By integrating a user-friendly GUI, this project enables users to upload facial images, select desired attributes for analysis, and view/download results conveniently without the need for command-line operations.

### Requirements
- Python 3.8+
- Flask
- Compiled OFIQ Library

### Instructions for Setup and Use

#### Step 1: Clone the OFIQ Project
To use this GUI, you first need to build the OFIQ Project:
1. Visit the official [OFIQ Github repository](https://github.com/BSI-OFIQ/OFIQ-Project).
2. Follow the installation instructions provided there to build the OFIQ project on your machine.
3. After building the project, ensure the `OFIQ-Project-main` directory is ready.

#### Step 2: Clone This GUI Repo
1. Open a terminal and run:
   ```bash
   git clone https://github.com/7eina/OFIQ-Project-Local-GUI.git
   cd OFIQ-Project-Local-GUI

2. Place the OFIQ-Project-main directory inside the OFIQ_GUI_Project folder so that the structure looks like this:
   ```
    OFIQ_GUI_Project/
    ├── OFIQ-Project-main/
    ├── templates/
    ├── uploads/
    ├── ofiq_gui.py
    ├── requirements.txt
    └── ...
#### Step 3: Set Up the Virtual Environment
1. Create a virtual environment:
    ```
    python -m venv venv
2. Activate the virtual environment:
- On Windows
```

    venv\Scripts\activate
```
- On macOS/Linux
```

    source venv/bin/activate
```
1. Install the required dependencies:
```

    pip install -r requirements.txt
```
#### Step 4: Run the GUI App
1. Start the application:
```

    python ofiq_gui.py
```
2. Open your browser and go to:
```

    http://127.0.0.1:5000
```
#### Step 5: Build the Standalone Executable (Optional)
If you wantto distribute the GUI as a standalone executable:
1. Ensure you have `PyInstaller` installed:

```
    pip install pyinstaller
```
2. Run the following command to create the executable:

```
    pyinstaller --onefile --add-data "templates;templates" ofiq_gui.py
```
3. The executable will be located in the `dist/` folder. Distribute the executable along with instructions for users to place the `OFIQ-Project-main` directory in the same folder.
