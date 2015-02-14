$(document).ready( function() {
    myDate($('#datepicker1'),0);
    myDate($('#datepicker2'),0);
    myTime($('#timepicker1'));
    myTime($('#timepicker2'));
});
function myDate(jqueryObject, start){
    var nowDate = new Date();
    
    nowDate.setDate(nowDate.getDate() + start);
    var zeroYear = nowDate.getFullYear().toString();
    var zeroMonth = (nowDate.getMonth()+1).toString();
    var zeroDay = nowDate.getDate().toString();
    
    var tenDate = nowDate.setDate(nowDate.getDate() + 9 );
    var tenYear = nowDate.getFullYear().toString();
    var tenMonth = (nowDate.getMonth()+1).toString();
    var tenDay = nowDate.getDate().toString();
    jqueryObject.datetimepicker({
        pickTime: false,
        minDate:zeroMonth+"/"+zeroDay+"/"+zeroYear,
        maxDate:tenMonth+"/"+tenDay+"/"+tenYear
    });
}
function myTime(jqueryObject){
    jqueryObject.datetimepicker({
        format: 'HH:mm',
        pickDate: false,
        useSeconds: false,
        pick12HourFormat: false
        //icons = {time: 'glyphicon glyphicon-time'}
    });
}
function ajax_get_cars(){
    
    var frm = $("#carform");
    frm.submit(function(e)
    {
        var getData = frm.serializeArray();
        var formURL = $(this).attr("action");
        $.ajax(
            {
            url : formURL,
            type: "GET",
            data : getData,
            dataType: "json",
            success: function (data) {
               if(data.length>0 && data[0]["fields"]["error_time"]!=''){
                    var div = $("#time_error");
                    div.html("<font size=\"3\" color=\"red\">*"+data[0]["fields"]["error_time"]+"</font>");
               }
               else{
                   $("#time_error").html('');
                   var list = $("#mycars");
                   if(list.children().length > 0) {
                        list.empty();
                   }
                   for (var i = 0; i < data.length; i++) {
                        var car_id=data[i]["fields"]["car_id"];
                        var car_CIN=data[i]["fields"]["car_CIN"];
                        var car_type=data[i]["fields"]["car_type"];
                        var car_fee=data[i]["fields"]["car_fee"];
                        var car_status=data[i]["fields"]["car_status"];
                        var car_mile=data[i]["fields"]["car_mile"];
                        var car_from_date=data[i]["fields"]["from_date"];
                        var car_from_time=data[i]["fields"]["from_time"];
                        var car_to_date=data[i]["fields"]["to_date"];
                        var car_to_time=data[i]["fields"]["to_time"];
    
               
                        var newli = document.createElement("li");
                        newli.setAttribute("id", car_id);
                        newli.setAttribute("class", "myclass-border");
                   
                        var new_img="<img style=\"float:left\" src=\"/CRSapp/search_car_picture/"+car_type+"\"  width=\"200px\"/>";
                        var new_div=" <div style=\"float:left;width:340px\">";
                        var new_CIN="<p class=\"media-body media-heading\"  style=\"margin-left:20px\">CIN:<a href=\"#\"> <strong>"+car_CIN+"</strong></a></p><input type=\"hidden\" id=\"CIN"+car_id+"\" value=\""+car_CIN+"\">";
                        var new_type="<p class=\"media-body media-heading\"  style=\"margin-left:20px\">TYPE:<a href=\"#\"> <strong>"+car_type+"</strong></a></p><input type=\"hidden\" id=\"TPYE"+car_id+"\" value=\""+car_type+"\">";
                        var new_fee="<p class=\"media-body media-heading\"  style=\"margin-left:20px\">FEE:"+car_fee+"</p><input type=\"hidden\" id=\"FEE"+car_id+"\" value=\""+car_fee+"\">";
                        var new_status=" <p class=\"media-body media-heading\"  style=\"margin-left:20px\">STATUS:"+car_status+" </p><input type=\"hidden\" id=\"STATUS"+car_id+"\" value=\""+car_status+"\"></div>";
                        var new_mile="<p class=\"media-body media-heading\"  style=\"margin-left:20px\">MILES: car_mile</p><input type=\"hidden\" id=\"MILE"+car_id+"\" value=\""+car_mile+"\">";
                        var new_input="<input data-toggle=\"modal\" data-target=\"#myModal\" style=\"float:right;margin-top:10px\"type=\"submit\" class=\"btn btn-primary\" value=\"Reserve\" onclick=\"reserveformContent("+car_id+")\"></div>";
                        var new_hidden_input="<input type=\"hidden\" id=\"FD"+car_id+"\" name=\"reserve_from_date\" 	value=\""+car_from_date+"\"><input type=\"hidden\"id=\"FT"+car_id+"\"  name=\"reserve_from_time\" 	value=\""+car_from_time+"\"><input type=\"hidden\" id=\"TD"+car_id+"\" name=\"reserve_to_date\" 	value=\""+car_to_date+"\"><input type=\"hidden\" id=\"TT"+car_id+"\" name=\"reserve_to_time\" 	value=\""+car_to_time+"\">"
               
                        newli.innerHTML=new_img+new_div+new_CIN+new_type+new_fee+new_status+new_mile+new_input+new_hidden_input;
                        list.append($(newli));
                   }
               }
            }
               //error: function() {alert();}
            });
        e.preventDefault();
    });
}


//window.setInterval(get_first_grumblrID, 10000);



