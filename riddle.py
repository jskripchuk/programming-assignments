#James Skripchuk
#CISC320
#PA2
#Dr. Atlas

import os
from functools import total_ordering

@total_ordering
class Contestant:
    def __init__(self, number, riddles_solved, penalty_time):
        self.number = number
        self.riddles_solved = riddles_solved
        self.penalty_time = penalty_time
        self.riddles_tried = {}

    #Overwriting python compare methods for custom sorting
    def __eq__(self,other):
        return self.number == other.number and self.riddles_solved == other.riddles_solved and self.penalty_time == other.penalty_time

    def __ne__(self,other):
        return self.number != other.number or self.riddles_solved != other.riddles_solved or self.penalty_time != other.penalty_time

    def __lt__(self,other):
        if self.riddles_solved != other.riddles_solved:
            return self.riddles_solved<other.riddles_solved
        elif self.penalty_time != other.penalty_time:
            return self.penalty_time>other.penalty_time
        else:
            return self.number<other.number

    #To string
    def __repr__(self):
        return str(self.number)+" "+str(self.riddles_solved)+" "+str(self.penalty_time)


#A single instance of a score row
class Score:
    def __init__(self, contestant, riddle_num, time, case):
        self.contestant = contestant
        self.riddle_num = riddle_num
        self.time = time
        self.case = case

contestants = {}

#Processes a single row of the scoreboard and updates the contestant
#that is part of the score. All operations in this function are on average O(1)
#due to hash tables.
def process_score(score):
    #O(1) average time for dictonary (hash table) acesses
    current_contestant = contestants[score.contestant]

    #If a riddle is incorrect, keep track of if it is tried again by the contestant
    if score.case == "I":
        if score.riddle_num not in current_contestant.riddles_tried:
            current_contestant.riddles_tried.update({score.riddle_num:1})
        else:
            current_contestant.riddles_tried[score.riddle_num]+=1

    #If a riddle is judged correct
    if score.case == "C":
        #Increment riddles solved
        current_contestant.riddles_solved+=1
        #Add the time it took to solve
        current_contestant.penalty_time+=score.time
        #If the riddle had been tried before incorrectly, add 5 min penalty to each time it was tried
        if score.riddle_num in current_contestant.riddles_tried:
            current_contestant.penalty_time+=5*current_contestant.riddles_tried[score.riddle_num]

def create_scoreboard(scores):
    #Hash table insert average O(1)
    #Iterates though all scores, so this is O(r)
    for score in scores:
        if score.contestant not in contestants:
            contestants.update({score.contestant:Contestant(score.contestant,0,0)})
        #process_score consists only of O(1) average case ops
        process_score(score)

    #Create a list out of the dictionary
    final_scores = list(contestants.values())

    #Python default sort is Timsort, which is average O(c*log(c))
    final_scores = sorted(final_scores,reverse=True)

    return final_scores

def read_write(inpath, outpath):
    #Make sure we're in the correct working directory
    script_dir = os.path.dirname(__file__)
    read = open(os.path.join(script_dir,inpath))
    write = open(os.path.join(script_dir,outpath), 'w')

    #O(r)
    content = read.readlines()

    #Strip newline chars
    #O(r)
    content = [x.strip("\n") for x in content]
    read.close()

    scores = []

    #Create score objects for each row in judging queue
    #O(r)
    for str in content:
        parts = str.split()
        #Appending to list is O(1) [or else Python has serious issues!]
        scores.append(Score(int(parts[0]), int(parts[1]), int(parts[2]), parts[3]))

    #O(r+c*log(c))
    final_scores = create_scoreboard(scores)

    #Write
    for score in final_scores:
        write.write(repr(score)+"\n")

    write.close()

read_write("input.txt","output.txt")
