pragma solidity >=0.7.0 <0.9.0;

//import "";

contract Settlement {
    enum Settlement_State{OPEN, CLOSED} // state of Settlement;
    // Values (uint):
    // 0 - OPEN;
    // 1 - CLOSED;
    
    enum Transaction_Type{SALE, RETURN} // Valid transaction types; 
    // Values (uint):
    // 0 - SALE;
    // 1 - RETURN;
    
    // structure for each transaction
    struct Transaction {
        Transaction_Type transactionType;
        uint transactionTime;
        uint totalAmount;
        uint last4Digits;
    }
    
    string private identifier; // Merchant identifier;
    uint private total_number_sales; // Total number of sale transactions;
    uint private total_number_returns; // Total number of return transactions;
    int private total_amount_sales; // Total amount from sale transactions;
    int private total_amount_returns; // Total amount from return transactions;
    int private net_total; // total amount ( = amount from sales - amount from returns);
    int private merchant_payout; // amount payed to merchant (net_total - costs);
    uint private settlement_time; // stored as Unix Timestamp;
    uint private transaction_count; // store current count;
    uint private max_transaction_count = 1000; // store max number of transactions this can hold; TODO: Figure out optimal number for this.
    bool private partner_block_set;
    address private partner_block;
    Transaction[] private transactions; // array of transactions;
    
    // Owner of the entire chain. 
    // So nobody else can modifier your chain.
    // Theoretically can be used by others.
    address private owner;
    
    //Current state; should start OPEN
    Settlement_State private settlementState;
    
    constructor(address _owner, address _partner_block) {
        //Set owner address
        owner = _owner;
        //Set initial state as open;
        settlementState = Settlement_State.OPEN;
        //initialize sale variables;
        total_number_sales = 0;
        total_amount_sales = 0;
        //initialize return variables;
        total_number_returns = 0;
        total_amount_returns = 0;
        if (_partner_block != address(0)){
            partner_block_set = true;
            partner_block = _partner_block;
        }
        else{
            partner_block_set = false;
            partner_block = address(0);
        }
    }
    
    //Modifier to require ownership to modify.
    modifier ownerOnly(address _allowed) {
        require(msg.sender == _allowed, "Not the owner.");
        _;
    }
    
    //********************************************************************************
    // Function: 
    // Parameters: 
    // Events: 
    // Notes: 
    // TODO: Give error if Transaction_Type is invalid number (0, 1);
    //********************************************************************************
    function addTransaction(Transaction_Type _type, uint _time, uint _amount, uint _digits) public ownerOnly(owner){
        if(_type == Transaction_Type.SALE){
            total_number_sales += 1;
            total_amount_sales += int(_amount);
            net_total = total_amount_sales - total_amount_returns;
        }
        else if(_type == Transaction_Type.RETURN){
            total_number_returns += 1;
            total_amount_returns += int(_amount);
            net_total = total_amount_sales - total_amount_returns;
        }
        else {
            // TODO: Give error if Transaction type is invalid (0, 1);
            revert('Bad Type Parameter');
        }
        transactions.push(Transaction(_type, _time, _amount, _digits));
        // assert(transactions[transactions.length] == Transaction)
    }
    
    //********************************************************************************
    // Function: 
    // Parameters: 
    // Events: 
    // Notes: 
    // TODO: 
    //********************************************************************************
    function settleTransactions(uint _time, int _payout) public ownerOnly(owner){
        settlementState = Settlement_State.CLOSED; // Change state to CLOSED;
        merchant_payout = _payout; // Finalize merchant_payout
        settlement_time = _time; // Finalize settlement time
    }
    
    //********************************************************************************
    // Function: 
    // Parameters: 
    // Events: 
    // Notes: 
    // TODO: 
    //********************************************************************************
    function viewTransactions() view public returns (Transaction[] memory){
        return transactions; // Returns the transactions array;
    }
}
