function reserveformContent(id){
    $("#mile_error").html('');
    $("#success").html('');
    $("#reserve").html('');
    $("#overlap_error").html('');
    $("#add_reserve_button").attr('onclick','ajax_add_reserve('+id+')');
    CIN=$("#CIN"+id).val();
    carFee=$("#FEE"+id).val();
    carType=$("#TPYE"+id).val();
    fromDate=$("#FD"+id).val();
    fromTime=$("#FT"+id).val();
    toDate=$("#TD"+id).val();
    toTime=$("#TT"+id).val();
    d1=new Date(fromDate);
    d2=new Date(toDate);
    var one_day=1000*60*60*24;
    var days = Math.round((d2.getTime()-d1.getTime())/one_day);
    if(calculateHoursDiff(fromTime,toTime)){
        days=days+1;
    }
    var reserveform=document.getElementById("reseverForm");
    var tax=7;//7%
    var insurnce=10;//$10/day
    var total=(parseInt(carFee)*(1+0.07)+insurnce)*days;
		total=total.toFixed(2);

    var formImg= "<img style=\"float:left\" src=\"/CRSapp/search_car_picture/"+carType+"\"  width=\"100px\"/>";
    var formFrom="<div style=\"float:left;width:300px\"> <p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>From</strong>:"+fromDate+" : "+fromTime+"</p>";
    var formTo= "<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>To</strong>:"+toDate+" : "+toTime+"</p>";
    var formType="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Type</strong>:"+carType+"</p>";
    var formRental="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Rental</strong>: $"+carFee+"/day</p>";
    var formTax="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Tax</strong>: "+tax+"%</p>";
    var formInsurance="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Insurance</strong>: $"+insurnce+"/day</p><hr />";
    var formtotal="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Total</strong>: $"+total+"</p>"
    var formSelectCustomer="<strong>SELECT A CUSTOMER:</strong><br><select class=\"form-control\" id=\"selectGeneralUser\" name=\"generalusername\" style=\" width:100px\"></select></div>";
    //var formInputMiles="Old Miles:<input class=\"form-control\" type=\"text\" name=\"oldmiles\" value = \"\"style=\"float:right;width:100px\">";
    var formHiddenInput_FD="<input type=\"hidden\" name=\"h_fromdate\" value=\""+fromDate+"\" >";
    var formHiddenInput_FT="<input type=\"hidden\" name=\"h_fromtime\" value=\""+fromTime+"\" >";
    var formHiddenInput_TD="<input type=\"hidden\" name=\"h_todate\" value=\""+toDate+"\" >";
    var formHiddenInput_TT="<input type=\"hidden\" name=\"h_totime\" value=\""+toTime+"\" >";
    //var formHiddenInput_totalfee="<input type=\"hidden\" name=\"h_totalfee\" value=\""+total+"\" >"
    var formHiddenInput_CIN="<input type=\"hidden\" name=\"h_CIN\" value=\""+CIN+"\" >";
    
    //reserveform.innerHTML=formImg+formFrom+formTo+formType+formRental+formTax+formInsurance+formtotal+formSelectCustomer+formInputMiles+formHiddenInput_FD+formHiddenInput_FT+formHiddenInput_TD+formHiddenInput_TT+formHiddenInput_totalfee+formHiddenInput_CIN;
    reserveform.innerHTML=formImg+formFrom+formTo+formType+formRental+formTax+formInsurance+formtotal+formSelectCustomer+formHiddenInput_FD+formHiddenInput_FT+formHiddenInput_TD+formHiddenInput_TT+formHiddenInput_CIN;

    ajax_get_generalUsers();
}

function calculateHoursDiff(fromTime,toTime){
    time1=fromTime.split(":");
    time2=toTime.split(":");
    hour1=parseInt(time1[0]);
    hour2=parseInt(time2[0]);
    if(hour2-hour1>5){
        return 1;
    }
    else if (hour2-hour1<-5){
        return -1;
    }
    else {
        return 0;
    }
}
function delete_car_sheet(CIN){
    $("#success_delete").html('');
    $("#error_delete").html('');
    var Alert="<div style=\"float:left;width:400px\"> <p>Are you sure to delete this car now?</p></div>";
    var HiddenInput_CIN="<input type=\"hidden\" name=\"h_CIN\" value=\""+CIN+"\" >";
    $("#delete_car_button").attr('onclick','ajax_delete_car(\"'+CIN+'\")');
    $("#deleteForm").html(Alert+HiddenInput_CIN);
}
function ajax_delete_car(CIN){
    $("#success_delete").html('');
    $("#error_delete").html('');
    var frm = $("#delete_car_form");
    frm.submit(function(e){
        $(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
        var postData = frm.serializeArray();
        var formURL = $(this).attr("action");
        e.preventDefault();
        $.ajax({
               url : formURL,
               type: "POST",
               data : postData,
               dataType: "json",
               error:function(){
                    console.log("no");
               },
               success: function (data) {
                   if(data[0]["fields"]["error"]!=''){
                       var div = $("#error_delete");
                       div.html("<font size=\"3\" color=\"red\">*"+data[0]["fields"]["error"]+"</font>");
                   }else{
                       var div = $("#success_delete");
                       div.html("<font size=\"3\" color=\"green\">*"+data[0]["fields"]["success"]+"</font>");
                       var car_object = document.getElementById("inventoryInfo_row_"+CIN);
                       $(car_object).remove();
                   }
               }
        });
        $("#delete_car_form").unbind('submit');
    });
}

function ajax_get_generalUsers(){
    $.ajax({
           url: "/CRSapp/get_all_generalUsers",
           type: "GET",
           dataType:"json",
           success:function (data) {
              var select = $("#selectGeneralUser");
              if(select.children().length > 0) {
                  select.empty();
              }
              for (var i = 0; i < data.length; i++) {
                  var username=data[i]["fields"]["username"];
                  var newoption = document.createElement("option");
                  newoption.setAttribute("value", username);
                  newoption.innerHTML=username;
                  select.append($(newoption));
              }
           }
    });
}
function ajax_add_reserve(list_id){
    $("#mile_error").html('');
    $("#success").html('');
    $("#reserve").html('');
    $("#overlap_error").html('');
    
    var frm = $("#sub_form");
    frm.submit(function(e){
        $(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
        var postData = frm.serializeArray();
        var formURL = $(this).attr("action");
        e.preventDefault();
        $.ajax({
               
               url : formURL,
               type: "POST",
               data : postData,
               dataType: "json",
               error:function(){
                    console.log("no");
               },
               success: function (data) {
                    console.log("yes");
                   if(data[0]["fields"]["error_mile"]!=''){
                       var div = $("#mile_error");
                       div.html("<font size=\"3\" color=\"red\">*"+data[0]["fields"]["error_mile"]+"</font>");
                   }
                   else if(data[0]["fields"]["reserve"]!=''){
                        var div = $("#reserve");
                        div.html("<font size=\"3\" color=\"red\">*"+data[0]["fields"]["reserve"]+"</font>");
                   }
                   else if(data[0]["fields"]["error_overlap"]!=''){
                        var div = $("#overlap_error");
                        div.html("<font size=\"3\" color=\"red\">*"+data[0]["fields"]["error_overlap"]+"</font>");
                    }
                   else if(data[0]["fields"]["success"]!=''){
                        var div = $("#success");
                        div.html("<font size=\"4\" color=\"green\">"+data[0]["fields"]["success"]+"</font>");
                        $("#"+list_id).remove();
                    }
               
               }
        });
        $("#sub_form").unbind('submit');
    });
}
function cancel_error(){
    $("#mile_error").html('');
    $("#success").html('');
    $("#reserve").html('');
    $("#overlap_error").html('');
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function ajax_get_return_car(){
    $("#error_CIN_required").html('');
    $("#error_username_email_required").html('');
    $("#error_match_required").html('');

    var frm = $("#return_car_info");
    frm.submit(function(e)
    {
        var getData = frm.serializeArray();
        var formURL = $(this).attr("action");
        $.ajax({
            url : formURL,
            type: "GET",
            data : getData,
            dataType: "json",
            error:function(){
                    console.log("no");
            },
            success: function (data) {

                if(data[0]["errors"]["error_CIN"]!=''){
                    var div = $("#error_CIN_required");
                    div.html("<font size=\"3\" color=\"red\">*"+data[0]["errors"]["error_CIN"]+"</font>");
                }else if(data[0]["errors"]["error_username_email"]!=''){
                    var div = $("#error_username_email_required");
                    div.html("<font size=\"3\" color=\"red\">*"+data[0]["errors"]["error_username_email"]+"</font>");
                }
                if(data[0]["errors"]["error_match"]!=''){
                    var div = $("#error_match_required");
                    div.html("<font size=\"3\" color=\"red\">*"+data[0]["errors"]["error_match"]+"</font>");
                }
                if("fields" in data[0]){
                    if(data[0]["fields"]["CIN"]!=''){
                        $("#car_CIN").html(data[0]["fields"]["CIN"]);
                        $("#input_car_CIN").val(data[0]["fields"]["CIN"]);
                    }
                    if(data[0]["fields"]["Name"]!=''){
                        $("#customer_name").html(data[0]["fields"]["Name"]);
                        $("#input_customer_name").val(data[0]["fields"]["Name"]);
                    }
                    if(data[0]["fields"]["Email"]!=''){
                        $("#customer_email").html(data[0]["fields"]["Email"]);
                        $("#input_customer_email").val(data[0]["fields"]["Email"]);
                    }
                    if(data[0]["fields"]["Fromdate"]!=''){
                        $("#customer_fromdate").html(data[0]["fields"]["Fromdate"]);
                        $("#input_customer_fromdate").val(data[0]["fields"]["Fromdate"]);
                    }
                    if(data[0]["fields"]["Fromtime"]!=''){
                        $("#customer_fromtime").html(data[0]["fields"]["Fromtime"]);
                        $("#input_customer_fromtime").val(data[0]["fields"]["Fromtime"]);
                    }
                    if(data[0]["fields"]["Todate"]!=''){
                        $("#customer_todate").html(data[0]["fields"]["Todate"]);
                        $("#input_customer_todate").val(data[0]["fields"]["Todate"]);
                    }
                    if(data[0]["fields"]["Totime"]!=''){
                        $("#customer_totime").html(data[0]["fields"]["Totime"]);
                        $("#input_customer_totime").val(data[0]["fields"]["Totime"]);
                    }
                }else{
                    cancel_search();
                }
            }
        });
        e.preventDefault();
        $("#return_car_info").unbind('submit');
    });
}
function cancel_search(){
    $("#car_CIN").html("None");
    $("#input_car_CIN").val("");

    $("#customer_name").html("None");
    $("#input_customer_name").val("");

    $("#customer_email").html("None");
    $("#input_customer_email").val("");

    $("#customer_fromdate").html("None");
    $("#input_customer_fromdate").val("");

    $("#customer_fromtime").html("None");
    $("#input_customer_fromtime").val("");

    $("#customer_todate").html("None");
    $("#input_customer_todate").val("");

    $("#customer_totime").html("None");
    $("#input_customer_totime").val("");
}
function generate_sheet(){
    $("#select_error").html("");
    $("#mile_error").html("");
    $("#success").html("");
    var frm = $("#generate_sheet");
    frm.submit(function(e)
    {
        var getData = frm.serializeArray();
        var formURL = $(this).attr("action");
        $.ajax({
            url : formURL,
            type: "GET",
            data : getData,
            dataType: "json",
            error:function(){
                    console.log("no");
            },
            success: function (data) {
                if(data[0]["errors"]["error_mile_match"]!=''){
                    var div = $("#mile_error");
                    div.html("<font size=\"3\" color=\"red\">*"+data[0]["errors"]["error_mile_match"]+"</font>");
                    return;
                }
                if(data[0]["errors"]["error_sheet"]!=''){
                    var div = $("#select_error");
                    div.html("<font size=\"3\" color=\"red\">*"+data[0]["errors"]["error_sheet"]+"</font>");
                    return;
                }
                if(data[0]["sheet"]["mile_diff"]!=''){
                    var mile_final = data[0]["sheet"]["mile_final"];
                    var mile_diff = data[0]["sheet"]["mile_diff"];
                    var CIN = data[0]["sheet"]["CIN"];
                    var car_fee = data[0]["sheet"]["car_fee"];
                    var email = data[0]["sheet"]["email"];
                    var fromdate = data[0]["sheet"]["fromdate"];
                    var fromtime = data[0]["sheet"]["fromtime"];
                    var todate = data[0]["sheet"]["todate"];
                    var totime = data[0]["sheet"]["totime"];
                    var d1=new Date(fromdate);
                    var d2=new Date();
                    //var d2=new Date(todate);
                    var one_day=1000*60*60*24;
                    var days = Math.round((d2.getTime()-d1.getTime())/one_day);
                    if(days==0){
                        days=1;
                    }else{
                        if(calculateHoursDiff(fromtime,totime)){
                        days=days+1;
                        }
                    }
                    var returnForm=document.getElementById("returnForm");
                    var tax=7;//7%
                    var insurnce=10;//$10/day\
                    var milefee=0;
                    if(parseFloat(mile_diff)>150){
                        //>150 0.1dollar/mile
                        milefee=(parseFloat(mile_diff)-150)*0.1;
                    }
                    var total=(parseInt(car_fee)*(1+0.07)+insurnce)*days+milefee;
                    total=total.toFixed(2);
                    var formFrom="<div style=\"float:left;width:300px\"> <p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>From</strong>:"+fromdate+" - "+fromtime+"</p>";
                    var formTo= "<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>To</strong>:"+todate+" - "+totime+"</p>";
                    var formRealRuturn= "<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Real Return</strong>:"+getCurrentDate()+" - "+getCurrentTime()+"</p>";
                    var formRental="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Rental</strong>: $"+car_fee+"/day</p>";
                    var formTax="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Tax</strong>: "+tax+"%</p>";
                    var formMile="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Mile Fee</strong>: "+milefee+"$. ("+mile_diff+" miles)</p>";
                    var formInsurance="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Insurance</strong>: $"+insurnce+"/day</p><hr />";
                    var formtotal="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Total</strong>: $"+total+"</p>";
                    var formCIN="<input type=\"hidden\" name=\"h_CIN\" value=\""+CIN+"\" >";
                    var formemail="<input type=\"hidden\" name=\"h_email\" value=\""+email+"\" >";
                    var formfromdate="<input type=\"hidden\" name=\"h_fromdate\" value=\""+fromdate+"\" >";
                    var formtodate="<input type=\"hidden\" name=\"h_todate\" value=\""+todate+"\" >";
                    var formMile_final="<input type=\"hidden\" name=\"h_mile_final\" value=\""+mile_final+"\" >";
                    returnForm.innerHTML=formFrom+formTo+formRealRuturn+formRental+formTax+formMile+formInsurance+formtotal+formCIN+formemail+formfromdate+formtodate+formMile_final;
                }
            }
        });
        e.preventDefault();
        $("#generate_sheet").unbind('submit');
    });
}
function getCurrentDate(){
    var today=new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();
    var hour = today.getHours();
    var minute = today.getMinutes();
    return mm+'/'+dd+'/'+yyyy;
}
function ajax_add_return(){
    $("#add_return_error").html("");
    $("#success").html("");
    var frm = $("#return_form");
    frm.submit(function(e){
        $(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
        var postData = frm.serializeArray();
        var formURL = $(this).attr("action");
        e.preventDefault();
        $.ajax({
               url : formURL,
               type: "POST",
               data : postData,
               dataType: "json",
               error:function(){
                    console.log("no");
               },
               success: function (data) {
                   console.log("yes");
                   if(data[0]["addreturn"]["error"]!=''){
                       var div = $("#add_return_error");
                       div.html("<font size=\"3\" color=\"red\">*"+data[0]["addreturn"]["error"]+"</font>");

                   }else if(data[0]["addreturn"]["success"]!=''){
                       var div = $("#success");
                       div.html("<font size=\"4\" color=\"green\">"+data[0]["addreturn"]["success"]+"</font>");
                   }
               }
        });
        $("#return_form").unbind('submit');
    });
}
function cancel_return_info(){
    $("#add_return_error").html("");
    $("#success").html("");
}
function getCurrentTime(){
    var today=new Date();
    var hour = today.getHours();
    var minute = today.getMinutes();
    return hour+':'+minute;
}

/************************************************/
function confirm(id){
    $("#mile_error").html("");
    $("#success").html("");
    CIN=$("#CIN"+id).val();
    
    console.log(CIN);
    
    orderID=id;
    fromDate=$("#FD"+id).val();
    fromTime=$("#FT"+id).val();
    toDate=$("#TD"+id).val();
    toTime=$("#TT"+id).val();
    user=$("#USER"+id).val();
    
    var confirmform=document.getElementById("confirmForm");
    
    //$('#con').click(function(e){
    //$(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
    //var postData = frm.serializeArray();
    console.log("beginfunction");
    //var formURL = $(this).attr("href");
    var formURL = "/CRSapp/get_confirmdata/"+id;
    console.log(formURL);
    //e.preventDefault();
    $.ajax({
           
           url : "/CRSapp/get_confirmdata/"+id,
           type: "GET",
           //data:"",
           //dataType: "json",
           error:function(){
           console.log(arguments[2]);
           },
           success: function (data) {
           console.log("yes");
           
           var car_id=data[0]["fields"]["car_id"];
           var car_CIN=data[0]["fields"]["car_CIN"];
           var car_type=data[0]["fields"]["car_type"];
           var car_fee=data[0]["fields"]["car_fee"];
           var car_status=data[0]["fields"]["car_status"];
           var car_mile=data[0]["fields"]["car_mile"];
           
           var new_img="<img style=\"float:left\" src=\"/CRSapp/search_car_picture/"+car_type+"\"  width=\"100px\"/>";
           
           d1=new Date(fromDate);
           d2=new Date(toDate);
           var one_day=1000*60*60*24;
           var days = Math.round((d2.getTime()-d1.getTime())/one_day);
           if(calculateHoursDiff(fromTime,toTime)){
           days=days+1;
           }
           
           var tax=7;//7%
           var insurnce=10;//$10/day
           var total=(parseInt(car_fee)*(1+0.07)+insurnce)*days;
           total=total.toFixed(2);
           
           var new_div=" <div style=\"float:left;width:340px\">";
           var new_CIN="<p class=\"media-body media-heading\"  style=\"margin-left:20px\"><strong>CIN</strong>:<a href=\"#\"> <strong>"+car_CIN+"</strong></a></p><input type=\"hidden\" id=\"CIN"+car_id+"\" value=\""+car_CIN+"\">";
           var new_type="<p class=\"media-body media-heading\"  style=\"margin-left:20px\"><strong>TYPE</strong>:<a href=\"#\"> <strong>"+car_type+"</strong></a></p><input type=\"hidden\" id=\"TPYE"+car_id+"\" value=\""+car_type+"\">";
           var new_fee="<p class=\"media-body media-heading\"  style=\"margin-left:20px\">FEE:"+car_fee+"</p><input type=\"hidden\" id=\"FEE"+car_id+"\" value=\""+car_fee+"\">";
           var new_status=" <p class=\"media-body media-heading\"  style=\"margin-left:20px\">STATUS:"+car_status+" </p><input type=\"hidden\" id=\"STATUS"+car_id+"\" value=\""+car_status+"\"></div>";
           var new_mile="<p class=\"media-body media-heading\"  style=\"margin-left:20px\"><strong>MILES</strong>:"+car_mile+"</p><input type=\"hidden\" id=\"MILE"+car_id+"\" value=\""+car_mile+"\">";
           
           var formFrom="<div style=\"float:left;width:300px\"> <p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>From</strong>:"+fromDate+" : "+fromTime+"</p>";
           
           var formTo= "<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>To</strong>:"+toDate+" : "+toTime+"</p>";
           
           var formRental="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Rental</strong>: $"+car_fee+"/day</p>";
           var formTax="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Tax</strong>: "+tax+"%</p>";
           var formInsurance="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Insurance</strong>: $"+insurnce+"/day</p><hr />";
           var formtotal="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Total</strong>: $"+total+"</p>";
           
           var formInputMiles="<p class=\"media-body media-heading\" style=\"margin-left:20px;float:left\"><strong>Old Miles</strong>:</p><input class=\"form-control\" type=\"text\" name=\"oldmiles\" value = \"\"style=\"width:150px\">";
           //var formInputMiles="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Old Miles</strong>:<input class=\"form-control\" type=\"text\" name=\"oldmiles\" value = \"\"></p>";
           var formHiddenInput_FD="<input type=\"hidden\" name=\"h_fromdate\" value=\""+fromDate+"\" >";
           var formHiddenInput_FT="<input type=\"hidden\" name=\"h_fromtime\" value=\""+fromTime+"\" >";
           var formHiddenInput_TD="<input type=\"hidden\" name=\"h_todate\" value=\""+toDate+"\" >";
           var formHiddenInput_TT="<input type=\"hidden\" name=\"h_totime\" value=\""+toTime+"\" >";
           var formHiddenInput_USER="<input type=\"hidden\" name=\"h_user\" value=\""+user+"\" >";
           var formHiddenInput_CIN="<input type=\"hidden\" name=\"h_CIN\" value=\""+CIN+"\" >";
           var formHiddenInput_orderid="<input id=\"orderid\" type=\"hidden\" name=\"h_orderid\" value=\""+id+"\" >";
           
           confirmform.innerHTML=new_img+new_div+new_CIN+new_type+new_mile+formFrom+formTo+formRental+formTax+formInsurance+formtotal+formInputMiles+formHiddenInput_FD+formHiddenInput_FT+formHiddenInput_TD+formHiddenInput_TT+formHiddenInput_USER+formHiddenInput_CIN+formHiddenInput_orderid;
           }
           });
    $("#con").unbind('click');
    // });
}

function deleteorder(id){
    $("#success_delete").html("");
    CIN=$("#CIN"+id).val();
    
    console.log(id);
    
    orderID=id;
    fromDate=$("#FD"+id).val();
    fromTime=$("#FT"+id).val();
    toDate=$("#TD"+id).val();
    toTime=$("#TT"+id).val();
    user=$("#USER"+id).val();
    
    var deleteform=document.getElementById("deleteForm");
    
    var formFrom="<div style=\"float:left;width:300px\"> <p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>From</strong>:"+fromDate+" : "+fromTime+"</p>";
    
    var formTo= "<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>To</strong>:"+toDate+" : "+toTime+"</p>";
    
    var formHiddenInput_FD="<input type=\"hidden\" name=\"h_fromdate\" value=\""+fromDate+"\" >";
    var formHiddenInput_FT="<input type=\"hidden\" name=\"h_fromtime\" value=\""+fromTime+"\" >";
    var formHiddenInput_TD="<input type=\"hidden\" name=\"h_todate\" value=\""+toDate+"\" >";
    var formHiddenInput_TT="<input type=\"hidden\" name=\"h_totime\" value=\""+toTime+"\" >";
    var formHiddenInput_USER="<input type=\"hidden\" name=\"h_user\" value=\""+user+"\" >";
    var formHiddenInput_CIN="<input type=\"hidden\" name=\"h_CIN\" value=\""+CIN+"\" >";
    var formHiddenInput_orderid="<input id=\"orderid_del\" type=\"hidden\" name=\"h_orderid\" value=\""+id+"\" >";
    
    //deleteform.innerHTML=formFrom+formTo+formHiddenInput_FD+formHiddenInput_FT+formHiddenInput_TD+formHiddenInput_TT+formHiddenInput_USER+formHiddenInput_CIN+formHiddenInput_orderid;
    deleteform.innerHTML="Are you sure to delete this reservation?"+formHiddenInput_FD+formHiddenInput_FT+formHiddenInput_TD+formHiddenInput_TT+formHiddenInput_USER+formHiddenInput_CIN+formHiddenInput_orderid;
}

function ajax_add_confirm(){
    $("#mile_error").html('');
    $("#success").html('');
    orderid = $("#orderid").val();
    console.log(orderid);
    
    var frm = $("#sub_form");
    frm.submit(function(e){
               $(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
               var postData = frm.serializeArray();
               var formURL = $(this).attr("action");
               e.preventDefault();
               $.ajax({
                          url : formURL,
                          type: "POST",
                          data : postData,
                          dataType: "json",
                          error:function(){
                              console.log("no");
                          },
                          success: function (data) {
                              console.log("yes");
                              if(data[0]["fields"]["error_mile"]!=''){
                                  var div = $("#mile_error");
                                  div.html("<font size=\"3\" color=\"red\">*"+data[0]["fields"]["error_mile"]+"</font>");
                              }
                              else if(data[0]["fields"]["success"]!=''){
                                  var div = $("#success");
                                  div.html("<font size=\"4\" color=\"green\">"+data[0]["fields"]["success"]+"</font>");
                                  console.log("#opration"+orderid);
                                  $("#opration"+orderid).html("");
                                  $("#status"+orderid).html("Confirmed");
                              }

                          }
                      });
               $("#sub_form").unbind('submit');
               });
}

function ajax_add_delete(){
    $("#mile_error").html('');
    $("#success").html('');
    orderid = $("#orderid_del").val();
    console.log(orderid);
    
    var frm = $("#delete_form");
    frm.submit(function(e){
               $(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
               var postData = frm.serializeArray();
               var formURL = $(this).attr("action");
               e.preventDefault();
               $.ajax({
                          url : formURL,
                          type: "POST",
                          data : postData,
                          dataType: "json",
                          error:function(){
                              console.log("no");
                          },
                          success: function (data) {
                              console.log("yes");

                              if(data[0]["fields"]["success"]!=''){
                                  var div = $("#success_delete");
                                  div.html("<font size=\"4\" color=\"green\">*"+data[0]["fields"]["success"]+"</font>");
                                  console.log("#opration"+orderid);
                                  $("#opration"+orderid).html("");
                                  $("#status"+orderid).html("Deleted");
                                  console.log("refresh the status");
                              }

                          }
                      });
               $("#delete_form").unbind('submit');
               });
}
function edit(id){
    $("#success_edit").html("");
    CIN=$("#"+id).val();

    console.log(id);

    var deleteform=document.getElementById("editForm");

    var editInputMiles="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Miles</strong>:<input id=\"inputmile\" class=\"form-control\" type=\"text\" name=\"miles\" value = \"\"style=\"width:100px\"></p>";
    var editInputFee="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Rental Fee</strong>:<input id=\"inputfee\" class=\"form-control\" type=\"text\" name=\"fee\" value = \"\"style=\"width:100px\"></p>";

    var editHiddenInput_CIN="<input type=\"hidden\" name=\"ed_CIN\" value=\""+CIN+"\" >";
    var editHiddenInput_carid="<input id=\"carid_edit\" type=\"hidden\" name=\"ed_carid\" value=\""+id+"\" >";

    deleteform.innerHTML="<p class=\"media-body media-heading\" style=\"margin-left:20px\">Enter the new value</p>"+editInputMiles+editInputFee+editHiddenInput_CIN+editHiddenInput_carid;
}
function ajax_edit_car(){
    $("#mile_error_edit").html('');
    $("#success_edit").html('');
    editid = $("#carid_edit").val();
    cartype = $("#type"+editid).html();
    console.log(cartype);

    var frm = $("#edit_form");
    frm.submit(function(e){
               $(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
               var postData = frm.serializeArray();
               var formURL = $(this).attr("action");
               e.preventDefault();
               $.ajax({
                      url : formURL,
                      type: "POST",
                      data : postData,
                      dataType: "json",
                      error:function(){
                      console.log(arguments[2]);
                      },
                      success: function (data) {
                      console.log("yes");

                      if(data[0]["fields"]["error_mile"]!=''){
                      var div = $("#mile_error_edit");
                      div.html("<font size=\"4\" color=\"red\">*"+data[0]["fields"]["error_mile"]+"</font>");
                      }

                      if(data[0]["fields"]["success"]!=''){
                      var div = $("#success_edit");
                      div.html("<font size=\"4\" color=\"green\">*"+data[0]["fields"]["success"]+"</font>");
                      $(".fee"+cartype).html(data[0]["fields"]["fee"]);
                      $("#mile"+editid).html(data[0]["fields"]["mile"]);
                      console.log("refresh the status");
                      }

                      }
                      });
               $("#edit_form").unbind('submit');
               });
}






