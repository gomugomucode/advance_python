def withdraw_money(account_balance, amount, is_connected):
    try:
        print("Connecting to bank server...")

        if not is_connected:
            raise ConnectionError("No internet connection!")

        if amount > account_balance:
            raise ValueError("Insufficient balance!")

        # If no error, proceed with withdrawal
        account_balance -= amount

    except ConnectionError as ce:
        print(f"Connection failed: {ce}")

    except ValueError as ve:
        print(f"Transaction failed: {ve}")

    except Exception as e:
        # Catch-all for any other unexpected errors
        print(f"Unexpected error: {e}")

    else:
        print(f"Transaction successful! Withdrawn: Rs. {amount}")
        print(f"Remaining balance: Rs. {account_balance}")

    finally:
        print("Closing connection to bank server.\n")

# ✅ Test Cases
withdraw_money(5000, 3000, is_connected=True)    
withdraw_money(2000, 5000, is_connected=True)    
withdraw_money(5000, 1000, is_connected=False)   
