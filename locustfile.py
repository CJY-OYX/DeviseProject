from locust import HttpUser, task, between, LoadTestShape
import json

class CarDataUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:8000"

    @task(5)
    def get_users_list(self):
        self.client.get("/myApp/getUsersList/")

    @task(5)
    def get_car_info_list(self):
        self.client.get("/myApp/getCarInfoList/")

    @task(3)
    def search_user(self):
        headers = {"Content-Type": "application/json"}
        self.client.post("/myApp/searchUser/", json={"keyword": "admin"}, headers=headers)

    @task(2)
    def get_crawler_logs(self):
        self.client.get("/myApp/getCrawlerLogs/")

class StagesShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 1},
        {"duration": 120, "users": 50, "spawn_rate": 5},
        {"duration": 180, "users": 100, "spawn_rate": 10},
        {"duration": 240, "users": 200, "spawn_rate": 20},
        {"duration": 300, "users": 50, "spawn_rate": 50},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None