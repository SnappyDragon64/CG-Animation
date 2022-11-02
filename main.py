from PyQt5 import QtCore, QtGui, QtWidgets
import animate
import sys


def get_frame(size: tuple):
    return QtCore.QRect(0, 0, size[0], size[1])


class MainWindow(QtWidgets.QMainWindow):
    x = 0

    def __init__(self):
        super().__init__()

        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

        self.set_size(500, 375)
        self.setWindowTitle('Bresenham Line Generation Algorithm')
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))

        self.set_text("X1", 100)
        self.set_text("Y1", 150)
        self.set_text("X2", 300)
        self.set_text("Y2", 350)

        self.set_cb(self.on_change_x1, 100)
        self.set_cb(self.on_change_y1, 150)
        self.set_cb(self.on_change_x2, 300)
        self.set_cb(self.on_change_y2, 350)

        button = QtWidgets.QPushButton('Start', self)
        button.clicked.connect(self.on_click)
        button.resize(200, 100)
        button.move(150, 200)

    def set_text(self, text, pos):
        label = QtWidgets.QLabel(self)
        label.setText(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.resize(50, 40)
        label.move(pos, 60)

    def set_cb(self, on_change, pos):
        cb = QtWidgets.QComboBox(self)
        cb.addItems([str(i) for i in range(0, 21)])
        cb.currentIndexChanged.connect(on_change)
        cb.resize(50, 40)
        cb.move(pos, 100)

    def on_change_x1(self, i):
        self.x1 = i

    def on_change_x2(self, i):
        self.x2 = i

    def on_change_y1(self, i):
        self.y1 = i

    def on_change_y2(self, i):
        self.y2 = i

    def on_click(self):
        animate.generate_animation((self.x1, self.y1), (self.x2, self.y2), 'out/anim.gif')

        self.set_size(1226, 920)

        widget = QtWidgets.QWidget(self)
        label = QtWidgets.QLabel(widget)
        self.setCentralWidget(widget)

        movie = QtGui.QMovie('out/anim.gif')
        label.setMovie(movie)
        movie.start()

    def set_size(self, w, h):
        frame = QtCore.QRect(0, 0, w, h)
        size = QtCore.QSize(w, h)

        self.setMinimumSize(size)
        self.setMaximumSize(size)

        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
