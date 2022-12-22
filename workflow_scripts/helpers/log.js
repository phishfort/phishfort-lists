module.exports = {
    log: {
        info: (value) => console.info("\x1b[34m", value),
        error: (value) => console.error("\x1b[31m", value),
    }
}