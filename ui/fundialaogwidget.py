from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QSplashScreen, QTextBrowser, QDialog, QWidget, QLabel, QSizePolicy, QPushButton, QVBoxLayout


class FunDialogPlayer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("QMovie to show animated gif")

        # set up the movie screen on a label
        self.movie_screen = QLabel()
        # expand and center the label
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout)

        # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QMovie("giphy.gif", QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)

        self.movie.start()

    def start(self):
        """sart animnation"""
        self.show()
        self.movie.start()

    def stop(self):
        """stop the animation"""
        self.movie.stop()
        self.hide()

