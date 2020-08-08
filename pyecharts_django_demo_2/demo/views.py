 # -*- coding: utf-8 -*-
from django.shortcuts import render
import json
from django.http import HttpResponse
from pyecharts.charts import Bar,Line
from pyecharts import options as opts 
from pyecharts.globals import ThemeType
import pandas as pd
from datetime import datetime
import sys
sys.path.append(r'C:\Python37\Lib')
import PIIS_Hotel_Client_ALL as PIIS


def response_as_json(data):
    json_str=json.dumps(data)
    response=HttpResponse(json_str,content_type="application/json")
    response["Access-Control-Allow-Origin"]="*"
    return response

def json_response(data,raw_data,code=200):
    data={"code":code,"msg":"success","data":data,'raw_data':raw_data}
    return response_as_json(data)

def json_error(error_string="error",code=500,**kwargs):
    data={"code":code,"msg":error_string,"data":{}}
    data.update(kwargs)
    return response_as_json(data)

JsonResponse=json_response
jsonError=json_error



def Daily_Segment_1_Get_Data_Dict(par):
   
    chart_data=Daily_Segment_1_Get_Data(par)
    raw_data=chart_data.copy()
    # 对OCC做处理，*100取整数
    data_a = [round(float(n.replace('%','')),0) for n in chart_data.iloc[-1,].to_list()]
    #获取 ADR数据
    data_b = [ n for n in chart_data.iloc[-7,].to_list()]
 
    #data_b = [round(n*100,2) for n in [0.1233, 0.231, 0.4522, 0.5612, 0.6667, 0.745]]
    pdt_list = chart_data.columns.to_list()
    data_dict= {'data':[data_a,data_b], 'head':['OCC %','ADR'], 'item':pdt_list}

    #调用图表函数，将参数传入
    bar=create_bar_Line(data_dict)
  

    return bar,raw_data
 
     
 
def Daily_Segment_1_Get_Data(par):
  
    par="67,"+User_Name+","+User_Password+","+par
    data=PIIS.Client(par)
    data=eval(data)
    data_table=pd.DataFrame(data.get('Daily1'))
    #对表格首行至倒数第二行取整数处理
    data_table_1=data_table.iloc[0:-1,:].round(0)
    #对表格最后一行添加百分号处理
    data_table_2=data_table.iloc[-1,].map(lambda x:format(x,'.2%')) 
        
    for nrow in range(len(data_table_1.columns)):
        data_table_1.iloc[:,nrow]=data_table_1.iloc[:,nrow].apply(lambda x:format(int(x),','))
    
    
    data_table=data_table_1.append(data_table_2,ignore_index=True)
    data_table.columns=pd.to_datetime(data_table.columns).strftime('%d %a')
    #data_table.columns=pd.data_table.columns
    #data_table.iloc[1:,2:-1]=build_formatters(data_table.iloc[1:,2:-1],num_format)
    #data_table=data_table.to_html()
    return data_table



def Daily_Segment_1_Create_Bar(bar_dict) -> Bar:
    # 建立百分比的柱状图
    bar_item = bar_dict['item']
    bar_head = bar_dict['head']
    bar_data = bar_dict['data']

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(bar_item)
        .add_yaxis(bar_head[0], bar_data[0],label_opts=opts.LabelOpts(formatter="{c} "))
        

        #.add_yaxis(bar_head[0], bar_data[0],label_opts=opts.LabelOpts(formatter="{c} "))
        #.add_yaxis(bar_head[0], [randrange(0, 100) for _ in range(6)],label_opts=opts.LabelOpts(formatter="{c} %"))
        .set_global_opts(title_opts=opts.TitleOpts(title="Daily Segment Performance", subtitle="占比情况"),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} %"), interval=10),
                         datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                         )
                        
        .dump_options_with_quotes()
     )   

    return bar



def create_bar_Line(bar_dict) -> Bar:
    # 建立百分比的柱状图
    bar_item = bar_dict['item']
    bar_head = bar_dict['head']
    bar_data = bar_dict['data']

    bar = (Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT)))

    bar.add_xaxis(bar_item)
    bar.add_yaxis(bar_head[1], bar_data[1],label_opts=opts.LabelOpts(is_show=False),)
 
    bar.extend_axis(yaxis=opts.AxisOpts(name='OCC',
                                        type_='value',
                                        interval=10,
                                        axislabel_opts=opts.LabelOpts(formatter="{value} "),))
                    

    bar.set_global_opts(
                        tooltip_opts=opts.TooltipOpts(is_show=True,trigger='axis'),#axis_pointer_type='cross'),
                        title_opts=opts.TitleOpts(title="Daily Performance of ADR and OCC",pos_top='top',pos_left='center'),
                        legend_opts=opts.LegendOpts(pos_bottom=15),
                        xaxis_opts=opts.AxisOpts(type_='category',
                                                 axispointer_opts=opts.AxisPointerOpts(is_show=True,type_='shadow'),),
                        yaxis_opts=opts.AxisOpts(name='ADR',
                                                 type_='value',
                                                 interval=100,
                                                 axislabel_opts=opts.LabelOpts(formatter="{value}"),
                                                 axistick_opts=opts.AxisTickOpts(is_show=True),
                                                 splitline_opts=opts.SplitLineOpts(is_show=True),
                                                 ),
                        )
  
    
    line = Line()
    line.add_xaxis(xaxis_data=bar_item)
    line.add_yaxis(series_name=bar_head[0],yaxis_index=1,
                   y_axis=bar_data[0],
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(width=2),
                   z=10,
                   #areastyle_opts=opts.AreaStyleOpts(opacity=0.1)
                   )
    
    #line.dump_options_with_quotes()
                  

    return bar.overlap(line).dump_options_with_quotes()

def bar_line(dict_data):
    x_data = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

    bar = (
        Bar(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="蒸发量",
            y_axis=[
                2.0,
                4.9,
                7.0,
                23.2,
                25.6,
                76.7,
                135.6,
                162.2,
                32.6,
                20.0,
                6.4,
                3.3,
            ],
            label_opts=opts.LabelOpts(is_show=False),
        )
      
        .add_yaxis(
            series_name="降水量",
            y_axis=[
                2.6,
                5.9,
                9.0,
                26.4,
                28.7,
                70.7,
                175.6,
                182.2,
                48.7,
                18.8,
                6.0,
                2.3,
            ],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="温度",
                type_="value",
                min_=0,
                max_=25,
                interval=5,
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            )
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            ),
            yaxis_opts=opts.AxisOpts(
                name="水量",
                type_="value",
                min_=0,
                max_=250,
                interval=50,
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
    )
    
    line = (
        Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="平均温度",
            yaxis_index=1,
            y_axis=[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    
    #bar.overlap(line).render("mixed_bar_and_line.html")
    
    return bar.overlap(line).dump_options_with_quotes()


def Daily_Segment_Data(request):
    par = request.GET['param']
    chart_data, raw_data = Daily_Segment_1_Get_Data_Dict(par)
    return JsonResponse(json.loads(chart_data), json.loads(raw_data.to_json(orient='split', force_ascii=False)))

def Daily_Segment_Par(request):
    Par_Data={}

    Business_Year=[str(datetime.now().year),str(datetime.now().year-1),str(datetime.now().year-2),str(datetime.now().year-3)]

    Par_Data['Hotel_Area_Value']=Hotel_Area_Value
    Par_Data['Hotel_Brand_Value']=Hotel_Brand_Value
    Par_Data['Hotel_City_Value']=Hotel_City_Value
    Par_Data['Hotel_Owner_Value']=Hotel_Owner_Value

    Par_Data['Hotel_Name_Value']=Hotel_Name_Value

    Par_Data['Business_Year_Value']=Business_Year

    return HttpResponse(json.dumps(Par_Data))


def Daily_Segment(request):
    if '67' in UA_Value[0].strip(',').split(','):
        return render(request,'Daily_Segment.html')
    else:
        return HttpResponse('<script>alert("No Access for this page.");location.href="/demo/index/"</script>')

def index(request):
    return render(request,'index.html')


def login(request):

    return render(request, 'login.html')


#登录用户
def dologin(request):

    # try:
    #    user = request.POST['User_Name']
    #    password = request.POST['User_Password']
    #    print(user,password)
    #    return HttpResponse('<script>alert("登录成功");location.href="/demo/index"</script>')

    global User_Name,User_Password,Hotel_Name_Value,Hotel_Area_Value,WF_Version_Value,Hotel_Brand_Value,Hotel_City_Value,Hotel_Owner_Value,UA_Value

    #params=get_parameter_dic(request)
        #par=params.get('User_Name')
    User_Name=request.POST['User_Name']
    User_Password=request.POST['User_Password']
    #3--用户名和密码验证    
    par="3,"+User_Name+","+User_Password
    data=PIIS.Client(par)

    #1--Hotel Name
    Hotel_Name_Data="1,"+User_Name+","+User_Password
    Hotel_Name_Data=PIIS.Client(Hotel_Name_Data)
    Hotel_Name_Data=eval(Hotel_Name_Data)
    Hotel_Name_Value=Hotel_Name_Data.get('HOTEL_NAME')
    #2--Weekly Forecast Version
    WF_Version_Data="2,"+User_Name+","+User_Password
    WF_Version_Data=PIIS.Client(WF_Version_Data)
    WF_Version_Data=eval(WF_Version_Data)
    WF_Version_Value=WF_Version_Data.get('version')
    #5---Hotel Area
    Hotel_Area_Data="5,"+User_Name+","+User_Password
    Hotel_Area_Data=PIIS.Client(Hotel_Area_Data)
    Hotel_Area_Data=eval(Hotel_Area_Data)
    Hotel_Area_Value=Hotel_Area_Data.get('AREA')
    #6---Hotel Brand
    Hotel_Brand_Data="6,"+User_Name+","+User_Password
    Hotel_Brand_Data=PIIS.Client(Hotel_Brand_Data)
    Hotel_Brand_Data=eval(Hotel_Brand_Data)
    Hotel_Brand_Value=Hotel_Brand_Data.get('HOTEL_BRAND')
    #7---Hotel City
    Hotel_City_Data="7,"+User_Name+","+User_Password
    Hotel_City_Data=PIIS.Client(Hotel_City_Data)
    Hotel_City_Data=eval(Hotel_City_Data)
    Hotel_City_Value=Hotel_City_Data.get('CITY')
    #8---Hotel Owner
    Hotel_Owner_Data="8,"+User_Name+","+User_Password
    Hotel_Owner_Data=PIIS.Client(Hotel_Owner_Data)
    Hotel_Owner_Data=eval(Hotel_Owner_Data)
    Hotel_Owner_Value=Hotel_Owner_Data.get('OWNER_TYPE')
    #9---User Access List
    UA_Data="9,"+User_Name+","+User_Password
    UA_Data=PIIS.Client(UA_Data)
    UA_Data=eval(UA_Data)
    UA_Value=UA_Data.get('MODULE')

        
    if data=='1':
        #return HttpResponse(content=open("./templates/index.html",encoding='UTF-8').read())
        return HttpResponse('<script>location.href="/demo/index/"</script>')
    else:
        return HttpResponse('<script>alert("Wrong User Name or Password, Please try it again.");location.href="/demo/login/"</script>')
    








