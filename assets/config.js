var require = {
    baseUrl: '/assets',
    paths: {
        stripe: 'https://js.stripe.com/v2/?1',
        jquery: 'components/jquery/jquery',
        nprogress: 'components/nprogress/nprogress',
        requirejs: 'components/requirejs/require'
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
