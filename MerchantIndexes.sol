pragma solidity >=0.7.0 < 0.9.0;

import "./Merchant.sol";

    //********************************************************************************
    // Contract: MerchantIndexes
    // Parameters: Address - the owner of the this contract;
    // Functions: addNewMerchant; updateMostRecentMerchantBlock;
    // Events: 
    // Notes: This contract will hold the latest block for each merchant; stores 
    //  the latest because most searches are done from until an earlier date.
    // TODO: Testing; Metrics;
    //********************************************************************************
contract MerchantIndexes {
    address private parent_contract; // Parent contract
    mapping(string => Merchant) private merchants; // Mapping merchant_identifiers to Merchant blocks;
    mapping(string => bool) private merchant_initialized; //
    uint private merchant_count; // Current merchant count for this contract;
    uint private max_merchant_count = 500; // Max number of merchants for a contract; TODO: find optimum number;
    address private next_block; // Next MerchantIndexes block; used once this one is full;
    bool private next_block_created;
    
    // Used to ensure only the owner modifies/adds to these contracts;
    address private owner; // Owner of the contract
    
    constructor(address _parent_contract, address _owner) {
        parent_contract = _parent_contract;
        owner = _owner;
        merchant_count = 0;
        next_block_created = false;
    }
    
    //Modifier to require ownership to modify.
    modifier ownerOnly(address _allowed) {
        require(msg.sender == _allowed, "Not the owner.");
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
    function addNewMerchant(string memory _merchant_identifier) public ownerOnly(owner) {
        //If merchant has been alread been initialized and needs a new block;
        if (merchant_count <= max_merchant_count && merchant_initialized[_merchant_identifier] == true){
            updateMostRecentMerchantBlock(_merchant_identifier);
        } //If merchant is being added for the first time;
        else if (merchant_count <= max_merchant_count && merchant_initialized[_merchant_identifier] == false){
            merchant_count++;
            Merchant m = new Merchant(msg.sender, _merchant_identifier, address(0)); // Create a new merchant block;
            merchant_initialized[_merchant_identifier] = true;// set merchant as initialized;
            
            emit MerchantAdded(msg.sender, address(m));  // emit the merchant added event;
        } // If this index block is full create new index block, if new block hasn't already been created;
        else if (merchant_count > max_merchant_count && next_block_created == false){
            emit MerchantIndexFull(msg.sender, address(this));
        }
    }
    
    function updateMostRecentMerchantBlock(string memory _merchant_identifier) private {
        address previous_address = address(merchants[_merchant_identifier]);
        Merchant m = new Merchant(msg.sender, _merchant_identifier, address(merchants[_merchant_identifier]));
        merchants[_merchant_identifier] = m;
        
        emit MerchantUpdated(msg.sender, address(m), previous_address);
    }
}
