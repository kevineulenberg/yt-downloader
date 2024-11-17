# YouTube Downloader for macOS

A sleek, user-friendly macOS application to download YouTube videos and audio with a clean, minimal interface based on PyQt6 and yt-dlp. yt-dl is a feature-rich command-line audio/video downloader that is integrated into this app: it provides a simple and easy-to-use interface for downloading YouTube videos and audio in MP4 and MP3 formats.

## Features

- Download YouTube videos in high quality MP4 format
- Extract audio as MP3
- Clean, minimal user interface
- Progress bar for download status
- Automatic downloads folder creation
- High-quality video and audio selection
- Native macOS application

## Installation

### Prerequisites

1. **Install Homebrew** (if not already installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Required Dependencies**
   ```bash
   brew install yt-dlp ffmpeg
   ```

### Application Installation

1. Download `YouTube Downloader.app` from the releases page
2. Move the app to your Applications folder
3. Double-click to launch!

Note: On first launch, macOS might show a security warning. To fix this:
1. Go to System Settings → Privacy & Security
2. Scroll down to the message about "YouTube Downloader"
3. Click "Open Anyway"

## Usage

1. Launch the application
2. Paste a YouTube URL into the text field
3. Select your preferred format (MP4 video or MP3 audio)
4. Click "Download"
5. Files will be saved to `~/Downloads/YouTube Downloader/`

## Building from Source

If you want to build the application yourself:

1. Clone the repository
   ```bash
   git clone [your-repo-url]
   cd mac-app
   ```

2. Create a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Install PyInstaller
   ```bash
   pip install pyinstaller
   ```

5. Build the application
   ```bash
   pyinstaller --onefile --windowed --name "YouTube Downloader" youtube_downloader.py
   ```

The built application will be in the `dist` folder.

## System Requirements

- macOS 10.15 or later
- Internet connection
- Homebrew (for installing dependencies)

## Troubleshooting

1. **No sound in downloaded videos**
   - Make sure ffmpeg is installed: `brew install ffmpeg`
   - Try reinstalling yt-dlp: `brew reinstall yt-dlp`

2. **Download fails**
   - Check your internet connection
   - Verify that yt-dlp is installed: `which yt-dlp`
   - Update yt-dlp: `brew upgrade yt-dlp`

3. **App won't open**
   - Ensure all dependencies are installed
   - Check system security settings
   - Try reinstalling the application

## Updates

yt-dlp is regularly updated to handle YouTube changes. To update:
```bash
brew update && brew upgrade yt-dlp
```

## Credits

- Built with Python and PyQt6
- Uses yt-dlp for downloads
- FFmpeg for media processing
