# TeleRipper
TeleRipper is an OSINT tool that allows investigators to download contents from any specified telegram channels

# Pre-Requisites 

1. Telegram account
2. Telegram API
(Refer to Appendix: Telegram API for instructions to get the Telegram API for your account)

# Installation
1. Clone the repository

``git clone https://github.com/RC-92/TeleRipper.git``

3. Navigate the cloned directory

``cd TeleRipper``

4. Run installation Script

``./setup.sh``

5. Activate Python Virtual Enviroment

``source venv/bin/activate``

# Usage
1. Initial run

``python3 teleripper.py``
_(On the first attempt of running the script you will be prompted to key in your account API key and API Hash, refer to Appendix: API Keys on the steps to retrieve them )_


3. Key in API ID: 


![image](https://github.com/user-attachments/assets/0f259233-8814-48be-9b69-93dfa8afe842)

4. Key in API Hash

![image](https://github.com/user-attachments/assets/498d0488-7bd3-4e95-981b-c400201fec2b)


5. Retrieve channel ID


![image](https://github.com/user-attachments/assets/a21a6fce-a0aa-4c80-b6cb-741c2684f51c)


6. Download from channel


``python3 TeleRipper-v3.py --d CHANNELID``


![image](https://github.com/user-attachments/assets/f1f3de8f-3779-4848-a557-29f62679accb)

7. Download to specified Directory

``python3 TeleRipper-v3.py --d CHANNELID -dir /path/to/dir``


7. Download specified type of media 

``python3 TeleRipper-v3.py --d CHANNELID -dir /path/to/dir -type TYPE``


## Currently available types
Videos
- mp4
- avi
- mkv
- mov
- wmv
- flv
- webm
- 3gp
- m4v

Image
- jpg
- jpeg
- png
- gif
- bmp
- webp
- svg
- tiff

Document
- pdf
- doc
- docx
- xls
- xlsx
- ppt
- pptx
- txt
- rtf
- odt

Audio
- mp3
- wav
- ogg
- flac
- m4a
- aac
- wma

Archive
- zip
- rar
- 7z
- tar
- gz
- bz2

Program
- exe
- apk
- iso

Data
- json
- xml
- csv
- sql
Web
- html
- css
- js

# Appendix: Get Account API credentials

1. Navigate to https://my.telegram.org
2. Select "API development account"


![image](https://github.com/user-attachments/assets/cad6fde8-04f4-4d0b-86de-b6005d6aec8c)


3. Key App Name and App short name, leave the rest as it is and hit save changes


![image](https://github.com/user-attachments/assets/e4631880-a14c-4258-be30-d4bd9a7762a5)
