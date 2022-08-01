$(document).ready(function () {
    // login button function
    $('#loginbtn').click(function () {
        console.log('login clicked');
        console.log($('#userid').val());
        $.ajax({
            type: "POST",
            url: "/check_user",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                'userID': $('#userid').val(),
                'account_passwd': $('#password').val()
            }),
            success: function (res) {
                console.log(res.response)
                if (res.success) {
                    location.href = '/';
                } else {
                    location.reload();
                    console.log('User not found');
                }
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    
});