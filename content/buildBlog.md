title: pelican建站攻略补充（站内搜索，和标签云）
date: 2014-09-25 21:00
author: guozhongxin
category: Python
slug: build_blog_with_pelican
tags: pelican, python,    
summary: 添加google站内搜索，添加百度站内搜索

##pelican建站准备  
  
参见lizherui的[一步一步打造Geek风格的技术博客](http://www.lizherui.com/pages/2013/08/17/build_blog.html)，不累述
* * *  

##添加站内搜索  

由于原日志中关于添加google站内搜索的链接失效，在其他地方没有看到特别好的介绍。  
我首先尝试了直接在`pelicanconf.py`中直接添加`GOOGLE_CUSTOM_SEARCH_NAVBAR`这一条属性，结果在`make html`之后，左上角的search框，在参考了lizhurui的博客代码后，我是这样实现的。  


###添加google站内搜索
####修改主题：  
找到这个主题（`tuxlite_tbs`）的templates文件夹中的`base.html`，在这个div(`<div class="nav-collapse">`)的最后，添加以下内容：  

	<form class="navbar-search pull-right" action="/search.html">
    	<input type="text" class="search-query" placeholder="Search" name="q" id="s">
	</form>  
更新pelican的主题：

	pelican-themes -U .../tuxlite_tbs

	
####创建search.html
之后，在output目录下，新建一个名为search.html的文件，写入下面的内容，其中需要你自己修改的是google站内搜索的ID号，需要自己在[google站内搜索](https://www.google.com/cse/)的网站上自己申请。


	<!DOCTYPE html>
    <html lang="zh_CN">
    <head>
    <meta charset="utf-8">
    <title>站内搜索</title>
    </head>
      <body>
    <style>
    #search-box {
        position: relative;
        width: 50%;
        margin: 0;
        padding: 1em;
    }

    #search-form {
        height: 30px;
        border: 1px solid #999;
        -webkit-border-radius: 5px;
        -moz-border-radius: 5px;
        border-radius: 5px;
        background-color: #fff;
        overflow: hidden;
    }

    #search-text {
        font-size: 14px;
        color: #ddd;
        border-width: 0;
        background: transparent;
    }

    #search-box input[type="text"] {
        width: 90%;
        padding: 4px 0 12px 1em;
        color: #333;
        outline: none;
    }
    </style>
    <div id='search-box'>
      <form action='/search.html' id='search-form' method='get' target='_top'>
        <input id='search-text' name='q' placeholder='Search' type='text'/>
      </form>
    </div>
    <div id="cse" style="width: 100%;">Loading</div>
    <script src="http://www.google.com/jsapi" type="text/javascript"></script>
    <script type="text/javascript"> 
      google.load('search', '1', {language : 'zh-CN', style : google.loader.themes.V2_DEFAULT});
      google.setOnLoadCallback(function() {
        var customSearchOptions = {};  var customSearchControl = new google.search.CustomSearchControl(
          '012191777864628038963:**********<!写入你申请的google站内搜索的ID号>）', customSearchOptions);
        customSearchControl.setResultSetSize(google.search.Search.FILTERED_CSE_RESULTSET);
        var options = new google.search.DrawOptions();
        options.enableSearchResultsOnly(); 
        customSearchControl.draw('cse', options);
        function parseParamsFromUrl() {
          var params = {};
          var parts = window.location.search.substr(1).split('\x26');
          for (var i = 0; i < parts.length; i++) {
            var keyValuePair = parts[i].split('=');
            var key = decodeURIComponent(keyValuePair[0]);
            params[key] = keyValuePair[1] ?
                decodeURIComponent(keyValuePair[1].replace(/\+/g, ' ')) :
                keyValuePair[1];
          }
          return params;
        }

        var urlParams = parseParamsFromUrl();
        var queryParamName = "q";
        if (urlParams[queryParamName]) {
          customSearchControl.execute(urlParams[queryParamName]);
        }
      }, true);
    </script>
    </body>
    </html>

####生成html，发布
将这个html文件保存在output目录（网站的根目录）下，执行

	make html
	make github

这样，搜索框就出来了。  

![1](http://www.guozhongxin.com/images/searchwithgoogle.png)

为了让google站内搜索功能更好的工作，你可在google站长工具中提交你的sitemap（这个可以在pelicanconf.py中配置sitemap插件，着执行make html后能自动生成）。

####提交sitemap
引入sitemap插件的工程见lizherui的日志。这样在`make html`之后就能生成sitemap.xml文件，提交到google站长上，搜索就可以生效了。  

* * *

###添加百度站内搜索
虽然实现了google站内搜索的功能，但是由于GFW的原因导致实际在使用google站内搜索时加载太慢，最终，我还是无奈的选择了百度站内搜索。。。  

####注册
在[百度站长平台](http://zhanzhang.baidu.com/)中注册一个账号，之后添加网站，按照提示验证网站。  
之后左侧`其他工具`中找到`站内搜索`，按照提示填写基本信息，选择搜索框样式，之后点击`查看代码`，复制其中内容，留用。  

####修改主题
同样在`base.html`的这个个div(`<div class="nav-collapse">`)的最后，新建一个`div`，刚才注册最后复制的代码粘贴到这个`div`中： 

	<div class="navbar-search pull-right">
		<script>  
			<!略>
		</script>
	</div>
更新pelican的主题：

	pelican-themes -U .../tuxlite_tbs

####生成html，发布
同上  

![2](http://www.guozhongxin.com/images/searchwithbaidu.png)

####提交sitemap
在百度站长工具里提交sitemap的过程和google的类似，需要注意的是百度有自己的[sitemap格式](http://zhanzhang.baidu.com/wiki/170#_2什么是sitemap索引文件？)，直接用lizherui日志中的方法生成的sitemap.xml不符合百度的要求：  
  
![3](http://www.guozhongxin.com/images/sitemapofbaidu.png)

百度sitemap要求有

	<data><display></display></data>

而我们使用的sitemap工具里没有这个，需要手动的对这个插件进行修改.

####配置符合百度站内搜索规则的pelican sitemap插件
找到`.../pelican-plugins/sitemap/sitemap.py`，找到全局变量`XML_URL`，将其修改为以下形式：

	XML_URL = """
	<url>
	<loc>{0}/{1}</loc>
	<lastmod>{2}</lastmod>
	<changefreq>{3}</changefreq>
	<priority>{4}</priority>
	<data>
	<display>
	</display>
	</data>
	</url>
	"""
这样，重新`make html`就能生成一份符合百度站内搜索的sitemap.xml。将其提交到百度站内搜索“提交数据”中，等待百度验证之后，就能体验百度站内搜索功能。

在这里吐槽一句，百度的站长工具确实不如google webmasters，同样是提交sitemap，google可以做到立即生效，百度的要等至少一个小时。如果没有GFW，才懒得用百度的呢。

* * *

##添加Tags链接
在其他一些pelican主题中，看到有标签云，想到Tags的链接可能比Categories的链接更有用，通过更改主题，添加了侧栏中红框内的Tags链接框。

####修改主题
还是找到`base.html`，找到categories部分：

	{% if categories %}
	<div class="well" style="padding: 8px 0; background-color: #FBFBFB;">
	<ul class="nav nav-list">
    	<li class="nav-header"> 
    	Categories
    	</li>
    
    	{% for cat, null in categories %}
    	<li><a href="{{ SITEURL }}/{{ cat.url }}">{{ cat }}</a></li>
    	{% endfor %}                   
	</ul>
	</div>
	{% endif %}
看到这一部分的代码之后，很容易仿写tags链接框的部分：

	{% if tags %}
	<div class="well" style="padding: 8px 0; background-color: #FBFBFB;">
	<ul class="nav nav-list">
	    <li class="nav-header"> 
	    Tags
	    </li>

	{% for name, tag in tags %}
	    <li><a href="{{ SITEURL }}/{{ name.url }}">{{ name }}</a></li>
	{% endfor %}
	</ul>
	</div>
	{% endif %}
将tags代码添加到categories框之后。执行

	pelican-themes -U .../tuxlite_tbs
	make html
	make github
这时，你就能看到左侧栏出现的TAGS链接框了。  
![4](http://www.guozhongxin.com/images/tags.png)
  
实际上这不是一个能体现tag出现频次的tag云，小弟实在没学过前端技术，大神看到有感兴趣的可以提出解决的方法。