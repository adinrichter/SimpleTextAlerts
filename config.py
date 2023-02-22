# credentials for the Twilio API
account_sid = 'your-account-sid'
auth_token = 'your-auth-token'

# number used to send messages
twilio_number = 'your-twilio-number'

# database queries
db_create_table = '''
    CREATE TABLE IF NOT EXISTS phone_numbers
    (id INTEGER PRIMARY KEY,
    number INTEGER,
    permission INTEGER DEFAULT 0,
    name TEXT NOT NULL DEFAULT "")
    '''

db_add_number = '''
    INSERT INTO phone_numbers
    (number)
    VALUES (?)
    '''

db_remove_number = '''
    DELETE FROM phone_numbers
    WHERE id = ?
    '''

db_find_number = '''
    SELECT id FROM phone_numbers
    WHERE number = ?
    '''

db_list_numbers = '''
    SELECT * FROM phone_numbers
    '''

db_get_permission = '''
    SELECT permission FROM phone_numbers
    WHERE number = ?
    '''

db_get_name = '''
    SELECT name FROM phone_numbers
    WHERE number = ?
    '''

# message templates
msg_subscribe_confirmation = '''
    You have subscribed.\nText "2" at any time to unsubscribe.
    '''

msg_unsubscribe_confirmation = '''
    You have successfully unsubscribed.\nText "1" at any time to resubscribe.
    '''

msg_not_subscribed = '''
    If you want to receive notifications, reply with "1".
    '''

msg_already_subscribed = '''
    You're already subscribed to recieve notifications.\nText "2" at any time to unsubscribe.
    '''

msg_server_error = '''
    There was an error processing your request. Please try again later.
    '''

msg_not_allowed = '''
    An error has occurred and your message was not sent. Please try again later.
    '''

# dictionary of phone numbers and names to send messages from
# any message sent from a number in this dictionary will be sent to all subscribers, and the sender's name and phone numberwill be included in the message
allowed_senders = {"1234567890": "name"}