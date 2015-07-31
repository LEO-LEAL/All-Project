$(document).ready(function(){
  setInterval(function(){
    var left_right_movement = Math.random() * 100;
    var up_down_movement = Math.random() * 100;
    var leftrightp = "" + left_right_movement + "vh";
    var updownp = "" + up_down_movement + "vh";
    console.log(leftrightp + " " + updownp);
     $("#bulls").animate({ left: leftrightp, top: updownp} , 4000, 'swing')
   },0);
 });
