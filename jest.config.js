/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */
module.exports = {
    preset: 'ts-jest',
    clearMocks: true,
    coverageProvider: "v8",
    testEnvironment: "jsdom",
    testMatch: [
        '**/*.test.ts'
    ],
    setupFilesAfterEnv: ['<rootDir>/jest-setup.ts']
};