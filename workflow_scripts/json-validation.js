const fs = require('fs');
const path = require('path');
const { isValidJSON } = require("./helpers/is-valid-json");
const { getJsonFileNames } = require("./helpers/get-json-file-names");
const { log } = require("./helpers/log");

const init = async () => {
    const fileNames = await getJsonFileNames();

    for (let fn of fileNames) {
        const dirPath = path.join(__dirname, '..', `/${fn}`);
        let data = fs.readFileSync(dirPath);

        if (isValidJSON(data)) {
            log.info(`[${fn}] - JSON file is valid.`);
            data = JSON.parse(data);
        } else {
            log.error(`[${fn}] - Invalid JSON file.`);
            process.exit(1);
        }

        if (!Array.isArray(data)) {
            log.error(`[${fn}] - Data type inside the file is not an array`);
            process.exit(1);
        }

        for (let url of data) {
            if (typeof url !== 'string') {
                log.error(`'${url}' in "${fn}" is not a string.`);
                process.exit(1);
            }
        }
    }
}

init();