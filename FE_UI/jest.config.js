// jest.config.js
module.exports = {
  preset: "ts-jest",
  transform: {
    "^.+\\.(ts|tsx)?$": "ts-jest",
    "^.+\\.(js|jsx)$": "babel-jest",
  },
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.ts"],
  testEnvironment: "jsdom",
  moduleNameMapper: {
    "\\.(css|less|scss)$": "<rootDir>/__mocks__/styleMock.js", // Adjust the path if necessary
    "^components/(.*)$": "<rootDir>/src/components/$1", // Adjust according to your structure
    "^utils/(.*)$": "<rootDir>/src/utils/$1",

    "^@/(.*)$": "<rootDir>/src/$1",
    "^react-dnd$": "react-dnd/dist/cjs",
    "^react-dnd-html5-backend$": "react-dnd-html5-backend/dist/cjs",
    "^dnd-core$": "dnd-core/dist/cjs",
  },
  transformIgnorePatterns: [
    "/node_modules/(?!(uuid|@emerald-react))/", // Example of packages to transpile
    // "/node_modules/(?!(uuid|@emerald/nxcore)/)",
  ],
  globals: {
    "ts-jest": {
      useESM: true,
    },
  },
};
