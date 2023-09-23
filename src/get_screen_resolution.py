import screeninfo

def get_screen_resolution():
    screen_info = screeninfo.get_monitors()
    if screen_info:
        screen = screen_info[0]
        return screen.width, screen.height
    else:
        return 1920, 1080