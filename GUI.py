from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
import os, sys
from youtube import Youtube
from get_wordcloud import Wordcloud

# couldn't modulization
# cnt = connection
class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.yt = Youtube()
        self.wc = Wordcloud()

        # conponent
        self.search_text = QLineEdit()

        self.label_search = QLabel('검색어')
        self.label_search.setAlignment(Qt.AlignCenter)
        self.label_channel = QLabel('채널 선택')
        self.label_channel.setAlignment(Qt.AlignCenter)
        self.label_videos = QLabel('참고 영상 수')
        self.label_videos.setAlignment(Qt.AlignCenter)
        self.label_font = QLabel('글씨체(font)')
        self.label_font.setAlignment(Qt.AlignCenter)

        # button
        self.btn_search = QPushButton('검색', self)
        self.btn_search.clicked.connect(self.btn_search_func)

        self.btn_reset = QPushButton('초기화', self)
        self.btn_reset.clicked.connect(self.btn_reset_func)

        self.btn_print = QPushButton('출력', self)
        self.btn_print.clicked.connect(self.btn_print_func)
        self.btn_print.setMaximumHeight(500)

        self.btn_quit = QPushButton('나가기', self)
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)

        # combobox
        self.cb_selectChannel = QComboBox(self)
        self.cb_selectVideos = QComboBox(self)


        self.cb_selectFont = QComboBox(self)
        for i in range(len(self.wc.fonts)):
            self.cb_selectFont.addItem(self.wc.fonts[i])

        # set component position
        #group box_1
        self.form_lbx = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        self.setLayout(self.form_lbx)

        self.gb_1 = QGroupBox(self)
        self.gb_1.setTitle("검색어 입력")
        self.form_lbx.addWidget(self.gb_1)

        self.lbx = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        self.gb_1.setLayout(self.lbx)
        self.lbx.addWidget(self.search_text)
        self.lbx.addWidget(self.btn_search)

        #group_box 2
        self.gb_2 = QGroupBox(self)
        self.gb_2.setTitle("옵션")
        self.form_lbx.addWidget(self.gb_2)
        self.layout_form = QFormLayout()
        self.gb_2.setLayout(self.layout_form)
        self.layout_form.addRow(self.label_channel, self.cb_selectChannel)
        self.layout_form.addRow(self.label_videos, self.cb_selectVideos)
        self.layout_form.addRow(self.label_font, self.cb_selectFont)
        self.layout_form.addRow(self.btn_print)
        self.layout_form.addRow(self.btn_reset)

        #group_box 3
        self.gb_3 = QGroupBox(self)
        self.gb_3.setTitle("워드 클라우드")
        self.form_lbx.addWidget(self.gb_3)
        self.lbx = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        self.gb_3.setLayout(self.lbx)

        self.pixmap = QPixmap("")
        self.pixmap = self.pixmap.scaledToWidth(500)
        self.lb_1 = QLabel()
        self.lb_1.setPixmap(self.pixmap)

        self.lbx.addWidget(self.lb_1)
        self.setWindowTitle('Youtube Crawling')
        self.setGeometry(300, 300, 500, 500)
        self.form_lbx.addWidget(self.btn_quit)


        self.show()


    def btn_search_func(self):
        self.cb_selectChannel.clear()
        num_youtubers = self.yt.search_youtuber(self.search_text.text())
        for i in range(len(self.yt.channels)):
            self.cb_selectChannel.addItem(f"{i+1}.. {self.yt.channels[i][1]}")
        for i in range(1,31):
            self.cb_selectVideos.addItem(str(i))


    def btn_reset_func(self):
        self.search_text.setText('')
        self.cb_selectVideos.clear()
        self.cb_selectChannel.clear()
        self.lb_1.clear()

    def btn_print_func(self):
        channel = int(self.cb_selectChannel.currentText().split("..")[0])
        videos = int(self.cb_selectVideos.currentText())
        self.yt.get_video_lists(channel)

        self.wc.font = self.cb_selectFont.currentText()

        self.wc.show_wordcloud(self.yt.get_comments(videos))
        self.yt.driver.close()
        self.pixmap = QPixmap('./wc.png')
        self.pixmap.scaledToWidth(100)
        self.lb_1.setPixmap(self.pixmap)

