# hupubbs

基于scrapy开发的，对[虎扑论坛](https://bbs.hupu.com/)进行爬取的爬虫。

## 部署

* clone项目到本地
* 修改`hupubbs/pipelines.py`里`MySQLPipeline.opoen_spider`里`self.db`里的MySQL连接参数，使其指向自己的mysql服务器。
* 在命令行进入项目目录，运行`scrapy crawl hupubbs`。

## 设计文档

* [虎扑论坛网络架构分析](docs/虎扑论坛网络架构分析.md)
* [爬虫设计](docs/爬虫设计.md)
* [数据字典](docs/数据字典.md)
* [数据库设计](docs/数据库设计.md)

## 使用范例

虎扑可以让用户隐藏自己的动态，这样就不知道用户主要在哪个版块**回帖**。使用爬虫爬取后，在数据库里运行

```SQL
select plate.url, count(*)
from reply
    left join thread on reply.thread_id = thread.id
    left join plate on thread.plate_id = plate.id
    left join user on reply.user_id = user.id
where user.url_id = 245307700327195 # `https://my.hupu.com/245307700327195`
group by plate.id;
```

可以查看该用户在各分区的回帖数。
