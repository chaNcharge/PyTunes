import sys
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.title = 'PyQt5 music player'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 150
        self.userAction = -1  # 0- stopped, 1- playing 2-paused
        self.initUI()

    def initUI(self):
        # Add file menu
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')

        fileAct = QAction('Open File', self)
        folderAct = QAction('Open Folder', self)

        fileAct.setShortcut('Ctrl+O')

        folderAct.setShortcut('Ctrl+D')

        filemenu.addAction(fileAct)
        filemenu.addAction(folderAct)

        fileAct.triggered.connect(self.openFile)
        folderAct.triggered.connect(self.addFiles)

        self.addControls()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def addControls(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # Add song controls
        volumeslider = QSlider(Qt.Horizontal, self)
        volumeslider.setFocusPolicy(Qt.NoFocus)
        volumeslider.valueChanged[int].connect(self.changeVolume)
        volumeslider.setValue(100)
        playBtn = QPushButton('Play')  # play button
        pauseBtn = QPushButton('Pause')  # pause button
        stopBtn = QPushButton('Stop')  # stop button
        # Add playlist controls
        prevBtn = QPushButton('Prev')
        shuffleBtn = QPushButton('Shuffle')
        nextBtn = QPushButton('Next')
        # Add button layouts
        controlArea = QVBoxLayout()  # centralWidget
        controls = QHBoxLayout()
        playlistCtrlLayout = QHBoxLayout()
        # Add buttons to song controls layout
        controls.addWidget(playBtn)
        controls.addWidget(pauseBtn)
        controls.addWidget(stopBtn)
        # Add buttons to playlist controls layout
        playlistCtrlLayout.addWidget(prevBtn)
        playlistCtrlLayout.addWidget(shuffleBtn)
        playlistCtrlLayout.addWidget(nextBtn)
        # Add to vertical layout
        controlArea.addWidget(volumeslider)
        controlArea.addLayout(controls)
        controlArea.addLayout(playlistCtrlLayout)
        wid.setLayout(controlArea)
        # Connect each signal to their appropriate function
        playBtn.clicked.connect(self.playhandler)
        pauseBtn.clicked.connect(self.pausehandler)
        stopBtn.clicked.connect(self.stophandler)

        prevBtn.clicked.connect(self.prevSong)
        shuffleBtn.clicked.connect(self.shufflelist)
        nextBtn.clicked.connect(self.nextSong)

        self.statusBar()
        self.playlist.currentMediaChanged.connect(self.songChanged)

    def openFile(self):
        print("File button clicked!")
        song = QFileDialog.getOpenFileName(self, "Open Song", "~", "Sound Files (*.mp3 *.ogg *.wav *.m4a)")
        print(song[0])

        if song[0] != '':
            url = QUrl.fromLocalFile(song[0])
            if self.playlist.mediaCount() == 0:
                self.playlist.addMedia(QMediaContent(url))
                self.player.setPlaylist(self.playlist)
                self.player.play()
                self.userAction = 1
                print(self.playlist.mediaCount())
            else:
                self.playlist.addMedia(QMediaContent(url))
                print(self.playlist.mediaCount())

    def addFiles(self):
        print("Folder button clicked!")
        if self.playlist.mediaCount() != 0:
            self.folderIterator()
            print(self.playlist.mediaCount())
        else:
            self.folderIterator()
            self.player.setPlaylist(self.playlist)
            self.player.playlist().setCurrentIndex(0)
            self.player.play()
            print(self.playlist.mediaCount())
            self.userAction = 1
    
    def folderIterator(self):
        folderChosen = QFileDialog.getExistingDirectory(self, 'Open Music Folder', '~')
        if folderChosen != None:
            it = QDirIterator(folderChosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    print(it.filePath(), fInfo.suffix())
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                        print('added file', fInfo.fileName())
                        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                fInfo = it.fileInfo()
                print(it.filePath(), fInfo.suffix())
                if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                    print('added file', fInfo.fileName())
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
    
    def playhandler(self):
        if self.playlist.mediaCount() == 0:
            self.openFile()
        elif self.playlist.mediaCount() != 0:
            self.player.play()
            print(self.playlist.mediaCount())
            self.userAction = 1

    def pausehandler(self):
        self.userAction = 2
        self.player.pause()

    def stophandler(self):
        self.userAction = 0
        self.player.stop()
        self.playlist.clear()
        print("Playlist cleared!")
        self.statusBar().showMessage("Stopped and cleared playlist")

    def changeVolume(self, value):
        self.player.setVolume(value)

    def prevSong(self):
        if self.playlist.mediaCount() == 0:
            self.openFile()
        elif self.playlist.mediaCount() != 0:
            self.player.playlist().previous()
    
    def shufflelist(self):
        self.playlist.shuffle()
        print("Shuffled playlist!")

    def nextSong(self):
        if self.playlist.mediaCount() == 0:
            self.openFile()
        elif self.playlist.mediaCount() != 0:
            self.player.playlist().next()
    
    def songChanged(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            self.statusBar().showMessage(url.fileName())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
