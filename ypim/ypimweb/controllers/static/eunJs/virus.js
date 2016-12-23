
$(document).ready(function(){
var makeTable = function(keys, values){
                    var tr = $("<tr />", {});

                    var td_url_scanner = $("<td />", {
                        text : keys
                    });

                    var td_detected = $("<td />", {
                        text : values['detected']
                    });

                    var td_result = $("<td />", {
                        text : values['result']
                    });

                    detail_href = values['detail']

                    if(detail_href != null && detail_href.length > 70){
                       detail_href = detail_href.substring(0,60) + "..."
                    }

                    detail_link = $("<a />", {
                        href : values['detail'],
                        text : detail_href
                    })

                    td_detail = $("<td />", {

                    }).append(detail_link);

                    tr.append(td_url_scanner).append(td_detected).append(td_result).append(td_detail)

                    if ( values['detected'] != false || values['result'] != 'clean site'){
                        tr.css({"color":"red"})
                    }

                    $('#virus_info_tbody').append(tr)

            }

  $(document).on("click",".cls_vir",function(){

                this_url = $(this).attr("alt")
                text_url = this_url

                if ( text_url.length > 80 ){
                       text_url = text_url.substring(0,80)+"..."
                }
                swal({
                      title: "URL 악성코드 분석",
                      text: text_url+"\n\n웹 사이트에 접속하기 전에 악성 코드를 검사해보시겠습니까?",
                      type: "warning",
                      showCancelButton: true,
                      confirmButtonColor: "#DD6B55",
                      confirmButtonText: "검사할래요",
                      cancelButtonText: "사이트로 이동할래요",
                      closeOnConfirm: false,
                      closeOnCancel: false
                    },
                    function(isConfirm){
                      if (isConfirm) {
                           swal({
                              title: "ANALYZING..",
                              imageUrl: "{{url_for('static',filename='img_dir/cat.gif')}}",
                              imageSize : "200x200",
                              showConfirmButton : false
                            });

                           $.ajax({
                                url:"/urlvirus",
                                data: this_url,
                                type:"POST"
                           }).done(function(data){

                                if (data != "Virus total app key Error"){
                                    var data_string = ""
                                    var data_scans = "======================================================================================================================= \n"
                                    $.each(data, function(key, val){

                                              if(key != 'scans'){
                                                  data_string += key + " = " + val +"\n"
                                              } else {
                                                    console.log(val)
                                                    $.each(val, function(key_, val_){

                                                               makeTable(key_, val_);
                                                    });

                                              }// end if
                                    });
                                    swal.close();
                                    info_virus(data_string, this_url);
                               }else{
                                    swal("ERROR!", data, "error");
                               }
                           }) //end ajax

                      } else {
                        swal.close();
                        window.open(this_url)

                      }
                });
            }); //end vir

             var info_virus = function(data, url){
                           var text_url = url
                           $('#virus_info_body').empty()
                           $('#virus_info_header').empty()
                            if ( text_url.length > 100 ){
                                text_url = text_url.substring(0,100)+"..."
                            }
                           $('#virus_info_body').append(data)
                           $('#virus_info_header').append(text_url)
                           $('#btn_go_website').attr('onclick', 'window.open("'+url+'")');
                           $('#virus_info').modal('show')
             }

             });