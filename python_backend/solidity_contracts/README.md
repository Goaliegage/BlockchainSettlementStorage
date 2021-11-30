# BlockchainSettlementStorage

# Project flow using python backend: 
##Initial Setup
    1. Create SettlementStorage Contract
    2. Store address of contract in configs.
##Add a new Merchant
    1. Get address of SettlementStorage Contract
    2. Store address from calling SettlementStorage:GetMerchantIndexAddress
    3. Load MerchantIndex Contract with address
    4. Call addNewMerchant(merchant_identifier) from MerchantIndex Contract
##Create Settlement for a Merchant
    1. Get address of SettlementStorage Contract
    2. Store address from calling SettlementStorage:GetMerchantIndexAddress
    3. Load MerchantIndex Contract with address
    4. 
    