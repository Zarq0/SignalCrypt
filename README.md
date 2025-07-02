# SignalCrypt
- SignalCrypt is a tool used for encrypting Signal Desktop user data into a singular encrypted file that you can backup.
- It is currently only usable on Windows computers.

# Usage
-  You'll need 7zip to use this tool, you can download it at https://www.7-zip.org/
-  After that, you'll need to add the location 7zip is downloaded to your PATH.
- Once you're done, you can proceed with those steps:

1. Download the latest stable release from https://github.com/Zarq0/SignalCrypt/releases/
2. Run the latest stable release
3. Follow the instructions on the screen

# Building from source
If you'd rather build SignalCrypt from source, you'll need:
- Python >= 3.12.3 (Downloads can be found at https://www.python.org/downloads/)
- Git (Downloads can be found at https://git-scm.com/downloads)

Once you have them downloaded, make sure to check they are correctly added to your PATH by running;
- `git --version`
- `python --version`

Once you verify they are downloaded, you can procceed to the building process:

1. Clone the repository using `git clone https://github.com/Zarq0/SignalCrypt.git`
2. Move into the cloned repository, after which download the required Python libraries using `pip install -r requirements.txt`
3. After you're done installing required Python libraries, run `pyinstaller --onefile --name SignalCrypt main.py`
4. Navigate to the created `dist` folder once the building process is done for the built executable file.
