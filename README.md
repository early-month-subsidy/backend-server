# backend-server
the backend of this ordering system

### 部署说明

#### 运行环境

* python 3.5.6
* mysql
* redis

#### 环境变量设置

* 主要需要设置如下几个环境变量：
* FLASK_APP（flask的入口py文件名称）
* DATABASE_USER（mysql用户名）
* DATABASE_PASSWORD（mysql密码）
* REDIS_PASSWORD（redis密码）
* APPID（微信小程序appid）
* APP_SECRET（微信小程序APP_secret）
* SECRET_KEY（用于密码哈希）
* JWT_SECRET_KEY（用于JWT哈希）

#### 部署步骤

* 下载代码

  git clone https://github.com/early-month-subsidy/backend-server.git

* 安装python依赖包

  pip install -r requirements.txt

* 数据库更新

  flask db upgrade

* 运行进程

  flask run