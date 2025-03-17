from locust import HttpUser, task, between

class Pet4AllUser(HttpUser):
    wait_time = between(1, 5)

    # Sample test data - Expand this as needed
    test_user_data = {
        "name": "Jane Doe",
        "age": 30,
        "username": "janedoe",
        "email": "jane@example.com",
        "password1": "strongpassword",
        "password2": "strongpassword"
    }

    pet_data = {
        "name": "Buddy",
        "age": 3,
        "breed": "Golden Retriever",
        "status": "Adoption",
        "price": None,
        "description": "Friendly and playful",
        "seller_phone": "5551234"
    }

    @task(2)
    def home_page(self):
        self.client.get("/")

    @task(2)
    def view_buy_page(self):
        self.client.get("/buy")

    @task
    def register(self, test_user_data):
        self.client.post("/register", data=test_user_data)

    @task
    def login(self, test_user_data):
        self.client.post("/login",
                         data={"username": test_user_data["username"], "password": test_user_data["password1"]})

    @task
    def add_pet(self, pet_data):
        with open("sample_pet_image.jpg", "rb") as f:
            pet_data["image"] = f
        self.client.post("/add", data=pet_data)

    @task
    def logout(self):
        self.client.get("/logout")
