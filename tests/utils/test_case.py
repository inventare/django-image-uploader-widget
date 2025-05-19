import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from match_snapshot import MatchSnapshot
from playwright.sync_api import sync_playwright

from tests.pom.django_admin import DjangoAdminPO


class TestCase(MatchSnapshot, StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.context = cls.browser.new_context(
            viewport={
                "width": 1280,
                "height": 720
            }
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.context.new_page()
        self.admin_po = DjangoAdminPO(self.page, self.live_server_url)
        self.admin_po.create_user_and_execute_login()
