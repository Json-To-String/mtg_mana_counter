import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.setStyleSheet('''
            QWidget {
                font-size: 28px;
                background-color: #23272f;
                color: #f5f6fa;
            }
            QLabel {
                font-weight: 500;
                padding: 6px 0;
            }
            QPushButton {
                background-color: #353b48;
                color: #f5f6fa;
                border: none;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 28px;
            }
            QPushButton:hover {
                background-color: #4078c0;
                color: #fff;
            }
            QPushButton:pressed {
                background-color: #273c75;
            }
        ''')

        self.color_counter_dict = {
            "White": 0,
            "Blue": 0,
            "Black": 0,
            "Red": 0,
            "Green": 0,
            "Colorless": 0
        }

        self.labels = {}

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        for color in self.color_counter_dict.keys():
            row = QHBoxLayout()

            color_label = QLabel(color)
            color_label.setFixedWidth(150)
            row.addWidget(color_label)

            dec_btn = QPushButton("➖")
            dec_btn.setFixedWidth(60)
            dec_btn.clicked.connect(lambda _, c=color: self.change_counter(c, -1))
            row.addWidget(dec_btn)

            counter_label = QLabel(str(self.color_counter_dict[color]))
            counter_label.setFixedWidth(60)
            counter_label.setAlignment(Qt.AlignCenter)
            self.labels[color] = counter_label
            row.addWidget(counter_label)

            inc_btn = QPushButton("➕")
            inc_btn.setFixedWidth(60)
            inc_btn.clicked.connect(lambda _, c=color: self.change_counter(c, 1))
            row.addWidget(inc_btn)

            reset_btn = QPushButton("🔄")
            reset_btn.setFixedWidth(80)
            reset_btn.clicked.connect(lambda _, c=color: self.reset_counter(c))
            row.addWidget(reset_btn)

            row.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            main_layout.addLayout(row)

        main_layout.addStretch()

    def change_counter(self, color, delta):
        self.color_counter_dict[color] += delta
        self.labels[color].setText(str(self.color_counter_dict[color]))

    def reset_counter(self, color):
        self.color_counter_dict[color] = 0
        self.labels[color].setText("0")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MainApp()
    myApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')