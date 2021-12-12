import json
from json import JSONDecodeError

from jsonRes import *

class Bussiness:
    def set_ui(self,Ui):
        self.ui = Ui

    def output_to_ui(self,data):
        self.ui.plainTextEdit_2.setPlainText(data)

    def do_translate(self):
        inputText = self.ui.plainTextEdit.toPlainText()
        self.text_input(inputText,self.ui.comboBox.currentIndex())

    def text_input(self,inputText,optIndex):
        print(inputText)
        try:
            jsdata = json.loads(inputText)
            print(jsdata)
            #纯数字会被识别为json,需要进行判断，合法数据会进入ValueError
            if isinstance(int(inputText),int):
                print("err json int")
                self.output_to_ui("err json int")
                return
        except JSONDecodeError:
            print("err json")
            self.output_to_ui("err json")
            return
        except ValueError:
            #正常流程
            data = self.data_deal(jsdata,optIndex)
            self.output_to_ui(data)


    def text_input_test(self,inputText,optIndex):
        print(inputText)

        try:
            jsdata = json.loads(inputText)
            print(jsdata)
            #纯数字会被识别为json,需要进行判断，合法数据会进入ValueError
            if isinstance(int(inputText),int):
                print("err json int")
                return
        except JSONDecodeError:
            print("err json")
            return
        except ValueError:
            #正常流程
            data = self.data_deal(jsdata,optIndex)
            print(data)



    def data_deal(self,jsdata,type):
        if type == 0:
            data = self.assemble_process(jsdata) + self.analyse_process(jsdata)
        elif type == 1:
            data = self.assemble_process(jsdata)
        elif type == 2:
            data = self.analyse_process(jsdata)
        return data


    def assemble_process(self,jsdata):
        head_data = ""
        middle_data = ""
        tail_data = ""

        head_data += assemble_fun_head

        head_data += assemble_item_var.format(node_name = "root")
        tail_data += assemble_create_item.format(node_name = "root",
                                                type = "Object",
                                                 fn_param = "")

        for subItemName in jsdata:
            subItemValue = jsdata[subItemName]
            head_data_tmp,tail_data_tmp = self.json_assemble_traversal(subItemName,
                                                                            subItemValue,
                                                                            "root",
                                                                            "Object")
            head_data += head_data_tmp
            tail_data += tail_data_tmp


        tail_data += assemble_fun_tail

        middle_data += assemble_fun_middle

        return head_data+middle_data+tail_data

    #jsonType 1 object 2 array

    def json_assemble_traversal(self,itemName,itemValue,fatherName,fatherJsonType):
        head_data = ""
        tail_data = ""

        if isinstance(itemValue,dict):
            print("dict")
            objectName = itemName
            objectJson = itemValue
            node_name = itemName

            head_data += assemble_item_var.format(node_name = node_name)
            tail_data += assemble_create_item.format(node_name = node_name,
                                                     type = "Object",
                                                     fn_param = "")
            tail_data += assemble_father_add_item.format(type = fatherJsonType,
                                father_name = fatherName,
                                extra_info = ",\""+itemName+"\"" if fatherJsonType == "Object" else "",
                                node_name = node_name)

            for subItemName in objectJson:
                subItemValue = objectJson[subItemName]
                head_data_tmp,tail_data_tmp = self.json_assemble_traversal(subItemName,
                                                                                subItemValue,
                                                                                objectName,
                                                                                "Object")
                head_data += head_data_tmp
                tail_data += tail_data_tmp
        elif isinstance(itemValue,list):
            print("list")
            arrayName = itemName
            arrayJson = itemValue
            node_name = itemName
            
            head_data += assemble_item_var.format(node_name = node_name)
            tail_data += assemble_create_item.format(node_name = node_name,
                                                     type = "Array",
                                                     fn_param = "")
            tail_data += assemble_father_add_item.format(type = fatherJsonType,
                                 father_name = fatherName,
                                 extra_info = ",\""+itemName+"\"" if fatherJsonType == "Object" else "",
                                 node_name = node_name)

            for i, subItem in enumerate(arrayJson):
                head_data_tmp,tail_data_tmp = self.json_assemble_traversal(arrayName+"_"+str(i),
                                                                                subItem,
                                                                                arrayName,
                                                                                "Array")
                head_data += head_data_tmp
                tail_data += tail_data_tmp
        elif isinstance(itemValue,bool):
            print("bool")
            node_name = fatherName+"_"+itemName
            head_data += assemble_item_var.format(node_name = node_name)
            tail_data += assemble_create_item.format(node_name = node_name,
                                                     type = "Bool",
                                                     fn_param = "TRUE" if itemValue == True else "FALSE")
            tail_data += assemble_father_add_item.format(type = fatherJsonType,
                                 father_name = fatherName,
                                 extra_info = ",\""+itemName+"\"" if fatherJsonType == "Object" else "",
                                 node_name = node_name)
        elif isinstance(itemValue,int):
            print("int")
            node_name = fatherName+"_"+itemName
            head_data += assemble_item_var.format(node_name = node_name)
            tail_data += assemble_create_item.format(node_name = node_name,
                                                     type = "Number",
                                                     fn_param = itemValue)
            tail_data += assemble_father_add_item.format(type = fatherJsonType,
                                 father_name = fatherName,
                                 extra_info = ",\""+itemName+"\"" if fatherJsonType == "Object" else "",
                                 node_name = node_name)

        elif isinstance(itemValue,str):
            print("str")
            node_name = fatherName+"_"+itemName
            head_data += assemble_item_var.format(node_name = node_name)
            tail_data += assemble_create_item.format(node_name = node_name,
                                                     type = "String",
                                                     fn_param = "\""+itemValue+"\"")
            tail_data += assemble_father_add_item.format(type = fatherJsonType,
                                 father_name = fatherName,
                                 extra_info = ",\""+itemName+"\"" if fatherJsonType == "Object" else "",
                                 node_name = node_name)

        else:
            print("other")
            node_name = fatherName+"_"+itemName
            head_data += assemble_item_var.format(node_name = node_name)
            tail_data += assemble_create_item.format(node_name = node_name,
                                                     type = "Null",
                                                     fn_param = "")
            tail_data += assemble_father_add_item.format(type = fatherJsonType,
                                 father_name = fatherName,
                                 extra_info = ",\""+itemName+"\"" if fatherJsonType == "Object" else "",
                                 node_name = node_name)

        return (head_data,tail_data)





    def analyse_process(self,jsdata):
        head_data = ""
        middle_data = ""
        tail_date = ""

        head_data += analyse_fun_head

        head_data_tmp,tail_date_tmp = self.json_analyse_traversal(jsdata,"root")
        head_data += head_data_tmp
        tail_date += tail_date_tmp

        tail_date += analyse_fun_tail

        middle_data += analyse_fun_middle

        return head_data+middle_data+tail_date


    def json_analyse_traversal(self,jsonObject,ObjectName):
        head_data = ""
        tail_data = ""
        for itemName in jsonObject:
            itemValue = jsonObject[itemName]
            print(itemName,end="+")
            print(itemValue,end=" ")

            if isinstance(itemValue,dict):
                print("dict")
                head_data += analyse_item_var.format(node_name = itemName)
                tail_data += analyse_item.format(node_name = itemName,object_name=ObjectName,type = "Object")

                head_data_tmp,tail_data_tmp = self.json_analyse_traversal(itemValue,itemName)

                head_data += head_data_tmp
                tail_data += tail_data_tmp
            elif isinstance(itemValue,list):
                print("list")
                head_data += analyse_array_var.format(array_name = itemName)
                tail_data += analyse_array.format(array_name = itemName,object_name=ObjectName,type = "Array")
            elif isinstance(itemValue,bool):
                print("bool")
                head_data += analyse_item_var.format(node_name = itemName)
                tail_data += analyse_item.format(node_name = itemName,object_name=ObjectName,
                                                 type = "True" if itemValue == True else "False")

            elif isinstance(itemValue,int):
                print("int")
                head_data += analyse_item_var.format(node_name = itemName)
                tail_data += analyse_item.format(node_name = itemName,object_name=ObjectName,type = "Number")
            elif isinstance(itemValue,str):
                print("str")
                head_data += analyse_item_var.format(node_name = itemName)
                tail_data += analyse_item.format(node_name = itemName,object_name=ObjectName,type = "String")

            else:
                print("other")
                head_data += analyse_item_var.format(node_name = itemName)
                tail_data += analyse_item.format(node_name = itemName,object_name=ObjectName,type = "NULL")

        return (head_data,tail_data)




if __name__ == '__main__':
    bussiness = Bussiness()

    bussiness.text_input_test(test_content2,0)