const { log } = require("./log");

module.exports = {
    isValidJSON: (str) => {
        try {
            JSON.parse(str);
        } catch (e) {
            log.error(e);
            return false;
        }

        return true;
    }
}