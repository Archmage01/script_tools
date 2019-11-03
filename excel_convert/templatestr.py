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
    %(descript01)s
    CPPUNIT_TEST_SUITE_END();

public:
    %(name)s_test();
    virtual ~%(name)s_test();
    virtual void setUp();
    virtual void tearDown();
    %(descript02)s
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
    //uint16_t  ret = 0;
    //CPPUNIT_EASSERT(0, ret);
}
//test case
%(case)s

CPPUNIT_TEST_SUITE_REGISTRATION(%(name)s_test );

"""

current_case = \
"""
void %(name)s_test::test_%(name)s_%(casenum)s()
{

}

"""

descript_case_01 = \
"""    
    CPPUNIT_TEST(test_%(name)s_%(casenum)s  );
"""

descript_case_02 = \
"""    
    void  test_%(name)s_%(casenum)s()  ;
"""




# def  create_test_file(classname):
#     for i in range(len(classname)):
#         name = {"name":classname[i] }
#         file = "test_" + classname[i] +".cpp"
#         if False == os.path.exists(file):
#             testfile = open(file,"a")
#             testfile.write(test_template%name)
#             testfile.close()
#         else:
#             print("�ļ�:%s �Ѿ�����"%file )
#         pass
