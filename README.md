# vue-flask-demo

本项目是一个演示项目，用于演示如何用 vue 和 flask 搭建一个简单的SPA应用

主要实现如下功能：



- [x] 前后端分离，前端VUE，后端FLASK
- [x] 解决跨域问题
- [x] 后端提供API
- [x] 前端调用API
- [x] 方便部署



## 效果

#### 前端

> http://localhost:8080/test

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gfry2xh4msj30gq0760sz.jpg)

#### 后端 - 访问页面

> http://localhost:5000

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gfry4owbshj30dz079t8q.jpg)

#### 后端 - 访问test页

> http://localhost:5000/test

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gfry2xh4msj30gq0760sz.jpg)

#### 后端 -- 访问API

> http://localhost:5000/api/test

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gfry6acwyfj30ba04zq33.jpg)



## 目录结构

```
|
| -- frontend
		| -- 
		| -- src 
			|-- 
| -- backend
		|-- app.py
| -- dist
		| -- index. html
		| -- static
	
```



## 实现过程

### 1.前端：

###### 1. 新建项目

新建目录 vue-flask-demo

```
$ mkdir vue-flask-demo
```

进入根目录

```
$ cd vue-flask-demo
```

新建前端项目

```
$ vue init webpack vue-flask-demo 
```

运行前端

```
$ npm run dev
```

###### 2. 安装必要的包

```
$ npm install vue-router  --save
```

```
$ npm install vuex  --save
```

```
$ npm install element-ui  --save
```

```
$ npm install axios  --save
```

###### 3. 首页

在components目录下新建page目录，并在page目录中新建页面 Home.vue 并添加代码

```
<template>
  <div>
    <p>主页</p>
  </div>
</template>
```

在 /src/router/index.js 中加入路由

```
import Vue from 'vue'
import Router from 'vue-router'

import Home from '../components/page/Home.vue'
Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
  ]
})
```

###### 4. 404页面

在page目录中新建页面 Home.vue 并添加代码

```
<template>
  <div>
    <p>404 - Not Found</p>
  </div>
</template>
```

在 /src/router/index.js 中加入路由

```
import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'

import Home from '../components/page/Home.vue'
import NotFound from '../components/page/NotFound.vue'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '*',
      component: NotFound ,
    }
  ]
})

```

###### 5. 测试页

在page目录中新建页面  并添加代码

```
<template>
  <div>
    <p>test</p>
    <el-button @click='getTestData'>从后端获取数据</el-button>
    <p>{{testData}}</p>
  </div>
</template>

<script>
  export default{
    name:'test',
    computed:{
      testData(){
        return this.$store.state.testData
      }
    },
    methods:{
      getTestData(){
        this.$store.dispatch('getTestData')
      }
    }
  }
</script>

<style>
</style>
```

在 /src/router/index.js 中加入路由

```
import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'

import Home from '../components/page/Home.vue'
import NotFound from '../components/page/NotFound.vue'
import Test from '../components/page/Test.vue'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/test',
      name: 'Test',
      component: Test
    },
    {
      path: '*',
      component: NotFound ,
    }
  ]
})
```

新建/src/store/store.js 并加入如下代码

```
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:5000/api'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state:{
    testData : ''
  },
  getters:{

  },
  mutations:{
    getTestData(state,testData){
      state.testData = testData
    }
  },
  actions:{
    getTestData(context){
      axios.get('/test')
      .then(response => {
        let testData = response.data.data.token
        context.commit('getTestData',testData)
      })
      .catch(err => {
        console.log(err)
      })
    }
  }
})
```

###### 6. 前端打包

修改打包路径

我们希望打包之后的代码放在根目录/vue-flask-demo/下

需要修改/frontend/config/index.js中的配置

> 将index和assetsRoot 修改成下面的样子

```
build: {
    // Template for index.html
    index: path.resolve(__dirname, '../../dist/index.html'),

    // Paths
    assetsRoot: path.resolve(__dirname, '../../dist'),
```

在/frontend/目录下运行如下命令来打包前端代码

```
$ npm run build
```

- [ ] 

此时会在根目录下生成dist目录

### 2. 后端

###### 1. 新建项目

在 /vue-flask-demo目录下新建 backend 目录，并进入backend目录

```
$ mkdir backend
$ cd backend
```

安装pipenv(也可以使用virtualenv等虚拟环境)

```
$ pip install pipenv
// 安装pipenv虚拟环境
$ pipenv install 
// 安装必要的包
$ pipenv install flask 
$ pipenv install flask-restful
$ pipenv install flask-cors
```

新建app.py

``` 
touch app.py
```

在app.py 中添加代码

```
from flask import Flask


app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
```

进入虚拟环境

```
$ pipenv shell
```

运行flask程序

```
$ flask run
```

一个简单的flask程序就运行在5000端口上了。

app.py 中的代码使得对flask程序的访问跳转到对vue页面的访问。

>  此时访问 http://localhost:5000 应该就能看到home页面了。

###### 2. 示例API

在/backend/目录下创建/apis目录，用户放置所有的API

在/backend/apis/ 目录下创建 testapi.py

进入如下代码

```python
import json
from flask import Flask
from flask import jsonify,make_response
from flask_restful import Resource

class TestAPI(Resource):
	def get(self):
		token = 'this is a test string'
		response = make_response(jsonify(code=0,data={'token':token},message='OK'))
		return response
```

在app.py 中声明刚刚创建的API

```python
from flask import Flask, render_template
from flask_restful import Api
from apis.testapi import TestAPI
app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")


api = Api(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


api.add_resource(TestAPI, '/api/test', endpoint='test')
```

> 此时访问 http://localhost:5000/api/test 应该能看到后端返回的json

###### 3. 跨域

通过flask_cors 实现跨域

```
from flask import Flask, render_template
from flask_restful import Api
from apis.testapi import TestAPI
from flask_cors import CORS


app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")


api = Api(app)
# 请求跨域
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


api.add_resource(TestAPI, '/api/test', endpoint='test')
```