# pizza/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from .models import User, Order
from django.contrib.auth.models import User
from .bot_messages import BOT_MESSAGES
import random
from datetime import datetime

#print("saad",User)
#print(User)
order_statuses = {1: "being proceed", 2: "being Check by Seller", 3: "Check status of Bid", 4: "Done"}

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.bot_message = "Hi, welcome to Bidding Store!"
        self.send(text_data=json.dumps({
            'bot_message': self.bot_message
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if self.bot_message in [BOT_MESSAGES.get("mobile"), BOT_MESSAGES.get("incorrect_mobile"), BOT_MESSAGES.get("ask_mobile")]:
            if message.isdigit() and len(message) == 11:
                self.mobile = int(message)
                try:
                    #print(self.username)
                    self.bot_message = "Welcome, To chat-bot \n"
                    self.bot_message += "\n"
                    self.bot_message += BOT_MESSAGES.get("first_question")
                except Exception:
                    self.bot_message = BOT_MESSAGES.get(User.username)
            else:
                if self.talk_to_bot(message):
                    self.bot_message = BOT_MESSAGES.get("incorrect_mobile")

        elif self.bot_message == BOT_MESSAGES.get("name"):
            self.name = message
            self.bot_message = BOT_MESSAGES.get("first_question")

        elif self.bot_message == BOT_MESSAGES.get("address"):
            self.address = message
            #push_user_details = myuser(name=self.name, phone=self.mobile, address=self.address)
            #push_user_details.save()
            self.bot_message = BOT_MESSAGES.get("first_question")

        elif BOT_MESSAGES.get("first_question") in self.bot_message:
            if message.lower() in ["1", "Place a bid", "order"]:
                self.bot_message = BOT_MESSAGES.get("second_question")
            elif message.lower() in ["2", "Check my bid status", "track"]:
                self.bot_message = BOT_MESSAGES.get("bid-check")
                self.bot_message += BOT_MESSAGES.get("thanks-bye")
            else:
                self.bot_message = BOT_MESSAGES.get("first_question")

        elif self.bot_message == BOT_MESSAGES.get("second_question"):
            if message.lower() in ["1", "Laptop"]:
                self.bot_message = BOT_MESSAGES.get("Laptop")
            elif(message.lower() in ["2", "Mobile"]):
                self.bot_message = BOT_MESSAGES.get("mobile_bid")
            else:
                self.bot_message = BOT_MESSAGES.get("first_question")

        elif self.bot_message == BOT_MESSAGES.get("mobile_bid"):
            if message.lower() in ["1", "Apple"]:
                self.bot_message = BOT_MESSAGES.get("mobile_b")
            else:
                self.bot_message = BOT_MESSAGES.get("first_question")

        elif self.bot_message == BOT_MESSAGES.get("mobile_b"):
            if (int(message)<500):
                self.bot_message = "Sorry your range is too low"
                self.bot_message += BOT_MESSAGES.get("thanks-bye")
            else:
                self.bot_message = BOT_MESSAGES.get("mob_quantity")

        elif self.bot_message == BOT_MESSAGES.get("mob_quantity"):
            if (int(message)<10):
                self.bot_message = "Sorry your quantity is too low"
                self.bot_message += BOT_MESSAGES.get("thanks-bye")
            else:
                self.bot_message = "Check link below:) "
                self.bot_message += BOT_MESSAGES.get("apple-link")
                self.bot_message += BOT_MESSAGES.get("thanks-bye")


        elif self.bot_message == BOT_MESSAGES.get("Laptop"):
            if message.lower() in ["1", "HP"]:
                self.bot_message = BOT_MESSAGES.get("Laptop_bid")
            else:
                self.bot_message = BOT_MESSAGES.get("first_question")

        elif self.bot_message == BOT_MESSAGES.get("Laptop_bid"):
            if (int(message)<1000):
                self.bot_message = "Sorry your range is too low"
                self.bot_message += BOT_MESSAGES.get("thanks-bye")
            else:
                self.bot_message = BOT_MESSAGES.get("quantity")

        elif self.bot_message == BOT_MESSAGES.get("quantity"):
            if (int(message)<40):
                self.bot_message = "Sorry your quantity is too low"
                self.bot_message += BOT_MESSAGES.get("thanks-bye")
            else:
                self.bot_message = "Check link below :)"
                self.bot_message += BOT_MESSAGES.get("hp-link")
                self.bot_message += BOT_MESSAGES.get("thanks-bye")


        elif self.bot_message == BOT_MESSAGES.get("order_id"):
            if message.isdigit():
                try:
                    order_status = self.fetch_order_status(message)
                    self.bot_message = "Your order is {}.\n".format(order_status)
                    self.bot_message += BOT_MESSAGES.get("thanks-bye")
                except Exception:
                    self.bot_message = BOT_MESSAGES.get("invalid_order")

        else:
            if self.talk_to_bot(message):
                self.bot_message = BOT_MESSAGES.get("ask_mobile")

        self.send(text_data=json.dumps({
            'bot_message': self.bot_message,
            'user_message': message
        }))

    def talk_to_bot(self, message):
        '''
        Flow for small talk with the bot.
        Variables:
            message: User's message to the bot.
            self.bot_message: Contains bot's message.
        Returns:
            Boolean: if user's message or bot's message is not part of the small talk flow.
        '''
        if message.lower() in BOT_MESSAGES.get("user-hello"):
            self.bot_message = random.choice(BOT_MESSAGES.get("bot-hello"))
        elif message.lower() in BOT_MESSAGES.get("user-bye"):
            self.bot_message = random.choice(BOT_MESSAGES.get("bot-bye"))
        elif message.lower() in BOT_MESSAGES.get("user-whatsup"):
            self.bot_message = random.choice(BOT_MESSAGES.get("bot-whatsup"))
        elif message.lower() in BOT_MESSAGES.get("user-greeting"):
            self.bot_message = random.choice(BOT_MESSAGES.get("bot-greeting"))
        else:
            return True

    def create_order(self):
        '''
        Creates a new order for user in the db.
        Variables:
            random_order_id: Generates a random 6 digits order id.
            fetched_user_id: Contains user's id based on mobile number in the db.
            order_object: Sets the order id in the db for Order model object.
        Returns:
            random_order_id: Random 6 digits order id to be shared with the user.
        '''
        random_order_id = random.randint(10**(6-1),10**6-1)
        user_model_object = myuser.objects.get(phone=self.mobile)
        user_details = user_model_object.__dict__
        fetched_user_id = user_details.get("id")
        order_object = Order(order_id=random_order_id, user_id=fetched_user_id, order_status=1)
        order_object.save()
        return random_order_id
    
    def fetch_order_status(self, message):
        '''
        Fetches the order status from DB based on the order ID shared by user.
        Variables:
            message: string order id given by user.
            order_exists: checks in db if order exists.
            time_passed_in_minutes: time passed in minutes since the order was placed.
        Returns:
            order_status: Status of the order.
        '''
        order_exists = Order.objects.get(order_id=int(message))
        order_details = order_exists.__dict__
        order_status = order_details.get("order_status")
        creation_date = order_details.get("created_on")
        creation_date = creation_date.replace(tzinfo=None)
        time_passed = datetime.now() - creation_date
        time_passed_in_minutes = int(time_passed.seconds/60)
        if time_passed_in_minutes < 2:
            order_status = order_statuses.get(1)
        elif 2 <= time_passed_in_minutes < 4:
            order_status = order_statuses.get(2)
        elif 4 <= time_passed_in_minutes < 5:
            order_status = order_statuses.get(3)
        else:
            order_status = order_statuses.get(4)
        return order_status