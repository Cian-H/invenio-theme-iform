const config = {
    singleQuote: false,
    tabWidth: 4,
    trailingComma: "all",
    printWidth: 100,
    plugins: ["prettier-plugin-jinja-template"],
    overrides: [
        {
            files: ["*.html"],
            options: {
                parser: "jinja-template",
            },
        },
        {
            files: "*.yaml",
            options: {
                tabWidth: 2,
            },
        },
        {
            files: "*.yml",
            options: {
                tabWidth: 2,
            },
        },
    ],
};

export default config;
