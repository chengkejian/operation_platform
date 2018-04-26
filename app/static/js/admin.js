//JS for delete user
function DeleteUser(url){
    $('#deleteUserClick').click(function(){
        window.location.href = url;
    });
    $('#deleteUserModle').modal();
}

//JS for edit user
function EditUser(url){
    $.getJSON(url,function(data){
        $('#editUserName').val(data.username);
        $('#editEmail').val(data.email);
//        $('#editConfirmed').checked=String(data.confirmed);
//        $('#editConfirmed').val(Number(data.confirmed));
        document.getElementById("editConfirmed").checked = data.confirmed;
        $('#editRole').val(data.role);
        $('#editName').val(data.name);
        $('#editDepartment').val(data.department);
        $('#editAboutme').val(data.about_me);
        $('#editUserModle').modal();
        $('#editUserClick').click(function(){
            document.editUser.action="/admin/edit_user_info/"+data.id;
//            document.getElementById("demo").innerHTML = data.id;
        });
    });
}

//JS for delete post
function DeletePost(url){
    $('#deletePostClick').click(function(){
        window.location.href = url;
    });
    $('#deletePostModle').modal();
}

//JS for filter android channel
$(document).ready(function(){
    arguments=window.location.search.substr(1).split("&");
    var arguments2={};
    for(var n=0;n<arguments.length;n++){
        arguments2[arguments[n].split("=")[0]]=arguments[n].split("=")[1];
    }
    version_filter=document.getElementById("version_filter");
    package_link_filter=document.getElementById("package_link_filter");
    replace_ico_filter=document.getElementById("replace_ico_filter");
    package_status=document.getElementById("package_status_filter");
    package_upload_status=document.getElementById("package_upload_status_filter");
    for(var i=0;i<version_filter.options.length;i++){
        if(version_filter.options[i].value==arguments2.version){
            version_filter.options[i].selected=true;
        }
    }
    for(var i=0;i<package_link_filter.options.length;i++){
        if(package_link_filter.options[i].value==arguments2.package_link){
            package_link_filter.options[i].selected=true;
        }
    }
    for(var i=0;i<replace_ico_filter.options.length;i++){
        if(replace_ico_filter.options[i].value==arguments2.replace_ico){
            replace_ico_filter.options[i].selected=true;
        }
    }
    for(var i=0;i<package_status_filter.options.length;i++){
        if(package_status_filter.options[i].value==arguments2.package_status){
            package_status_filter.options[i].selected=true;
        }
    }
    for(var i=0;i<package_upload_status_filter.options.length;i++){
        if(package_upload_status_filter.options[i].value==arguments2.package_upload_status){
            package_upload_status_filter.options[i].selected=true;
        }
    }
})

//JS for filter url
$(document).ready(function(){
    $('#filterChannelClick').click(function(){
        var platform = window.location.pathname.split("/")[3].split("?")[0];
        var version=document.getElementById("version_filter").value;
        var package_link=document.getElementById("package_link_filter").value;
        var replace_ico=document.getElementById("replace_ico_filter").value;
        var package_status=document.getElementById("package_status_filter").value;
        var package_upload_status=document.getElementById("package_upload_status_filter").value;
        document.getElementById('FilterChannelForm').action =
            "/android/androidpack/"+platform+"?"+"version="+version+"&package_link="+package_link
            +"&replace_ico="+replace_ico+"&package_status"+package_status+"&package_upload_status"+package_upload_status;
    });
})


//JS for 渠道列表
//$(".nav-pills").delegate('li', "click", function(){
//    $(this).addClass("active");
//    alert(location.href);
//});

$(document).ready(function(){
    id_name = window.location.pathname.split("/")[3];
//    alert(id_name[3]);
    $("#"+id_name).addClass("active");
})

//JS for delete android channel
function deleteChannel(url){
    $('#deleteChannelClick').click(function(){
        window.location.href = url;
    });
    $('#deleteChannelModle').modal();
}

//JS for select-all
$(document).ready(function(){
    $('#select-all').click(function () {
        if ($(this).prop('checked')) {
            $('.op_check').prop('checked', true);
        } else {
            $('.op_check').prop('checked', false);
        }
    });
})

//JS for delete android channels
function deleteChannels(){

    if ($('.op_check').filter(':checked').size() > 0) {
        var channelIds = [];
        $('.op_check:checked').each(function(){
            channelIds.push($(this).val());
        });
        var channelIdsJson = JSON.stringify(channelIds);
        $('#del_channelIds').val(channelIdsJson)
        $('#delChannlesModel').modal();
    } else {
        $('#selChannlesModel').modal();
      }
    $('#delChannelsClick').click(function(){
        $('#delChannelsForm').submit();
    });
}

//JS for package android channels
function packageChannels(){
    if ($('.op_check').filter(':checked').size() > 0) {
        var channelIds = [];
        $('.op_check:checked').each(function(){
            channelIds.push($(this).val());
        });
        var channelIdsJson = JSON.stringify(channelIds);
        $('#pkg_channelIds').val(channelIdsJson)
        $('#pkgChannlesModel').modal();
    } else {
        $('#allpkgChannlesModel').modal();
        $('#allpkgChannlesModel').on('shown.bs.modal',function() {
            $('#allpkgChannelsForm').formValidation('resetForm', true);
        });
      }
    $('#pkgChannelsClick').click(function(){
        $('#pkgChannelsForm').submit();
    });
}

//JS for publish android channels
function publishChannels(){
    if ($('.op_check').filter(':checked').size() > 0) {
        var channelIds = [];
        $('.op_check:checked').each(function(){
            channelIds.push($(this).val());
        });
        var channelIdsJson = JSON.stringify(channelIds);
        $('#pub_channelIds').val(channelIdsJson)
        $('#pubChannlesModel').modal();
    } else {
        $('#allpubChannlesModel').modal();
      }
}

//JS for edit android channels version
function editChannels(){
    if ($('.op_check').filter(':checked').size() > 0) {
        var channelIds = [];
        $('.op_check:checked').each(function(){
            channelIds.push($(this).val());
        });
        var channelIdsJson = JSON.stringify(channelIds);
        $('#edit_channelIds').val(channelIdsJson)
        $('#editChannlesModel').modal();
    } else {
        $('#selChannlesModel').modal();
      }
}


//JS for check search channel id
function check_channelId(form) {
    if(form.channleId.value==''){
        $('#search-channel').addClass("has-error");
        form.channleId.placeholder='不能为空!';
        return false;
    }
    if(isNaN(form.channleId.value)){
        $('#search-channel').addClass("has-error");
        form.channleId.value='';
        form.channleId.placeholder='请按channel号查找!';
        return false;
    }
    return true
}

//JS for add channel
$(document).ready(function(){
    $('#addChannel').click(function(){
        $('#addChannelModle').modal('show');
    });
    $('#addChannelModle').on('shown.bs.modal',function() {
        $('#addChannelForm').formValidation('resetForm', true);
        $('#package_link-0').prop('checked', true);
        $('#need_replace_ico-1').prop('checked', true);
        $('#need_replace_ico-0').click(function() {
            $('#image_upload').show();
        });
        $('#need_replace_ico-1').click(function() {
            $('#image_upload').hide();
        });
        if($('input:radio[name="need_replace_ico"]:checked').val()=='1'){
            $('#image_upload').show();
        } else{
            $('#image_upload').hide();
        }
    });
})


//function for fileinput 初始化
function InitFileinput(img) {
    $("#"+img).fileinput({
                language: 'zh', //设置语言
                uploadUrl: "/android/img_upload", //上传的地址
                allowedFileExtensions : ['jpg', 'png'],//接收的文件后缀,
                maxFileCount: 5,
                enctype: 'multipart/form-data',
                showUpload: true, //是否显示上传按钮
                showCaption: false,//是否显示标题
                browseClass: "btn btn-primary", //按钮样式
                dropZoneEnabled: true,  //是否显示拖拽区域
                previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
                msgFilesTooMany: "选择上传的文件数量({n}) 超过允许的最大数值{m}！",
                layoutTemplates:{
                 actions: '<div class="file-actions">\n' +
                        '    <div class="file-footer-buttons">\n' +
                        '        {upload} {delete}' +
                        '    </div>\n' +
                        '    <div class="file-upload-indicator" tabindex="-1" title="{indicatorTitle}">{indicator}</div>\n' +
                        '    <div class="clearfix"></div>\n' +
                        '</div>'
                }
         });
}


// JS for 初始化 fileinput控件
$(document).ready(function(){
// JS for 初始化 add channel fileinput控件
    InitFileinput("img-input");
// JS for 初始化 edit channel fileinput控件
    InitFileinput("edit_img-input");
})


//JS for edit channel
function EditChannel(url){
    $.getJSON(url,function(data){
        $('#edit_ChannelName').val(data.channelname);
        $('#edit_Channel').val(data.channel);
        $('#edit_version').val(data.version);
        $('#edit_AppName').val(data.app_name);
        if (data.package_link=='package'){
            $('#edit_package_link-0').prop('checked', true);
        } else {
            $('#edit_package_link-1').prop('checked', true);
        };
        if (data.need_replace_ico){
            $('#edit_need_replace_ico-0').prop('checked', true);
        } else {
            $('#edit_need_replace_ico-1').prop('checked', true);
        };

        $('#editChannelModle').modal('show');

        $('#editChannelModle').on('shown.bs.modal',function() {
            $('#editChannelForm').formValidation('resetForm', false);
            if (data.need_replace_ico){
                document.getElementById('channel-img').src="/static/images/channelIco/native_R"+data.version+"/channelIco/"+data.channel+"-"+data.platform+"/ivp_common_app_icon.png"+"?"+Math.random()
                $('#edit_need_replace_ico-0').click(function() {
                    $('#edit_channelImage').show();
                    $('#edit_image_upload').hide();
                });
                $('#edit_need_replace_ico-1').click(function() {
                    $('#edit_channelImage').hide();
                    $('#edit_image_upload').hide();
                });
                if($('input:radio[name="edit_need_replace_ico"]:checked').val()=='1'){
                    $('#edit_channelImage').show();
                    $('#edit_image_upload').hide();
                } else {
                    $('#edit_channelImage').hide();
                    $('#edit_image_upload').hide();
                };
            } else{
                $('#edit_need_replace_ico-0').click(function() {
                    $('#edit_image_upload').show();
                    $('#edit_channelImage').hide();
                });
                $('#edit_need_replace_ico-1').click(function() {
                    $('#edit_image_upload').hide();
                    $('#edit_channelImage').hide();
                });
                if($('input:radio[name="edit_need_replace_ico"]:checked').val()=='1'){
                    $('#edit_image_upload').show();
                    $('#edit_channelImage').hide();
                } else {
                    $('#edit_channelImage').hide();
                    $('#edit_image_upload').hide();
                };
            };
        });
        $('#editChannelClick').click(function(){
        document.getElementById('editChannelForm').action ="/android/edit_channel_info/"+data.id+"?"+"page="+data.page;
        });
    });
}

//Function for edit channel change img
function ChangeImg() {
    $('#edit_image_upload').show();
    $('#edit_channelImage').hide();
}

//JS for channel package
function packageChannel(channelId,page){
    $('#packageChannelClick').click(function(){
        document.getElementById('channelPackageForm').action ="/android/channel_package/"+channelId+"?"+"page="+page;
    });
    $('#packageChannelModle').modal();
}

//JS for channel package upload
function uploadChannelapk(url){
    $('#uploadChannelapkClick').click(function(){
        window.location.href = url;
    });
    $('#uploadChannelapkModle').modal();
}

//JS for package_status view
$(document).ready(function(){
    var platform = window.location.pathname.split("/")[3];
    var data={};
    $.ajax({
        type:'GET',
        url:"/android/package_status?platform="+platform,
        data:data,
        dataType:'json',
        success:function(re){
            document.getElementById('package_now').innerText=re.package_now;
            document.getElementById('package_error').innerText=re.package_error;
            document.getElementById('upload_now').innerText=re.upload_now;
            document.getElementById('upload_error').innerText=re.upload_error;
        },
        error:function(xhr, type){
            document.getElementById('package_now').innerText='未知';
            document.getElementById('package_error').innerText='未知';
            document.getElementById('upload_now').innerText='未知';
            document.getElementById('upload_error').innerText='未知';
        }
    });
})


