import os


class ImageMockMixin:
    def _get_mock_image(self, name: str):
        base_dir = os.path.dirname(__file__)
        mocks_dir = os.path.join(base_dir, "..", "__mocks__")
        return os.path.join(mocks_dir, name)

    @property
    def image1(self):
        """Get the file path of the image1."""
        return self._get_mock_image("image1.png")

    @property
    def image2(self):
        """Get the file path of the image2."""
        return self._get_mock_image("image2.png")

    @property
    def image3(self):
        """Get the file path of the image2."""
        return self._get_mock_image("image3.png")
