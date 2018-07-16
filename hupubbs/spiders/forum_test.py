import unittest

from hupubbs.spiders.forum import ForumSpider

class TestForumSpider(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_next_forum_page_url(self):
        spider = ForumSpider()
        self.assertEqual("https://bbs.hupu.com/china-soccer-2", spider.next_forum_page_url("https://bbs.hupu.com/china-soccer"))
        self.assertEqual("https://bbs.hupu.com/china-soccer-3", spider.next_forum_page_url("https://bbs.hupu.com/china-soccer-2"))

    def test_next_thread_page_url(self):
        spider = ForumSpider()
        self.assertEqual("https://bbs.hupu.com/22900973-2.html", spider.next_thread_page_url("https://bbs.hupu.com/22900973.html"))
        self.assertEqual("https://bbs.hupu.com/22900973-3.html", spider.next_thread_page_url("https://bbs.hupu.com/22900973-2.html"))

    def test_thread_id(self):
        spider = ForumSpider()
        self.assertEqual("22907925", spider.thread_id("https://bbs.hupu.com/22907925.html"))
        self.assertEqual("22886870", spider.thread_id("https://bbs.hupu.com/22886870-3.html"))

    def test_plate_page(self):
        spider = ForumSpider()
        self.assertEqual(4, spider.plate_page("https://bbs.hupu.com/china-soccer-4"))
        self.assertEqual(1, spider.plate_page("https://bbs.hupu.com/china-soccer"))
        self.assertEqual(40, spider.plate_page("https://bbs.hupu.com/hengda-40"))
        self.assertEqual(1, spider.plate_page("https://bbs.hupu.com/hengda"))
