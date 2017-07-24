# encoding=utf-8
# author: haven

import re
import scrapy
import codecs
import json
import sys
import time
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings
from scrapy.utils.response import get_base_url
from selenium import webdriver
from zhilian_resume.items import ZhilianResumeItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from lib2to3.pgen2.tokenize import Ignore

reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.selector import Selector


class ZhiLianResumeSpider(scrapy.Spider):
    """
    智联简历爬虫
    """
    name = "zhilianresume"
    base_url = 'http://localhost:8080'
    # start_urls = ['http://localhost:8080/fetch/views/index.jsp', ]
    start_urls = ['http://localhost:8080/fetch/views/login.jsp', ]

    def __init__(self):
        # 使用Firefox浏览器
        # self.driver = webdriver.Firefox(executable_path='G:\statisticData\geckodriver.exe')
        # 使用PhantomJS浏览器引擎
        dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)  # 设置userAgent
        dcap[
            "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0"
        self.driver = webdriver.PhantomJS(
            executable_path='I:\\CIIC_Documents\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',
            desired_capabilities=dcap)
        self.driver.set_page_load_timeout(5)  # 设置页面完全加载的超时时间，完全加载即完全渲染完成，同步和异步脚本都执行完
        self.driver.set_script_timeout(5)
        self.driver.maximize_window()  # 设置全屏（最大化屏幕）

    # def start_requests(self):
    #     """
    #     首次发起请求
    #     :return:
    #     """
    #     yield scrapy.Request(self.start_url, self.parse_pagecontent)

    def set_sleep_time(self):
        """
        设置加载超时最大时长（单位：s）
        :return:
        """
        self.driver.implicitly_wait(30)  # 识别对象的智能等待时间
        self.driver.set_page_load_timeout(30)  # 设置页面完全加载的超时时间，完全加载即完全渲染完成，同步和异步脚本都执行完
        self.driver.set_script_timeout(30)  # 设置异步脚本的超时时间

    def parse(self, response):
        """
        解析页面内容
        :param response:
        :return:
        """
        print "你好：", get_base_url(response)
        self.driver.get(response.url)
        print "开始点击"
        # time.sleep(5)
        self.set_sleep_time()
        self.driver.find_element_by_class_name('index_loginin').find_element_by_tag_name('a').click()
        self.set_sleep_time()
        print "进入主页"
        sreach_window = self.driver.current_window_handle
        self.driver.switch_to_window(sreach_window)
        self.driver.find_element_by_id('datagrid-row-r5-2-1').find_element_by_tag_name('a').click()
        self.set_sleep_time()
        # time.sleep(5)
        page_content = self.driver.page_source  # 获取完整网页内容
        page_selector = Selector(text=page_content)
        td_list = page_selector.css("td[field*=fetchUrl]").extract()  # 提取td内容，由于网页中的标签几乎没有id
        td_list.pop(0)  # 移除第一个
        for td in td_list:
            td_selector = Selector(text=td)
            resume_url = td_selector.css("a::attr(href)").extract_first()
            print self.base_url + resume_url
            yield scrapy.Request(self.base_url + resume_url, self.parse_resume)

        print "=====================循环开始了============================"
        while True:
            # 获取下一页的按钮点击
            pager = self.driver.find_element_by_class_name('datagrid-pager')
            print len(pager.find_elements_by_tag_name('td'))
            pagedown = pager.find_elements_by_tag_name('td')[9].find_element_by_tag_name('a')
            print "标签属性：", str(pagedown.get_attribute("class"))
            # 首先判断按钮是否失效，失效即当前已是最后一页，直接退出
            if re.search(pattern="disabled",
                         string=pagedown.get_attribute("class").encode('unicode-escape').decode('string_escape'),
                         # get_attribute()得到的是unicode类型，需要经过转码得到string类型
                         flags=0) == None:
                print "点击了"
                pagedown.click()
                self.set_sleep_time()
                page_content = self.driver.page_source  # 获取完整网页内容
                selector = Selector(text=page_content)
                td_list = selector.css("td[field*=fetchUrl]").extract()  # 提取td内容，由于网页中的标签几乎没有id
                td_list.pop(0)  # 移除第一个
                print "=================简历个数:", len(td_list), "==============="
                for td in td_list:
                    td_selector = Selector(text=td)
                    resume_url = td_selector.css("a::attr(href)").extract_first()
                    print self.base_url + resume_url
                    yield scrapy.Request(self.base_url + resume_url, self.parse_resume)
            else:
                print "失效了"
                break
        print "=================循环结束了======================"

    def parse_resume(self, response):
        """
        解析简历内容
        :param response:
        :return:
        """
        print "到了"
        zhilianResumeItem = ZhilianResumeItem()
        # zhilianResumeItem.setAll()  # 设置item所有属性缺省值为None
        resume_selector = Selector(text=response.text)
        pattern = re.compile('["\n", " ", "\t", "\r"]*')  # 用于编译正则表达式并返回对象
        zhilianResumeItem["resume_name"] = re.sub(pattern=pattern, repl='', string=resume_selector.css(
            "strong[id=resumeName]::text").extract_first().encode('utf8'))
        zhilianResumeItem["expect_work"] = re.sub(pattern=pattern, repl='', string=resume_selector.css(
            "strong[id=desireIndustry]::text").extract_first().encode('utf8'))
        zhilianResumeItem["update_date"] = re.sub(pattern=pattern, repl='', string=resume_selector.css(
            "strong[id=resumeUpdateTime]::text").extract_first().encode('utf8'))
        zhilianResumeItem["resume_id"] = \
            re.sub(pattern=pattern, repl='',
                   string=resume_selector.css("span.resume-left-tips-id::text").extract_first().split(":")[1].encode(
                       'utf8'))
        zhilianResumeItem["person_info"] = resume_selector.css("div.summary-top").extract_first()
        # person_info1 = re.sub(pattern='(\xa0)+', repl='|',
        #                       string=resume_selector.css("div.summary-top span::text").extract_first()).split('|')
        # for info1 in person_info1:
        #     if re.search(pattern="[" + unicode('女', 'utf8') + unicode('男', 'utf8') + "]",
        #                  string=info1, flags=0) != None:
        #         print info1
        #         zhilianResumeItem["sex"] = re.sub(pattern=pattern, repl='', string=info1)
        #         continue
        #     if re.search(pattern=unicode('岁', 'utf8'), string=info1, flags=0) != None:
        #         print info1.split(unicode('岁','utf8'))[0]
        #         zhilianResumeItem["age"] = re.sub(pattern=pattern, repl='', string=info1.split(unicode('岁','utf8'))[0])
        #         continue
        #     if re.search(pattern=unicode('工作经验', 'utf8'), string=info1, flags=0) != None:
        #         print info1
        #         zhilianResumeItem["exper"] = re.sub(pattern=pattern, repl='', string=info1)
        #         continue
        #     if re.search(pattern="[" + unicode('初高技专EMBA其他大专本硕博', 'utf8') + "]+", string=info1,
        #                  flags=0) != None:
        #         print info1
        #         zhilianResumeItem["degree"] = re.sub(pattern=pattern, repl='', string=info1)
        #         continue
        #     if re.search(pattern="[" + unicode('未婚已婚离异', 'utf8') + "]", string=info1, flags=0) != None:
        #         print info1
        #         zhilianResumeItem["marry"] = re.sub(pattern=pattern, repl='', string=info1)
        #         continue
        # person_info2 = re.sub(pattern=pattern, repl='',
        #                       string=resume_selector.css("div.summary-top::text").extract()[2].encode('utf8'))
        # print person_info2
        # for info2 in person_info2.split('|'):
        #     if info2.split('：')[0] == unicode('现居住地', 'utf8'):
        #         print info2
        #         zhilianResumeItem["addr"] = info2.split('：')[1]
        #         continue
        #     if info2.split('：')[0] == unicode('户口', 'utf8'):
        #         print info2
        #         zhilianResumeItem["hometown"] = info2.split('：')[1]
        #         continue
        #     zhilianResumeItem["level"] = info2
        content = resume_selector.css("div.resume-preview-all").extract()
        for cont in content:
            contselector = Selector(text=cont)
            print contselector.css("h3::text").extract_first().encode('utf8')
            # unicode("求职意向", "utf8")
            if contselector.css("h3::text").extract_first().encode('utf8') == "求职意向":
                print "========找到了=========="
                tr_list = contselector.css("tr").extract()
                for tr in tr_list:
                    tr_selector = Selector(text=tr)
                    if tr_selector.css("td::text").extract_first().encode('utf8').split('：')[0] == "期望工作地区":
                        print tr_selector.css("td::text").extract()[1].encode('utf8').split('\n')
                        zhilianResumeItem["expect_work_city"] = re.sub(pattern=pattern, repl='',
                                                                       string=tr_selector.css("td::text").extract()[
                                                                           1].encode('utf8'))
                        continue
                    if tr_selector.css("td::text").extract_first().encode('utf8').split('：')[0] == "期望月薪":
                        print tr_selector.css("td::text").extract()[1].encode('utf8')
                        zhilianResumeItem["expect_sal"] = re.sub(pattern=pattern, repl='',
                                                                 string=tr_selector.css("td::text").extract()[1].encode(
                                                                     'utf8'))
                        continue
                    if tr_selector.css("td::text").extract_first().encode('utf8').split('：')[0] == "目前状况":
                        print tr_selector.css("td::text").extract()[1].encode('utf8')
                        zhilianResumeItem["current_situation"] = re.sub(pattern=pattern, repl='',
                                                                        string=tr_selector.css("td::text").extract()[
                                                                            1].encode('utf8'))
                        continue
                    if tr_selector.css("td::text").extract_first().encode('utf8').split('：')[0] == "期望工作性质":
                        print tr_selector.css("td::text").extract()[1].encode('utf8')
                        zhilianResumeItem["expect_job_nature"] = re.sub(pattern=pattern, repl='',
                                                                        string=tr_selector.css("td::text").extract()[
                                                                            1].encode('utf8'))
                        continue
                    if tr_selector.css("td::text").extract_first().encode('utf8').split('：')[0] == "期望从事职业":
                        print tr_selector.css("td::text").extract()[1].encode('utf8')
                        zhilianResumeItem["expect_job"] = re.sub(pattern=pattern, repl='',
                                                                 string=tr_selector.css("td::text").extract()[1].encode(
                                                                     'utf8'))
                        continue
                    if tr_selector.css("td::text").extract_first().encode('utf8').split('：')[0] == "期望从事行业":
                        print tr_selector.css("td::text").extract()[1].encode('utf8')
                        zhilianResumeItem["exxpect_indu"] = re.sub(pattern=pattern, repl='',
                                                                   string=tr_selector.css("td::text").extract()[
                                                                       1].encode('utf8'))
                        continue
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "自我评价":
                self_evalList = contselector.css("div.rd-break::text").extract()
                zhilianResumeItem["self_eval"] = re.sub(pattern=pattern, repl='',
                                                        string="".join(self_evalList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "工作经历":
                zhilianResumeItem["work_exper"] = re.sub(pattern=pattern, repl='', string=cont.encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "项目经历":
                zhilianResumeItem["project_exper"] = re.sub(pattern=pattern, repl='', string=cont.encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "教育经历":
                zhilianResumeItem["edu_exper"] = re.sub(pattern=pattern, repl='', string=contselector.css(
                    "div.resume-preview-dl::text").extract_first().encode(
                    'utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "在校学习情况":
                study_situationList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["study_situation"] = re.sub(pattern=pattern, repl='',
                                                              string="".join(study_situationList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "在校实践经验":
                practical_experList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["practical_exper"] = re.sub(pattern=pattern, repl='',
                                                              string="".join(practical_experList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "培训经历":
                zhilianResumeItem["train_exper"] = re.sub(pattern=pattern, repl='', string=cont.encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "证书":
                certificateList = contselector.css("h2::text").extract()
                zhilianResumeItem["certificate"] = re.sub(pattern=pattern, repl='',
                                                          string="".join(certificateList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "语言能力":
                languageList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["language"] = re.sub(pattern=pattern, repl='',
                                                       string="".join(languageList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "专业技能":
                profess_skillList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["profess_skill"] = re.sub(pattern=pattern, repl='',
                                                            string="".join(profess_skillList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "爱好":
                hobbyList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["hobby"] = re.sub(pattern=pattern, repl='', string="".join(hobbyList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "社会活动":
                social_activList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["social_activ"] = re.sub(pattern=pattern, repl='',
                                                           string="".join(social_activList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "获得荣誉":
                achieving_honorList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["achieving_honor"] = re.sub(pattern.pattern, repl='',
                                                              string="".join(achieving_honorList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "荣誉":
                honorList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["honor"] = re.sub(pattern=pattern, repl='', string="".join(honorList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "特殊技能":
                special_skillList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["special_skill"] = re.sub(pattern=pattern, repl='',
                                                            string="".join(special_skillList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "特长职业目标":
                special_occu_targetList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["special_occu_target"] = re.sub(pattern=pattern, repl='',
                                                                  string="".join(special_occu_targetList).encode(
                                                                      'utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "专利":
                patentList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["patent"] = re.sub(pattern=pattern, repl='',
                                                     string="".join(patentList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "著作/论文":
                paperList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["paper"] = re.sub(pattern=pattern, repl='', string="".join(paperList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "推荐信":
                recommendationList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["recommendation"] = re.sub(pattern=pattern, repl='',
                                                             string="".join(recommendationList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "专业组织":
                professional_orgList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["professional_org "] = re.sub(pattern=pattern, repl='',
                                                                string="".join(professional_orgList).encode('utf8'))
                continue
            if contselector.css("h3::text").extract_first().encode('utf8') == "宗教信仰":
                religionList = contselector.css("div.resume-preview-dl::text").extract()
                zhilianResumeItem["religion "] = re.sub(pattern=pattern, repl='',
                                                        string="".join(religionList).encode('utf8'))
                continue
        zhilianResumeItem["page_url"] = get_base_url(response)
        zhilianResumeItem["page_title"] = re.sub(pattern=pattern, repl='',
                                                 string=resume_selector.css("title::text").extract_first().encode(
                                                     'utf8'))
        zhilianResumeItem["curr_time"] = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        yield zhilianResumeItem
