from django.shortcuts import render
import json
from random import randrange
from django.http import HttpResponse
from rest_framework.views import APIView

from pyecharts.charts import Bar,Line
from pyecharts import options as opts 
from pyecharts.globals import ThemeType
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode

import sys
sys.path.append('/Users/jerry/desktop/PIIS/pyecharts_django_demo_2/demo') 
import PIIS_Hotel_Client_ALLwith as PIIS
import pandas as pd
import numpy as np
#### Create your views here.

####

def response_as_json(data):
	json_str=json.dumps(data)
	response=HttpResponse(json_str,content_type="application/json")
	response["Access-Control-Allow-Origin"]="*"
	return response

def json_response(data,raw_data,code=200):
	data={"code":code,"msg":"success","data":data,'raw_data':raw_data}
	return response_as_json(data)


def json_response_par(data):
   
    return response_as_json(data)    

def json_error(error_string="error",code=500,**kwargs):
	data={"code":code,"msg":error_string,"data":{}}
	data.update(kwargs)
	return response_as_json(data)

JsonResponse=json_response
JsonResponse_Par=json_response_par
jsonError=json_error


def get_data_dict(par):
   
    chart_data=get_data(par)
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
 
     
 
def get_data(par):
  
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



def create_bar(bar_dict) -> Bar:
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
    
    
    
    

from django.http import QueryDict
from rest_framework.request import Request
def get_parameter_dic(request, *args, **kwargs):
    if isinstance(request, Request) == False:
        return {}

    query_params = request.query_params
    if isinstance(query_params, QueryDict):
        query_params = query_params.dict()
    result_data = request.data
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params != {}:
        return query_params
    else:
        return result_data



class login(APIView):
    def get(self,request,*args,**kwargs):
        
        return HttpResponse(content=open("./templates/login.html",encoding='UTF-8').read())
    
    def post(self, request, *args, **kwargs):
        global User_Name,User_Password,Hotel_Name_Value

        params=get_parameter_dic(request)
        #par=params.get('User_Name')
        User_Name=params.get('User_Name')
        User_Password=params.get('User_Password')
        
        par="3,"+User_Name+","+User_Password
        data=PIIS.Client(par)


        Hotel_Name_Data="1,"+User_Name+","+User_Password
        Hotel_Name_Data=PIIS.Client(Hotel_Name_Data)
        Hotel_Name_Data=eval(Hotel_Name_Data)
        Hotel_Name_Value=Hotel_Name_Data.get('HOTEL_NAME')
        
        if data=='1':
            return HttpResponse(content=open("./templates/index.html",encoding='UTF-8').read())
        else:
            return HttpResponse('<script>alert("Wrong User Name or Password, Please try it again.");location.href="/demo/login"</script>')



class index(APIView):
    def get(self,request,*args,**kwargs):
        #global params
    
        #params=get_parameter_dic(request)#
        
        #a=request.query_params.dict().a
        #print("\n n value:",n)
        return render (request,"index.html")


class Segment_Daily_1_Data(APIView):
   
    def get(self,request,*args,**kwargs):
        par_Hotel_Name=request.GET['Hotel_Name']
       
        par_Hotel_Name1=params.get('Hotel_Name')
        par_Business_Year=params.get('Business_Year')
        par_Business_Month=params.get('Business_Month')

        par_Hotel_Area=params.get('Hotel_Area')
        par_Hotel_Brand=params.get('Hotel_Brand')
        par_Hotel_City=params.get('Hotel_City')
        par_Hotel_Owner=params.get('Hotel_Owner')   

        print("\n Hotel_Name is ---------------", par_Hotel_Name)
        try:
            #par="Hotel A,2020,4,ALL,ALL,ALL,ALL"     
            par=par_Hotel_Name+","+par_Business_Year+","+par_Business_Month+","+par_Hotel_Area+","+par_Hotel_Brand+","+par_Hotel_City+","+par_Hotel_Owner
        except TypeError:
            pass
        chart_data,raw_data=get_data_dict(par)


  
        return JsonResponse(json.loads(chart_data),json.loads(raw_data.to_json(orient='split',force_ascii=False)))


class Segment_Daily_1_Par(APIView):
   
    def get(self,request,*args,**kwargs):

        Par_Data={}
        Par_Data['Hotel_Name_Value']=Hotel_Name_Value

        return JsonResponse_Par(Par_Data)


  #return JsonResponse(json.loads(index()),json.loads(get_data().to_html()))
#
class Segment_Daily_1(APIView):
    def get(self,request,*args,**kwargs):
        global params
      
        params=get_parameter_dic(request)#
        
        #a=request.query_params.dict().a
        #print("\n n value:",n)
        return render (request,("Segment_Daily_1.html"))
        #return render(request,("Segment_Daily_1.html"))


if __name__=='__main__':
    get_data('5')
