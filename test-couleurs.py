#!/usr/bin/python3

from termcolor import colored, cprint
from os import system

pion_rouge = colored("●", "red", attrs=['bold'])
pion_jaune = colored("●", "yellow", attrs=['bold'])

system("clear")

print()

print("\t1-", end=" ")
for i in range(10):
    print(pion_rouge, end=" ")
    print(pion_jaune, end=" ")
print()

print("\t2-", colored("états initiaux et finaux", "green", attrs=["bold"]))

print("\t3-", colored("obtenir 4 litres dans l'une des cruches",
                      "white", attrs=["bold"]))

print("\t4-", colored("pas de solution", "cyan", attrs=["bold"]))
print("\t4-", colored("pas de solution", "cyan"))
print("\t4-", colored("pas de solution", "blue", attrs=["bold"]))
print("\t4-", colored("pas de solution", "blue"))

print("\t5-", end=" ")
print(colored(4, "white", attrs=['bold']), end=" ")
cprint("  ", "white", "on_red", attrs=['bold'], end=" ")
cprint(6, "white", "on_green", attrs=['bold'], end=" ")

print()
print()
