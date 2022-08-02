$(document).ready(function () {
    // login button function
    $('#loginbtn').click(function () {
        console.log('login clicked');
        console.log($('#userid').val());
        $.ajax({
            type: "POST",
            url: "/verify_user",
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

    // register button function
    $('#registerbtn').click(function () {
        console.log('register clicked');
        $.ajax({
            type: "POST",
            url: "/register",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                'name': $('#regname').val(),
                'password': $('#regpassword').val(),
                'age': $('#regage').val(),
                'Animation': $('#Animation').is(":checked") ? 1:0,
                'Comedy': $('#Comedy').is(":checked") ? 1:0,
                'Adventure': $('#Adventure').is(":checked") ? 1:0,
                'Action': $('#Action').is(":checked") ? 1:0,
                'Romance': $('#Romance').is(":checked") ? 1:0,
                'War': $('#War').is(":checked") ? 1:0
            }),
            success: function (res) {
                console.log(res.userid)
                if (res.success) {
                    console.log(res.userid)
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