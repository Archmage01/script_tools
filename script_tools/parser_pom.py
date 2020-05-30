#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-28 12:14:30


import xml.etree.ElementTree  as ET  #引入ElementTree的包


# 当要获取属性值时，用attrib方法。 
# 当要获取节点值时，用text方法。 
# 当要获取节点名时，用tag方法

tree = ET.parse("pom.xml") #parse方法读取xml文件，得到元素树
root = tree.getroot() 

print(root)
print('root-tag:',root.tag,',root-attrib:',root.attrib,',root-text:',root.text)
# for child in root:
#     print('child-tag是：',child.tag,',child.attrib：',child.attrib,',child.text：',child.text)
#     for sub in child:
#         print("子节点:",sub.getchildren())
#         for dp  in sub:
#             print("dp子节点:",dp.getchildren())
#             print(dp)
#             print('sub-tag是：',dp.tag,',sub.attrib：',dp.attrib,',sub.text：',dp.text)


## 不要递归太多层
def  xml_p(root):
    if root:
        for child in root:
            if  child.getchildren: #有子节点
                xml_p(child)
                if child.text :
                    if root.tag == "project"  and  child.tag == "artifactId":
                        print("模块名: ", child.text )
                    print("tag:",child.tag, "text:",child.text )
    else:
        return 


xml_p(root)