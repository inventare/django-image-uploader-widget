const path = require('path');

module.exports = (env) => ({
    entry: {
        widget: ['./src/ImageUploaderWidget.ts'],
        inline: ['./src/ImageUploaderInline.ts'],
    },
    mode: env.production ? "production" : "development",
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    output: {
        filename: env.production ? 'image-uploader-[name].min.js' : 'image-uploader-[name].js',
        path: path.resolve(__dirname, 'image_uploader_widget', 'static', 'admin', 'js'),
    }
});
