const fs = require('fs');
const path = require('path');
const { isValidJSON } = require("./helpers/is-valid-json");
const { getJsonWhitelistFileNames } = require("./helpers/get-json-file-names");
const { log } = require("./helpers/log");

const init = async () => {
	const fileNames = await getJsonWhitelistFileNames();

	for (let fn of fileNames) {
		const dirPath = path.join(__dirname, '..', `/${fn}`);
		let data = fs.readFileSync(dirPath);

		if (isValidJSON(data)) {
			data = JSON.parse(data);
		} else {
			log.error(`[${fn}] - Invalid JSON file.`);
			process.exit(1);
		}

		if (!Array.isArray(data)) {
			log.error(`[${fn}] - Data type inside the file is not an array`);
			process.exit(1);
		}

		// Check for duplicates:
		let hasDupes = data.filter((val, i) => data.indexOf(val) !== i);

		hasDupes.length && log.warn(`Duplicates found in ${fn}: ${hasDupes.toString()}`) && process.exit(1);

		hasDupes.length === 0 && log.info(`[${fn}] - No duplicates ✅`);
	}
}

init();