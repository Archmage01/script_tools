#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 17:07:00

import  sys,os,re 

sig_cmake = \
"""
# Auto CMakeLists.txt: frame  with  cppunit  use for lintcode/leetcode 
# minimum  cmake  version  
cmake_minimum_required(VERSION 3.7)

# top  project name
PROJECT(%(prjname)s)
SET(mname  %(prjname)s  )
SET( cppunit_test  cppunit_%(prjname)s_test )
SET( ROOTPATH ${CMAKE_SOURCE_DIR})

# defining common source variables
aux_source_directory(src   SRC )
aux_source_directory(test  TESTSRC )


#include(${ROOTPATH}/excmake/global.cmake)

message(">>>> cppbuilder init start:")
if(SRC)
    #add_executable( ${mtest}  ${SRC} )
    ADD_LIBRARY( ${mname}  ${SRC})   #生成库
    message("project src file show: ")
        foreach(_var ${SRC})
            message("   ${_var}")
        endforeach()
    message(" ")
endif(SRC)


#cppunit  test for  moduel
if(TESTSRC)
    #include_directories(lib)
    #target_link_libaraies
    add_executable( ${cppunit_test}  ${SRC}  ${TESTSRC}  )
        message("cppunit test file show: ")
        foreach(_var ${TESTSRC})
            message("   ${_var}")
        endforeach()
        
    target_link_libraries(
        ${cppunit_test}  
        cppunit
    )
endif(TESTSRC)

message(">>>> cppbuilder init end <<<<")
"""

cppfile_template = \
"""
#include <stdio.h>
#include<stdlib.h>
#include <iostream>


"""


cppunit_testfile = \
"""
#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/ui/text/TestRunner.h>
#include <iostream>

extern "C" 
{
}
#define CPPUNIT_EASSERT(a,b) CPPUNIT_ASSERT_EQUAL((int)a, (int)b)

class  %(prjname)s_test : public CPPUNIT_NS::TestFixture
{
    CPPUNIT_TEST_SUITE(%(prjname)s_test);
    CPPUNIT_TEST(%(prjname)s_test_ver            );
    CPPUNIT_TEST_SUITE_END();

public:
    %(prjname)s_test();
    virtual ~%(prjname)s_test();
    virtual void setUp();
    virtual void tearDown();
    void %(prjname)s_test_ver ();
};

%(prjname)s_test::%(prjname)s_test()
{
}
%(prjname)s_test::~%(prjname)s_test()
{
}

void %(prjname)s_test::setUp()
{
}

void %(prjname)s_test::tearDown()
{
}

void %(prjname)s_test::%(prjname)s_test_ver()
{
}

//将TestSuite注册到一个名为alltest的TestSuite中
CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(  %(prjname)s_test,"%(prjname)s_test");

void  main()
{
    CppUnit::TextUi::TestRunner runner;

    // 增加监听器，eventManager返回TestResult类的对象，维护一个Listener集合，Listener将决定测试过程表现，包括日志输出格式
    //CPPUNIT_NS::BriefTestProgressListener progress;
    // 从注册的TestSuite中获取特定的TestSuite, 没有参数获取未命名的TestSuite.
    CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry("%(prjname)s_test");
    // 添加这个TestSuite到TestRunner中
    runner.addTest( registry.makeTest() );
    // 设置输出，注意对象被runner释放
    //runner.setOutputter(new CPPUNIT_NS::CompilerOutputter(&runner.result(), std::cerr));
    //运行程序
    runner.run();

}


"""

