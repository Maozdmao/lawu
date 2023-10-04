
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QProgressBar
from PyQt6.QtCore import QUrl, QThread, pyqtSignal
import sys
import os
import subprocess
import time
import re

class DownloadThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file

    def run(self):
       while True:
           if os.path.exists(self.log_file):
               with open(self.log_file, 'r') as f:
                   lines = f.readlines()
                   if lines:
                       last_line = lines[-1]
                       progress = self.parse_progress(last_line)
                       if progress is not None:
                           self.progress.emit(progress)
           time.sleep(1)

    def parse_progress(self, line):
        m = re.search(r'(\d+)%\s', line)
        if m:
            return int(m.group(1))
        return None

class Downloader(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.url_entry = QLineEdit(self)
        self.download_button = QPushButton('下载', self)
        self.download_button.clicked.connect(self.download)
        self.progress_bar = QProgressBar(self)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('输入下载链接：'))
        vbox.addWidget(self.url_entry)
        vbox.addWidget(self.download_button)
        vbox.addWidget(self.progress_bar)

        self.setLayout(vbox)
        self.setWindowTitle('下载器')

    def download(self):
        url = self.url_entry.text()
        #download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        download_dir = os.path.join( 'Users/zhendongmao/Downloads')
        log_file = os.path.join(download_dir, 'wget.log')
        command = ['wget', '-P', download_dir, '-o', log_file, url]
        QMessageBox.information(self, "下载路径", f"文件将被下载到：{download_dir}")
        try:
            subprocess.Popen(command)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "下载错误", str(e))

        self.thread = DownloadThread(log_file) # type: ignore
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.start()

def main():
    app = QApplication(sys.argv)

    downloader = Downloader()
    downloader.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()


#https://macyy.oss-cn-beijing.aliyuncs.com/AutoCAD%202024%20Crack_MacApp.dmg
#wget -P