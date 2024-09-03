import streamlit as st
from web3 import Web3

# Connect to local Ethereum node (Ganache)
ganache_url = "https://ethereum-sepolia-rpc.publicnode.com"  # Adjust if needed
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connection is successful
if not web3.is_connected():
    st.error("Failed to connect to the Ethereum node.")
    st.stop()

# Set the default account (first account in Ganache)
web3.eth.default_account = web3.eth.accounts[0]

# ABI and Contract Address (Replace with your deployed contract details)
contract_abi =[
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "videoHash",
        "type": "bytes32"
      },
      {
        "internalType": "uint256",
        "name": "newResult",
        "type": "uint256"
      }
    ],
    "name": "updateVideoResult",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "bytes32",
        "name": "videoHash",
        "type": "bytes32"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "result",
        "type": "uint256"
      }
    ],
    "name": "VideoResultUpdated",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "videoHash",
        "type": "bytes32"
      }
    ],
    "name": "getVideoResult",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "videoHash",
        "type": "bytes32"
      }
    ],
    "name": "isVideoDetected",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]

contract_address = "0x376703356C644096708347Ed2d90614968eAC15D"  # Replace with your contract address

# Create a contract object
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Streamlit UI
st.title("Deepfake Detection - Blockchain Integration")
st.write("Latest block number:", web3.eth.block_number)

option = st.selectbox("Choose an action", ["Check Hash", "Store Result", "Retrieve Result"])

if option == "Check Hash":
    video_hash = st.text_input("Enter the video hash (in hex format)")
    if st.button("Check"):
        try:
            is_present = contract.functions.isVideoDetected(web3.to_bytes(hexstr=video_hash)).call()
            if is_present:
                st.success("The hash is detected as a deepfake.")
            else:
                st.warning("The hash is not detected as a deepfake.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif option == "Store Result":
    video_hash = st.text_input("Enter the video hash (in hex format)")
    result = st.number_input("Deepfake detection result (0 = Not Detected, >0 = Detected)", min_value=0)
    if st.button("Store"):
        try:
            # Explicitly include 'from' in the transaction
            tx_hash = contract.functions.updateVideoResult(web3.to_bytes(hexstr=video_hash), result).transact({'from': web3.eth.default_account})
            web3.eth.wait_for_transaction_receipt(tx_hash)
            st.success("Result stored successfully on the blockchain.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif option == "Retrieve Result":
    video_hash = st.text_input("Enter the video hash (in hex format)")
    if st.button("Retrieve"):
        try:
            result = contract.functions.getVideoResult(web3.to_bytes(hexstr=video_hash)).call()
            st.success(f"Deepfake Detection Result: {result}")
        except Exception as e:
            st.error(f"Error: {str(e)}")