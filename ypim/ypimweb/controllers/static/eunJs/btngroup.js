  $(document).ready(function(){

   var group_ajax = function(val){

                if( val == "TOTAL"){
                    $now_page = 0
                    $total_cnt = 0
                    $('#input_data').empty();
                    $('#groups').empty();
                    $('#more_btn').hide();
                    go_ajax()
                } else {
                        $.ajax({
                        url : "groups/q={{query}}/w="+val,
                        type : 'GET'
                    }).done(function(data){
                        if ( data.length > 0 ){
                            $('#input_data').empty();
                            $('#more_btn').hide();
                            $.each(data, function(key, val){
                                makeHtml(val)
                            })//end each
                        }
                    }); //end ajax
                } //end if
            };

            var makeGroupBtns = function(val){
                var button = $("<button />", {
                    text : val['web_site'] + " ",
                    click : function(){
                        group_ajax(val['web_site'])
                    }
                }).addClass('btn btn-default')

                var span = $("<span />", {
                    text : val['cnt']
                }).addClass('badge')
                $total_cnt += val['cnt']

                button.append(span)

                $('#groups').append(button)
            };
var groups = function(){
                $.ajax({
                    url : "groups/q={{query}}",
                    type : 'GET'

                }).done(function(data){
                    if(data.length > 0){
                        $.each(data, function(key,val){
                            makeGroupBtns(val)

                        });//end each
                        var json = new Object();
                        json.web_site = 'TOTAL'
                        json.cnt = $total_cnt
                        JSON.stringify(json)
                        makeGroupBtns(json);

                    }

                });//end ajax

            } //end groups

            });