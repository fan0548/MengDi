# WeChat History Viewer - User Manual

This is a Windows desktop application for viewing WeChat chat history locally. This guide explains the new dual-mode loading system for a better user experience.

## 1. Environment Preparation

Before running this program, please ensure that you have a Python environment installed on your computer (Python 3.8 or higher is recommended).

1.  **Clone or Download the Project**
    Download all project files to any location on your computer.

2.  **Install Dependencies**
    Open a command-line tool (CMD or PowerShell), navigate to the project's root directory, and run the following command:
    ```bash
    pip install -r requirements.txt
    ```

## 2. How to Run and Use the Program

The program now offers two ways to load user data: **Automatic Online Loading** and **Manual Path Selection**.

### Method 1: Automatic Online Loading (Recommended)

This is the easiest way to view the chat history of a currently logged-in account.

1.  **Log in to WeChat on PC**: Ensure the WeChat account you want to view is **running and logged in**.
2.  **Start the Application**: Run `python main.py` from the project's root directory (preferably with administrator rights).
3.  **Click "自动加载在线用户" (Auto-load Online Users)**: The program will try to detect all logged-in accounts.
    *   **On Success**: A list of online users will appear (e.g., "在线用户: John Doe"). Double-click a user to open their chat history.
    *   **On Failure**: An error message will appear (see Troubleshooting section). The "手动选择路径" (Manual Path Selection) button will now become active, allowing you to proceed to Method 2.

### Method 2: Manual Path Selection (Fallback)

Use this method if auto-loading fails or if you want to view the history of an account that is not currently logged in.

1.  **Activate the Button**: This button is only active after the automatic loading has failed.
2.  **Click "手动选择路径" (Manual Path Selection)**: An "open folder" dialog will appear.
3.  **Select "WeChat Files" Folder**: Navigate to and select your `WeChat Files` folder. Its typical location is `C:\Users\YourUsername\Documents\WeChat Files`.
4.  **View Historical Users**: The program will list all user accounts that have ever been used on this computer (e.g., "历史用户: wxid_12345...").
5.  **Double-click a User to Decrypt**:
    *   A pop-up will appear, asking you to **log in to the corresponding WeChat account** (the one matching the `wxid_...` you just clicked). This step is necessary to get the decryption key from the live process.
    *   After you have logged in, click the **"我已登录" (I have logged in)** button.
    *   The program will then re-scan the online users, find the key for the account you logged into, and open the chat history.

## 3. How to Package as an .exe File

1.  **Install PyInstaller**: `pip install pyinstaller`
2.  **Execute Packaging Command**: In the project's root directory, run:
    ```bash
    pyinstaller --onefile --windowed --name WeChatHistoryViewer main.py
    ```
    This will create a `WeChatHistoryViewer.exe` file inside a new `dist` folder.

## 4. Troubleshooting / Common Issues

*   **Error on "自动加载在线用户"**:
    *   **Cause**: The program could not detect a running WeChat process or lacked permissions.
    *   **Solutions**:
        1.  **Run as Administrator**: This is the most common fix.
        2.  **Ensure WeChat is Logged In**: Double-check that WeChat is running.
        3.  **Antivirus/Version Issues**: Your antivirus might be blocking the program, or your WeChat version might be too new for the `pywxdump` library.

*   **Manual Mode: "无法在当前登录的账号中找到 ... 的密钥" (Could not find the key in the currently logged-in account)**
    *   **Cause**: You double-clicked a historical user (`wxid_...`) but then logged into a *different* WeChat account.
    *   **Solution**: Make sure you log into the exact account that corresponds to the `wxid_...` you are trying to view. The program needs to match them to get the correct key.