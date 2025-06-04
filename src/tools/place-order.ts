import { MCPTool } from "mcp-framework";
import { execSync } from "child_process";
import { z } from "zod";
import { fileURLToPath } from "url";
import path from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

interface Placinginput {
    OrderType: string;
    Exchange: string;
    ExchangeType: string;
    ScripCode: number;
    Qty: number;
    Price: number;
    StopLossPrice: number;
    IsIntraday: boolean;
  }
  
function getPythonCommand(): string {
  const commands = ["python3", "python"];
  for (const cmd of commands) {
    try {
      const version = execSync(`${cmd} --version`).toString();
      if (version.toLowerCase().includes("python")) {
        return cmd;
      }
    } catch {
      // Try the next one
    }
  }
  throw new Error("No suitable Python interpreter found. Please install Python.");
}  

class PlacingTool extends MCPTool<Placinginput> {
  name = "Place_Order";
  description = "Place the order with the scrip code";
  schema = {
    OrderType: {
        type: z.enum(['B', 'S']),
        description: "Type of order, B for Buy, S for Sell",
    },
    Exchange: {
        type: z.enum(['N', 'B']),
        description: "N for NSE and B for BSE",
    },
    ExchangeType: {
        type: z.enum(['C', 'D', 'U']),
        description: "C for Equity, D for Derivatives and U for Currency",
    },
    ScripCode: {
        type: z.number(),
        description: "Code for asset",
    },
    Qty: {
        type: z.number(),
        description: "Quantity of asset",
    },
    Price: {
        type: z.number(),
        description: "Limit price of order, 0 if market order",
    },
    StopLossPrice: {
      type: z.number(),
      description: "Stop loss price, consider 0 if not mentioned",
    },
    IsIntraday: {
      type: z.boolean(),
      description: "Is this intraday order or not, true if yes and false for delivary",
    },
  };    

  async execute({ OrderType, Exchange, ExchangeType, ScripCode, Qty, Price, StopLossPrice, IsIntraday }: Placinginput) {
    try {
      const pythonCmd = getPythonCommand();
      const scriptPath = path.resolve(__dirname, "../tools/exec_codes/place_order.py");
      const command = `${pythonCmd} ${scriptPath} ${OrderType} ${Exchange} ${ExchangeType} ${ScripCode} ${Qty} ${Price} ${StopLossPrice} ${IsIntraday}`  
      const output = execSync(command);
      const data = output.toString();
      return data;
    } catch (error) {
      if (error instanceof Error) {
        // Optional: if using a library that throws custom error objects with "code"
        const errWithCode = error as Error & { code?: string };
    
        if (errWithCode.code === 'NETWORK_ERROR') {
          throw new Error('Unable to reach external service');
        }
    
        throw new Error(`Operation failed: ${errWithCode.message}`);
      } else {
        throw new Error('An unknown error occurred');
    }
  }
}
}

export default PlacingTool;
