$(document).ready(function () {
    let chat_list_id = null;
    let total_objects = 0;
    let border = 0;
    let chat_list = {};

    function chat_room_build(data, pk) {
        let message_li = $('<li class="message-chat-list-room" id="' + pk + '"></li>');
        let message_room_url = $('<a href="' + data.url + '"></a>');
        let user_info = $('<div class="message-chat-list-room-image"></div>');
        let user_image = $('<img class="img-circle" src="' + data.user_image + '">');
        let user_username = $('<span class="message-chat-list-room-username">' + data.username + '</span>');
        let message_created = $('<span class="message-chat-list-room-created">' + data.created + '</span>');
        let message_text = $('<div class="message-chat-list-text"><span class="data-message-text">' + data.last_message + '</span></div>');
        let border_bottom = $('<div class="message-border"></div>');
        if (data.check == false){
            message_text.append($('<div class="unread-dot" data-check=' + data.check + '></div>'));
        }
        else{
            message_text.append($('<div class="read-dot" data-check=' + data.check + '></div>'));
        }
        if (data.last_message_user_image){
            message_text.prepend(('<img class="img-circle text" src="' + data.last_message_user_image + '">'));
        }
        message_room_url.append(user_info.append(user_image).append(user_username)
                    .append(message_created)).append(message_text).append(border_bottom);
        message_li.append(message_room_url);
        chat_list[pk] = data;
        return message_li;
    }

    function last_message_update(data, key){
        data.update = false;
        chat_list[key] = data;
        let message_node = $('.message-chat-list').find('#' + key).find('.message-chat-list-text');
        let dot = message_node.find('[data-check="false"]');
        if (dot && data.check == true){
            dot.attr('class', 'read-dot');
        }
        if (dot == undefined && data.check == false){
            dot.attr('class', 'unread-dot');
        }
        message_node.find('.data-message-text').text(data.last_message_text);
    }


    function refresh_call(scroll=false){
        $.ajax({
            type: 'POST',
            url: '/get_chat_list_data/',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: {'data': JSON.stringify(chat_list), 'border': JSON.stringify(border)},
            success: function (response) {
                total_objects = response.total_messages;
                if (response.message){
                    $('.message-chat-list').append($('<div>' + response.message + '</div>'))
                }
                else{
                    let room_list = response.chat_room_list;
                    for (let key in room_list){
                        if (room_list[key].update == true){
                            last_message_update(room_list[key], key);
                    }
                    else{
                        $('.message-chat-list').append(chat_room_build(room_list[key], key));
                        }
                    }
                }
            },
            complete: function () {
                if (scroll == false){
                    setTimeout(function() {refresh_call()}, 2000)
                }
            }
        })
    }

    refresh_call();
});
