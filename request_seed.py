import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str):
    # Read Public Key
    with open("keys/student_public.pem", "r") as pub_file:
        public_key = pub_file.read()

    # Convert newlines to \n automatically for JSON
    public_key = public_key.replace("\n", "\\n")

    payload = {
        "student_id": "24A95A0516",
        "github_repo_url": "https://github.com/jyothitulli/microservice-with-docker-24A95A0516",
        "public_key": "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAj/Wc7+gHxkB3RtOCVA4b\nVrbZ/cnfV98X5Z5QcvSKT4uZykTlHMxLttHHR325Be0uAanb5a7UZcH4N5CykAYQ\nBWxIDSoZCvBSOSCJNXZ1OKzcS47thmtCf//+sdrP6g6foLZTXHa6M7DUZivbOelh\nMvjzclhAHc/nRc44naUixGgBBFId6prjIB7+syhxG8Krveuz7aWhuuRoq1bOQJLl\n8XzExK9x9aVzF74RCH56rZ7CrZVbun2rX4Amxb2bOlFrb97lfoggjYzq8pqsxqmn\nSbo/UyKNqqBa62RZ8C3osSWIEyqAf5FaE06xIFjPtwNxr0R+u0Ajsj8lhNCmSkrD\npM8aaEth58lzS35iNfC21oHdsLZa1qA9/6vmTAbLWS0t6rtSDkZr+g3Ck9/La5qu\nXqKNxbTQ+BUXRNe9uroLocpIm/Rm3qiN8pzXYg5jFLuQDR59DZa3wOUax5FwJtp6\nohGPhjSIkQr4H1B9+tx6CW1SWrNhySBt5cNIqPacGzh77Pt35M0n57Blw7eCLqq8\nJCLGN+yUSk+oL8l37zlEFYHK+lGFJQ/TedhMTm3giVkUgjvy89FbDk+nF/T0pQ6+\nKMEcUg4Z2iidQsf1ceHHNy9jSLjvCxpo6Er5a17icOdDJrxgW+lZchjuEOTY/cY1\nNahSWh14u/gQD4Expl6OXeMCAwEAAQ==\n-----END PUBLIC KEY-----"
     
    }

    headers = {"Content-Type": "application/json"}

    # Send POST request
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        encrypted_seed = data.get("encrypted_seed")

        if encrypted_seed:
            with open("encrypted_seed.txt", "w") as seed_file:
                seed_file.write(encrypted_seed)

            print("Encrypted seed received and saved to encrypted_seed.txt")
        else:
            print("Error: No encrypted_seed in response:", data)
    else:
        print("Request failed:", response.status_code, response.text)


if __name__ == "__main__":
    student_id = input("Enter your Student ID: ")
    repo_url = input("Enter your GitHub Repo URL: ")
    request_seed(student_id, repo_url)
