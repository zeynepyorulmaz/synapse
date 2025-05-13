"""
Real XRP client implementation using xrpl-py
"""

from xrpl.clients import JsonRpcClient
from xrpl.models import Payment, AccountInfo
from xrpl.wallet import generate_faucet_wallet
from xrpl.utils import xrp_to_drops
from decimal import Decimal

class XrpClient:
    """Real XRP client using xrpl-py library."""
    
    def __init__(self, testnet: bool = True):
        """
        Initialize the XRP client.
        
        Args:
            testnet: Whether to use testnet (True) or mainnet (False)
        """
        self.testnet = testnet
        self.client = JsonRpcClient("https://s.altnet.rippletest.net:51234" if testnet else "https://xrplcluster.com")
        
    async def sendPayment(self, request: dict) -> dict:
        """
        Send a payment using XRP.
        
        Args:
            request: Dictionary containing payment details
                - fromAgentId: Sender's account address
                - toAgentId: Receiver's account address
                - amount: Amount in XRP
                - memo: Optional payment memo
                
        Returns:
            Dictionary containing transaction result
        """
        try:
            # Convert amount to drops (1 XRP = 1,000,000 drops)
            amount_drops = xrp_to_drops(Decimal(str(request["amount"])))
            
            # Create payment transaction
            payment = Payment(
                account=request["fromAgentId"],
                destination=request["toAgentId"],
                amount=amount_drops,
                memo=request.get("memo")
            )
            
            # Submit and wait for validation
            response = await self.client.submit_and_wait(payment)
            
            return {
                "success": response.is_successful(),
                "transaction_hash": response.result.get("hash"),
                "timestamp": response.result.get("date"),
                "error": None if response.is_successful() else response.result.get("error")
            }
            
        except Exception as e:
            return {
                "success": False,
                "transaction_hash": None,
                "timestamp": None,
                "error": str(e)
            }
    
    async def getBalance(self, account_id: str) -> float:
        """
        Get XRP balance for an account.
        
        Args:
            account_id: Account address
            
        Returns:
            Account balance in XRP
        """
        try:
            # Get account info
            account_info = AccountInfo(
                account=account_id,
                ledger_index="validated",
                strict=True
            )
            response = await self.client.request(account_info)
            
            # Convert balance from drops to XRP
            balance_drops = Decimal(response.result["account_data"]["Balance"])
            balance_xrp = balance_drops / Decimal("1000000")
            
            return float(balance_xrp)
            
        except Exception as e:
            raise Exception(f"Failed to get balance: {str(e)}")
    
    async def verifyTransaction(self, tx_hash: str) -> bool:
        """
        Verify an XRP transaction.
        
        Args:
            tx_hash: Transaction hash to verify
            
        Returns:
            True if transaction is valid and successful
        """
        try:
            # Get transaction details
            response = await self.client.request({
                "command": "tx",
                "transaction": tx_hash
            })
            
            # Check if transaction was successful
            return response.result.get("validated", False)
            
        except Exception as e:
            raise Exception(f"Failed to verify transaction: {str(e)}")
            
    @staticmethod
    def create_test_wallet() -> dict:
        """
        Create a test wallet using the XRP testnet faucet.
        
        Returns:
            Dictionary containing wallet details
        """
        try:
            # Generate a new wallet using the testnet faucet
            wallet = generate_faucet_wallet(client=JsonRpcClient("https://s.altnet.rippletest.net:51234"))
            
            return {
                "address": wallet.classic_address,
                "secret": wallet.seed,
                "sequence": wallet.sequence
            }
            
        except Exception as e:
            raise Exception(f"Failed to create test wallet: {str(e)}") 