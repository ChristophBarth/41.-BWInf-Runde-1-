import re

word = "[A-Za-z',.!?ßäöü»«]+"

alice_im_wunderland = open("res/Alice_im_Wunderland.txt", "r").read().lower()
expression = open("res/stoerung1.txt", "r").read().replace("_", word)
print(expression)

res = re.findall(expression, alice_im_wunderland)
print([r for r in res])
