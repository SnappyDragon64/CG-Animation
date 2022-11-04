from PyQt5 import QtCore, QtGui, QtWidgets
import animate
import sys


class MainWindow(QtWidgets.QMainWindow):
    x = 0

    def __init__(self):
        super().__init__()

        self.set_size(500, 375)
        self.setWindowTitle('Bresenham Line Generation Algorithm')
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))

        elements = {'X1': 100, 'Y1': 150, 'X2': 300, 'Y2': 350}
        self.le_list = []
        for val in elements:
            self.set_text(val, elements[val])
            self.le_list.append(self.set_le(elements[val]))

        label = QtWidgets.QLabel(self)
        label.setText('Co-ordinates must be between 0 and 20')
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.resize(400, 40)
        label.move(50, 140)

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

    def set_le(self, pos):
        le = QtWidgets.QLineEdit(self)
        le.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression('^([0-1]?[0-9]|20)$/'), self))
        le.resize(50, 40)
        le.move(pos, 100)
        le.setText('0')
        return le

    def on_click(self):
        animate.generate_animation((self.get_val(0), self.get_val(1)), (self.get_val(2), self.get_val(3)), 'out/anim'
                                                                                                           '.gif')

        self.set_size(1226, 920)

        widget = QtWidgets.QWidget(self)
        label = QtWidgets.QLabel(widget)
        self.setCentralWidget(widget)

        movie = QtGui.QMovie('out/anim.gif')
        label.setMovie(movie)
        movie.start()

    def get_val(self, index):
        return int(self.le_list[index].text())

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


if __name__ == '__main__':
    main()
