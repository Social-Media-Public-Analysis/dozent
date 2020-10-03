from pyfiglet import Figlet
from shutil import get_terminal_size

DEFAULT_FONT = 'slant'
DEFAULT_TERMINAL_WIDTH = 80
DEFAULT_TERMINAL_HEIGHT = 20
TERMINAL_WIDTH = get_terminal_size((DEFAULT_TERMINAL_WIDTH, DEFAULT_TERMINAL_HEIGHT)).columns
text_renderer = Figlet(font=DEFAULT_FONT, width=TERMINAL_WIDTH)

if __name__ == '__main__':
    print(text_renderer.renderText('Hello World'))
