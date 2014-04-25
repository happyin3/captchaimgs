/* __author__ = "happyin3" */

$(document).ready(function(){
    $(window).scroll(function(){
        var top = $(this).scrollTop();
        var flowSearch = $("#mainsearch");
        flowSearch.css("top", top+10);
    })

    $("#thesis").click(function(){
        var url = $("#thesislink").val()
        $.post("/getThesisImage",{"url": url},
            function(data, status){
                if(data == "1"){
                    alert("输入为空");
                }
                else if(data == "2"){
                    alert("资源不存在");
                }
                else if(data == "3"){
                    alert("下载失败");
                }
                else if(data == "4"){
                    alert("格式未转换");
                }
                else if(data == "5"){
                    alert("图片未提取");
                }
                else if(data == "6"){
                    alert("文档中没有图片");
                }
                else{
                    alert(data);
                    $("img").attr("src", data);
                }
            }
        );
    });
   
    $("#patent").click(function(){
        var patentno = $("#patentno").val()
        $.post("/getPatentImage",{"patentno": patentno},
            function(data, status){
                if(data == "1"){
                    alert("输入为空");
                }
                else if(data == "2"){
                    alert("资源不存在");
                }
                else if(data == "3"){
                    alert("下载不成功");
                }
                else if(data == "4"){
                    alert("为提取图片");
                }
                else if(data == "5"){
                    alert("文档中没有图片");
                }
                else{
                    alert(data);
                    $("img").attr("src", data);
                }
            }
        );
    });
});
