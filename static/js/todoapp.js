     function createList(ele){
                $('#modal2').modal('open');
          }

          $('#new_list').submit(function(event){
               event.preventDefault();
               var formdata = $(this).serializeArray();
               console.log(formdata);
               var newlist = new Object();
                for(var i=0;i<formdata.length;i++){
                     newlist[formdata[i].name] = formdata[i].value;
                }
               $.ajax({
                    url: "/todoapp/api/lists/",
                    headers: {
                    'X-CSRFToken' : GetCookie('csrftoken')
                    },
                    dataType: "json",
                    type: "POST",
                    data : newlist,
                    success: function(data){
                         swal("Booya! New List has been Added!", "", "success")
                         console.log("sucess");
                         data["items"] = new Array();
                         console.log(data);
                         var makedatatmpl = new Array();
                         makedatatmpl.push(data);
                         $("#listTemplate").tmpl(makedatatmpl).appendTo('#todolists');
                    },
                    error:function(){
                         swal("Something went wrong!","",failure);
                         console.log("error");
                    }
               });
          });

          function deleteList(ele){
               console.log(ele);
               var listid = ele.id.replace(/^del_list_/, '')

               swal({
                 title: "Are you sure? you are about to delete complete list!",
                 text: "You will not be able to recover the while list again!",
                 type: "warning",
                 showCancelButton: true,
                 confirmButtonColor: "#DD6B55",
                 confirmButtonText: "Yes, delete it!",
                 closeOnConfirm: false
               },
               function(){
                    $.ajax({
                         url: "/todoapp/api/lists/"+listid+"/",
                         headers: {
                              'X-CSRFToken' : GetCookie('csrftoken')
                         },
                         dataType: "json",
                         type: "DELETE",
                         success: function(data){
                              console.log("sucess");
                              var domid = "#lis_"+listid;
                              console.log(domid);
                              $(domid).remove();
                              swal("Deleted!", "Your todo list has been deleted.", "success");

                         },
                         error:function(){
                              swal("Something went wrong, try again","failure");
                              console.log("error");
                         }
                    });
               })
          }

          function updateFun(ele){
               $('#modal1').modal('open');
          }

          function postFun(ele){
               console.log(ele);
               var listid = ele.id.replace(/^butt_/, '')
               var desc = $('#new_item_'+listid).val();
               var dueby = $('#new_date_'+listid).val();
               var compl = $('#new_compl_'+listid).prop('checked')
               console.log(listid);
               console.log(desc);
               console.log(dueby);
               console.log(compl);
               var post_data = new Object();
               post_data["description"] = desc;
               post_data["due_by"] = dueby;
               post_data["completed"] = compl;

               $.ajax({
                    url: "/todoapp/api/lists/"+listid+"/items/",
                    headers: {
                         'X-CSRFToken' : GetCookie('csrftoken')
                    },
                    dataType: "json",
                    type: "POST",
                    data : post_data,
                    success: function(data){
                         swal("Good job!", "You added a new todo item!", "success")
                         console.log("sucess");
                         console.log(data);
                         var rowBegin = ' <tr id=items_'+data["id"]+' class=\"item\">';
                         var row1 =  ' <td id=items_desc_'+data["id"]+'>'+data["description"] +'</td>';
                         var row2 =  ' <td id=items_due_'+data["id"]+'>'+ data["due_by"] +'</td>';
                         var row3 =  ' <td id=items_desc_'+data["id"]+'>'+data["completed"] + '</td>';
                         console.log(rowBegin);
                         console.log(row1);
                         console.log(row2);
                         console.log(row3);
                         var row4 = ' <td><a id=\"upd_item_'+data['id']+'\"' + ' class="modal-trigger waves-effect waves-teal" href="#modal1"> <i class="material-icons">input</i> </a> </td>';
                         var row5 = ' <td><a id=item_'+data["id"]+' class="del_item" href="javascript:;"> <i class="material-icons">delete</i> </a> </td>';
                         var rowEnd = ' </tr>';
                         var html = rowBegin+row1+row2+row3+row4+row5+rowEnd;
                         console.log(html);
                         var domid = "#table_"+listid;
                         $(domid).prepend(html);
                    },
                    error:function(){
                         swal("Something went wrong!", ":(", "success")
                         console.log("error");
                    }
               });
          }

     function GetCookie(sName){
            var aCookie = document.cookie.split("; ");
            for (var i=0; i < aCookie.length; i++){
              var aCrumb = aCookie[i].split("=");
              if (sName == aCrumb[0])
                return unescape(aCrumb[1]);
            }
            return null;

       }

     $(document).ready(function(){
          $("#welcomeuser").text("Welcome "+GetCookie("username")+" !");

          $('.dropdown-button').dropdown({
                inDuration: 300,
                outDuration: 225,
                hover: true, // Activate on hover
                belowOrigin: true, // Displays dropdown below the button
                alignment: 'right' // Displays dropdown with edge aligned to the left of button
              }
            );
             $('.modal').modal();

              var date = new Date();

              var day = date.getDate();
              var month = date.getMonth() + 1;
              var year = date.getFullYear();

              if (month < 10) month = "0" + month;
              if (day < 10) day = "0" + day;

              var today = year + "-" + month + "-" + day;
              $("#theDate").attr("value", today);

           $.ajax({
               url: "/todoapp/api/lists/",
               headers: {
                    'Content-Type': 'application/json',
               },
               dataType: "json",
               type: "GET",
               contentType: "application/json; charset=utf-8",
               success: function(data){
                    $("#response").html(data);
                    $('#loader').hide();
                    console.log(data);
                    $("#listTemplate").tmpl(data).appendTo('#todolists');
               },
               error:function(){
                    console.log("error");
               }
          });

          $('body').on('click','.del_item',function(){
               var id = this.id.replace(/^item_/, '');
               var hide = "#items_"+id;
               swal({
                 title: "Are you sure?",
                 text: "You will not be able to recover this todo item again!",
                 type: "warning",
                 showCancelButton: true,
                 confirmButtonColor: "#DD6B55",
                 confirmButtonText: "Yes, delete it!",
                 closeOnConfirm: false
               },
               function(){

                  $.ajax({
                         url: "/todoapp/api/items/"+id+"/",
                         headers: {
                              'Content-Type': 'application/json',
                              'X-CSRFToken' : GetCookie('csrftoken')
                         },
                         dataType: "json",
                         type: "DELETE",
                         contentType: "application/json; charset=utf-8",
                         success: function(data){
                              swal("Deleted!", "Your todo item has been deleted.", "success");
                              $(hide).remove();
                         },
                         error:function(){
                              swal("Some Error Occured","failure");
                              console.log("error");
                         }
                    });

               });

          });

          var itemid;
          var listid;

          $('#modal3').modal({dismissible: true, opacity: .5, inDuration: 300, outDuration: 200, startingTop: '4%', endingTop: '10%',
               ready: function(modal, trigger) { listid = trigger["0"].id.replace(/^upd_list_/, ''); },
               complete: function(){ }
          });

          $('#modal1').modal({
               dismissible: true, opacity: .5, inDuration: 300, outDuration: 200, startingTop: '4%',endingTop: '10%',
               ready: function(modal, trigger) { itemid = trigger["0"].id.replace(/^upd_item_/, '');  },
               complete: function(){  }
          });

          $('#update_list').submit(function(event){
               event.preventDefault();
               var formdata = $(this).serializeArray();
               console.log(formdata);
               var newlist = new Object();
               for(var i=0;i<formdata.length;i++){
                     newlist[formdata[i].name] = formdata[i].value;
               }
               console.log(newlist);
                     console.log(listid);
                     $.ajax({
                         url: "/todoapp/api/lists/"+listid+"/",
                         headers: {
                              'X-CSRFToken' : GetCookie('csrftoken')

                         },
                         dataType: "json",
                         type: "PUT",
                         data : newlist,
                         success: function(data){
                              swal("Sucessfully Updated!", "Good job!", "success")
                              console.log("sucess");
                              $('#lists_name_'+listid).html(newlist["name"]);
                              $('#lists_date_'+listid).html(newlist["creation_date"]);

                         },
                         error:function(){
                              swal("Something went wrong!", "", "failure")
                              console.log("error");
                         }
               });
          });

          $('#updform').submit(function(event){
                    event.preventDefault();
                    console.log(itemid);
                    var formdata = $(this).serializeArray();
                    var upd_data = new Object();
                    console.log(formdata);
                    for(var i =0;i<formdata.length;i++){
                         if(formdata.name == "item_status"){
                              if(formdata.value["item_status"]=="on"){
                                   upd_data["completed"] = true;
                              }
                              else{
                                   upd_data["completed"] = false;
                              }
                         }
                         else{
                              upd_data[formdata[i].name] = formdata[i].value;
                         }
                    }
                    if(!upd_data.hasOwnProperty("completed")){
                         upd_data["completed"] = false;
                    }

                    console.log(upd_data);
                    $.ajax({
                         url: "/todoapp/api/items/"+itemid+"/",
                         headers: {
                              'X-CSRFToken' : GetCookie('csrftoken')
                         },
                         dataType: "json",
                         type: "PUT",
                         data : upd_data,
                         success: function(data){
                              swal("Sucessfully Updated!", "", "success")

                              console.log("sucess");
                              $('#items_desc_'+itemid).html(upd_data["description"]);
                              $('#items_due_'+itemid).html(upd_data["due_by"]);
                              $('#items_compl_'+itemid).html(upd_data["completed"]);
                         },
                         error:function(){
                              swal("Something went wrong!", "", "failure")
                              console.log("error");
                         }
                    });
               })
       });