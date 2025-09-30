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
    Please ensure that the WeChat account you want to view is **currently running and logged in** on your Windows PC. This is a critical step as the program needs to read information from the running WeChat process.

2.  **Start the Program**
    In the project's root directory, right-click and choose "Run as administrator" if possible, then run the `main.py` file from the command line:
    ```bash
    python main.py
    ```

3.  **Using the Application**
    a. The main window will be displayed after the program starts.
    b. Click the **"1. 点击加载已登录的微信用户"** button.
    c. The program will attempt to automatically find all logged-in WeChat accounts and display them in the list.
    d. Double-click the account you want to view to enter the chat history interface.
    e. In the chat interface, the left side is the contact list (with search support), and the right side is the chat history with that contact.

## 3. How to Package as an .exe File

If you want to run this program on a computer without a Python environment, you can package it into a single `.exe` file. We recommend using the `PyInstaller` tool.

1.  **Install PyInstaller**
    In the command line, run: `pip install pyinstaller`

2.  **Execute the Packaging Command**
    In the project's root directory, run the following command:
    ```bash
    pyinstaller --onefile --windowed --name WeChatHistoryViewer main.py
    ```
    This will create a `WeChatHistoryViewer.exe` file inside a new `dist` folder.

## 4. Troubleshooting / Common Issues

You may encounter някои error messages. Here is how to interpret and solve them:

*   **Error: "未找到任何登录的微信用户" (No logged-in WeChat user found)**
    *   **Cause**: The program could not detect a running WeChat process.
    *   **Solution**: Make sure your WeChat desktop client is running and you are logged in *before* you click the "加载用户" button.

*   **Error: "获取用户信息时发生未知错误" (Unknown error while getting user info)**
    *   **Cause**: This is a general error that can have several causes.
    *   **Solutions**:
        1.  **Run as Administrator**: The most common solution. The program needs high-level permissions to read memory from another process. Close the application, then right-click your command prompt or the `.exe` file and select "Run as administrator".
        2.  **WeChat/pywxdump Version Incompatibility**: The `pywxdump` library may not support the very latest version of WeChat. If running as admin doesn't work, this might be the issue. You can check the official `pywxdump` GitHub page for information on supported versions.
        3.  **Antivirus Software**: Your antivirus might be blocking the program from accessing WeChat's memory.

*   **Error: "核心库 'pywxdump' 未安装" (Core library 'pywxdump' not installed)**
    *   **Cause**: The main dependency is missing.
    *   **Solution**: Run `pip install -r requirements.txt` in the project's root directory.

*   **Antivirus Warnings**
    *   **Cause**: The `pywxdump` library works by reading the WeChat process memory to obtain the decryption key. This behavior is similar to how some malware operates, so security software may flag it as suspicious.
    *   **Solution**: This is expected behavior for this type of tool. Please "allow" or "trust" the program in your antivirus software. The code for this project is fully visible and does not contain any malicious behavior.

---
If you continue to experience issues, please ensure you have the latest version of this program and the libraries mentioned in `requirements.txt`.