pragma solidity >= 0.7.0 < 0.9.0;

//"SPDX-License-Identifier: UNLICENSED"

import "./MerchantIndexes.sol";

    //********************************************************************************
    // Contract: SettlementStorage
    // Parameters: N/A
    // Functions: 
    // Events: 
    // Notes: Each payment network should really only have one of these contracts, which
    //  just links to the starting MerchantIndexes contract;
    // TODO: Testing; Metrics;
    //********************************************************************************
contract SettlementStorage {
    address private owner;
    mapping(address => address) private merchant_indexes; // Stores address of Merchant indexes with the address of the sender;

    event StorageInitialized(address indexed _from, address indexed _merchant_indexes); // Event triggered when startMerchantIndexStorage is completed;
    event MerchantIndexAdded(address indexed _owner, address indexed _next_block);

    constructor() {
        owner = msg.sender;
        startMerchantIndexStorage();
    }
    
    //********************************************************************************
    // Function: startMerchantIndexStorage
    // Parameters: N/A
    // Events: StorageInitialized
    // Notes: This should only really be triggered once to initialize the storage 
    //  system for each owner/company/etc or used to split between prod and qa.
    // TODO: 
    //********************************************************************************
    function startMerchantIndexStorage() private {
        MerchantIndexes mi = new MerchantIndexes(address(this), msg.sender);
        merchant_indexes[msg.sender] = address(mi);
        
        emit StorageInitialized(msg.sender, address(mi));
    }

    //********************************************************************************
    // Function: newMerchantIndex
    // Parameters: N/A
    // Events: MerchantIndexAdded
    // Notes:
    // TODO:
    //********************************************************************************
    function newMerchantIndex() public {
        require(msg.sender == owner);
        MerchantIndexes mi = new MerchantIndexes(merchant_indexes[msg.sender], msg.sender);
        merchant_indexes[msg.sender] = address(mi);

        emit MerchantIndexAdded(msg.sender, merchant_indexes[msg.sender]);
    }

    //********************************************************************************
    // Function: getMerchantIndexAddress()
    // Parameters: N/A
    // Events: N/A
    // Notes:
    // TODO:
    //********************************************************************************
    function getMerchantIndexAddress() public view returns(address){
        return merchant_indexes[msg.sender];
    }
}
