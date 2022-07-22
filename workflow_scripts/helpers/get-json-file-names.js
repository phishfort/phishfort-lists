const glob = require("glob");
const { log } = require("./log");

const getJsonFileNames = () => {
    return new Promise((resolve, reject) => {
        glob( '*(whitelists|blacklists)/*.json',(err, files) => {
            if (err) {
                log.error(err);
            } else {
                resolve(files);
            }
        })
    })
}

module.exports = {
    getJsonFileNames: async () => await getJsonFileNames()
}