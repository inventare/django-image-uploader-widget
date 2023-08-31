import os

class ImageMixin:
    """
    Provides an mixin to help working with images inside
    django-admin and selenium.
    """

    @property
    def image1(self):
        """gets the file path of the image1."""
        base_dir = os.path.dirname(__file__)
        mocks_dir = os.path.join(base_dir, "mocks")
        image = os.path.join(mocks_dir, "image.png")
        return image

    @property
    def image2(self):
        """gets the file path of the image2."""
        base_dir = os.path.dirname(__file__)
        mocks_dir = os.path.join(base_dir, "mocks")
        image = os.path.join(mocks_dir, "image2.png")
        return image
