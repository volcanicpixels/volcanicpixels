import $ from "jquery";
import NProgress from "nprogress";
import { showElement, hideElement, doError } from "modules/helpers";
import { setup, tokenize, setStripeKey } from "modules/credit-card/index";

$(document).ready(function(){

    setup();

    var stripeKey = $('.stripe-key').val();
    setStripeKey(stripeKey);

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
        if (hostname.length < 10) {
            return false;
        }
        var naked = hostname.match(/[a-z0-9][a-z0-9\-]*[a-z0-9]\.[a-z\.]{2,6}$/i);
        return naked ? (naked[0] === hostname) : null;
    };

    var verifyCSRRequest;

    var verifyCSR = function() {
        // cancel previous request
        try {
            verifyCSRRequest.abort();
        } catch (err) {
            // no request to cancel
        }

        var $csr = $('.csr');
        var $button = $('.load-csr');
        var $select = $('.verification-email-address');

        $csr.parent().addClass('loading');
        $select.parent().addClass('loading');
        $button.prop('disabled', true).text('Loading ...');

        hideElement('.csr-loaded');

        verifyCSRRequest = $.getJSON('verify_csr', {"csr": $csr.val()}, function(response){
            $csr.parent().removeClass('loading');
            $select.parent().removeClass('loading');
            $button.prop('disabled', false).text('Load Certificate Signing Request');
            if(doError(response)) {
                return;
            }


            $select.html('');

            $.each(response.data.emails, function(key, value){
                if (value === '') {
                    return;
                }
                $('<option></option>').html(value).val(value).appendTo($select);
            });

            showElement('.csr-loaded');
        });
    };

    $('.load-csr').click(verifyCSR);

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

        if (domain == undefined || domain.length == 0) {
            return;
        }

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

    var approverEmailRequest;

    var getApproverEmails = function(domain) {
        if (domain == undefined || domain.length == 0) {
            return;
        }
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
        var defaultEmail = $select.attr('data-default');

        $select.parent().addClass('loading');
        $('<option selected></option>').html('Loading...').prependTo($select);

        approverEmailRequest = $.getJSON('get_approver_emails', {"domain": domain}, function(response){
            $select.find('option:first').remove();
            $select.parent().removeClass('loading');
            if(doError(response)) {
                return;
            }


            $select.html('');

            $.each(response.data, function(key, value){
                if (value === '') {
                    return;
                }
                if(value == defaultEmail) {
                    $('<option selected></option>').html(value).val(value).appendTo($select);
                } else {
                    $('<option></option>').html(value).val(value).appendTo($select);
                }
            });

            $select.attr('data-domain', domain);
        });
    };


    var approvalEmailTimeout;

    /**
     * This is wrapped in a timeout to give other functions a chance to
     * change the value before we send it.
     */
    $('.domain').change(function(){
        var domain = $(this).val();
        clearTimeout(approvalEmailTimeout);
        approvalEmailTimeout = setTimeout(function(){
            getApproverEmails(domain);
        }, 100);

    }).change();

    var cardChange = function() {
        if ($('.new-card').is(':selected') ) {
            showElement('.credit-card-fieldset');
        } else {
            hideElement('.credit-card-fieldset');
        }
    };

    $('.chosen-card').change(cardChange);

    var addCards = function(cards) {
        if (cards.length === 0) {
            return;
        }

        $('.chosen-card option:not(.new-card)').remove();

        for (var i in cards) {
            var card = cards[i];
            var option = $('<option></option>');
            option.val(card['id']);
            option.text(card['name']);

            if (card['default']) {
                option.prop('selected', true);
            }

            option.appendTo('.chosen-card');
        }

        $('.chosen-card').change();

        $('.chosen-card').parent().removeClass('hide');

        // Todo - move "new card" to bottom
    };

    // If the user is loggedin then let's get their credit cards
    var getCards = function(email, password) {
        showElement('.loading-cards');
        var data = {};
        if (email) {
            data['email'] = email;
            data['password'] = password;
        }

        $('.credit-card').parent().addClass('loading');
        $.getJSON('get_cards', data,  function(response){
            $('.credit-card').parent().removeClass('loading');
            hideElement('.loading-cards');
            if (doError(response)) {
                $('.credit-card').parent().addClass('error');
                return;
            }

            addCards(response.data.cards);
        });
    };

    if ($('body').hasClass('loggedin')) {
        getCards();
    }

    var checkPasswordRequest;

    var checkPassword = function() {
        var $password = $('.password');
        var password = $password.val();
        var email = $('.email').val();

        if (password === '') {
            return;
        }

        try {
            checkPasswordRequest.abort();
        } catch (err) {
            // all is well
        }

        $password.parent().addClass('loading').removeClass('error');

        checkPasswordRequest = $.getJSON('check_password', {"password":password, "email":email}, function(response){
            $password.parent().removeClass('loading');
            if (doError(response)) {
                $password.parent().addClass('error');
                return;
            }

            if (response.data.user === 'incorrect') {
                // this is a new user
                hideElement('.new-user');
                hideElement('.correct-password');
                showElement('.incorrect-password');
                return;
            }

            if (response.data.user === 'correct') {
                // this is an existing user
                // TODO: parse credit cards
                hideElement('.new-user');
                hideElement('.incorrect-password');
                showElement('.correct-password');
                getCards(email, password);
                return;
            }
        });
    };

    /**
     * This timeout is so the checkPassword function is only called when the
     * user stops typing
     */
    var passwordChangeTimeout;

    var passwordChange = function() {
        clearTimeout(passwordChangeTimeout);
        passwordChangeTimeout = setTimeout(checkPassword, 650);
    };


    /**
     * If not logged in then we need to do some clever stuff with the supplied
     * email address.
     */

    var checkEmailRequest;

    var checkEmail = function() {
        var $email = $('.email');
        var email = $email.val();

        if (email === '') {
            return;
        }

        try {
            checkEmailRequest.abort();
        } catch (err) {
            // this is ok
        }

        $email.parent().addClass('loading').removeClass('error');

        checkEmailRequest = $.getJSON('check_email', {"email":email}, function(response){
            $email.parent().removeClass('loading');
            if (doError(response)) {
                $email.parent().addClass('error');
                return;
            }

            if (response.data.type === 'new') {
                // this is a new user
                hideElement('.existing-user');
                showElement('.new-user');
                $('.password').off('keyup', passwordChange);
                $('.password').off('blur', checkPassword);
            }

            if (response.data.type === 'existing') {
                // this is an existing user
                showElement('.existing-user');
                hideElement('.new-user');
                $('.password').on('keyup', passwordChange);
                $('.password').on('blur', checkPassword);
                checkPassword();
                // Add credit cards and select default one
            }

            if (response.data.academic) {
                showElement('.academic-user');
                hideElement('.non-academic-user');
            } else {
                hideElement('.academic-user');
                showElement('.non-academic-user');
            }
        });

    };

    /**
     * This timeout is so the checkEmail function is only called when the
     * user stops typing
     */
    var emailChangeTimeout;

    var emailChange = function() {
        clearTimeout(emailChangeTimeout);
        emailChangeTimeout = setTimeout(checkEmail, 650);
    };

    $('.email').on('keyup', emailChange);


    // A flag to let form submission occur after the form has been processed
    var formProcessed = false;

    /**
     * Purchase button flow:
     *  - Verify details (locally then server side)
     *  - Make sure credit card details are a stripe token
     *  - Initiate purchase
     */
    var purchase = function(e) {
        // check that a domain has been selected
        if (formProcessed) {
            console.log('Form Processed');
            return;
        }

        var submitOrder = function() {
            formProcessed = true;
            $('form').submit();
        };

        e.preventDefault();

        var errorFunc = alert;

        if($('.domain').val() === '') {
            return errorFunc("You haven't entered a domain");
        }

        if($('.country').val() === '') {
            return errorFunc("You haven't selected a country");
        }


        NProgress.start();
        if ($('.new-card').is(':selected')) {
            tokenize(function(){
                //submit form
                NProgress.set(0.4);
                submitOrder();
            }, function(){
                //an error
                NProgress.done();
            });
        } else {
            submitOrder();
        }
    };

    $('form').on('submit', purchase);

    // Disable form submission on enter
    $(document).on("keypress", 'form', function (e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            e.preventDefault();
            return false;
        }
    });

});
