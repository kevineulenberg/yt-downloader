from setuptools import setup

APP = ['youtube_downloader.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'CFBundleName': 'YouTube Downloader',
        'CFBundleDisplayName': 'YouTube Downloader',
        'CFBundleGetInfoString': "Download YouTube videos",
        'CFBundleIdentifier': "com.youtubedownloader.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': u"Copyright 2024, Your Name, All Rights Reserved"
    },
    'packages': ['PyQt6'],
    'includes': ['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    'excludes': ['tkinter'],
    'strip': True
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
