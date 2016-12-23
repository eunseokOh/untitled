$(document).ready(function(){


$max_page = -1
$now_page = 0
$total_cnt = 0

var go_ajax = function(){
                $.ajax({
                    url : "/search/q={{query}}/isfirst"
                }).done(function(data){
                    console.log(data)
                    if ( data == 'None' ) {
                            var strong = $("<strong />", {
                                    text : "{{query}} 관련된 데이터를 웹에서 수집하고 있습니다. 약 5분 후 다시 검색해주세요.",

                                }).css({'color':'white', 'fontSize':'20px'})
                         $('#input_data').append(strong)
                    }
                })
                        $now_page += 1

                        $.ajax({
                          url: location.href,
                          type: 'POST',
                          data: {"page":$now_page},
                          dataType : 'json'
                        }).done(function( data ) {

                                if (data.length > 0){

                                    $max_page = data[0]['max_page']

                                    if( $now_page == 1 ){
                                        groups()
                                    }
                                    if (  data[0]['max_page'] > 1  ){
                                       $('#more_btn').show()
                                    }

                                    $.each(data, function(key, val){
                                          makeHtml(val)
                                    }); //end each

                                } else {
                                    var strong = $("<strong />", {
                                    text : "{{query}}와 관련된 데이터를 웹에서 찾지 못했습니다.",

                                    }).css({'color':'white', 'fontSize':'20px'})
                                    $('#input_data').append(strong)
                                }


                               if (  $now_page >= $max_page ){
                                $('#more_btn').hide()
                                $now_page = $max_page
                               }
                       });
                }//end go_ajax



                $('#more_btn').click(function(){
                    go_ajax()
                });

                $('#more_btn').hide()
                go_ajax()
});