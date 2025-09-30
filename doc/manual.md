# WeChat History Viewer - User Manual

This is a Windows desktop application for viewing WeChat chat history locally.

## 1. Environment Preparation

Before running this program, please ensure that you have a Python environment installed on your computer (Python 3.8 or higher is recommended).

1.  **Clone or Download the Project**
    Download all project files to any location on your computer.

2.  **Install Dependencies**
    Open a command-line tool (CMD or PowerShell), navigate to the project's root directory, and run the following command to install all necessary third-party libraries:
    ```bash
    pip install -r requirements.txt
    ```
    This command will automatically install `pywxdump`, `PyQt5`, and `requests`.

## 2. How to Run the Program

1.  **Log in to WeChat on PC**
    Please ensure that the WeChat account you want to view is currently logged into your Windows PC.

2.  **Start the Program**
    In the project's root directory, run the `main.py` file from the command line:
    ```bash
    python main.py
    ```

3.  **Using the Application**
    a. The main window will be displayed after the program starts.
    b. Click the **"1. Click to select WeChat folder"** button.
    c. In the dialog that opens, find and select your WeChat file storage directory. Typically, this directory is located at `C:\Users\YourUsername\Documents\WeChat Files`.
    d. After selecting the folder, the program will automatically load all WeChat accounts that have been logged into on that computer and display them in a list.
    e. Double-click the account you want to view to enter the chat history interface.
    f. In the chat interface, the left side is the contact list (with search support), and the right side is the chat history with that contact.

## 3. How to Package as an .exe File

If you want to run this program on a computer without a Python environment, you can package it into a single `.exe` file. We recommend using the `PyInstaller` tool.

1.  **Install PyInstaller**
    Run the following command in the command line:
    ```bash
    pip install pyinstaller
    ```

2.  **Execute the Packaging Command**
    In the project's root directory, run the following command to package the application:
    ```bash
    pyinstaller --onefile --windowed --name WeChatHistoryViewer main.py
    ```

    *   `--onefile`: Packages everything into a single `.exe` file.
    *   `--windowed`: Prevents a black command-line window from appearing when the program runs.
    *   `--name WeChatHistoryViewer`: Specifies the name of the generated executable file.
    *   `main.py`: Specifies the program's entry point file.

3.  **Find the .exe File**
    The packaging process may take a few minutes. When it's complete, `PyInstaller` will create a `dist` folder in the project's root directory. You can find the generated `WeChatHistoryViewer.exe` file inside the `dist` folder.

    You can copy this `.exe` file to any Windows computer and run it directly without installing any dependencies.

---
**Important Note**: The `pywxdump` library works by reading the WeChat process memory to obtain the decryption key. Some antivirus software may issue a warning about this behavior. This is normal; please allow the program to run. This project's code is fully open-source and contains no malicious behavior.