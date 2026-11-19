# -*- coding: utf-8 -*-
"""为 www.gosite.com.cn 生成本地文章页：
- 新增 article-multi-site-seo.html（基于 article-geo.html 模板）
- 更新 news.html 资讯列表、sitemap.xml、sitemap.html
不执行任何线上部署。
"""
import os, re, json

SITE = "D:/项目管理文件夹/2026-11-12-11-29-50/跨境极站"
FN = "article-multi-site-seo.html"
DATE = "2026-11-20"
TITLE = "集团多主体网站如何做好SEO：关键词分工与冲突规避"
DESC = "母公司官网与专业子公司官网同属一个品牌，关键词与内容容易互相分流。梳理多主体网站常见的SEO冲突，以及关键词分工、标题写法、结构化数据与互链的具体做法。"
KEYS = "极站 · AI 建站,集团官网,多站点SEO,关键词分工,结构化数据,站点收录,极站"

def read(name):
    with open(os.path.join(SITE, name), encoding="utf-8") as f:
        return f.read()

def write(name, s):
    with open(os.path.join(SITE, name), "w", encoding="utf-8") as f:
        f.write(s)

def build_article():
    tpl = read("article-geo.html")
    url = "https://www.gosite.com.cn/" + FN
    # 1) head 元信息
    tpl = tpl.replace("AI 问答时代的内容结构：事实段落、FAQ 与结构化数据", TITLE)
    tpl = tpl.replace("解析面向生成式引擎的内容组织方式：可被直接引用的事实、问答结构与结构化标注如何配合", DESC)
    tpl = tpl.replace("极站 · AI 建站,GEO,AI问答,结构化数据,FAQ,内容结构", KEYS)
    tpl = tpl.replace("https://www.gosite.com.cn/article-geo.html", url)
    tpl = tpl.replace('"dateModified":"2026-11-05"', '"dateModified":"%s"' % DATE)
    tpl = tpl.replace('"datePublished":"2026-11-05"', '"datePublished":"%s"' % DATE)
    tpl = tpl.replace('datetime="2026-11-05"', 'datetime="%s"' % DATE)
    tpl = tpl.replace("2026-11-05", DATE)
    # 2) 封面图
    tpl = tpl.replace("assets/img/covers/cover-geo.png", "assets/img/covers/seo-multi-1.jpg")
    tpl = tpl.replace("AI 问答时代的内容结构：事实段落、FAQ 与结构化数据 封面图", TITLE + " 封面图")
    # 3) hero 副标题
    tpl = tpl.replace("搜索从「给出链接」逐渐走向「直接给出答案」。页面能不能被引用，取决于事实是否清楚、结构是否容易被解析。",
                      "同一品牌下的总站与专业站，需要划清关键词边界：品牌大词归总站，垂直业务词归子站。")
    # 4) 正文主体
    body_old = re.search(r'(<div class="article-body">).*?(</div>\s*<div class="pill-row")', tpl, re.S)
    if not body_old:
        raise SystemExit("找不到正文区块")
    blocks = [
        ("三类常见冲突", "品牌词正面竞争：两站标题都放同一集团名称，搜索结果条目高度雷同，权重更低的一方的投入被抵消。业务范围词重叠：子公司页面照搬集团的大词，搜索引擎难以判断该展示哪一个。内容与身份模糊：正文大量复述集团简介，却没有说明自己的独立定位。"),
        ("分工的基本思路", "品牌词归总站，垂直业务词归专业站。集团总站围绕集团名称、企业服务、产业投资、财税等词展开；专业站则聚焦知识产权代理、专利申请、商标注册、高新技术企业认定等具体服务词，让每一类搜索意图都有对应页面承接。"),
        ("标题与描述怎么写", "标题采用业务词前置、地域词居中、品牌词收尾的结构，每个页面只对应一类服务。描述控制在八十个字符以内，写清服务内容、地域与机构身份，并保留联系方式，比堆砌关键词更有助于转化。"),
        ("用数据说明关系", "结构化数据中标明 parentOrganization，指向集团官网，说明该站是旗下专业机构而非镜像站。规范链接、站点名称与分享信息统一使用该专业站品牌，避免身份混淆。"),
        ("互链与收录推进", "专业站全站页脚保留指向集团官网的链接，集团站相应位置加入反向入口，形成双向关联。结构就绪后再依次完成站点验证、站点地图提交与 API 加速推送，收录工作才能顺利推进。"),
    ]
    body_new = '<div class="article-body">'
    for h, p in blocks:
        body_new += '<div class="prose-block reveal"><h3>%s</h3><p>%s</p></div>' % (h, p)
    body_new += '</div>\n<div class="pill-row"'
    tpl = tpl[:body_old.start()] + body_new + tpl[body_old.end():]
    # 5) 配图插入正文（三张信息图）
    imgs = [
        ("seo-multi-2.jpg", "三类SEO冲突与规避方式对照"),
        ("seo-multi-3.jpg", "站点验证、地图提交与API推送流程"),
    ]
    html_imgs = "\n".join(
        '<figure class="article-figure reveal"><img src="assets/img/covers/%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (src, alt, alt)
        for src, alt in imgs
    )
    tpl = tpl.replace('<div class="article-body">', html_imgs + '\n<div class="article-body">', 1)
    # 6) 标签
    tpl = tpl.replace('<span class="pill">GEO</span><span class="pill">结构化数据</span><span class="pill">内容策略</span>',
                      '<span class="pill">多站点SEO</span><span class="pill">关键词分工</span><span class="pill">站点收录</span>')
    write(FN, tpl)
    print("created", FN)

def update_news():
    s = read("news.html")
    card = '''<article class="article-card reveal" data-pager-item="news" data-cat="insight" data-date="%s">
<a class="article-cover" href="%s"><img src="assets/img/covers/seo-multi-1.jpg" alt="%s 封面图" loading="lazy"></a>
<span class="article-cat">SEO 优化</span><h3><a href="%s">%s</a></h3><p>%s</p>
<div class="article-meta"><time class="article-time" datetime="%s">%s</time> · SEO 优化 · 多站点 · 关键词分工</div>
<a class="btn btn-ghost btn-sm" href="%s">阅读全文</a></article>''' % (DATE, FN, TITLE, FN, TITLE, DESC, DATE, DATE, FN)
    marker = '<div class="pager" data-pager="news" data-per-page="3"><div class="article-grid">'
    if marker not in s:
        raise SystemExit("news.html 找不到卡片容器")
    s = s.replace(marker, marker + card, 1)
    write("news.html", s)
    print("updated news.html")

def update_sitemap_xml():
    s = read("sitemap.xml")
    entry = ('  <url><loc>https://www.gosite.com.cn/%s</loc>'
             '<xhtml:link rel="alternate" hreflang="zh-CN" href="https://www.gosite.com.cn/%s"/>'
             '<xhtml:link rel="alternate" hreflang="x-default" href="https://www.gosite.com.cn/"/>'
             '<lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>\n') % (FN, FN, DATE)
    if FN in s:
        print("sitemap.xml 已含该页面")
        return
    s = s.replace("</urlset>", entry + "</urlset>")
    write("sitemap.xml", s)
    print("updated sitemap.xml")

def update_sitemap_html():
    s = read("sitemap.html")
    anchor = '<h3>建站观察</h3><ul><li><a href="news.html">建站观察</a></li>'
    if anchor not in s:
        raise SystemExit("sitemap.html 找不到建站观察分组")
    item = '<li><a href="%s">%s</a></li>' % (FN, TITLE)
    s = s.replace(anchor, anchor + item, 1)
    write("sitemap.html", s)
    print("updated sitemap.html")

build_article()
update_news()
update_sitemap_xml()
update_sitemap_html()
