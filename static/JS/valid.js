window.onload = function () {
        var random_str = ''
        $('#email-input').keyup(function(){
            if($(this).val().trim()!=''){
                $('#send-email').prop('disabled', false)
        }
    });
        $('#send-email').click(function () {
            var email = $('#email-input').val().trim();
            var num = 59
            $('#send-email').val(num+'秒');
            var t = setInterval(()=>{
                $(this).prop('disabled', true);
                num -= 1;
                $('#send-email').val(num+'秒');
                if(num==0){
                    clearInterval(t);
                    $('#send-email').val('发送验证码');
                    $(this).prop('disabled', false);
                }
            },1000);
            $.ajax({
                url: "/register_s/verify/",
                type: 'post',
                dataType: 'json',
                data: {'email': email},
                headers: {'X-CSRFToken': '{{ csrf_token }}'},
                success: function (data) {
                        $('#smscode_info').html('发送验证码成功').css('color', 'green');
                    random_str = data;
                    }
                })

        })

        $('#register').click(function (){
            flag = false;
            var valid = document.getElementById("valid-get").value;
            if (!valid){
                $('#valid-info').html('请先填写验证码').css('color', 'green')
            }
            else {
                $.ajax({
                    url: "/register_s/verify/",
                    type: 'post',
                    dataType: 'json',
                    data: {'valid': valid, 'random_str':random_str},
                    headers: {'X-CSRFToken': '{{ csrf_token }}'},
                    success: function (data) {
                        if (data == "ok"){
                            flag = true;
                            document.getElementById('register_form').submit()
                        }
                        else
                            $('#valid-info').html("验证码错误").css('color', 'green')
                        }
                })
            }
            if(flag){
                return true
            }
            else {
                return false
            }
        })
        }