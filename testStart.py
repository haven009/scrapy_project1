# encoding=utf-8
# author: haven
from scrapy.cmdline import execute

class TestClass:
    def test_start(self):
        execute("scrapy crawl zhilianresume".split())

testClass = TestClass()
testClass.test_start()