from pushbullet import Pushbullet
import requests

class Meal:
    def __init__(self, meal_json_tree):
        self.content = meal_json_tree
        self.canteen = self.content["@attributes"]["canteen"]
        self.meal = self.content["@attributes"]["meal"]
        self.message = self.content["@attributes"]["disabled"]
        self.date = self.content["@attributes"]["date"]
        self.menu_items = ""

    @property
    def place_of_meal(self):
        return self.canteen

    @property
    def time_of_meal(self):
        return self.meal

    @property
    def warning_message(self):
        return self.message

    @property
    def menu(self):
        return self.menu_items

    @property
    def time(self):
        return self.date

    def populate_menu(self):
        if self.warning_message == "0":
            items = ""
            for n in range(0, len(self.content["items"]["item"])):
                if "@attributes" not in self.content["items"]["item"][n]:
                    items += self.content["items"]["item"][n] + "\n"
            self.menu_items = items


if __name__ == "__main__":
    message = ""
    message_time = ""
    r = requests.get('http://services.web.ua.pt/sas/ementas?format=json')
    data = r.json()
    meal = ""

    for i in range(0, 3, 2):  # Lunch @ Santiago and Crasto
        meal = Meal(data["menus"]["menu"][i])
        meal.populate_menu()
        if meal.warning_message == "0":
            message += meal.time_of_meal + " @ " + meal.place_of_meal + "\n----------------------------------------\n" + meal.menu + "\n"
        else:
            message += meal.time_of_meal + " @ " + meal.place_of_meal + "\n----------------------------------------\n" + meal.warning_message + "\n\n"
    message += meal.time

    pb = Pushbullet("<your pushbullet API key here>")
    # send message to your own device
    push = pb.push_note("Today's lunch options", message, device=pb.devices[0])
    # send message to a friend
    push = pb.push_note("Today's lunch options", message, chat=pb.chats[0])
    # print(message)
