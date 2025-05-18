class _DarkMode:
    def __init__(self, page):
        self.page = page

    def __enter__(self):
        self.page.emulate_media(color_scheme="dark")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.page.emulate_media(color_scheme="light")


def dark_theme(page):
    return _DarkMode(page)
