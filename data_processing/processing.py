# encoding=utf-8
# author: haven
import pymongo
import re
from scrapy import Selector

from zhilian_resume.util.regularPatternUtil import RegularPatternUtil


class DataProcess():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db_name = 'zhilian'
    db = client[db_name]
    collection_preresume = db['resume']
    collection_affresume = db['resume_processed']

    def processing(self):
        """
        处理操作方法
        :return:
        """
        regularPatternUtil = RegularPatternUtil()  # 正则表达式工具类
        for resume in self.collection_preresume.find():
            resume_selector = Selector(text=resume['person_info'])
            person_info1 = re.sub(pattern='(\xa0)+', repl='|',
                                  string=resume_selector.css("div.summary-top span::text").extract_first()).split('|')
            for info1 in person_info1:
                if re.search(pattern="[" + unicode('女', 'utf8') + unicode('男', 'utf8') + "]",
                             string=info1, flags=0) != None:
                    # print info1
                    resume["sex"] = regularPatternUtil.substituteStrFunc1(info1)
                    continue
                if re.search(pattern=unicode('岁', 'utf8'), string=info1, flags=0) != None:
                    # print info1.split(unicode('岁','utf8'))[0]
                    resume["age"] = regularPatternUtil.substituteStrFunc1(info1.split(unicode('岁','utf8'))[0])
                    continue
                if re.search(pattern=unicode('工作经验', 'utf8'), string=info1, flags=0) != None:
                    # print info1
                    resume["exper"] = regularPatternUtil.substituteStrFunc1(info1)
                    continue
                if re.search(pattern="[" + unicode('初高技专EMBA其他大专本硕博', 'utf8') + "]+", string=info1,
                             flags=0) != None:
                    # print info1
                    resume["degree"] = regularPatternUtil.substituteStrFunc1(info1)
                    continue
                if re.search(pattern="[" + unicode('未婚已婚离异', 'utf8') + "]", string=info1, flags=0) != None:
                    # print info1
                    resume["marry"] = regularPatternUtil.substituteStrFunc1(info1)
                    continue
            person_info2 = regularPatternUtil.substituteStrFunc1(resume_selector.css("div.summary-top::text").extract()[2].encode('utf8'))
            for info2 in person_info2.split('|'):
                # print info2.split('：')[0]
                if info2.split('：')[0] == '现居住地':
                    print info2
                    resume["addr"] = info2.split('：')[1]
                    continue
                if info2.split('：')[0] == '户口':
                    print info2
                    resume["hometown"] = info2.split('：')[1]
                    continue
                resume["level"] = info2
            resume.pop('person_info')
            self.collection_affresume.insert(resume)  # 存入到mongodb集合中
