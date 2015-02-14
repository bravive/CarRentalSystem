function reserveformContent(id){
    CIN=$("#CIN"+id).val();
    carFee=$("#FEE"+id).val();
    carType=$("#TPYE"+id).val();
    fromDate=$("#FD"+id).val();
    fromTime=$("#FT"+id).val();
    toDate=$("#TD"+id).val();
    toTime=$("#TT"+id).val();
    var array_FT = fromTime.split(" ");
    var array_TT = toTime.split(" ");
    console.log(array_FT);
    d1=new Date(fromDate);
    d2=new Date(toDate);
    var one_day=1000*60*60*24;
    var days = Math.round((d2.getTime()-d1.getTime())/one_day);
    if(calculateHoursDiff(array_FT,array_TT)){
        days=days+1;
    }
    var reserveform=document.getElementById("reseverForm");
    var tax=7;//7%
    var insurnce=10;//$10/day
    var total=(parseInt(carFee)*(1+0.07)+insurnce)*days;
    console.log(total);
    
    var formImg= "<img style=\"float:left\" src=\"/CRSapp/search_car_picture/"+carType+"\"  width=\"100px\"/>";
    var formFrom="<div style=\"float:left;width:350px\"> <p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>From</strong>: "+fromDate+" : "+fromTime+"</p>";
    var formTo= "<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>To</strong>: "+toDate+" : "+toTime+"</p>";
    var formType="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Type</strong>: "+carType+"</p>";
    var formRental="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Rental</strong>: $"+carFee+"/day</p>";
    var formTax="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Tax</strong>: "+tax+"%</p>";
    var formInsurance="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Insurance</strong>: $"+insurnce+"/day</p><hr />";
    var formtotal="<p class=\"media-body media-heading\" style=\"margin-left:20px\"><strong>Total</strong>: $"+total+"</p>"
    
    reserveform.innerHTML=formImg+formFrom+formTo+formType+formRental+formTax+formInsurance+formtotal;
}
function calculateHoursDiff(array_FT,array_TT){
    time1=array_FT[0].split(":")
    time2=array_TT[0].split(":")
    if (array_FT[1]=="AM"){
        hour1=parseInt(time1[0]);
    }
    else{
        hour1=parseInt(time1[0])+12;
    }
    if (array_TT[1]=="AM"){
        hour2=parseInt(time2[0]);
    }
    else{
        hour2=parseInt(time2[0])+12;
    }
    if(hour2-hour1>5){
        return 1;
    }
    else{
        return 0;
    }
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