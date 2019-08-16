## 一个简单的python web框架

基于PEP3333/PEP333和wsgi尝试实现web框架一般功能

## 目的 

只是了解下类django框架的实现原理。

了解一个东西的方法最好的方法就是拆开、装起来、然后自己造一个。

## 尝试实现的功能
- 请求URL->方法的 绑定/路由  √
- request封装 GET/POST   √
- response封装 模板/JSON/plain text  √  
- 简单模板渲染  √
- command 
- 中间件  √
- session/cookie
- view cache
- 文件上传/下载
- ORM
- 异步IO

## 运行
`cd wsgi_app_test && python run.py`