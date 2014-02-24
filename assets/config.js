var require = {
    baseUrl: '/assets',
    paths: {
        stripe: 'https://js.stripe.com/v2/?1',
        requirejs: 'components/requirejs/require',
        nprogress: 'components/nprogress/nprogress',
        jquery: 'components/jquery/jquery'
    },
    shim: {
        stripe: {
            exports: 'Stripe'
        },
        nprogress: {
            exports: 'NProgress',
            deps: [
                'jquery'
            ]
        }
    }
};
