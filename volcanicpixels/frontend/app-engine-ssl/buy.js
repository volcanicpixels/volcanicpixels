import $ from "jquery";


$(document).ready(function(){

var startsWith = function(input, test) {
    return (input.substring(0, test.length) === test);
};


/**
 * Helper function for determining whether this is a top level domain
 */
var isNaked = function(hostname) {
    if (hostname.indexOf('www') != -1) {
        return false;
    }
    var naked = hostname.match(/[a-z0-9][a-z0-9\-]*[a-z0-9]\.[a-z\.]{2,6}$/i);
    return naked ? (naked[0] === hostname) : null;
};

var showElement = function(selector) {
    if ($(selector).hasClass('dismissed')) {
        return;
    }
    if ($(selector).hasClass('hide')) {
        $(selector).hide().removeClass('hide').slideDown(100);
    }
};

var hideElement = function(selector) {
    if (!$(selector).hasClass('hide')) {
        $(selector).slideUp(100,function(){
            $(this).addClass('hide');
        });
    }
};


/**
 * When the domain field changes
 * 
 * Full should be true when this was triggered from a blur event otherwise
 * we will assume that it is not safe to modify the input just yet.     
 * @return {[type]} [description]
 */
var verifyDomain = function(full) {
    var $domain = $(this);
    var domain = $domain.val();

    // Does it contain an asterisk?
    if (domain.indexOf('*') != -1) {
        showElement('.wildcard-message');
    } else {
        hideElement('.wildcard-message');
    }

    domain = domain.replace('http://', '');
    domain = domain.replace('https://', '');
    domain = domain.replace('/', '');
    domain = domain.replace(' ', '');

    // Is it a naked domain?
    if (isNaked(domain)) {
        $('.naked-domain .hostname').html(domain);
        showElement('.naked-domain');
    } else {
        hideElement('.naked-domain');
    }

    if (full === true) {
        $domain.val(domain);
    }
};

$('.domain').change(function(){
    verifyDomain.call(this, true);
});
$('.domain').keyup(verifyDomain);


$('.naked-domain .yes').click(function(){
    var current = $('.domain').val();
    $('.domain').val( 'www.' + current).change();
});

$('.naked-domain .no').click(function(){
    $('.naked-domain').addClass('dismissed');
    hideElement('.naked-domain');
});

var doError = function(response) {
    if(!response.status || response.status !==  "SUCCESS") {
        var msg = response.msg || 'Unknown error occured';
        alert(msg);
        return true;
    }
    return false;
};

var approverEmailRequest;

var getApproverEmails = function(domain) {
    // cancel previous request
    try {
        approverEmailRequest.abort();
    } catch (err) {
        // no request to cancel
    }

    if ($('.verification-email-address').attr('data-domain') === domain) {
        return;
    }

    var $select = $('.verification-email-address');

    $select.prop('disabled', true);
    $select.parent().addClass('loading');

    approverEmailRequest = $.getJSON('get_approver_emails', {"domain": domain}, function(response){
        if(doError(response)) {
            return;
        }

        $select.prop('disabled', false);
        $select.parent().removeClass('loading');

        $select.html('');

        $.each(response.data, function(key, value){
            $('<option></option>').html(value).val(value).appendTo($select);
        });

        $select.attr('data-domain', domain);
    });
};


/**
 * This is wrapped in a timeout to give other functions a chance to
 * change the value before we send it.
 */
$('.domain').change(function(){
    var domain = $(this).val();
    setTimeout(function(){
        getApproverEmails(domain);
    }, 50);
    
});


/**
 * On wildcard signup then present email, name, and 'Notify me', 'Cancel'
 */


/**
 * Purchase button flow:
 *  - Verify details (locally then server side)
 *  - Make sure credit card details are a stripe token
 *  - Initiate purchase
 */


});
