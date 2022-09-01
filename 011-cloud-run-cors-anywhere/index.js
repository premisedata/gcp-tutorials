const cors_proxy = require('cors-anywhere');

const port= parseInt(process.env.CORS_PORT || '') || 8080;
const host = process.env.CORS_HOST || '0.0.0.0';

cors_proxy.createServer({
    originWhitelist: [], // Allow all origins
    requireHeader: ['origin', 'x-requested-with'],
    removeHeaders: ['cookie', 'cookie2']
}).listen(port, host, () => {
    console.log('Running CORS Anywhere on ' + host + ':' + port);
});