
# itemloadr提供了一个容器，让我们配置某一个字段该使用哪种规则。
#   add_css 
#   add_value
#   add_xpath
# 这种用法是用来简化response.xpath与response.css方法

from scrapy.loader import ItemLoader
from ArticleSpider.items import ArticleItemLoader #引入自定义的ItemLoader
def parse_details(self, response):
        #实例化
        article_item = JobBoleArticleItem()

        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图

        # 通过item loader加载item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)

        # 通过css选择器将后面的指定规则进行解析。
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        # 调用这个方法来对规则进行解析生成item对象
        article_item = item_loader.load_item()

        # 已经填充好了值调用yield传输至pipeline
        yield article_item
        
#  上面那个方法是用来替换下面的语句：
    def parse_details(self, response):
        #实例化
        article_item = JobBoleArticleItem()

        #Xpath的用法
        front_image_url = response.meta.get("front_image_url", "")
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        create_date = response.xpath('//div[@class="entry-meta"]/p/text()').extract()[0].strip().replace("·","").strip()
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        content = response.xpath('//div[@class="entry"]').extract()[0]
        praise_nums = response.xpath('//div[@class="post-adds"]/span/h10/text()').extract()[0]
        fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0].strip()
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0].strip()
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        # 为实例化后的对象填充值
        article_item['front_image_url'] = [front_image_url]
        article_item["url"] = response.url
        article_item["url_object_id"] = get_md5(response.url)
        article_item['title'] = title
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        article_item['tags'] = tags
        article_item['content'] = content
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums

        yield article_item

        
        
#  如果在item.py文件中自定义了ItemLoader
# 自定义itemloader实现默认取第一个值
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
# 那么在spider爬虫文件中使用的话需要引入
from ArticleSpider.items import ArticleItemLoader






