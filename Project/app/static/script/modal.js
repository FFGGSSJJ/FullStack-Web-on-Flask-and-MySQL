$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    
    // show create modal
    $('#create-modal').on('show.bs.modal', function (event) {
        console.log("Create Modal opened");
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'Create') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Task ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })

    // show search modal
    $('#search-modal').on('show.bs.modal', function (event) {
        console.log("Search Modal opened");
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
    })

    // show update modal
    $('#update-modal').on('show.bs.modal', function (event) {
        console.log("Update Modal opened");
        const button = $(event.relatedTarget) // Button that triggered the modal
        const mID = button.data('movieid')
        const mTitle = button.data('title')
        const mOverview = button.data('overview')
        const mTagline = button.data('tagline')

        const modal = $(this)
        modal.find('.display-name').val(mTitle)
        modal.find('.display-info').val(mOverview)
        modal.find('.display-tagline').val(mTagline)
    })


    // function of create modal
    $('#create-task').click(function () {
        console.log('Create Task clicked');
        $.ajax({
            type: 'POST',
            url: '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'movie_id': 0,
                'title': $('#create-modal').find('.input-name').val(),
                'release_date': $('#create-modal').find('.input-date').val(),
                'overview': $('#create-modal').find('.input-info').val(),
                'tagline': $('#create-modal').find('.input-tagline').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    // function of search modal
    $('#search-task').click(function () {
        console.log('Search Task clicked');
        $.ajax({
            type: 'POST',
            url: '/search_movie', 
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'movie_id': $('#search-modal').find('.input-id').val(),
                'title': $('#search-modal').find('.input-name').val()
            }),
            success: function (res) {
                console.log(res.response)
                // location.reload();
                location.href = "/search_result";
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    

    // function of update modal
    $('#update-task').click(function () {
        console.log('Update Task clicked');
        console.log($('.updatebtn').data('movieid'));
        $.ajax({
            type: 'POST',
            url: '/edit/' + $('.updatebtn').data('movieid'),
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'title': $('#update-modal').find('.display-name').val(),
                'overview': $('#update-modal').find('.display-info').val(),
                'tagline': $('#update-modal').find('.display-tagline').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
        
    });

    // function of advanced search 0
    $('#adv0').click(function () {
        console.log('Advanced Search 0 clicked');
        $.ajax({
            type: 'POST',
            url: '/adv_query_0',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
            }),
            success: function (res) {
                console.log(res.response)
                location.href = '/adv_result_0';
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    // function of advanced search 1
    $('#adv1').click(function () {
        console.log('Advanced Search 1 clicked');
        $.ajax({
            type: 'POST',
            url: '/adv_query_1',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
            }),
            success: function (res) {
                console.log(res.response)
                location.href = '/adv_result_1';
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    // function of delete modal
    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    // function of check button
    $('.check').click(function () {
        console.log('Check clicked');
        const id = $(this).data('source')
        $.ajax({
            type: 'POST',
            url: '/movie_info',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'movie_id': id
            }),
            success: function (res) {
                console.log(res.response)
                location.href = '/movieintro';
            },
            error: function () {
                console.log('Error');
            }
        });
    });

// functions in Homepage
    // sidebar function
    $('.fa-search').click(function () {
        console.log('Search page clicked');
        location.href = '/search_page';
    });

    $('.fa-home').click(function () {
        console.log('Home page clicked');
        location.href = '/';
    });

    $('.fa-users').click(function () {
        console.log('User page clicked');
        location.href = '/userpage';
    });

    $('.fa-bookmark').click(function () {
        console.log('Bookmark page clicked');
        location.href = '/watchlist_page';
    });


    // function of movie record
    $('.movie-list-item-button').click(function () {
        console.log('check clicked');
        const button = $(this) // Button that triggered the modal
        const id = button.data('movieid')
        $.ajax({
            type: 'POST',
            url: '/movie_info',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'movie_id': id
            }),
            success: function (res) {
                console.log(res.response)
                location.href = '/movieintro';
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    //function of logout button
    $('#logoutbtn').click(function () {
        console.log('logout clicked');
        location.href = '/login';
    });

    // function of add list item button
    $('#addfavbtn').click(function () {
        console.log('addlist clicked');
        console.log($(this).data('movie'))
        console.log($(this).data('user'))
        $.ajax({
            type: 'POST',
            url: '/create_watchlist_item',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'userID': $(this).data('user'),
                'movie_id': $(this).data('movie'),
                'watch_id': 0,
                'watch_add_date': 0
            }),
            success: function (res) {
                console.log(res.response)
                location.href = '/movieintro';
            },
            error: function () {
                console.log('Error');
            }
        });
    });

// functions in Search Page
    $('#search-btn').click(function () {
        console.log('Search clicked');
        if ($('#field').val() != ""){
            $.ajax({
                type: 'POST',
                url: '/search_movie',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify({
                    'title': $('#field').val()
                }),
                success: function (res) {
                    console.log(res.response)
                    location.href = '/search_result';
                },
                error: function () {
                    console.log('Error');
                }
            });
        } else {
            console.log("Genre Filter");
            $.ajax({
                type: 'POST',
                url: '/genre_filter',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify({
                    'Animation': $('#Animation').is(":checked") ? 1:0,
                    'Comedy': $('#Comedy').is(":checked") ? 1:0,
                    'Adventure': $('#Adventure').is(":checked") ? 1:0,
                    'Action': $('#Action').is(":checked") ? 1:0,
                    'Romance': $('#Romance').is(":checked") ? 1:0,
                    'War': $('#War').is(":checked") ? 1:0
                }),
                success: function (res) {
                    location.href = '/search_result';
                },
                error: function () {
                    console.log('Error');
                }
            });
        }
    });


});