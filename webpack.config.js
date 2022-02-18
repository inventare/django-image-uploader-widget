const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env) => ({
    entry: {
        widget: [
            './src/ImageUploaderWidget.ts',
            './src/ImageUploaderWidget.scss',
        ],
        inline: [
            './src/ImageUploaderInline.ts',
            './src/ImageUploaderInline.scss',
        ],
    },
    mode: env.production ? "production" : "development",
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "sass-loader",
                ]
            }
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js', '.scss'],
    },
    output: {
        filename: env.production ? 'image-uploader-[name].min.js' : 'image-uploader-[name].js',
        path: path.resolve(__dirname, 'image_uploader_widget', 'static', 'admin', 'js'),
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: `../css/image-uploader-[name]${env.production ? '.min' : ''}.css`,
        }),
    ],    
});
