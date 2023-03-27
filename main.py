from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QMessageBox,QWidget,QLineEdit,QLabel,QPushButton,QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from pytube import YouTube,Playlist
from os import getcwd
from os.path import join as joinPath
from requests import get
from time import sleep
import sys
from os import path
from threading import Thread

# url = https://content.videvo.net/videvo_files/video/free/2014-07/originalContent/Abstract_ball_lines.mp4
# video = https://www.youtube.com/watch?v=2bRRbD6pSeg
# Playlist = https://www.youtube.com/playlist?list=PLWPirh4EWFpGsim4cuJrh9w6-yfuC9XqI

class VideoDownloader(QWidget):
    def __init__(self):
        super(VideoDownloader,self).__init__()
        loadUi("videoDownloader.ui",self)
        self.setWindowTitle("Video Downloader | Python Projects")
        # self.setMinimumSize(1209,838)
        # self.setMaximumSize(1209,838)
        self.setWindowIcon(QIcon('logo.png'))
        self.allStrems = ["360p","480p","720p","1080p"]

        self.tabWidget = self.findChild(QTabWidget,"tabWidget")
        self.tabWidget_2 = self.findChild(QTabWidget,"tabWidget_2")
        self.tabWidget.tabBar().setVisible(False)

        self.videoStatusString = self.findChild(QLabel,"label_2")
        self.playlistStatusString = self.findChild(QLabel,"label_10")
        self.simpleVideoStatusString = self.findChild(QLabel,"label_13")

        self.videoTitle = self.findChild(QLabel,"label_4")
        self.playlistTitle = self.findChild(QLabel,"label_11")
        self.simpleVideoTitle = self.findChild(QLabel,"label_12")


        self.getVideoUrl = self.findChild(QLineEdit,"lineEdit")
        self.getPlaylistUrl = self.findChild(QLineEdit,"lineEdit_6")
        self.getSimpleVideoURL = self.findChild(QLineEdit,"lineEdit_3")

        self.getLocation = self.findChild(QLineEdit,"lineEdit_2")
        self.getPlaylistLocation = self.findChild(QLineEdit,"lineEdit_5")
        
        self.browseLocation = self.findChild(QPushButton,"pushButton")
        self.browsePlaylistLocation = self.findChild(QPushButton,"pushButton_10")        

        self.download = self.findChild(QPushButton,"pushButton_2")
        self.downloadPlaylist = self.findChild(QPushButton,"pushButton_11")
        self.downloadSimpleVideo = self.findChild(QPushButton,"pushButton_6")

        self.getVideoContent = self.findChild(QPushButton,"pushButton_3")
        self.getPlaylistContent = self.findChild(QPushButton,"pushButton_9")

        self.getYoutubeTab = self.findChild(QPushButton,"pushButton_4")
        self.getVideoTab = self.findChild(QPushButton,"pushButton_5")

        self.combo = self.findChild(QComboBox,"comboBox")
        self.combo_2 = self.findChild(QComboBox,"comboBox_2")
        
        self.browseLocation.clicked.connect(self.browse)
        self.browsePlaylistLocation.clicked.connect(self.browsePlaylist)

        self.download.clicked.connect(self.downloadYoutubeVideo)
        self.downloadPlaylist.clicked.connect(self.playlistDownloader)
        self.downloadSimpleVideo.clicked.connect(self.downloadSVideo)

        self.getVideoContent.clicked.connect(self.videoContent)
        self.getPlaylistContent.clicked.connect(self.playlistContent)
        self.getYoutubeTab.clicked.connect(self.youtubeTab)
        self.getVideoTab.clicked.connect(self.videotab)
        
        self.getLocation.setReadOnly(True)
        self.getPlaylistLocation.setReadOnly(True)

    def videotab(self):
        self.tabWidget.setCurrentIndex(1)

    def youtubeTab(self):
        self.tabWidget.setCurrentIndex(0)

    def downloadSVideo(self):
        if (self.getSimpleVideoURL.text() == ""):
            QMessageBox.warning(self,"Warning...","Please fill all required Fields")

        else:
            self.simpleVideoTitle.setText(str(self.getSimpleVideoURL.text()).split("/")[-1])
            r = get(str(self.getSimpleVideoURL.text()),stream=True)
            if r.status_code == 200:
                self.simpleVideoStatusString.setText("Video Downloading....")
                with open(str(self.simpleVideoTitle.text()),"wb") as f:
                    for data in r.iter_content(2048):
                        if data:
                            f.write(data)
                self.simpleVideoStatusString.setText(f"FIle saved at: {joinPath(getcwd(),self.simpleVideoTitle.text())}")
            else:
                QMessageBox.warning(self,"Warning","URL not Exists...\nPlease Enter Correct URL")

    def downloadVideo(self):
        try:
            if self.getVideoUrl.text() == "" or self.getLocation.text() == "":
                QMessageBox.warning(self,"Warning","Please Fill All Fields!")

            else:
                self.videoStatusString.setText("Dowloading Video....")
                sleep(1)
                self.video = self.youtube.streams.get_by_resolution(str(self.combo.currentText()))
                filePath, fileName = path.split(str(self.getLocation.text()))
                self.video.download(filePath,fileName)
                self.videoStatusString.setText("Video Location: {}".format(str(self.getLocation.text())))
        
        except Exception as e:
            QMessageBox.warning(self,"Error",str(e))
            

    def downloadYoutubeVideo(self):
        self.myThread = Thread(target=self.downloadVideo)
        self.myThread.start() 
            
    def videoContent(self):
        try:
            if str(self.getVideoUrl.text()) != "":
                sleep(1)
                self.getVideoUrl.setReadOnly(True)
                self.youtube = YouTube(str(self.getVideoUrl.text()))
                self.videoTitle.setText(f"Video Title: {str(self.youtube.title)}")
                self.combo.clear()
                for i in self.allStrems:
                    self.combo.addItem(str(i))
            
                
            else:
                QMessageBox.warning(self,"Warning","Please fill URL Field!")


        except Exception as e:
            QMessageBox.warning(self,"Error",str(e))


    def browse(self):
        if self.videoTitle.text() != "":
            self.getLocation.setText(str(QFileDialog.getSaveFileName(self,"Save Video File",f"{self.videoTitle.text()}.mp4","Video FIles (*.mp4)")[0]))
        
        else:
            self.getLocation.setText(str(QFileDialog.getSaveFileName(self,"Save Video File","untitled_video.mp4","Video FIles (*.mp4)")[0]))


    def browsePlaylist(self):
        self.getPlaylistLocation.setText(str(QFileDialog.getExistingDirectory(self,"Select Directory to Save Playlist")))


    def playlistDownloader(self):
        try:
            if (str(self.getPlaylistUrl.text())  != "") and (str(self.getPlaylistLocation.text()) != ""):
                for video in self.playlist.videos:
                    self.playlistStatusString.setText(f"Downloading: {video.title}")
                    video.streams.filter(file_extension="mp4").get_by_resolution(str(self.combo_2.currentText())).download(str(self.getPlaylistLocation.text()),f"{str(video.title)}.mp4")
                    
            else:
                QMessageBox.warning(self,"warning","Please fill all Fields!")
        
        except Exception as e:
            QMessageBox.warning(self,"Error",str(e))
            



    def playlistContent(self):
        try:
            if self.getPlaylistUrl.text() != "":
                self.playlist = Playlist(str(self.getPlaylistUrl.text()))
                self.playlistTitle.setText(f"Playlist Title: {str(self.playlist.title)}\nTotal Videos: {str(self.playlist.length)}")
                self.combo_2.clear()
                for quality in self.allStrems:
                    self.combo_2.addItem(str(quality))

        except Exception as e:
            QMessageBox.warning(self,"Error",str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoDownloader()
    window.show()
    sys.exit(app.exec())
