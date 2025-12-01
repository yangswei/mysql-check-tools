# OP工具介绍
  
## 开箱即用
```
1. 下载项目
2. 准备sql文件与目标库配置文件，分别放在app/sql与app/output目录下
3. 安装依赖 pip install --no-cache-dir -r requirements.txt
4. 启动项目 python run.py  默认启动在5000端口，可修改run.py中的端口号
```


## 镜像用法  

```shell
1. 在dockerfile所在目录执行
docker build -t  sqlcheckTools:v1 .

2.准备运行环境
mkdir -p sqlcheckdir
cd sqlcheckdir
mkdir sql output  config 
docker run -d -p 5000:5000 --name dop-tools -v $(pwd)/sql:/dop-tools/app/sql -v $(pwd)/output:/dop-tools/app/output -v $(pwd)/config:/dop-tools/app/config  dop-tools:v1

3. 检测配置
    3.1 要检测的数据库配置信息写到config/database_config.yaml文件中
    databases:
      # 默认数据库
      default:
        host: "localhost"
        port: 3306
        username: "root"
        password: "xxxxxxx"
        charset: "utf8mb4"
    3.2  将初始化的sql文件放到sql目录中
    3.3  调用接口http://ip:5000/sqlprase   将sql目录中的sql文件解析为json文件，输出到output目录下

4. 调用接口http://ip:5000/sqlcheck/<string:fileName>   将output目录下的json文件进行数据库校验，输出到output目录下   (如果有已经转移好的json或者yaml文件，可以直接放到output目录下，调用检测接口)
```



## 目录介绍
```shell  
dop-tools
├── config                配置文件,如数据库配置
├── models                模型层(数据校验部分未用到)
├── output                输出目录(将sql目录的sql文件生成到此目录下)
├── serivces              service层(核心业务逻辑)
├── sql                   sql文件目录(存放sql文件)
├── utils                 工具类
├── instance              实例(sqlite数据库实例)
├── mysql-local-test      本地mysql测试
``` 

## 接口说明
  

| 接口名称 | 请求方法 | 接口路径 | 描述 |
|---------|----------|----------|------|
| sql解析 | GET | `/sqlprase` | sql解析接口,通过MySQLSchemaParser类将sql转换为dict对象，通过DictFileConverter类转换为json文件 |
| sql校验 | GET | `/sqlcheck/<string:fileName>` | 首先通过DictFileConverter类将从output目录下去找指定名字json文件转换为dict对象,通过DatabaseValidator类校验数据库,输出md格式校验报告 |


## 其他


**MySQLSchemaParser** 主方法parse_sql_file，接收一个sql文件路径参数，解析SQL文件，返回数据库结构字典
```python
    sqlChecker = MySQLSchemaParser()
    file_path = 'app/sql/2.sql'
    sqlDict = sqlChecker.parse_sql_file(file_path)
```

**sqldictTofile** 中包含两个类，file_to_dict和dict_to_file
```python
    不指定type时，默认是json
    dict_to_file(sample_data, "output/data.yaml", "yaml")
    dict_to_file(sample_data, "output/data.json", "json")
    file_to_dict(file_path)
```

**DatabaseValidator**
```python
    validator = DatabaseValidator()
    validator.validate_schema(sqlDicte, "app/output/database_validation.md")
```


