import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QLineEdit, QPushButton, QLabel, QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

class DownloadThread(QThread):
    progress = pyqtSignal(float)
    finished = pyqtSignal(bool, str)
    error = pyqtSignal(str)
    
    def __init__(self, url, download_type):
        super().__init__()
        self.url = url
        self.download_type = download_type
        
    def run(self):
        try:
            # Create downloads directory in user's home directory
            home_dir = os.path.expanduser('~')
            download_dir = os.path.join(home_dir, 'Downloads', 'YouTube Downloader')
            os.makedirs(download_dir, exist_ok=True)
            
            # Base command
            cmd = ['/usr/local/bin/yt-dlp']
            
            # Add format and output template
            if self.download_type == 'mp3':
                cmd.extend([
                    '-x',  # Extract audio
                    '--audio-format', 'mp3',  # Convert to MP3
                    '--audio-quality', '0',  # Best quality
                ])
            else:
                cmd.extend([
                    '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',  # Best quality MP4 video + M4A audio
                    '--merge-output-format', 'mp4',  # Ensure output is merged as MP4
                    '--format-sort', 'res,fps,codec:h264,size,br,asr',  # Sort by resolution, then fps, etc.
                    '--prefer-free-formats',  # Prefer formats with free codecs
                    '--postprocessor-args', '-c:v copy -c:a aac',  # Use FFmpeg to copy video and convert audio to AAC
                ])
            
            # Add common options
            cmd.extend([
                '-o', os.path.join(download_dir, '%(title)s.%(ext)s'),  # Output template
                '--newline',  # Force progress on newline
                '--progress',  # Show progress bar
                '--no-part',  # Do not use .part files
                '--force-overwrite',  # Overwrite if file exists
                '--verbose',  # Show verbose output for debugging
                '--merge-output-format', 'mp4',  # Force MP4 as final format
                '--ffmpeg-location', '/usr/local/bin/ffmpeg',  # Specify FFmpeg location
                self.url
            ])

            # Print the command for debugging
            print(f"Running command: {' '.join(cmd)}")
            
            # Create process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Process output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(f"Output: {output.strip()}")
                    if '[download]' in output:
                        try:
                            progress = int(output.split('%')[0].split()[-1])
                            self.progress.emit(progress)
                        except (ValueError, IndexError):
                            pass
            
            # Get the final output and error
            stdout, stderr = process.communicate()
            
            # Print any remaining output
            if stdout:
                print(f"Final stdout: {stdout}")
            if stderr:
                print(f"Final stderr: {stderr}")
            
            # Check if the process was successful
            if process.returncode != 0:
                raise Exception(f"Download failed with error code {process.returncode}: {stderr}")
            
            # Verify the file exists
            expected_files = os.listdir(download_dir)
            print(f"Files in download directory: {expected_files}")
            
            self.finished.emit(True, "Download completed successfully!")
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            self.finished.emit(False, str(e))

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setFixedSize(500, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel('YouTube Downloader')
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Paste YouTube URL here')
        self.url_input.setMinimumHeight(40)
        self.url_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(self.url_input)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Download buttons
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2472a4;
            }
        """
        
        self.mp3_button = QPushButton('Download MP3')
        self.mp3_button.setStyleSheet(button_style)
        layout.addWidget(self.mp3_button)
        
        self.mp4_button = QPushButton('Download MP4')
        self.mp4_button.setStyleSheet(button_style)
        layout.addWidget(self.mp4_button)
        
        # Connect buttons
        self.mp3_button.clicked.connect(lambda: self.download('mp3'))
        self.mp4_button.clicked.connect(lambda: self.download('mp4'))
        
        # Center window
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def download(self, format_type):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, 'Error', 'Please enter a YouTube URL')
            return
            
        # Disable UI elements
        self.url_input.setEnabled(False)
        self.mp3_button.setEnabled(False)
        self.mp4_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        
        # Start download thread
        self.thread = DownloadThread(url, format_type)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()
        
    def update_progress(self, percentage):
        self.progress_bar.setValue(int(percentage))
        
    def download_finished(self, success, message):
        # Re-enable UI elements
        self.url_input.setEnabled(True)
        self.mp3_button.setEnabled(True)
        self.mp4_button.setEnabled(True)
        self.progress_bar.hide()
        
        if success:
            QMessageBox.information(self, 'Success', message)
            self.url_input.clear()
        else:
            QMessageBox.warning(self, 'Error', message)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
