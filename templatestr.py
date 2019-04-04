#!/usr/bin/env python3 
# -*- coding:gbk -*-
# Author: yang.gan  2019-2-18 12:13:15


import  sys,os,re, getopt


test_template = \
"""
#include <cppunit/extensions/HelperMacros.h>

#include "unifw.h"

extern "C" 
{
    void app_logic_post(uint32_t msg) {};
    void app_error_post(uint32_t msg) {};
}

class %(name)s_test : public CPPUNIT_NS::TestFixture
{
    CPPUNIT_TEST_SUITE(%(name)s_test     );
    CPPUNIT_TEST(test_%(name)s_test      );
    CPPUNIT_TEST_SUITE_END();

public:
    %(name)s_test();
    virtual ~%(name)s_test();
    virtual void setUp();
    virtual void tearDown();
    void test_%(name)s_test() ;
};

%(name)s_test::%(name)s_test()
{
}

%(name)s_test::~%(name)s_test()
{
}

void %(name)s_test::setUp()
{
}


void %(name)s_test::tearDown()
{
}

void %(name)s_test::test_%(name)s_test()
{
    uint16_t  ret = 0;



    CPPUNIT_EASSERT(0, ret);
}


CPPUNIT_TEST_SUITE_REGISTRATION(%(name)s_test);

"""    


def  create_test_file(classname):
    for i in range(len(classname)):
        name = {"name":classname[i] }
        file = "test_" + classname[i] +".cpp"
        if False == os.path.exists(file):
            testfile = open(file,"a")
            testfile.write(test_template%name)
            testfile.close()
        else:
            print("文件:%s 已经存在"%file )
        pass



stub_temlate = \
"""
/*-  %(countnum)s  %(name)s 桩函数 */
uint8_t   __%(name)s_stub_flag = 0 ; /*-< %(name)s函数打桩标识：默认不打桩 */
uint32_t  __%(name)s_cfg_num   = 0 ; /*-< %(name)s函数默认配置项个数为0       */
uint32_t  __%(name)s_run_loop  = 0 ; /*-< %(name)s函数默认当前执行次数为0 */ 
%(return_type)s   *__%(name)s_ret_list  = NULL ; /*-< %(name)s函数函数返回值列表NULL  */ 

void %(name)s_stub_cfg(uint8_t stub,uint32_t num, %(return_type)s  *ret_list )
{
    __%(name)s_stub_flag = stub;   
    __%(name)s_cfg_num   = num;
    __%(name)s_run_loop  = 0;
    __%(name)s_ret_list  = ret_list;/*-< 清除运行周期 */ 
}

/*- 起说明作用 */          
EXTERN_C_LINKAGE  %(return_type)s   %(function_def)s ;

EXTERN_C_LINKAGE  %(return_type)s   CppTest_Stub_%(function_def)s
{
    /*- 设置返回值,返回指针 */
    %(return_type)s  ret  = 0;
    /*- 桩函数执行次数 */
    uint32_t index = __%(name)s_run_loop;
    
    /*- 如果装标志位为0,则执行原函数  */
    if(0 == __%(name)s_stub_flag)
    {
        return %(function_def)s;
    }
    /*- 执行打桩函数 */
    else
    {
        /*- 计算调用的函数加1 */
        __%(name)s_run_loop++;
        /*- 打印函数执行次数,观察到底有没有被执行和到底配置了多少项,便于查看溢出情况 */
        printp("index = %%d %%d %%d\\n",index,__%(name)s_run_loop,__%(name)s_cfg_num);
        /*- 如果函数的次数已经大于测试项 */
        if(__%(name)s_run_loop >= __%(name)s_cfg_num)
        {
            /*- 那么去取最后一次的配置项 */
            __%(name)s_run_loop--;
        }
        printp("index = %%d %%d %%d\\n",index,__%(name)s_run_loop,__%(name)s_cfg_num);
        /*- 如果index小于函数的值*/
        if(index <  __%(name)s_cfg_num)
        {   
            ret = __%(name)s_ret_list[index];
        }
        else
        {
            /*- 桩函数溢出,此函数无法进入  */
            printp("\\n\\n 桩函数溢出:%%d ,%%d\\n\\n",__FILE__,__LINE__);
            /*- 陷入死循环 */
            while(1){};
        }
        /*- 返回列表 */
        return (ret);
    }
}
"""

ret_typepatt01 =  re.compile(r'^(\w+\s)')
ret_typepatt02 =  re.compile(r'^(\w+\s+\*)')
namepatt01 =  re.compile(r'((\W)+\w+)')
temppatt01 =  re.compile(r'(\w+.*)')


def  create_stubs_file(functionname, countnum):
    temp =  functionname.split("(")
    ret_type =  ret_typepatt02.search(temp[0]) 
    # get function  return  type
    if ret_type is not None:
        ret_type = ret_type.group()
        print(ret_type)
    else:
        ret_type =  ret_typepatt01.search(temp[0])  
        if ret_type is not None:
            ret_type = ret_type.group()
            print(ret_type)
        else:
            print("match  function  ret_type err")
    # get  function  name
    name_real =  namepatt01.search(temp[0]) 
    if name_real is not None:
        name_real = name_real.group()
        name_real = name_real.split(" ")
        name_real = name_real[-1]
        print(name_real)
    else:
        print("match  function name  err")

    function_def =  functionname.split(ret_type)
    function_def =  function_def[-1]
    function_def =  temppatt01.search(function_def)
    function_def  = function_def.group()
    print(function_def)

    keymap = {'name': name_real,'function_def': function_def,
    'return_type': ret_type,'countnum':str(countnum) }

    if False == os.path.exists("test_stubs.c"):
        testfile = open("test_stubs.c","a")   
        testfile.write(stub_temlate%keymap)
        testfile.close()
    else:
        testfile = open("test_stubs.c","a")   
        testfile.write(stub_temlate%keymap)
        testfile.close()