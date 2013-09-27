var require = {
    baseUrl: '/assets',
    paths: {
        stripe: 'https://js.stripe.com/v2/?1',
        nprogress: 'components/nprogress/nprogress',
        jquery: 'components/jquery/jquery',
        requirejs: 'components/requirejs/require'
    },
    shim: {
        stripe: {
            exports: 'Stripe'
        },
        nprogress: {
            exports: 'NProgress'
        }
    }
};
