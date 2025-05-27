import axios from "axios";

const config = {
    'database': 'scola',
    'port': ':8069',
};

const ApiManager = axios.create({
    // LOCAL
    baseURL: 'http://192.168.18.7' + config.port,
    // PRODUCTION
    // baseURL: 'http://192.168.1.8' + config.port,
    headers: {
        'Content-Type': 'application/json'
    }
});

export default ApiManager;