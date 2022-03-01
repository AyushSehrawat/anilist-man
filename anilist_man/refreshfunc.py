
class RefreshFunc():
    def __init__(self):
        pass

    def refreshToken():
        print(f"Visit https://anilist.co/api/v2/oauth/authorize?client_id=7501&response_type=token")
        token = str(input("\n[+] Enter your token: "))
        # Delete token.txt if it exists
        try:
            os.remove("token.txt")
        except FileNotFoundError:
            pass
        with open("token.txt", "w") as f:
            f.write(token)

    def refreshUid():
        uid = str(input("\n[+] Enter your user id: "))
        # Delete token.txt if it exists
        try:
            os.remove("id.txt")
        except FileNotFoundError:
            pass
        with open("id.txt", "w") as f:
            f.write(uid)