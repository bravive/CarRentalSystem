
function reserveformContent(id){
    $("#mile_error").html('');
    $("#success").html('');
    $("#reserve").html('');
    $("#overlap_error").html('');
    $("#add_reserve_button").attr('onclick','ajax_add_reserve('+id+')')
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
    var formInputMiles="Old Miles:<input class=\"form-control\" type=\"text\" name=\"oldmiles\" value = \"\"style=\"float:right;width:100px\">";
    var formHiddenInput_FD="<input type=\"hidden\" name=\"h_fromdate\" value=\""+fromDate+"\" >"
    var formHiddenInput_FT="<input type=\"hidden\" name=\"h_fromtime\" value=\""+fromTime+"\" >"
    var formHiddenInput_TD="<input type=\"hidden\" name=\"h_todate\" value=\""+toDate+"\" >"
    var formHiddenInput_TT="<input type=\"hidden\" name=\"h_totime\" value=\""+toTime+"\" >"
    var formHiddenInput_totalfee="<input type=\"hidden\" name=\"h_totalfee\" value=\""+total+"\" >"
    var formHiddenInput_CIN="<input type=\"hidden\" name=\"h_CIN\" value=\""+CIN+"\" >"
    
    reserveform.innerHTML=formImg+formFrom+formTo+formType+formRental+formTax+formInsurance+formtotal+formSelectCustomer+formInputMiles+formHiddenInput_FD+formHiddenInput_FT+formHiddenInput_TD+formHiddenInput_TT+formHiddenInput_totalfee+formHiddenInput_CIN;
    ajax_get_generalUsers();
}
function calculateHoursDiff(fromTime,toTime){
    time1=fromTime.split(":")
    time2=toTime.split(":")
    hour1=parseInt(time1[0]);
    hour2=parseInt(time2[0]);
    if(hour2-hour1>5){
        return 1;
    }
    else if (hour2-hour1<-5){
        return -1;
    }
    else{
        return 0;
    }
    
}
function delete_car(CIN){
    car_object = document.getElementById("inventoryInfo_row_"+CIN);
    string= "/CRSapp/delete_car/"+CIN;
    $.post(escape(string),{csrfmiddlewaretoken: getCookie('csrftoken')});
    $(car_object).remove();
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






