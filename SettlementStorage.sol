pragma solidity >= 0.7.0 < 0.9.0;

import "./MerchantIndexes.sol";

    //********************************************************************************
    // Contract: SettlementStorage
    // Parameters: N/A
    // Functions: 
    // Events: 
    // Notes: Each payment network should really only have one of these blocks, which 
    //  just links to the starting MerchantIndexes block;
    // TODO: Testing; Metrics;
    //********************************************************************************
contract SettlementStorage {
    mapping(address => address) private merchant_indexes; // Stores address of Merchant indexes with the address of the sender;
    event StorageInitialized(address indexed _from, address indexed _merchant_indexes); // Event triggered when startMerchantIndexStorage is completed;
    
    constructor() {
        
    }
    
    //********************************************************************************
    // Function: startMerchantIndexStorage
    // Parameters: N/A
    // Events: StorageInitialized
    // Notes: This should only really be triggered once to initialize the storage 
    //  system for each owner/company/etc or used to split between prod and qa.
    // TODO: 
    //********************************************************************************
    function startMerchantIndexStorage() public {
        MerchantIndexes mi = new MerchantIndexes(address(this), msg.sender);
        merchant_indexes[msg.sender] = address(mi);
        
        emit StorageInitialized(msg.sender, address(mi));
    }
}
