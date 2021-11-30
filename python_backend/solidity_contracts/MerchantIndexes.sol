pragma solidity >=0.7.0 < 0.9.0;

//"SPDX-License-Identifier: UNLICENSED"

import "./Merchant.sol";

    //********************************************************************************
    // Contract: MerchantIndexes
    // Parameters: Address - the owner of the this contract;
    // Functions: addNewMerchant; updateMostRecentMerchantBlock;
    // Events: 
    // Notes: This contract will hold the latest block for each merchant; stores 
    //  the latest because most searches are done from current date until an earlier
    //  date.
    // Testing:
    // TODO: Testing; Metrics;
    //********************************************************************************
contract MerchantIndexes {
    address private parent_contract; // Parent contract
    mapping(string => address) private merchants; // Mapping merchant_identifiers to Merchant blocks;
    mapping(string => bool) private merchant_initialized; //
    uint private merchant_count; // Current merchant count for this contract;
    uint private max_merchant_count = 1000; // Max number of merchants for a contract; TODO: find optimum number;
    address private next_block; // Next MerchantIndexes block; used once this one is full;
    bool private next_block_created;

    address private owner; // Owner of the contract; Used to ensure only the owner modifies/adds to these contracts;
    
    constructor(address _parent_contract, address _owner) {
        parent_contract = _parent_contract;
        owner = _owner;
        merchant_count = 0;
        next_block = address(0);
    }
    
    // Modifier to require ownership to modify.
    modifier ownerOnly(address _allowed) {
        require(msg.sender == _allowed, "Not the owner.");
        _;
    }

    // Modifier to require max_merchant_count hasn't been reached;
    modifier notFull(string memory _identifier) {
        require(merchant_count <= max_merchant_count, "Max Merchants.");
        require(merchant_initialized[_identifier] == false, "Merchant Already Stored.");
        _;
    }

    // Modifier to require that this contract has a previous MerchantIndex block.
    modifier hasNextBlock() {
        require(next_block_created == true, "Last MerchantIndex.");
        _;
    }
    
    // Event for a merchant being added;
    event MerchantAdded(address indexed _owner, address indexed _merchant_address);
    
    // Event for updatingMostRecentMerchantBlock;
    event MerchantUpdated(address indexed _owner, address indexed _merchant_address, address indexed _previous_address);
    
    // Event for new index block being created;
    event MerchantIndexFull(address indexed _owner, address indexed _next_block);
    
    //********************************************************************************
    // Function: addNewMerchant
    // Parameters: _merchant_identifier(string)
    // Events: MerchantAdded
    // Notes: 
    // Metrics[Time]: 
    // Metrics[Gas]: 
    // TODO: 
    //********************************************************************************
    function addNewMerchant(string memory _merchant_identifier) public ownerOnly(owner) notFull(_merchant_identifier) {
        merchant_count++; // Increment count
        Merchant m = new Merchant(msg.sender, _merchant_identifier, address(0)); // Creates new Merchant contract
        merchants[_merchant_identifier] = address(m); // Maps address(m) to the _merchant_identifier;
        merchant_initialized[_merchant_identifier] = true; // Set merchant as initialized;

        emit MerchantAdded(msg.sender, address(m));  // emit the merchant added event;
    }

    //********************************************************************************
    // Function: getPreviousAddress()
    // Parameters:
    // Events:
    // Notes:
    // Metrics[Time]:
    // Metrics[Gas]:
    // TODO:
    //********************************************************************************
    function getPreviousAddress() public view ownerOnly(owner) hasNextBlock() returns (address) {
        return next_block;
    }

    //********************************************************************************
    // Function: updateMostRecentMerchantBlock
    // Parameters: _merchant_identifier(string)
    // Events: MerchantUpdated
    // Notes:
    // Metrics[Time]:
    // Metrics[Gas]:
    // TODO:
    //********************************************************************************
    function updateMostRecentMerchantBlock(string memory _merchant_identifier) private {
        address previous_address = address(merchants[_merchant_identifier]);
        Merchant m = new Merchant(msg.sender, _merchant_identifier, address(merchants[_merchant_identifier]));
        merchants[_merchant_identifier] = address(m);
        
        emit MerchantUpdated(msg.sender, address(m), previous_address);
    }
}
