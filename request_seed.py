import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str):
    # Read Public Key
    with open("student_public.pem", "r") as pub_file:
        public_key = pub_file.read()

    # Convert newlines to \n automatically for JSON
    public_key = public_key.replace("\n", "\\n")

    payload = {
        "student_id": "24A95A0516",
        "github_repo_url": "https://github.com/jyothitulli/microservice-with-docker-24A95A0516",
        "public_key": "-----BEGIN PUBLIC KEY-----MIIEIjANBgkqhkiG9w0BAQEFAAOCBA8AMIIECgKCBAEAq4QI08D4DNCsJ25uF5ePtFDGsZMFu6VE79v70vF2xWWgKagN1cKeq9Ty7viOn9bEbi7efo3juWvr8t3fCjyK7Ab2X3FBSAGtOrGH6EjbNGpsssfMMnpj1rcOdXfXCavdC/cOXuQck+TmZ143CwtYVyvjaNRjT08028PdW02CC1WYEznWzwSC1MUj873HeYA/7cVg82ViWTy4/DYmL3I6kcIgnnnzF4X7yXsuFg8n4dj1J5x9FO/lQZSBYtk7K+rmw7O705x+uGq2Ftd/uHnwvKzjQ6rqcjFgyDjv4FvwtEPzbkD3C95KijUA8GMu02xGIxegmUp8TRfwbHhC0RNK0PzC+EDB+MADyceoOHsRq4tQmp8Y85b3qfkF8/JdpWLP8QTa3Qin3EbWjVHPgy3zzICe0vCiXbuZLCJ22nxZtHDDRAvfWlZ1DT+guGcyyGK4gxL44+5S9DFLJQbk4qzmBjv1thRrUmG5MwrosqpD7cYaBlRyHKuvq2jaNDEyJd65HeSL9rDZHCzPL4a+EjzRSvPmS9Vmel3mNRE9JZiuaSOggYEDVy6dVURO0ZOWpfMwxfkxdrX/iNzmTldQww4pxCFXJOflmdSlfNsnOcfVYHgSZyePqOdq8zmZ6GZAIKMTsrn/k/of2aQtgWGUQWAAzya3uyI1IPHsBL4yKqYK7Z/dHPdwAapGoZGN2XZafY0ihezXpm/fvD7JqlRbC2Vco9bZeJLuU85EnGabjD857dWiDz4QnIFT8yAZj10BPX2Xb52hZdBZtdOBe1Klm6biF79Ho38IYavyshAUHYmS3d/137XUknsFN2BogWnPSrrLM9PsuiEvC6uR7N6ywuVP7Me81GpUgViNHsVOQ0hRD3m/ZqTA5rgRqRN6FITMSihYSGx7DZzFrhFwThQiTf0U2bzTuDsOgYXy8Nj/fMvoxd5JzrxDDmFB1Nt82sFoGQ2/Bj7Lvh2efoESFcr5jieYApZPIgen3wMU+ms19jOuarR/hID7pLs3hGbHqRgis0vVISrK9K7oFcHjgnBN7Xm54cF6AaFv5/U4sKSQ+MoEMDGolfjDiWiDnCdPbmcmfeFs2cQY9otNCsh1oM8q1lGnPx4cGkHNf9LgKBcS0HBp0pWfMK1P+QydPkBSU03MMQv5KbfCInHAcvg+IAVe9PLRq3XufZiLqU/FnNKmDSJmnkm2lEvM9eqJSp7aJvyfQFkiRoLbKRBcGBOrlKxFVqHkaZqZe72r+D15SFM5o1wOyc+xvq6TLW3kaSE/XlGBY1fPP2T8dAjLZRz3jhzkFMd8KiQ4BRU9F/QNCok7s+em1eX4rlrMjlYOvx3PjPsNYECdFJl9F8klPwRt7vXrI9vQIDAQAB-----END PUBLIC KEY-----"

        # -----BEGIN PUBLIC KEY-----MIIEIjANBgkqhkiG9w0BAQEFAAOCBA8AMIIECgKCBAEAq4QI08D4DNCsJ25uF5eP\ntFDGsZMFu6VE79v70vF2xWWgKagN1cKeq9Ty7viOn9bEbi7efo3juWvr8t3fCjyK\n7Ab2X3FBSAGtOrGH6EjbNGpsssfMMnpj1rcOdXfXCavdC/cOXuQck+TmZ143CwtY\nVyvjaNRjT08028PdW02CC1WYEznWzwSC1MUj873HeYA/7cVg82ViWTy4/DYmL3I6\n+kcIgnnnzF4X7yXsuFg8n4dj1J5x9FO/lQZSBYtk7K+rmw7O705x+uGq2Ftd/uHn\nwvKzjQ6rqcjFgyDjv4FvwtEPzbkD3C95KijUA8GMu02xGIxegmUp8TRfwbHhC0RN\nK0PzC+EDB+MADyceoOHsRq4tQmp8Y85b3qfkF8/JdpWLP8QTa3Qin3EbWjVHPgy3\nzzICe0vCiXbuZLCJ22nxZtHDDRAvfWlZ1DT+guGcyyGK4gxL44+5S9DFLJQbk4qz\nmBjv1thRrUmG5MwrosqpD7cYaBlRyHKuvq2jaNDEyJd65HeSL9rDZHCzPL4a+Ejz\nRSvPmS9Vmel3mNRE9JZiuaSOggYEDVy6dVURO0ZOWpfMwxfkxdrX/iNzmTldQww4\npxCFXJOflmdSlfNsnOcfVYHgSZyePqOdq8zmZ6GZAIKMTsrn/k/of2aQtgWGUQWA\nAzya3uyI1IPHsBL4yKqYK7Z/dHPdwAapGoZGN2XZafY0ihezXpm/fvD7JqlRbC2V\nco9bZeJLuU85EnGabjD857dWiDz4QnIFT8yAZj10BPX2Xb52hZdBZtdOBe1Klm6b\niF79Ho38IYavyshAUHYmS3d/137XUknsFN2BogWnPSrrLM9PsuiEvC6uR7N6ywuV\nP7Me81GpUgViNHsVOQ0hRD3m/ZqTA5rgRqRN6FITMSihYSGx7DZzFrhFwThQiTf0\nU2bzTuDsOgYXy8Nj/fMvoxd5JzrxDDmFB1+Nt82sFoGQ2/Bj7Lvh2efoESFcr5ji\neYApZPIgen3wMU+ms19jOuarR/hID7pLs3hGbHqRgis0vVISrK9K7oFcHjgnBN7X\nm54cF6AaFv5/U4sKSQ+MoEMDGolfjDiWiDnCdPbmcmfeFs2cQY9otNCsh1oM8q1l\nGnPx4cGkHNf9LgKBcS0HBp0pWfMK1P+QydPkBSU03MMQv5KbfCInHAcvg+IAVe9P\nLRq3XufZiLqU/FnNKmDSJmnkm2lEvM9eqJSp7aJvyfQFkiRoLbKRBcGBOrlKxFVq\nHkaZqZe72r+D15SFM5o1wOyc+xvq6TLW3kaSE/XlGBY1fPP2T8dAjLZRz3jhzkFM\nd8KiQ4BRU9F/QNCok7s+em1eX4rlrMjlYOvx3PjPsNYECdFJl9F8klPwRt7vXrI9\nvQIDAQAB\n-----END PUBLIC KEY-----"
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
