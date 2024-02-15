import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import {config as dotenvConfig} from 'dotenv';
dotenvConfig();

const accounts: string[] = [process.env.SK!];

const config: HardhatUserConfig = {
  networks:{
    tenderlyeth:{
      url: process.env.TENDERLY_RPC_URL!,
      accounts
    },
    polygon: {
      url:"https://polygon.drpc.org",
      accounts
    }
  },
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: {
        enabled: true,
        runs: 1000,
      },
    },
  },
};

export default config;
