import pandas as pd

df = pd.read_csv("../resources/contacts.csv")  # Ensure CSV has 'Phone' column

phone_numbers = df['Phone'].tolist()
names = df['Name'].tolist()

# print(phone_numbers)
# print(names)
#
with open('../resources/message.txt', 'r') as file:
    message = file.read().strip()
    # print(message)

index = 0

for number in phone_numbers:
    message_personalized = f"Hello {names[index]}!\n{message}"
    index += 1
    print(message_personalized)

