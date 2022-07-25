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
                'title': $('#search-modal').find('.input-name')
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

    $('.state').click(function () {
        const state = $(this)
        const tID = state.data('source')
        const new_state = null;
        if (state.text() === "In Progress") {
            new_state = "Complete"
        } else if (state.text() === "Complete") {
            new_state = "Todo"
        } else if (state.text() === "Todo") {
            new_state = "In Progress"
        }

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});