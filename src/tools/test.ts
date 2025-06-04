import { fileURLToPath } from "url";
import path from "path";
// import { MCPTool } from "mcp-framework";
import { execSync } from "child_process";

// Emulate __filename and __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Resolve the Python script path relative to this file
const scriptPath = path.resolve(__dirname, "../tools/exec_codes/fetch_holdings.py");
// const output = execSync(`python3 ${scriptPath}`);
// const data = output.toString();

// Output for testing
console.log("__filename:", __filename);
console.log("__dirname:", __dirname);
console.log("Resolved script path:", scriptPath);
// console.log("Final output", data)
