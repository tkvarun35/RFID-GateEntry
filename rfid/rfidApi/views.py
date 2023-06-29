from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ctypes import *


# Create your views here.




def index(request):
    print("hello")
    return HttpResponse("Hello world!")

def connect(request):
    # Connection
    global timeout,protocol,ip,port,passwd
    protocol='TCP'
    ip='10.21.66.68'  
    # ip='192.168.1.210'
    port=4370
    passwd=''
    timeout=4000
    params = "protocol=%s,ipaddress=%s,port=%d,timeout=%d,passwd=%s"%(protocol,ip,port,timeout,passwd)
    params=params.encode('ASCII')
    global commpro
    commpro = windll.LoadLibrary("./dll/plcommpro.dll")
    constr = create_string_buffer(params)
    global hcommpro
    hcommpro = commpro.Connect(constr)
    print(hcommpro)
    if(hcommpro>0):
        return HttpResponse(hcommpro)
    elif(hcommpro==-2):
        timeout=50000
        connect('')
        return HttpResponse(hcommpro)
    else:
        return HttpResponse("Connection Failed")

def getDeviceData(request):
    table=request.GET['table']
    table=table.encode('ASCII')
    fieldname='*'
    fieldname=fieldname.encode('ASCII')
    filter=''
    filter=filter.encode('ASCII')
    options=''
    options=options.encode('ASCII')
    query_buf=create_string_buffer(4*1024*1024)
    query_table=create_string_buffer(table)
    query_fieldname=create_string_buffer(fieldname)
    query_filter=create_string_buffer(filter)
    query_options=create_string_buffer(options)
    connect('')
    ret= commpro.GetDeviceData(hcommpro,query_buf,4*1024*1024,query_table,query_fieldname,query_filter,query_options)
    print(ret)
    print(query_buf.value)
    return HttpResponse(query_buf.value)
    # return HttpResponse(tab)

def getRTlog(request):
    rt_log=create_string_buffer(256)
    connect('')
    ret=commpro.GetRTLog(hcommpro,rt_log,256)
    return HttpResponse(rt_log.value )
    # return JsonResponse({'msg':rt_log},safe=False)

def searchDevice(request):
    dev_buf=create_string_buffer(b'',64*1024)
    commpro = windll.LoadLibrary("./dll/plcommpro.dll")
    ret=commpro.SearchDevice("UDP","255.255.255.255",dev_buf)
    print(ret)
    return HttpResponse(dev_buf.value)

def getDeviceParam(request):
    dev_buf=create_string_buffer(2048)
    items=('DeviceID,Door2SensorType,Door1Drivertime,Door3Intertime,InBIOTowWay')
    items=items.encode('ASCII')
    p_items=create_string_buffer(items)
    print(p_items)
    connect('')
    ret=commpro.GetDeviceParam(hcommpro,dev_buf,256,p_items)
    return HttpResponse(dev_buf.value)

def setDeviceParam(request):
    items="DeviceID=1,Door1SensorType=2 ,Door1DriverTime=6,Door2Intertime=0"
    p_items=create_string_buffer(items.encode('ASCII'))
    connect('')
    ret=commpro.SetDeviceParam(hcommpro,p_items)
    print(ret)
    return HttpResponse(ret)

def restart(request):
     operation_id=3
     door_id=0
     index=0
     state=0 
     reserved=0
     connect('')
     ret=commpro.ControlDevice(hcommpro,operation_id,door_id,index,state,reserved)
     print(ret)
     return HttpResponse(ret)


def addUser(request):
    table="user"
    table2="userauthorize"
    pin=int(request.GET['pin'])
    cardno=int(request.GET['cardno'])
    password=int(request.GET['pswd'])
    name=request.GET['name']
    timezone=int(request.GET['timezone'])
    door=int(request.GET['door'])
    data= "Pin=%d\tCardNo=%d\tPassword=%d\tName=%s"%(pin,cardno,password,name)
    data2="Pin=%d\tAuthorizeTimezoneId=%d\tAuthorizeDoorId=%d"%(pin,timezone,door)
    p_table=create_string_buffer(table.encode('ASCII'))
    p_table2=create_string_buffer(table2.encode('ASCII'))
    str_buf=create_string_buffer(data.encode('ASCII'))
    str_buf2=create_string_buffer(data2.encode('ASCII'))
    connect('')
    ret=commpro.SetDeviceData(hcommpro,p_table,str_buf,'')      #add data in user table
    ret2=commpro.SetDeviceData(hcommpro,p_table2,str_buf2)      ##add data in userauthorize table
    print(ret)
    print(ret2)
    return HttpResponse(ret2)

def deleteUser(request):
    table="user"
    table2="userauthorize"
    data="Pin=%d"%(int(request.GET['pin']))
    p_table=create_string_buffer(table.encode('ASCII'))
    p_table2=create_string_buffer(table2.encode('ASCII'))
    p_data=create_string_buffer(data.encode('ASCII'))
    print(p_data)
    connect('')
    ret=commpro.DeleteDeviceData(hcommpro,p_table,p_data,'')     #delete data from user table
    ret2=commpro.DeleteDeviceData(hcommpro,p_table2,p_data,'')   #delete data from userauthorize table
    print(ret)
    print(ret2)
    return HttpResponse(ret2)

