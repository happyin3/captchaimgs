/*__author__ = "happyin3" */

$(document).ready(function(){
    $("#test").click(function(){
        $.post("/getThesisImage",{"url": "/qk/81177X/201303/45912275.html"},
            function(data, status){
                if(data == "1"){
                    alert("输入为空");
                }
                else if(data == "2"){
                    alert("资源不存在");
                }
                else{
                    alert(data);
                    $("img").attr("src", data);
                }
            }
        );
    });
});
