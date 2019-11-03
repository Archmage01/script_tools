#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 17:07:00

import  sys,os,re 

cppunit_testmain = \
"""
#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/ui/text/TestRunner.h>

#ifdef  CPPUNIT_TEST
void  main()
{
    CppUnit::TextUi::TestRunner runner;
    CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry("cppunit_test_all");
    runner.addTest( registry.makeTest() );
    runner.run();
}
#endif

"""

cppunit_testfile = \
"""
#include <cppunit/extensions/HelperMacros.h>
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
CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(  %(prjname)s_test,"cppunit_test_all");
"""

cppfile_template = \
"""
#include <stdio.h>
#include<stdlib.h>
#include <iostream>


"""

cppfile_template_lintcode = \
"""
#include <iostream>

using  namespace  std ;

class Solution {
public:
    void test()
    {

    }
};


void  main()
{
    
}

"""