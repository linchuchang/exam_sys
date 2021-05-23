window.onload = function (){
    var show=document.getElementById("show").getElementsByTagName("span");
    var time_start = new Date();
    var clock_start = time_start.getTime();

    function get_time_spent(){
        var time_now = new Date();
        return((time_now.getTime()-clock_start)/1000)
    }

    setInterval(function(){
        var num= get_time_spent();
        num-= num%(1);
        var second = num%60;
        num -= second;
        var minute=parseInt(num/60);
        num -= minute*60;
        var hour=parseInt(num/60);

      show[0].innerHTML=hour;
      show[1].innerHTML=minute;
      show[2].innerHTML=second;
    },100)
}

