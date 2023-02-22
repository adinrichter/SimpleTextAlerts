import sqlite3, config
from flask import Flask, request, jsonify
from twilio.rest import Client

client = Client(config.account_sid, config.auth_token)

app = Flask(__name__)

# database is placed in the db folder in the working directory by default
# this can be changed by changing the path in the connect() function
conn = sqlite3.connect('./db/numbers.db', check_same_thread=False)
c = conn.cursor()

c.execute(config.db_create_table)
conn.commit()

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From'].strip("+1")
    message_body = request.form['Body']

    # if a number is allowed to send messages, whatever message they send will be sent to all subscribers
    # it also includes the name of the sender and their number so that no one can be impersonated or send messages without accountability
    if number in config.allowed_senders:
        send_all(f"{message_body}\n\nFrom:\n{sender_name(number)}, {number}")
        return jsonify("Message sent to all subscribers")
    else:
        if is_new_number(number) and message_body == "1":
            try:
                add_number(number)
                send_sms(number, config.msg_subscribe_confirmation)
                return jsonify("Subscription successful")
            except:
                send_sms(number, config.msg_server_error)
                return jsonify("An error occurred")
        elif is_new_number(number):
            send_sms(number, config.msg_not_subscribed)
            return jsonify(config.msg_not_subscribed)
        elif message_body == "2":
            try:
                remove_number(number)
                send_sms(number, config.msg_unsubscribe_confirmation)
                return jsonify(config.msg_unsubscribe_confirmation)
            except:
                send_sms(number, config.msg_server_error)
                return jsonify(config.msg_not_subscribed)
        else:
            send_sms(number, config.msg_already_subscribed)
            return jsonify(config.msg_already_subscribed)


def sender_name(number):
    try:
        return config.allowed_senders[number]
    except:
        return "An error occurred"

def is_new_number(number):
    c.execute(config.db_find_number, (number,))
    conn.commit()
    return c.fetchone() == None

def get_permission(number):
    c.execute(config.db_get_permission, (number,))
    conn.commit()
    return c.fetchone()[0]

def get_name(number):
    c.execute(config.db_get_name, (number,))
    conn.commit()
    return c.fetchone()[0]

def add_number(number):
    if is_new_number(number):
        c.execute(config.db_add_number, (number,))
        conn.commit()
        return True
    else:
        return False

def remove_number(number):
    try:
        c.execute(config.db_find_number, (number,))
        id = c.fetchone()[0]
        c.execute(config.db_remove_number, (id,))
        conn.commit()
        return True
    except:
        return False

def send_sms(phone_number, message_body):
    message = client.messages.create(
        body=message_body,
        from_=config.twilio_number,
        to=phone_number
    )
    print(message.body)

def send_all(message_body):
    c.execute(config.db_list_numbers)
    conn.commit()
    for row in c.fetchall():
        send_sms(row[1], message_body)

if __name__ == '__main__':
    app.run(debug=True)