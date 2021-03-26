from PIL import Image,ImageDraw,ImageFont
import textwrap

class widget:

    def __init__(self, config, tileSize):
        self.config = config
        self.tileSize = tileSize
        print('note widget initialised')

    def render(self):
        print('rendering note')
        bg_color = 255 if self.config['config']['colorMode']=='light' else 0
        text_color = 0 if self.config['config']['colorMode']=='light' else 255

        widget_width = self.tileSize*self.config['width'] - 10
        widget_height = self.tileSize*self.config['height'] - 10

        widget_img = Image.new(mode='1', size=(widget_width, widget_height), color=bg_color)
        widget_draw = ImageDraw.Draw(widget_img)
        title_font = ImageFont.load_default()
        content_font = ImageFont.truetype('OpenSans.ttf', 16)
        
        widget_draw.rectangle(xy=[(0, 0), (widget_width, widget_height)], outline=0, width= 5)

        widget_draw.text(xy=(10, 10), text='note', font=title_font, fill=text_color)

        note_lines = textwrap.wrap(self.config['config']['text'], width=round(widget_width* 0.1))
        y_text = 30
        for line in note_lines:
            width, height = content_font.getsize(line)
            widget_draw.text(((widget_width - width) / 2, y_text), line, font=content_font, fill=text_color)
            y_text += height

        return widget_img