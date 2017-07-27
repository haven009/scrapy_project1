# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianResumeItem(scrapy.Item):
    # define the fields for your item here like:
    resume_name = scrapy.Field()  # 简历名称
    expect_work = scrapy.Field()  # 期望从事职业
    update_date = scrapy.Field()  # 简历更新时间
    resume_id = scrapy.Field()  # 简历ID
    person_info = scrapy.Field()  # 个人信息
    # sex = scrapy.Field()  # 性别
    # age = scrapy.Field()  # 年龄
    # exper = scrapy.Field()  # 几年工作经验
    # degree = scrapy.Field()  # 学历
    # marry = scrapy.Field()  # 婚姻状况
    # addr = scrapy.Field()  # 现居地
    # hometown = scrapy.Field()  # 户口
    # level = scrapy.Field()  # 政治面貌
    expect_work_city = scrapy.Field()  # 期望工作地区
    expect_sal = scrapy.Field()  # 期望月薪
    current_situation = scrapy.Field()  # 目前状况
    expect_job_nature = scrapy.Field()  # 期望工作性质
    expect_job = scrapy.Field()  # 期望从事职业
    exxpect_indu = scrapy.Field()  # 期望从事行业
    self_eval = scrapy.Field()  # 自我评价
    work_exper = scrapy.Field()  # 工作经历
    project_exper = scrapy.Field()  # 项目经历
    edu_exper = scrapy.Field()  # 教育经历
    study_situation = scrapy.Field()  # 在校学习情况
    practical_exper = scrapy.Field()  # 在校实践经验
    train_exper = scrapy.Field()  # 培训经历
    certificate = scrapy.Field()  # 证书
    language = scrapy.Field()  # 语言能力
    profess_skill = scrapy.Field()  # 专业技能
    hobby = scrapy.Field()  # 兴趣爱好
    social_activ = scrapy.Field()  # 社会活动
    achieving_honor = scrapy.Field()  # 获得荣誉
    honor = scrapy.Field()  # 荣誉
    special_skill = scrapy.Field()  # 特殊技能
    special_occu_target = scrapy.Field()  # 特长职业目标
    patent = scrapy.Field()  # 专利
    paper = scrapy.Field()  # 著作 / 论文
    recommendation = scrapy.Field()  # 推荐信
    professional_org = scrapy.Field()  # 专业组织
    religion = scrapy.Field()  # 宗教信仰
    page_url = scrapy.Field()  # 采集页面url
    page_title = scrapy.Field()  # 采集页面标题
    curr_time = scrapy.Field()  # 采集页面时间
    zhilianresume_uuid = scrapy.Field()  # UUID

    def setAll(self):
        """
        设置item属性缺省值
        :return:
        """
        self["resume_name"] = None
        self["expect_work"] = None
        self["update_date"] = None
        self["resume_id"] = None
        self["person_info"] = None
        # self['sex'] = None
        # self['age'] = None
        # self['exper'] = None
        # self['degree'] = None
        # self['marry'] = None
        # self['addr'] = None
        # self['hometown'] = None
        # self['level'] = None
        self["expect_work_city"] = None
        self["expect_sal"] = None
        self["current_situation"] = None
        self["expect_job_nature"] = None
        self["expect_job"] = None
        self["exxpect_indu"] = None
        self["self_eval"] = None
        self["work_exper"] = None
        self["project_exper"] = None
        self["edu_exper"] = None
        self["study_situation"] = None
        self["practical_exper"] = None
        self["train_exper"] = None
        self["certificate"] = None
        self["language"] = None
        self["profess_skill"] = None
        self["hobby"] = None
        self["social_activ"] = None
        self["achieving_honor"] = None
        self["honor"] = None
        self["special_skill"] = None
        self["special_occu_target"] = None
        self["patent"] = None
        self["paper"] = None
        self["recommendation"] = None
        self["professional_org"] = None
        self["religion"] = None
        self["page_url"] = None
        self["page_title"] = None
        self["curr_time"] = None
