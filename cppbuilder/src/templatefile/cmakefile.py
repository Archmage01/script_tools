#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 17:07:00

import  sys,os,re 

topcmake = \
"""
# Auto CMakeLists.txt: frame  with  cppunit  use for lintcode/leetcode 
cmake_minimum_required(VERSION 3.7)

message("CMake version: " ${CMAKE_MAJOR_VERSION} .  ${CMAKE_MINOR_VERSION} . ${CMAKE_PATCH_VERSION})
if ( NOT PROJECT_SOURCE_DIR)
    PROJECT(%(prjname)s)
    MESSAGE(STATUS "## Making project " ${CMAKE_PROJECT_NAME})
    SET(ROOTPATH ${CMAKE_SOURCE_DIR})
    # INCLUDE(${ROOTPATH}/cm/global.cmake)
    # INCLUDE(${ROOTPATH}/cm/pclint.cmake)
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


#include(${ROOTPATH}/excmake/global.cmake)

message(">>>> cppbuilder init start:")
if(SRC)
    #add_executable( ${mtest}  ${SRC} )
    ADD_LIBRARY( ${mname}  ${SRC})   
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


lintcode_cmake = \
"""
# Auto CMakeLists.txt: use for lintcode/leetcode 
# minimum  cmake  version  
cmake_minimum_required(VERSION 3.7)

# top  project name
SET( mname  Solution  )

# defining common source variables
aux_source_directory(main   SRC )

message(">>>> cppbuilder init start: \n")
if(SRC)
    add_executable( t_${mname}  ${SRC} )
endif(SRC)

message(">>>> cppbuilder init end <<<<\n")
"""