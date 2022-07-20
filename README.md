# Purpose
DAOs have proven to be one of the most important aspects of the web3 space. Although their adoption has grown, the complexity of the contracts can deter a lot of developers from trying to implement them. This is why we created this library: to simplify the lifes of developers and, by doing so, bringing them to the Vechain space. By simplifing the DAO framework, devs are more free to study and try to implement more specific use cases by playing around with the solidity code. Although there is much use for websites who simplify this type of creations, libraries are essential to the space as they allow for the manipulation and discovery of new aspects of the DAO governance.

Vechain is also a perfect place to create a DAO governance due to the low fees and speed it offers.

In the bigger scope, we would love to build more libraries related to the main web3 apsects as of now, like NFTs and ERC20 tokens. The main goal is to funel devs interested in the blockchain space into Vechain, by creating an almost non-existent barrier of entry for them.

# How to use?
This library can be used in two ways:
1) If the user wants to simply build a DAO, he can just git clone this repository which will provide a good starting ground for that porpuse. If this is the case, then the [Folders](#Folders) section in this README is relevant, otherwise it can be ignored. In this event, you can just install the requirments using the *requirements.txt*:
```
pip install requirements.txt
```
2) If the user wants to simply use the library in a larger project it can just install it with pip and import it normaly. The user also needs to create a .env file to store the variables explained in [.env.example](#.env.example) (NOT YET READY)
```
pip install VE_DAO
```
# Sample Script
A sample of a possible DAO creation script using this library, can be seen in *test_lib.py*. It show 3 main sections:
1) *val* function: only used to check the value present in the Box.sol contract we are trying to change with the governance;
2) *init* function: deploy contracts, grant and revoke roles;
3) *main* function: we create a proposal, vote on it with 2 different wallets (one with a "For" vote with 2 weight and another with an "Against" vote with 1 weight, making the proposal pass), queue and then execute it. Some time.sleep breaks are used to simulate the passage of time;

The console output resulting from running this script can be seen in the figure bellow:
![Console Output](/images/output.png "Console Output")


# Folders
## Only for Convinience/Can be deleted:
- **build**: holds the compiled contracts. The name of this folder may very from what you use to compile your smart contracts, but that is irrelavent as you need to provide the path to you contract compilation when initializing the library;
- **build_static**: a place to hold contract which are already deployed/won't be changed/don't need recompilation;
- **contracts**: holds the contracts to be used:
    * GovernanceContract.sol: Imports a variety of core contracts that contain all the logic and primitives. More information about all the contracts that it can inherit can be found in [the OpenZeppelin documentation](https://docs.openzeppelin.com/contracts/4.x/api/governance#governor). This contract can be costumized and fitted to the users needs using the [OpenZeppelin contract wizard](https://wizard.openzeppelin.com/#governor).
  
    * GovernanceTimeLock.sol: Contract module which acts as a timelocked controller. When set as the owner of an Ownable smart contract, it enforces a timelock on all onlyOwner maintenance operations. This gives time for users of the controlled contract to exit before a potentially dangerous maintenance operation is applied. More information can be found in [the OpenZeppelin documentation](https://docs.openzeppelin.com/contracts/4.x/api/governance#TimelockController)
    * Box.sol: a simple contract to be controlled by the DAO;
## Indispenseable
- **scripts**: hold the library and the example implementation of the library showed in [the Sample Script section](#Sample-Script). The libraries sections are shown in the figure bellow;

    ![Library Structure](/images/lib.png "Library Structure")
  


# .env.example
The .env.example file gives an example of how the .env file should look like. This file is where the contract addresses will be stored for easy access, automated substitution or manual change.
The .env file will keep the following variables:

1) **MNEMONIC_1 to MNEMONIC_X**: being X the amount of wallets the lib user whishes to import and use. 
2) **Token_contract_address**: contract of a token that will be wrapped (was not made with the the ERC20Votes extension standard for DAOs) or of a token that does not require wrapping;
3) **wToken_contract_address**: the address of the wrapped version of Token_contract_address(if the wrapping was necessary, otherwise this will be left blank because it will not be used)
4) **TimeLock_contract_address**: address of the TimeLock contract that is deployed by the DAO lib (or of an already deployed one)
5) **Governance_contract_address**: address of the Governance contract that is deployed by the DAO lib (or of an already deployed one)
6) **Changeable_contract_address**: address of the contract that is to be changed by the DAO governance that is deployed by the DAO lib (or of an already deployed one)



# DAO_lib
This section details the various components of this library. This can be used to learn how to use it faster or for easier fork modifications to fit more specific use cases.
## A) Variables:
| Variable      | Type | Description |
| ----------- | ----------- | ----------- |
| network_choice     | int       | Defines if the user wants to connect to the testnet (1) or mainnet (2) |
| self    |        | Refers to the variables that are globally assigned in a specific class |
| connector   | object        | See thor_requests.connect from the [thor_requests library](https://github.com/laalaguer/thor-requests.py)|
| _wallet     | object       | imported wallet object|
| _wallet_address   | string(address)        | imported wallet address |
| TimeLock_build_dir     | string(address)       | path to the the build of the GovernanceTimeLock.sol (ex: "build\contracts\GovernanceTimeLock.json")|
| Governance_build_dir   | string(address)        | path to the the build of the GovernanceContract.sol|
| Changeable_build_dir     | string(address)       | path to the the build of the contract the user wishes to control with the DAO governance (called "Changeable" in the code)|
| Token_build_file_dir   | string(address)        | path to the the build of the token we want to use to vote|
| wToken_build_file_dir     | string(address)       | path to the the build of the wrapping of the token. This is only needed if the original token was not made with the ERC20Votes extension, necessary for the the standard DAO governance contract|
| wrapped   | string        | Tells the lib classes if there was a need to wrap a token or if the original token was already according to DAO standard ("yes" if it required wrapping and "no" otherwise) |
| min_delay   | int        | delay for governance decisions to be executed. The workflow is extended to require a queue step before execution. With these modules, proposals are executed by the external timelock contract, thus it is the timelock that has to hold the assets that are being governed.|
| quorum_percentage   | int        |Quorum required for a proposal to be successful. This function includes a blockNumber argument so the quorum can adapt through time, for example, to follow a token’s totalSupply |
| voting_period   | int        | Delay (in number of blocks) since the proposal starts until voting ends.|
| voting_delay   | int        | Delay (in number of blocks) since the proposal is submitted until voting power is fixed and voting starts. This can be used to enforce a delay after a proposal is published for users to buy tokens, or delegate their votes.|
| func_name   | strind        | Used to pass the name of the function that the proposal refers to. For example, if we want to change the "value" variable to "53" then the *func_name* would be "store" (see the Box.sol contract) |
| params   | array( with various types inside)       |The parameters that will be used in the function that the proposal is aimed at. For example, if we want to change the "value" variable to "53" then the *params* would be "[53]" (see the Box.sol contract)|
| proposal   | string        | A small discription of the proposal|
| proposal_id   | int        | An identifier is created for each different proposal|
| vote   | int        | Denotes the intention of the voter towards a proposal: 0->Against, 1->For, 2->Abstain|

## B) Basic.py: 
Wallet import and connection to Vechain nodes (testnet or mainnet). This is just a simplification of the [thor_requests library](https://github.com/laalaguer/thor-requests.py) to make it easier to import various wallets using the .env file.
### Functions:
* wallet_import_mnemonic(num): receives a number (*num*) that identifies which mnemonic we want to get from the .env file in order to import a specific wallet;
* connect(network_choice): connects to the testnet node (network_choice == 1) or to the mainnet (network_choice == 2) through veblocks; 

## C) DAO.py
proposal, voting and queue/excute functions for the DAO
### Functions:
* init(self, connector, _wallet, _wallet_address, TimeLock_build_dir, Governance_build_dir, Changeable_build_dir, Token_build_dir): initializes these values to be used by the class;
* set_wToken(self, wToken_build_dir): if there was a need to wrap a token, this function is used to specify the build location and to get the address from .env file;
* propose(self, _wallet, func_name, params, proposal): creates and submits a proposal to be voted on. Returns the *proposal_id*;
* check_proposal_by_id(self, proposal_id): checks the state of a certain proposal (identified by a *proposal_id*). Returns a string with the current state. The possible states are:
    * Pending => 0
    * Active => 1
    * Canceled => 2
    * Defeated => 3
    * Succeeded => 4
    * Queued => 5
    * Expired => 6
    * Executed => 7

* prop_end_block(self, proposal_id): returns the current chain block and the block in which the the voting for this proposal will end;
* vote(self, _wallet, _wallet_address, proposal_id, vote): casts a vote on a certain proposal: vote = 0->Against,vote = 1->For,vote = 2->Abastain. This function uses the *Token_contract_address*, so if you needed to wrap your token, you should use the *vote_wToken* function;
* vote_wToken(self, _wallet, _wallet_address, proposal_id, vote): same as *vote* but uses the *wToken_contract_address* from .env. If a token holder does not have the wrapped token, he has until the end of the *voting_delay* of that proposal to wrap them in order to be able to vote in that proposal. He can do this using the [wToken class](#F-wToken.py);
* queue(self, _wallet, func_name, params, proposal, proposal_id):   queues a successfull proposal. This proposal will have to wait the *min_delay* imposed by the TimeLock.sol, before it can be executed
* execute(self, _wallet, func_name, params, proposal, proposal_id): executes a queued and successfull proposal. This inacts the changes proposed in that proposal;

## D) Deployments.py
deploys the TimeLock and Governance contracts. It can also deploy a contract to be governed, called Changeable.
### Functions:
* init(self, connector, _wallet, _wallet_address, TimeLock_build_dir, Governance_build_dir, Changeable_build_dir, Token_build_dir, wrapped): initializes these values to be used by the class. If "wrapped == 'no'" then we fetch the "Token_contract_address" from the .env file, if "wrapped == 'yes'" then we fetch the "wToken_contract_address" from the .env;
* deploy_TimeLock(self, min_delay): deploys the GovernanceTimeLock.sol contract and saves the contract address in the .env file;
* deploy_Governance(self, quorum_percentage, voting_period, voting_delay): deploys the GovernanceContract.sol contract and saves the contract address in the .env file;
* deploy_Changeable_contract(self): deploys the contract we want to be governed by the DAO and saves the contract address in the .env file;
* transfer_ownership_to_TimeLock(self): transfers the ownership of the Changeable contract to the GovernanceTimeLock.sol address. This way, only the governance can inact chenges in any function within the Changeable contract that has the *onlyOwner* modifier;
* checkOwner(self): a simple function to check if the new Owner address of the Changeable contract is the same as the GovernanceTimeLock.sol address. If it is not, then the *transfer_ownership_to_TimeLock* function failed;
  
## E) Roles.py
grants propose role to everybody, executor role to the governance contract address and revokes the Timelock admin role from the contract deployer (so that he no longer controls the DAO in any way);
### Functions:
* init(self, connector, _wallet, _wallet_address, TimeLock_build_dir, Governance_build_dir, Changeable_build_dir): initializes these values to be used by the class;
* get_role_codes(self): gets the role codes for the PROPOSER_ROLE, EXECUTOR_ROLE and TIME_ADMIN_ROLE, from the TimeLock.sol contract. This codes are needed to grant or revoke roles within the governance;
* grant_proposer_role(self): grants the role of proposer to the GovernanceContract.sol address;
* grant_executor_role(self): grants the role of executor to everybody. This means anyone can call execute the modifications of a proposal who was successfully passed;
* revoke_TimeLockAdmin_role(self): removes the TIME_ADMIN_ROLE from the wallet that deployed the governance contracts. This makes it so no one can modify the Changeable contrat except if a proposal is successfull;
* check_role_distribution(self): simple check to see if the granting and revoking was successfull;

## F) wToken.py
Deployes the wrapping contract, Wraps and unwraps the ERC20 token of the DAO. This is only needed if the token does not have the ERC20Votes extension an, as so, needs a wrapped version which has. This class may belong to a more extensive ERC20 dedicated library if there is enough interesse.
* init(self, connector, wToken_build_dir): initializes these values to be used by the class;
* deploy_wToken(self, Token_contract_address, testwallet): deploys the wrapped token contract. This is only necessary if that contract wasn't already deployed;
* wallet_balance(self, _contract_Token, Token_contract_address, _wallet_address): sees a wallets balance of a certain Token (by address);
* wrap_Token(self, _wallet, _wallet_address, _contract_Token, Token_contract_address, _contract_wToken, wToken_contract_address): wraps a wallets entire balance of a token to its wrapped version;
* unwrap_Token(self, _wallet, _wallet_address, _contract_Token, Token_contract_address, _contract_wToken, wToken_contract_address): unwraps a wallets entire balance of a wrapped token to its unwrapped version;
* delegate(self, _wallet, delegate_to_address, wToken_contract_address): delegates the voting capibility of the callers wrapped tokens to somebody. If the user want to vote for himself *delegate_to_address* should be equal to the senders wallet address;

  
# TO DO
- Irrelevant: Make it so the proposal snapshot can be taken before each vote in order to wrap the token the moment you vote, and unwrap after
- Place "params" variable in the deploy_Changeable_contract function so it can receive some params to send to the changeable contract contructor
- Change the role attribution to being able to receive addresses
- Make it so the propose function receives the testnet or mainet as well for the web3 = Web3(Web3.HTTPProvider(link)) part and the changeable contract dir as well