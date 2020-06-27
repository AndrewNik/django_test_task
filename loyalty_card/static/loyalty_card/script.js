$(function () {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $(".dropdown-menu a").click(function () {
        change_card(this);
    });

    function change_card(dd_elem) {
        let card = $(dd_elem).parentsUntil('card', '.card'),
            ser_num = card.find('.card-title > span').text(),
            status = $(dd_elem).text();

        let selText = $(dd_elem).text();

        $.ajax({
            url: `${window.location.origin}/loyalty/card/update/`,
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: {'series': ser_num.split(' ')[0], 'number': ser_num.split(' ')[1], 'status': status},
            success: function(data) {
                if(data.result)
                    $(dd_elem).parent().siblings('.btn').children('.selection').text(selText);
            }
        });
    }

    $(".card-delete").click(function () {
        let cur_elem = $(this);
            ser_num = cur_elem.parent().siblings('.card-body').find('.card-title span').text();

        $.ajax({
            url: `${window.location.origin}/loyalty/card/delete/`,
            type: 'DELETE',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: {'series': ser_num.split(' ')[0], 'number': ser_num.split(' ')[1]},
            success: function(data) {
                if(data.result) {
                    let card_cont = cur_elem.parentsUntil('card-container', '.card-container');
                    card_cont.remove();
                }
            }
        });
    })
});