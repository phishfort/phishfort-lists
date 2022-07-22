const fs = require("fs");
const path = require("path");
const tldjs = require("tldjs");
const { getDomainJsonFileNames } = require("./helpers/get-json-file-names");
const { log } = require("./helpers/log");

const init = async () => {
    const fileNames = getDomainJsonFileNames();

    let failed = false;
    for (let fn of fileNames) {
        const dirPath = path.join(__dirname, "..", `/${fn}`);
        const data = JSON.parse(fs.readFileSync(dirPath));

        for (let url of data) {
            if (tldjs.parse(url).hostname !== url) {
                log.error(`'${url}' in "${fn}" is not a valid domain.`);
                failed = true;
            }
        }
    }

    if (failed) process.exit(1);
};

init();
