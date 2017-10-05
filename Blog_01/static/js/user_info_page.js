$(window).load(function () {
    let current_objects = {};
    let border = 0;

    function buildBlackListUserInfo(response){
        let info_list = $('.user-info-activity-list');
        $('.user-info-activity-title').text('черный список');
        $('.user-info-blacklist-button').attr('class', 'btn btn-primary btn-large user-info-current-activity-button').text('текущая активность');
        info_list.empty();
        $.each(response.data, (key, value) => {
            let blacklisted_user = $('<div class="blacklisted-user" id="' + value + '"></div>');
            let blacklisted_user_username = $('<span class="blacklisted-user-username">' + value + '</span>');
            let blacklisted_user_remove = $('<span class="glyphicon glyphicon-remove blacklisted-glyphicon"></span>');
            info_list.append(blacklisted_user.append(blacklisted_user_username).append(blacklisted_user_remove));
        });
    }

    function blacklistUserInfo() {
        let redirect_url = window.location.pathname.match(/\/[^/]+\/([^/]+)\//ig) + 'user_blacklist/';
        $.ajax({
            type: 'POST',
            url: redirect_url,
            dataType: 'json',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            success: function (response) {
                history.pushState('data', '', redirect_url);
                return buildBlackListUserInfo(response);
            }
        });
    }

    function current_activity_element_builder(response, key){
        let wrapper = $('<div class="activity-element"></div>');
        let header = $('<div class="activity-element-header"></div>');
        let header_avatar = $('<img src="' + response.avatar + '" height="32" class="img-circle">');
        let header_username = $('<span class="activity-element-username">' + response.username + '</span>');
        let header_created = $('<span class="activity-element-created">' + response.created + '</span>');
        let header_info = $('<span class="activity-element-info">' + response.info + '</span>');
        let text = $('<div class="activity-element-text">' + response.text + '</div>');
        header.append(header_avatar).append(header_created).append(header_username).append(header_info);
        wrapper.append(header).append(text);
        current_objects[key] = response[key];
        return wrapper;
    }

    function day_builder(key) {
        return $('<div class="day-border">' + key + '</div>');
    }

    function current_activity_builder(response){
        let user_activity_list = $('.user-info-activity-list');
        user_activity_list.empty();
        for (let key in response){
            user_activity_list.append(day_builder(key));
            for (let event in response[key]){
                let event_object = response[key][event];
                user_activity_list.append(current_activity_element_builder(event_object, event_object.pk));
            }
        }
    }

    function load_data(){
        $.ajax({
            type: 'POST',
            url: $(location).attr('pathname'),
            dataType: 'json',
            data: {'data': JSON.stringify(current_objects), 'border': JSON.stringify(border)},
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            success: function (response) {
                if ('errors' in response){
                    return errorCatcher(response.errors);
                }
                else{
                    $('.glyphicon-thumbs-up').next().text(response.total_likes);
                    $('.glyphicon-thumbs-down').next().text(response.total_dislikes);
                    return current_activity_builder(response.data);
                }
            }
        })
    }

    $(document).on('click', '.user-info-blacklist-button', () => blacklistUserInfo());

    $(document).on('click', '.user-info-current-activity-button',() => {
        $('.user-info-activity-title').text('последняя активность');
        history.pushState('data', '', window.location.pathname.match(/\/[^/]+\/([^/]+)\//ig));
        $('.user-info-current-activity-button').attr('class', 'btn btn-primary btn-large user-info-blacklist-button')
            .text('черный список');
        return load_data();
    });

    $(document).on('click', '.blacklisted-glyphicon', function(){
        $(this).parent().hide();
        let username = $(this).parent().attr('id');
        $.ajax({method: 'GET',
                dataType: 'json',
                url: '/block_user/' + username,
                success: (response) => {
                    return errorCatcher(response);
                }})
    });

    $(document).on('click', '.blacklisted-user-username', function(){
        window.location.href = '/' + $(this).parent().attr('id') + '/user_info/';
        }
    );

    if (window.location.pathname.search(/\/[^/]+\/[^/]+\/user_blacklist\//) == 0){
        $('.user-info-button').attr('class', 'btn btn-primary btn-large user-info-current-activity-button');
        return blacklistUserInfo();
    }
    else{
        $('.user-info-button').attr('class', 'btn btn-primary btn-large user-info-blacklist-button');
        return load_data();
    }

});
