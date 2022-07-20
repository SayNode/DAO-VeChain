from DAO_lib.basic import *
from DAO_lib.DAO import DAO
from DAO_lib.Deployments import Deployments
from DAO_lib.Roles import Roles
import time

#
# NOT PART OF THE LIBRARY: only used to check the value stored in the contract the governance aims to change (Box.sol)
#
def val():
    
    print("\n--------------------------\n-----------VAL------------\n--------------------------")
    from thor_requests.contract import Contract
    _contract_Changeable = Contract.fromFile("build\contracts\Box.json")
    Changeable_contract_address=config('Changeable_contract_address')
    connector = connect(1)
    value_stored = connector.call(
            caller='0x0000000000000000000000000000000000000000',
            contract=_contract_Changeable,
            func_name="retrieve",
            func_params=[],
            to=Changeable_contract_address,
    ) 
    print("The value stored in box is " + str(value_stored['decoded']['0']))

#
# Deploy contracts, grant and revoke roles
#
def init():

    print("\n--------------------------\n----------INIT------------\n--------------------------")


    #Import Wallet 1

    (_wallet, _wallet_address) = wallet_import_mnemonic(1)

    #Connect to the Node
    connector = connect(1)

 
    #Deploy Contracts 
    deploy = Deployments(connector, 
                         _wallet, _wallet_address, 
                        "build\contracts\GovernanceTimeLock.json", #TimeLock_build_dir 
                        "build\contracts\GovernanceContract.json", #Governance_build_dir 
                        "build\contracts\Box.json", #Changeable_build_dir 
                        "build\contracts\wDHN.json",
                        wrapped = 'yes' #Indicates if we want to use a wrapped ERC20 token to vote
                                        #or if the original ERC20 token was already fit for voting
                        )

    deploy.deploy_TimeLock(
                           2 #min_delay: delay for governance decisions to be executed
                          )

    deploy.deploy_Governance(
                             0, #quorum_percentage: quorum required for a proposal to be successful
                             10, #voting_period: delay (in number of blocks) since the proposal starts until voting ends
                             1 #voting_delay: Delay (in number of blocks) since the proposal is submitted 
                            )   #until voting power is fixed and voting starts.
                            
    
    deploy.deploy_changeable_contract()

    deploy.transfer_ownership_to_TimeLock()

                            


    #Grant and Revoke roles
    roles = Roles(connector, 
                  _wallet, _wallet_address, 
                  "build\contracts\GovernanceTimeLock.json", #TimeLock_build_dir 
                  "build\contracts\GovernanceContract.json", #Governance_build_dir 
                  "build\contracts\Box.json" #Changeable_build_dir 
                 )

    roles.get_role_codes()
    roles.grant_proposer_role()
    roles.grant_executor_role()
    roles.revoke_TimeLockAdmin_role()
    roles.check_role_distribution()


#
# Create a proposal, vote on it with 2 different wallets, queue and then execute it
#
def main():


    print("\n--------------------------\n----------MAIN------------\n--------------------------")

    #Import Wallets 1 and 2
    (_wallet, _wallet_address) = wallet_import_mnemonic(1)
    (_wallet2, _wallet2_address) = wallet_import_mnemonic(2)


    #Connect to the Node
    connector = connect(1)

    #Initialize the DAO class
    DohrniiDAO = DAO(connector, 
                  "build\contracts\GovernanceTimeLock.json", #TimeLock_build_dir 
                  "build\contracts\GovernanceContract.json", #Governance_build_dir 
                  "build\contracts\Box.json", #Changeable_build_dir 
                  "build_static\DHN.json"
                 )

    DohrniiDAO.set_wToken("build\contracts\wDHN.json")


    #Propose 
    proposal ="First Proposal"
    func_name = "store"
    params = [53]
    proposal_id = DohrniiDAO.propose(_wallet, func_name, params, proposal)
   


    #One vote for (with 2 weight) and one vote against (1 weight)   
    time.sleep(20)
    DohrniiDAO.vote_wToken(
                           _wallet, _wallet_address,
                           proposal_id,
                           1
                          )

    DohrniiDAO.vote_wToken(
                           _wallet2, _wallet2_address, 
                           proposal_id,
                           1
                          )


    #Queue
    time.sleep(150)
    DohrniiDAO.check_proposal_by_id(proposal_id)

    DohrniiDAO.queue(
                    _wallet,
                    func_name, params,
                    proposal, proposal_id
                    )

    DohrniiDAO.check_proposal_by_id(proposal_id)


    #Execute
    time.sleep(30)
    DohrniiDAO.execute( 
                _wallet,
                func_name, params,
                proposal, proposal_id
            )
    time.sleep(20)


init()
val()
main()
val()