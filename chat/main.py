# RegEx

import re

# text = "Phone number: +37491-234545"
# match = re.search(r"\d{5}-\d{6}", text)
# if match:
#     print("Գտնվել է ", match.group())


# text = "Hello Armenia"
# match = re.search(r"[a-fA-F]", text)
# if match:
#     print("Գտնվել է ", match.group())


# text = "Hello Armenia"
# letters = re.findall(r"[a-fA-F]", text)
# print(letters)

# text = "He22ll342o A111rme99nia"
# # numbers = re.findall(r"\d+", text)
# numbers = re.findall(r"[1-3]+", text)
# print(numbers)

# text = "Hello      Armenia   !"
# cleaned_text = re.sub(r"\s+", " ", text)
# print(cleaned_text)


prog_lang = "pPython1 3.01"
match = re.match(r"Python", prog_lang)
if match:
    print("Տեքստը սկսվում է Python-ով")


'''
    \d
    \s
    \w _
    . 
    ^ r"^Python"
    $ r"yan$"
    +
    * 
    {n,m}
    {n}
    [abc]


'''

# example@gmail.com
# examplegmail.com
# example@gmail.com
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
email = "asd@mail.ru"
gmail = "asd@gmailcom"


def test_email(email):
    if re.match(email_pattern, email):
        print(f"{email}-ը վավեր է")
    else:
        print(f"{email}-ը վավեր չէ")

test_email(email)
test_email(gmail)