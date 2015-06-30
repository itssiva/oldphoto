## Introduction ##
A web site for share photo, powerd by Django.

You can get the source from svn(http://oldphoto.googlecode.com/svn/trunk/), and see the demo on http://lzpian.haoluobo.com/.

## Requirements ##
  1. Python(>=2.4)
  1. Django(>=1.0)
  1. PIL

## Install ##
  * Run scripts/syncdb.bat syncdb, and run scripts/runserver.bat start the dev server.
  * The admin account create by syncdb will no UserProfile, you should add it by admin.
  * The config is in config.py

## 介绍 ##
使用Django开发的照片分享网站。

代码在SVN中(http://oldphoto.googlecode.com/svn/trunk/)。

你可以访问http://lzpian.haoluobo.com/ 查看演示。

## 所需组件 ##
  1. Python(>=2.4)
  1. Django(>=1.0)
  1. PIL

## 安装 ##
  * 进入scripts目录运行syncdb.bat初始化数据库，再运行runserver.bat启动开发服务器。
  * 由于自动生成的管理员帐户没有UserProfile信息，需要进入admin手动添加。
  * 相关配置放在config.py