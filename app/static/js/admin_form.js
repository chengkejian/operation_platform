//JS for register user
function RegisterUser(){
    $('#registerModel').modal();
    $('#registerModel').on('shown.bs.modal',function() {
        $('#registerForm').formValidation('resetForm', true);
    });
}

//JS for forget password
function ForgetPasswd(){
    $('#fopasswordModel').modal();
    $('#fopasswordModel').on('shown.bs.modal',function() {
        $('#fopasswordForm').formValidation('resetForm', true);
    });
}
//for form 验证
$(document).ready(function(){
//for register user form 验证
    $('#registerForm').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
//            feedback: 'fv-control-feedback'
        },
        fields: {
            username: {
                validators: {
                    notEmpty: {
                        message: '用户名不能为空！'
                    },
                regexp: {
                    regexp: /^[A-Za-z][A-Za-z0-9_]*$/,
                    message: '以字母开头，并且只能包含字母，数字，下划线~~'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: 'email不能为空！'
                    },
                    emailAddress: {
                        message: '不是有效的email地址'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: '密码不能为空！'
                    }
                }
            },
            password2: {
                validators: {
                    notEmpty: {
                        message: '请再次输入密码！'
                    },
                    identical: {
                        field: 'password',
                        message: '两次密码输入不一致，请重新输入'
                    }
                }
            }
        }
    });
//for edit channels version form 验证
    $('#fopasswordForm').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
//            feedback: 'fv-control-feedback'
        },
        fields: {
            name: {
                validators: {
                    notEmpty: {
                        message: '不能为空噢！'
                    },
                regexp: {
                    regexp: /^[A-Za-z][A-Za-z0-9_]*$/,
                    message: '以字母开头，并且只能包含字母，数字，下划线~~'
                    }
                }
            }
        }
    });
//for add channel form 验证
    $('#addChannelForm').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
//            feedback: 'fv-control-feedback'
        },
        fields: {
            channel_name: {
                validators: {
                    notEmpty: {
                        message: '渠道名不能为空！'
                    }
                }
            },
            channel: {
                validators: {
                    notEmpty: {
                        message: '渠道号不能为空！'
                    },
                    stringLength: {
                        min: 4,
                        message: '最少为4位！'
                    },
                    regexp: {
                        regexp: /^[0-9]+$/,
                        message: '只能为整数'
                    }
                }
            },
            version: {
                validators: {
                    notEmpty: {
                        message: '版本号不能为空！'
                    },
                 regexp: {
                        regexp: /^[0-9]+.[0-9]+.[0-9]+$/,
                        message: '格式错误，"X.Y.Z"  X,Y,Z均为整数~~'
                    }
                }
            },
            app_name: {
                validators: {
                    notEmpty: {
                        message: 'app名称不能为空！'
                    }
                }
            }
        }
    });
//for edit channel form 验证
    $('#editChannelForm').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
//            feedback: 'fv-control-feedback'
        },
        fields: {
            edit_channel_name: {
                validators: {
                    notEmpty: {
                        message: '渠道名不能为空！'
                    }
                }
            },
            edit_channel: {
                validators: {
                    notEmpty: {
                        message: '渠道号不能为空！'
                    },
                    stringLength: {
                        min: 4,
                        message: '最少为4位！'
                    },
                    regexp: {
                        regexp: /^[0-9]+$/,
                        message: '只能为整数'
                    }
                }
            },
            edit_version: {
                validators: {
                    notEmpty: {
                        message: '版本号不能为空！'
                    },
                 regexp: {
                        regexp: /^[0-9]+.[0-9]+.[0-9]+$/,
                        message: '格式错误，"X.Y.Z"  X,Y,Z均为整数~~'
                    }
                }
            },
            edit_app_name: {
                validators: {
                    notEmpty: {
                        message: 'app名称不能为空！'
                    }
                }
            }
        }
    });
//for edit channels version form 验证
    $('#editChannelsVersionForm').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
//            feedback: 'fv-control-feedback'
        },
        fields: {
            edit_version: {
                validators: {
                    notEmpty: {
                        message: '版本号不能为空！'
                    },
                regexp: {
                    regexp: /^[0-9]+.[0-9]+.[0-9]+$/,
                    message: '格式错误，"X.Y.Z"  X,Y,Z均为整数~~'
                    }
                }
            }
        }
    });
//for package channels version form 验证
    $('#allpkgChannelsForm').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
//            feedback: 'fv-control-feedback'
        },
        fields: {
            to_version: {
                validators: {
                    notEmpty: {
                        message: '版本号不能为空！'
                    },
                regexp: {
                    regexp: /^[0-9]+.[0-9]+.[0-9]+$/,
                    message: '格式错误，"X.Y.Z"  X,Y,Z均为整数~~'
                    }
                }
            }
        }
    });
})
