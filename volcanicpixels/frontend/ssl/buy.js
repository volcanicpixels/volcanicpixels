import $ from "jquery";
import NProgress from "nprogress";
import { showElement, hideElement } from "modules/helpers";
import { setup, tokenize } from "modules/credit-card/index";

$(document).ready(function(){

    setup();

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
                $('<option></option>').html(value).val(value).appendTo($select);
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
        
    });

    var checkPasswordRequest;

    var checkPassword = function() {
        var $password = $(this);
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
                return;
            }
        });
    };


    /**
     * If not logged in then we need to do some clever stuff with the supplied
     * email address.
     */

    var checkEmailRequest;

    var checkEmail = function() {
        var $email = $(this);
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

            if (response.data === 'new') {
                // this is a new user
                hideElement('.existing-user');
                showElement('.new-user');
                $('.password').off('change', checkPassword);
                return;
            }

            if (response.data === 'existing') {
                // this is an existing user
                showElement('.existing-user');
                hideElement('.new-user');
                $('.password').on('change', checkPassword);
                // Add credit cards and select default one
                return;
            }
        });

    };

    $('.email').change(checkEmail);


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
        console.log('Purchase');
        if (formProcessed) {
            console.log('Form Processed');
            return;
        }

        var submitOrder = function() {
            formProcessed = true;
            $('form').submit();
        };
        
        e.preventDefault();
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
