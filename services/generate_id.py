""" This is where random and unique IDs are generated for each users that are created to ensure distinct user identifiers. """

from random import randint


def generate_unique_id(existing_id):
    """ Generates a random unique ID for every user, once.
     
        Returns:
            str: The ID that has been generated for the specific user. """
    while True:
        id = id = ''.join(str(randint(0, 9)) for n in range(12))
        if id not in existing_id:
            return f'#{id}'