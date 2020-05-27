function cart() {
    $.ajax({
		url: '/cart_form/',
		dataType: 'json',
		success: function (data) {
            var form = '<form method="post" target="_blank" action="https://www.liqpay.ua/api/3/checkout/" accept-charset="utf-8">\n' +
            '<input type="hidden" name="data" value="' + data.data + '"/>\n' +
            '<input type="hidden" name="signature" value="' + data.signature + '"/>\n' +
            '<button style="display: none" id="liqpay">\n' +
            '<span style="vertical-align:middle; !important">Оформити</span>\n' +
            '</button>\n' +
            '</form>';
            document.getElementById('cart').innerHTML += form;
            document.getElementById('liqpay').click();
        },
	});
}


function subscription(name) {
    $.ajax({
		url: '/subscription/' + name,
		dataType: 'json',
		success: function (data) {
            var form = '<form method="post" target="_blank" action="https://www.liqpay.ua/api/3/checkout/" accept-charset="utf-8">\n' +
            '<input type="hidden" name="data" value="' + data.data + '"/>\n' +
            '<input type="hidden" name="signature" value="' + data.signature + '"/>\n' +
            '<button style="display: none" id="liqpay">\n' +
            '<span style="vertical-align:middle; !important">Оформити</span>\n' +
            '</button>\n' +
            '</form>';
            document.getElementById('buy_subscription').innerHTML += form;
            document.getElementById('liqpay').click();
        },
	});
}

function subscription_update(name) {
    $.ajax({
		url: '/subscription_update/' + name,
		dataType: 'json',
		success: function (data) {
            var form = '<form method="post" target="_blank" action="https://www.liqpay.ua/api/3/checkout/" accept-charset="utf-8">\n' +
            '<input type="hidden" name="data" value="' + data.data + '"/>\n' +
            '<input type="hidden" name="signature" value="' + data.signature + '"/>\n' +
            '<button style="display: none" id="liqpay">\n' +
            '<span style="vertical-align:middle; !important">Оформити</span>\n' +
            '</button>\n' +
            '</form>';
            document.getElementById('change_sub').innerHTML += form;
            document.getElementById('liqpay').click();
        },
	});
}

function tokens(name) {
    $.ajax({
		url: '/tokens/' + name,
		dataType: 'json',
		success: function (data) {
            var form = '<form method="post" target="_blank" action="https://www.liqpay.ua/api/3/checkout/" accept-charset="utf-8">\n' +
            '<input type="hidden" name="data" value="' + data.data + '"/>\n' +
            '<input type="hidden" name="signature" value="' + data.signature + '"/>\n' +
            '<button style="display: none" id="liqpay">\n' +
            '<span style="vertical-align:middle; !important">Оформити</span>\n' +
            '</button>\n' +
            '</form>';
            document.getElementById('buy_tokens').innerHTML += form;
            document.getElementById('liqpay').click();
        },
	});
}


function subscription_cancel() {
    $.ajax({
		url: '/cancel_subscription/',
		dataType: 'json',
		success: function (data) {
            console.log(data.answer)
            if (data.answer === true) {
                var text = '<h1 class="product-detail-name" style="color: #1eea07">You have been successfully unsubscribed</h1>';
            } else {
                var text = '<h1 class="product-detail-name" style="color: red">Something went wrong, please try again later</h1>';
            }
            document.getElementById('answer_cancel_sub').innerHTML += text;
        },
	});
}
