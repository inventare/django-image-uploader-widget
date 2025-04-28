import os

def get_mock_image(name: str):
    base_dir = os.path.dirname(__file__)
    mocks_dir = os.path.join(base_dir, "..", "__mocks__")
    return os.path.join(mocks_dir, name)
