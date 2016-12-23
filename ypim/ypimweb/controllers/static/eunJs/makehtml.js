$(document).ready(function(){
var makeHtml = function(val){
                var strong = $("<strong />", {
                    text : val['title']
                })


                var p = $("<p />",{

                }).append(strong).css('margin-top', '10px').css('height', ' 140px');


                var img = $("<img />", {
                    src : "/static/img_dir/"+val['img'],
                    width:"400",
                    height:"300"
                })

                var second_div = $("<div />", {}).addClass('thumbnail').css("cursor","pointer")

                second_div.append(img).append(p)


                $val_href = val['href']

                var a = $("<a />", {
                    class : "cls_vir",
                    alt : $val_href
                })

                var first_div = $("<div />", {

                }).addClass('col-sm-4').append(second_div)
                a.append(first_div)

                $('#input_data').append(a)

            }
});