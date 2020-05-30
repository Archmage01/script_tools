#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-15 13:48:41


topcmake = \
"""
# Auto CMakeLists.txt: frame  with  cppunit  use for lintcode/leetcode 
cmake_minimum_required(VERSION 3.7)

message("CMake version: " ${CMAKE_MAJOR_VERSION} .  ${CMAKE_MINOR_VERSION} . ${CMAKE_PATCH_VERSION})
if ( NOT PROJECT_SOURCE_DIR)
    PROJECT(%(prjname)s)
    MESSAGE(STATUS "## Making project " ${CMAKE_PROJECT_NAME})
    SET(ROOTPATH ${CMAKE_SOURCE_DIR})
endif()

add_subdirectory(src)

if (EXISTS ${CMAKE_SOURCE_DIR}/modsrc)
    file(GLOB MODSRC_SUB "modsrc/*")
    foreach(sd ${MODSRC_SUB})
        file(RELATIVE_PATH f ${CMAKE_SOURCE_DIR} ${sd})
        message(STATUS "Add modsrc sub directory: ${f}")
        add_subdirectory(${f})
    endforeach()
endif()
"""


src_leve_cmake = \
"""
# Auto CMakeLists.txt: frame  with  cppunit  use for lintcode/leetcode 
# minimum  cmake  version  
cmake_minimum_required(VERSION 3.7)

# top  project name
SET(mname  %(prjname)s  )
SET( cppunit_test  cppunit_%(prjname)s_test )
SET( ROOTPATH ${CMAKE_SOURCE_DIR})

# defining common source variables
aux_source_directory(main   SRC )
aux_source_directory(test_cppunit  TESTSRC )


    SET(LIBRARY_OUTPUT_PATH ${ROOTPATH}/lib) 
    SET(EXECUTABLE_OUTPUT_PATH ${root}/bin) 
    SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${ROOTPATH}/bin/Debug ) 
    MESSAGE(STATUS "library_output_path   : " ${LIBRARY_OUTPUT_PATH} )
    MESSAGE(STATUS "executable_output_path: " ${EXECUTABLE_OUTPUT_PATH} )
    MESSAGE(STATUS "cmake_runtime_output_directory_debug: " ${CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG} )



#include(${ROOTPATH}/excmake/global.cmake)

if(MSVC)
  # Force to always compile with W4
  if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "/W4" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
  else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
  endif()
  MESSAGE("-- CMAKE_CXX_FLAGS:  " ${CMAKE_CXX_FLAGS} \n )
elseif(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
  # Update if necessary
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-long-long -pedantic")
endif()

message(">>>> cppbuilder init start:")
if(SRC)
    include_directories(include)
    #add_executable( t_${mname}  ${SRC} )
    ADD_LIBRARY( ${mname}  ${SRC})  
    SET(LIBRARY_OUTPUT_PATH ${ROOTPATH}/lib) 
     
    #ADD_LIBRARY( ${mname}  SHARED ${SRC})   
    message("project src file show: ")
        foreach(_var ${SRC})
            message("   ${_var}")
        endforeach()
    message(" ")
    
    SET(EXECUTABLE_OUTPUT_PATH ${ROOTPATH}/bin) 
    SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${ROOTPATH}/bin/Debug ) 
endif(SRC)


#cppunit  test for  moduel
if(TESTSRC)
    #include_directories(lib)
    add_definitions(-DCPPUNIT_TEST)
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


leetcode_cmake = \
"""
# Auto CMakeLists.txt: use for lintcode/leetcode 
# minimum  cmake  version  
cmake_minimum_required(VERSION 3.7)

# top  project name
SET( mname  Solution  )

# defining common source variables
aux_source_directory(main   SRC )

    SET(LIBRARY_OUTPUT_PATH ${ROOTPATH}/lib) 
    SET(EXECUTABLE_OUTPUT_PATH ${root}/bin) 
    SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${ROOTPATH}/bin/Debug ) 
    MESSAGE(STATUS "library_output_path   : " ${LIBRARY_OUTPUT_PATH} )
    MESSAGE(STATUS "executable_output_path: " ${EXECUTABLE_OUTPUT_PATH} )
    MESSAGE(STATUS "cmake_runtime_output_directory_debug: " ${CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG} )


if(MSVC)
  # Force to always compile with W4
  if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "/W4" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
    MESSAGE("-- CMAKE_CXX_FLAGS:  " ${CMAKE_CXX_FLAGS} \n )
  else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
  endif()
elseif(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
  # Update if necessary
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-long-long -pedantic")
endif()

message("==================== cppbuilder init start: ====================")
if(SRC)
    ADD_LIBRARY( ${mname}_static  STATIC  ${SRC} )   
    #ADD_LIBRARY( ${mname} SHARED  ${SRC} )
    add_executable( t_${mname}  ${SRC} )
endif(SRC)

message("==================== cppbuilder   init  end ====================")
"""

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
#include <stdlib.h>
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


hhp_template = \
"""
#ifndef  __%(prjname)s_H__
#define  __%(prjname)s_H__

#ifdef __cplusplus
extern "C" {
#endif


//extern  int  myadd(int x, int y) ;



#ifdef __cplusplus
}
#endif

#endif



"""

base_header_hhp =\
"""
#ifndef  __BASEPUBLIC_H__
#define  __BASEPUBLIC_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef signed char         int8_t  ;
typedef short               int16_t ;
typedef int                 int32_t ;
typedef unsigned char       uint8_t ;
typedef unsigned short      uint16_t;
typedef unsigned int        uint32_t;
typedef unsigned long long  uint64_t;
typedef signed   long long  int64_t ;

#if  defined(CPPUNIT_TEST) 
    /*-   用于单元测试 -*/ 
    #define  STATIC  
    #define  CONST  

#else
    #define  STATIC   static 
    #define  CONST    const 
#endif

#ifndef NULL
    #define NULL (void *)(0)
#endif

/*-   模块描述 -*/ 
typedef struct _mod_dscrp
{
	char     name[15]   ;	/*- 模块名称   */
	char     time[31]   ;	/*- 编译时间   */
	uint8_t  major      ;	/*- 主要版本号 */
	uint8_t  minor      ;	/*- 次要版本号 */
	uint16_t patch      ;	/*- 修订版本号 */
}mod_dscrp_t;


/*-   宏定义  */
#define DLLAPI  extern "C" __declspec(dllexport)   

#define _SIZE_OFFSET(t,m) (uint32_t)(&((t*)0)->m)								/*- 获得type类型结构体成员的在目标地址的宽度偏移量 */
#define _SIZE_OFFSET_ARRAY(t,arr,index,m) (uint32_t)(&(((t*)0)->arr[index].m))	/*- 获得type类型结构体内成员结构体数组的各成员在目标地址的宽度偏移量 */
#define _TABLE(n)   n##_table      /*-  表格变量的名称    */
#define _TABLE_L(n) n##_table_len  /*-  表格长度变量的名称 */


#define PF              printf("[%12.12s][%.04d]", (strrchr(__FILE__, '\\\\')?strrchr(__FILE__, '\\\\')+1 : __FILE__),__LINE__ )
#define WSPNE(x,...)    do{printf(x,##__VA_ARGS__); }while(0)


#define  EASSERT(a,b)   do{if((int)a != (int)(b)){ PF;WSPNE(" fail: %d  %d \\n ",a,b); exit(1);  }}while(0)



#ifdef __cplusplus
}
#endif

#endif

"""