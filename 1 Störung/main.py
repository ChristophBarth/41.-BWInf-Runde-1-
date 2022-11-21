import re

word = "[A-Za-z',.!?ßäöü»«]+" #Regulärer Ausdruck für ein Wort variabler Länge mit Sonderzeichen

alice_im_wunderland = open("res/Alice_im_Wunderland.txt", "r").read().lower() #Wort
expression = open("res/stoerung1.txt", "r").read().replace("_", word) #Ausdruck - Erstetzen der fehlenden Wörter durch den regulären Ausdruck für Wort

res = re.findall(expression, alice_im_wunderland) #Alle Matches von Epression in Wort finden
print([r for r in res]) #Jedes Ergebnis ausgebem
