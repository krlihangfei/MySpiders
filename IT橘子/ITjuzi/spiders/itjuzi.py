# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ITjuzi.items import ItjuziItem


class ItjuziSpider(scrapy.Spider):
    name = 'itjuzi'
    allowed_domains = ['itjuzi.com']
    base_url = "https://www.itjuzi.com/company/"
    offset = 1

    start_urls = [base_url + str(offset)]

    cookies = {"gr_user_id" : "145c121f-fb8c-4a8e-8190-231596b3f2d7",
    "acw_tc" : "AQAAAM7mdTQQQQUARkDtt0YI0QT9zaO6",
    "identity" : "123636274%40qq.com",
    "remember_code" : "4lLP5CmF9x",
    "unique_token" : "332682",
    "MEIQIA_EXTRA_TRACK_ID" : "0upVCH2EUiLusLRQf3MWQiShmmu",
    "_ga" : "GA1.2.1588476138.1507779389",
    "_gid" : "GA1.2.1649085483.1507779389",
    "Hm_lvt_1c587ad486cdb6b962e94fc2002edf89" : "1507455148,1507778826,1507779493,1507798997",
    "Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89" : "1507805694",
    "session" : "69b2f122d9c68e558141ba8ce857e4be4a67072c"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies = self.cookies, callback = self.parse)


    def parse(self, response):

        if response.status == 200:
            soup = BeautifulSoup(response.body, "lxml")
            # cpy1: 基本信息
            item = ItjuziItem()

            cpy1 = soup.find("div", class_="infoheadrow-v2")
            if cpy1:

                item['name'] = cpy1.find("h1", class_="seo-important-title").contents[0].strip()
                item['slogan'] = cpy1.find(class_="seo-slogan").get_text().strip()
                item['scope_big'] = cpy1.find(class_="scope").find_all("a")[0].get_text().strip()
                item['scope_little'] = cpy1.find(class_="scope").find_all("a")[1].get_text().strip()
                item['province'] = cpy1.find(class_="loca").find_all("a")[0].get_text().strip()

                item['city'] = cpy1.find(class_="loca").find_all("a")[1].get_text().strip()

                a_list =  cpy1.find(class_="link-line").span.find_all("a")
                for a in a_list:
                    if "://www." in a.get_text():
                        item['home_link'] = a.get_text().strip()
                item['tag'] = cpy1.find(class_="tagset").get_text().strip().replace("\n", ", ")


            # cpy2：公司信息
            cpy2 = soup.find(class_="block-inc-info")
            if cpy2:
                try:
                    item['company_info'] = cpy2.find_all(class_="abstract")[-1].get_text().strip()
                except:
                    item['company_info'] = "None"

                item['company_fullname'] = cpy2.find(class_="des-more").find_all("h2")[0].get_text().strip()
                item['company_time'] = cpy2.find(class_="des-more").find_all("h2")[1].get_text().strip()
                item['company_size'] = cpy2.find(class_="des-more").find_all("h2")[2].get_text().strip()
                item['company_status'] = cpy2.find("span").get_text().strip()


            # cpy3：融资信息
            cpy3 = soup.find("table", class_="list-round-v2")
            if cpy3:
                tr_list = cpy3.find_all("tr")

                financing_list = []
                for tr in tr_list:
                    td_dict = {}
                    td_dict['financing_time'] = tr.find_all("td")[0].span.get_text()
                    td_dict['financing_stage'] = tr.find_all("td")[1].span.get_text()
                    td_dict['financing_money'] = tr.find_all("td")[2].span.get_text()
                    try:
                        td_dict['financing_company'] = tr.find_all("td")[3].a.get_text()
                    except:
                        td_dict['financing_company'] = "None"
                    financing_list.append(td_dict)

                item['financing'] = financing_list

            # cpy4：团队信息
            cpy4 = soup.find(class_="list-prodcase")
            if cpy4:
                li_list = cpy4.find_all("li")

                team_list = []
                for li in li_list:
                    li_dict = {}
                    li_dict['team_name'] = li.find(class_="title").find_all("span")[0].get_text().strip()

                    li_dict['team_title'] = li.find(class_="title").find_all("span")[1].get_text().strip()

                    li_dict['team_info'] = li.p.get_text().strip()
                    team_list.append(li_dict)

                item['team'] = team_list


            # cpy5: 产品信息
            cpy5 = soup.find(class_="list-prod")
            if cpy5:
                li_list = cpy5.find_all("li")

                product_list = []
                for li in li_list:
                    li_dict = {}
                    li_dict['product_type'] = li.h4.span.get_text().strip()
                    li_dict['product_name'] = li.b.get_text().strip()
                    li_dict['product_info'] = li.p.get_text().strip()
                    product_list.append(li_dict)

                item['product'] = product_list

            yield item


        self.offset += 1
        yield scrapy.Request(self.base_url + str(self.offset), callback = self.parse)


