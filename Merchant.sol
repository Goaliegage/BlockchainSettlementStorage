pragma solidity >=0.7.0 < 0.9.0;

import "./Settlement.sol";

contract Merchant {
    
    //Owner of the contract
    address private owner; // Owner of the contract
    string private identifier; // Merchant identifier
    address private previous_merchant_contract; // previous merchant contract; may be blank for new merchants
    
    uint private settlement_count; // stores current amount
    uint private max_settlement_count = 365; // stores the max number contract can hold; TODO: Figure out optimal number for this.
    
    Settlement[] private settlements;
    
    constructor(address _owner, string memory _indentifier, address _previous_merchant_contract) {
        owner = _owner;
        identifier = _indentifier;
        previous_merchant_contract = _previous_merchant_contract;
        settlement_count = 0;
    }
    
    // Events:
    event new_settlement_created(address indexed _owner, address indexed _settlement); // Signal new settlement has been created;
    event settlement_full(address indexed _owner, address indexed _this_address); // Signal Merchant is full;
    
    //********************************************************************************
    // Function: start_new_settlement
    // Parameters: None
    // Events: 
    // Notes: 
    // TODO: 
    //********************************************************************************
    function start_new_settlement() public {
        if(settlement_count <= max_settlement_count){
            Settlement s = new Settlement(owner, address(0));
            settlements.push(s);
            settlement_count++;
        
            emit new_settlement_created(msg.sender, address(s));
        }
        else if(settlement_count > max_settlement_count){
            
        }
    }
    
    //********************************************************************************
    // Function: current_settlement
    // Parameters: None
    // Events: 
    // Notes: 
    // TODO: 
    //********************************************************************************
    function current_settlement() public view returns (address) {
        require(settlement_count > 0);
        return address(settlements[settlement_count - 1]);
    }
    
    function view_settlements() public view returns (Settlement[] memory){
        return settlements;
    }
}
