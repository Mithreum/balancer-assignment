import { ethers } from "hardhat";

async function main() {

  const requester = await ethers.deployContract("SlipageRequester");

  await requester.waitForDeployment();

  console.log(`Deployed to ${requester.target}`);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
