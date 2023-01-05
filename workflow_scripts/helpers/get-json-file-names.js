const glob = require("glob");
const { log } = require("./log");

const getJsonFileNames = (globSelector) => {
    return new Promise((resolve, reject) => {
        glob(globSelector || "*(whitelists|blacklists)/*.json", (err, files) => {
            if (err) {
                log.error(err);
            } else {
                resolve(files);
            }
        });
    });
};

module.exports = {
    getJsonFileNames: async () => await getJsonFileNames(),
    getDomainJsonFileNames: () => ["blacklists/domains.json", "whitelists/domains.json"],
    getJsonWhitelistFileNames: async () => await getJsonFileNames("whitelists/*.json"),

};
