from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

class Wordcloud:
    def __init__(self):
        self.comments = []
        self.fonts = []
        self.font = ""
        file_list = dict(enumerate(os.listdir("./Fonts")))
        self.fonts = file_list

    def show_wordcloud(self, comments):
        text = """"""
        self.commnets = comments
        for comment in comments:
            text += """ """.join(comment)
        stopwords = set(STOPWORDS)
        usr_stopwords = ['br', 'quot', 'ㅋㅋㅋ', '진짜', 'ㅋ', 'ㅋㅋ', 'ㅋㅋㅋㅋ', 'ㅋㅋㅋㅋㅋ', 'ㅋ*']
        for i in usr_stopwords:
            stopwords.add(i)

        if len(text) > 100:
            wc = WordCloud(font_path=f'./Fonts/{self.font}',
                           stopwords=stopwords,
                           background_color='white',
                           width=1200,
                           height=1200,
                           max_words=60,
                           max_font_size=200).generate(text)
            plt.figure(figsize=(5, 5))  # 이미지 사이즈 지정
            plt.imshow(wc, interpolation='sinc')  # 이미지의 부드럽기 정도
            plt.axis('off')  # x y 축 숫자 제거
            plt.savefig('./wc.png')

