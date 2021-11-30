pragma solidity >=0.7.0 < 0.9.0;

//"SPDX-License-Identifier: UNLICENSED"

import "./Settlement.sol";

contract Merchant {
    address private owner; // Owner of the contract
    string private identifier; // Merchant identifier
    address private previous_merchant_contract; // previous merchant contract; may be blank for new merchants
    
    uint private settlement_count; // stores current amount
    //TODO: Figure out optimal number for this.
    uint private max_settlement_count = 365; // stores the max number contract can hold;
    address[] private settlements; // Array of settlement addresses

    uint256[2] private date_range; //
    
    constructor(address _owner, string memory _identifier, address _previous_merchant_contract) {
        owner = _owner;
        identifier = _identifier;
        previous_merchant_contract = _previous_merchant_contract;
        settlement_count = 0;
        date_range[0] = 2**256 - 1;// Set minimum to max uint value so anything less updates it.
        date_range[1] = 0; // Set maximum to 0 time so anything higher updates it.
    }
    
    // Events:
    event new_settlement_created(address indexed _owner, address indexed _settlement); // Signal new settlement has been created;
    event settlement_full(address indexed _owner, address indexed _this_address); // Signal Merchant is full;

    // Modifier to require ownership to modify.
    modifier ownerOnly(address _allowed) {
        require(msg.sender == _allowed, "Not the owner.");
        _;
    }

    // Modifier to require ownership to modify.
    modifier notFull() {
        require(settlement_count <= max_settlement_count, "Max Settlements Reached.");
        _;
    }

    // Modifier to require previousBlock is not empty(=address(0));
    modifier hasPreviousBlock() {
        require(previous_merchant_contract != address(0), "No Previous Block.");
        _;
    }

    //********************************************************************************
    // Function: start_new_settlement
    // Parameters: None
    // Events: 
    // Notes: 
    // TODO: 
    //********************************************************************************
    function start_new_settlement(uint _date) public ownerOnly(owner) notFull(){
        Settlement s = new Settlement(owner, address(0)); // create new settlement contract;
        settlements.push(address(s)); // add address to array;
        update_date_range(_date); // update date if needed;
        settlement_count++; // increase settlement_count
        
        emit new_settlement_created(msg.sender, address(s));
    }

    //********************************************************************************
    // Function: update_date_range
    // Parameters: _date(uint) - provide the date it is initialized;
    // Events:
    // Notes:
    // TODO: May need to change what date is provided for this.
    //********************************************************************************
    function update_date_range(uint _date) private {
        if(_date < date_range[0]){ // Set lower range
            date_range[0] = _date;
        }
        else if(_date > date_range[1]){ // Set higher range
            date_range[1] = _date;
        }
    }

    //********************************************************************************
    // Function: getPreviousBlock
    // Parameters: None
    // Events:
    // Notes:
    // TODO:
    //********************************************************************************
    function getPreviousBlock() public view hasPreviousBlock returns(address){
        return previous_merchant_contract;
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

    //********************************************************************************
    // Function: view_settlements
    // Parameters: None
    // Events:
    // Notes:
    // TODO:
    //********************************************************************************
    function view_settlements() public view returns (address[] memory){
        return settlements;
    }
}
