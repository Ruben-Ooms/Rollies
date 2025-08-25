# Rollies
Rollies is a simple TTRPG console dice roller. It was created as a small project for COSC 3389, Software Engineering 1 at Tarleton State University.

## Images

![image](https://github.com/user-attachments/assets/e83b2bad-33af-4cce-8fa6-19f9f98d48af)

## How to Roll
### DND
This app can perform roles for DND. 
These include single, multi die, advantage, disadvantage, and emphasis rolls.  
  
Basic Rolls:
To perform a single roll, enter a single number.  
To perform a multiroll, enter the number of dice and then the number of die sides seperated by a "d". Example: 5d6  
  
Roll Modifiers:
To perform a roll with advantage, append an "A" to a basic roll.  
To perform a roll with disadvantage, append a "D" to a basic roll.  
To perform a roll with emphasis, append an "E" to a basic roll.  
A numerical modifier can be used by appending a "+x" where x is the number you wish to add. Example: 8+5  

Multiple rolls can be performed at once by adding a space between them. However, only one modifier can be applied to each roll, excluding numerical modifier.  

### Animon
All roles are performed with a d6. So the user must enter the number of d6 to roll.  
  
Roll Modifiers:  
To perform a roll with a setback, append an "S" to a basic roll.  
To perform a roll with boost, append a "B" to a basic roll.  
Multiple can be appended and the effective number of setbacks or boosts will be caluclated.  
  
Multiple rolls can be performed at once by adding a space between them.  

### Fabula Ultima
All rolls are performed with two dice. You can enter a single number to roll the same number twice, or two numbers separated by a comma.
    Example: "8" rolls (2d8). "8,3" rolls (1d8+1d3).

Roll Modifiers:
A numberical modifier can be used by appending "+A" or "-A", where 'A' is the numerical modifier you wish to apply to the subtotal of the dice rolled.
    Example: '8,3+5' rolls (1d8+1d3+5). '8,3-2' rolls (1d8+1d3-2). 
You can perform the same roll multiple times by prepending "Ax", where 'A' is the number of times you want to perform the roll.
    Example: '3x8,3' rolls (1d8+1d3) three times.

Multiple rolls can be performed at once by adding a space between them.
    Example: '8 3,8' rolls (2d8) & (1d8+1d3).
    
###
This app can perform rolls for Adeptus Evangelion.
