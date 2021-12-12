assemble_fun_head = \
"""
//需上级函数提供存储空间
int cjson_assemble_deal(char *pdataOut,int maxlen)
{"""

assemble_fun_middle = \
"""
    char* str = NULL;
    int dwRet = ERROR;
    
    if((NULL == pdataOut)||(maxlen<=0))
    {
        printf("\\r\\n[%s %d] pdataOut is null or maxlen err!",__FUNCTION__,__LINE__);
        dwRet = ERROR;
        goto end;
    }
"""
assemble_fun_tail = \
"""

    dwRet = OK;

    str = cJSON_Print(js_root);
    if(NULL == str)
    {
        printf("\\r\\n[%s %d] json to str err!",__FUNCTION__,__LINE__);
        dwRet = ERROR;
        goto end;
    }
    strncpy(pdataOut,str,maxlen);
end:
    if(js_root)
    {
        cJSON_Delete(js_root);
    }
    if(str)
    {
        free(str);
    }
    return dwRet;
}
"""
assemble_item_var = \
"""
    cJSON* js_{node_name} = NULL;"""


assemble_create_item = \
"""

    js_{node_name} = cJSON_Create{type}({fn_param});"""

assemble_father_add_item = \
"""
    cJSON_AddItemTo{type}(js_{father_name}{extra_info},js_{node_name});"""



analyse_fun_head = \
"""
int cjson_analyse_deal(cJSON* js_root)
{
"""

analyse_fun_middle = \
"""
    int dwRet = ERROR;
"""

analyse_fun_tail = \
"""
    dwRet = OK;
end:
    
    return dwRet;
}
"""

analyse_item_var = \
"""
    cJSON* js_{node_name} = NULL;"""

analyse_array_var = \
"""
    cJSON* js_Array{array_name} = NULL;
    cJSON* js_ArrayItem{array_name} = NULL;
    int dwArraySize{array_name} = 0;
    int i_{array_name} = 0;"""

analyse_item = \
"""
    js_{node_name} = cJSON_GetObjectItem(js_{object_name},"{node_name}");
    if((NULL == js_{node_name}) || (cJSON_{type} != js_{node_name}->type))
    {{
        printf("\\r\\n[%s %d] js_{node_name} err!",__FUNCTION__,__LINE__);
        dwRet = ERROR;
        goto end;
    }}
    // TODO:
"""

analyse_array = \
"""
    js_Array{array_name} = cJSON_GetObjectItem(js_{object_name},"{array_name}");
    if(NULL == js_Array{array_name} || (cJSON_Array != js_Array{array_name}->type))
    {{
        printf("\\r\\n[%s %d] js_Array{array_name} err!",__FUNCTION__,__LINE__);
        dwRet = ERROR;
        goto end;
    }}
    dwArraySize{array_name} = cJSON_GetArraySize(js_Array{array_name});
    for(i_{array_name} = 0 ; i_{array_name} < dwArraySize{array_name}; i_{array_name}++)
    {{
        js_ArrayItem{array_name} = cJSON_GetArrayItem(js_Array{array_name},i_{array_name});
        if(NULL == js_ArrayItem{array_name})
        {{
            printf("\\r\\n[%s %d] js_ArrayItem{array_name} err!",__FUNCTION__,__LINE__);
            dwRet = ERROR;
            goto end;
        }}
        // TODO:
    }}
"""
test_content1 = """
    {
        "name":"xiaoming",
        "age":18,
        "info":
        {
            "addr":"M78",
            "likedrink":false,
            "book":null        
        },
        "school":
        [
            "tasixiaoxue",
            "ruzhouyizhong",
            "pingdingshanyizhong"
        ],
        "school1":
        [
            "tasixiaoxue",
            "ruzhouyizhong",
            "pingdingshanyizhong"
        ]
    }
    """

test_content2 = """
    {
        "name":"xiaoming",
        "age":18,
        "info":
        {
            "addr":"M78",
            "likedrink":false,
            "book":null        
        },
        "school":
        [
            {"xiaoxue":"tasixiaoxue"},
            {"chuzhong":"ruzhouyizhong"},
            {"gaozhong":"pingdingshanyizhong"}
        ]
        ,
        "school1":
        [
            {"xiaoxue":"tasixiaoxue"},
            {"chuzhong":"ruzhouyizhong"},
            {"gaozhong":"pingdingshanyizhong"}
        ]
    }
    """