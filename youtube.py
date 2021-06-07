from bs4 import BeautifulSoup as bs
from selenium import webdriver
from googleapiclient.discovery import build
import chromedriver_autoinstaller
import re

class Youtube:
    def __init__(self):
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument("disable-gpu")
        try: # chrome드라이버 없을 경우 설치
            self.driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=self.options)
        except:
            chromedriver_autoinstaller.install(True)
            self.driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=self.options)

        self.channels = {}
        self.channel = "" # 채널 검색어
        self.channel_id = "" # 선택한 채널 고유번호
        self.video_list = [] # 선택된 채널의 동영상 리스트
        self.soup = None # soup

    def search_youtuber(self, channel):
        self.driver.get('https://www.youtube.com/results?search_query='+ channel +'&sp=EgIQAg%253D%253D')
        self.driver.implicitly_wait(3)
        self.soup = bs(self.driver.page_source, "html.parser")
        channels = {}
        for num,i in enumerate(self.soup.find_all('div', id='content-section')):
            channel_id = i.find('a', class_='channel-link')['href']
            channel_name = i.find(id = 'text', class_='ytd-channel-name').text.strip()
            channels[num] = [channel_id, channel_name]

        self.channels = channels

    def get_video_lists(self,select):
        self.channel_id = self.channels[select-1][0]

        self.driver.get('https://www.youtube.com' + self.channel_id + '/videos')
        self.soup = bs(self.driver.page_source, "html.parser")

        video_list = []
        if self.soup == None:
            print('soup is empty')
            return -1

        for i in self.soup.find_all(id='video-title'):
            video_list.append(i['href'].split('=')[1])
        self.video_list = video_list

    def get_comments(self, ends):
        comments = [[]]
        if len(self.video_list) < ends:
            ends = len(self.video_list)
        for num, video in enumerate(self.video_list[:ends]):
            api_key = 'AIzaSyDxEjUOUxK9jUqhSbdVjP3QTTxeCWIFOT0'
            video_id = video
            api_obj = build('youtube', 'v3', developerKey=api_key)
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()
            print(f"processing {self.video_list[num]}...{num+1}/{ends}")
            comment = []
            count = 0
            while response:
                count += 1
                for item in response['items']:
                    temp = item['snippet']['topLevelComment']['snippet']
                    if int(temp['likeCount']) > -1:
                        temp = temp['textDisplay']
                        temp = re.sub('\<(.)*\>', "", temp) # , flags=re.MULTILINE
                        temp = re.sub('\((.)*\)', "", temp)
                        temp = re.sub('\&(.)*\;', "", temp)

                        comment.append(temp)
                if 'nextPageToken' in response and count < 30:  #
                    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
                else:
                    break
            comments.append(comment)
        return comments