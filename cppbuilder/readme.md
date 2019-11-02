# 本工具用于构建C/C++模板工程 

## 1   工程目录结构


    |  CMakeLists.txt  --顶层cmake文件
    |  
    |——target       --用于存放生成的target文件
    |——cmake        --cmake文件
    |——lib          --外部依赖的库文件
    |——include      --外部依赖模块的头文件
    |——src          --模块源代码
        |——include  --模块内部头文件
        |——main     --源代码
        |——cppunit  --单元测试

---
