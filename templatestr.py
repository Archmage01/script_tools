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
            print("�ļ�:%s �Ѿ�����"%file )
        pass



stub_temlate = \
"""
/*-  %(countnum)s  %(name)s ׮���� */
uint8_t   __%(name)s_stub_flag = 0 ; /*-< %(name)s������׮��ʶ��Ĭ�ϲ���׮ */
uint32_t  __%(name)s_cfg_num   = 0 ; /*-< %(name)s����Ĭ�����������Ϊ0       */
uint32_t  __%(name)s_run_loop  = 0 ; /*-< %(name)s����Ĭ�ϵ�ǰִ�д���Ϊ0 */ 
%(return_type)s   *__%(name)s_ret_list  = NULL ; /*-< %(name)s������������ֵ�б�NULL  */ 

void %(name)s_stub_cfg(uint8_t stub,uint32_t num, %(return_type)s  *ret_list )
{
    __%(name)s_stub_flag = stub;   
    __%(name)s_cfg_num   = num;
    __%(name)s_run_loop  = 0;
    __%(name)s_ret_list  = ret_list;/*-< ����������� */ 
}

/*- ��˵������ */          
EXTERN_C_LINKAGE  %(return_type)s   %(function_def)s ;

EXTERN_C_LINKAGE  %(return_type)s   CppTest_Stub_%(function_def)s
{
    /*- ���÷���ֵ,����ָ�� */
    %(return_type)s  ret  = 0;
    /*- ׮����ִ�д��� */
    uint32_t index = __%(name)s_run_loop;
    
    /*- ���װ��־λΪ0,��ִ��ԭ����  */
    if(0 == __%(name)s_stub_flag)
    {
        return %(function_def)s;
    }
    /*- ִ�д�׮���� */
    else
    {
        /*- ������õĺ�����1 */
        __%(name)s_run_loop++;
        /*- ��ӡ����ִ�д���,�۲쵽����û�б�ִ�к͵��������˶�����,���ڲ鿴������ */
        printp("index = %%d %%d %%d\\n",index,__%(name)s_run_loop,__%(name)s_cfg_num);
        /*- ��������Ĵ����Ѿ����ڲ����� */
        if(__%(name)s_run_loop >= __%(name)s_cfg_num)
        {
            /*- ��ôȥȡ���һ�ε������� */
            __%(name)s_run_loop--;
        }
        printp("index = %%d %%d %%d\\n",index,__%(name)s_run_loop,__%(name)s_cfg_num);
        /*- ���indexС�ں�����ֵ*/
        if(index <  __%(name)s_cfg_num)
        {   
            ret = __%(name)s_ret_list[index];
        }
        else
        {
            /*- ׮�������,�˺����޷�����  */
            printp("\\n\\n ׮�������:%%d ,%%d\\n\\n",__FILE__,__LINE__);
            /*- ������ѭ�� */
            while(1){};
        }
        /*- �����б� */
        return (ret);
    }
}
"""



'''
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
    if  function_def is not  None:
        function_def  = function_def.group()
        print(function_def)
    else:
        function_def = "NULL"

    keymap = {'name': name_real,'function_def': function_def,
    'return_type': ret_type,'countnum':str(countnum) }

    if False == os.path.exists("test_stubs.c"):
        pass
        #os.remove("test_stubs.c")
        #testfile = open("test_stubs.c","w")   
        # testfile.write(stub_temlate%keymap)
        # testfile.close()
    else:
        pass
        # testfile = open("test_stubs.c","a")   
        # testfile.write(stub_temlate%keymap)
        # testfile.close()
'''


outline_patt_00   =  re.compile(r'(;$)')  #����    ; �������� ������
outline_patt_01   =  re.compile(r'(.*\*/$)')      # ���˵��ĸ�ʽע��  /*-  */   
outline_patt_02   =  re.compile(r'^(//)|^(/\*)')  # ���˵��ĸ�ʽע��  /*-  */  
ret_typepatt01    =  re.compile(r'^(\w+\s)|^(\w+\*)')      #��ĸ + �հ� 
ret_typepatt02    =  re.compile(r'(\)$)')          #)��β
ret_typepatt03    =  re.compile(r'^(\w+\s+\*)|^(\w+\*)')      #��ĸ + �հ� + *
functionname_patt = re.compile(r'(\w$)')      #��ĸ��β



def  create_stubs_file(functionname, countnum):
    str_const  = "const"
    str_static = "static"
    functionname = functionname.strip() 
    fault_line00 = outline_patt_00.search(functionname)
    fault_line01 = outline_patt_01.search(functionname)
    fault_line02 = outline_patt_02.search(functionname)
    if  fault_line00 is not None or  fault_line01 is not None  or  fault_line02 is not None: #
        pass
    else:
        ret_type01 = ret_typepatt01.search(functionname)
        ret_type02 = ret_typepatt02.search(functionname)
        if ret_type01 is not None and  ret_type02 is not None:
            #(�ò� ����ʵ�ʹ��˲������� ���㺯�����������)
            ret_type     = ""  #��������ֵ
            name_real    = ""  #��������
            function_def = ""  #����ԭ����
            #print(functionname)
            ret_type03 = ret_typepatt03.search(functionname)
            function_def  =   functionname
            if ret_type03 is not None:
                ret_type = ret_type03.group()
                ret_type = ret_type.split("*")[0]
                ret_type = ret_type.strip() + "  *"
                #�ǲ��Ƿ���ָ��ĺ���   Ŀǰֻ���Ƿ��ص���ָ��ĺ���
                #print(ret_type)
                #��������
                functionname = functionname.split("(")
                t_function_def = functionname[-1]
                functionname = functionname[0].strip()
                name_real = functionname.split("*")[-1].strip()
                #print(functionname)
                function_def = name_real +"("+ t_function_def 
            else:
                ret_type =  ret_type01.group()
                ret_type =  ret_type.strip()
                #��������
                functionname = functionname.split("(")
                t_function_def = functionname[-1]
                functionname = functionname[0].strip()
                name_real = functionname.split(" ")[-1]
                #print(functionname)
                function_def = name_real +"("+ t_function_def 
            print("ret: %s name: %s  def: %s"%(ret_type,name_real,function_def))
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
        else:
            pass
        

if __name__ == "__main__":
    src = [
        "  uint16_t   get_location_base_num(ws_sequence_t *src_sequence_stb, uint32_t   ci_id )",
        "  uint32_t   *get_location_base_id_point(ws_sequence_t  *src_sequence_stb, uint32_t   ci_id ) ", 
    ]
    for  i in range(len(src)):
        create_stubs_file(src[i], i)
        print(" ")
