from PIL import Image,ImageDraw,ImageFont
import textwrap
import requests

class widget:

    def __init__(self, config, tileSize, boardBgColor):
        self.config = config
        self.tileSize = tileSize
        self.boardBgColor = boardBgColor
        print('news widget initialised')

    def getNews(self):
        url = "https://newsapi.org/v2/top-headlines?"
        url += "language=en"
        url += "&pageSize=3"
        url += "&apiKey=72d48922d4644d03bcda247a8ba59479"

        response = requests.get(url)
        data = response.json()
        
        return data['articles']

    def render(self):
        print('rendering news widget')

        # set all required variables
        newsData = self.getNews()

        bg_color = 255 if self.config['config']['colorMode']=='light' else 0
        text_color = 0 if self.config['config']['colorMode']=='light' else 255

        widget_width = self.tileSize*self.config['width'] - 10
        widget_height = self.tileSize*self.config['height'] - 10

        widget_img = Image.new(mode='1', size=(widget_width, widget_height), color=bg_color)
        widget_draw = ImageDraw.Draw(widget_img)
        title_font = ImageFont.load_default()
        content_font = ImageFont.truetype('OpenSans.ttf', 14)
        news_title_font = ImageFont.truetype('OpenSans.ttf', 10)
        
        # draw frame
        widget_draw.rectangle(
            xy = [(0, 0), (widget_width, widget_height)], 
            outline = (255-bg_color if self.boardBgColor==self.config['config']['colorMode'] else bg_color), 
            width = 5
        )

        # draw widget title
        widget_draw.text(xy=(10, 10), text='news', font=title_font, fill=text_color)

        # draw news
        x = 20
        y = 30
        for article in newsData:
            source = article['source']['name']
            sourceSize = content_font.getsize(source)
            widget_draw.rectangle(xy=[(x-5, y), (x+sourceSize[0]+5, y+25)], fill= text_color)
            widget_draw.text(xy=(x, y+2), text=source, font=content_font, fill=bg_color)

            title = article['title']
            note_lines = textwrap.wrap(title, width=round((widget_width-sourceSize[0]+10) * 0.17))
            y_text = y
            for line in note_lines:
                widget_draw.text(xy=(x+sourceSize[0]+10, y_text-2), text=line, font=news_title_font, fill=text_color)
                y_text += 15

            y += 40
        
        return widget_img