from threading import Thread, Timer
from random import randint

NUM_ITERATIONS = 1000
ONLY_WIN_ON_EXACT = True
ALL_LADDERS_ARE_SNAKES = True


turns_to_win = []
turns = []
num_fields = 100

jumps = jumps_dict = {
    2: 38,
    7: 14,
    8: 31,
    15: 26,
    16: 6,
    21: 42,
    28: 84,
    36: 44,
    46: 25,
    49: 11,
    51: 67,
    62: 19,
    64: 60,
    71: 91,
    74: 53,
    78: 98,
    87: 94,
    92: 88,
    95: 75,
    99: 80,
}
jumps = jumps.items()


def play():
    turn = 0
    player_pos = 1
    t = []
    while player_pos < num_fields:
        turn +=1
        roll = randint(1,6)
        player_pos = player_pos + roll
        if player_pos > num_fields:
            if ONLY_WIN_ON_EXACT:
                player_pos = num_fields - (player_pos-num_fields)
            else:
                player_pos = num_fields
        if ALL_LADDERS_ARE_SNAKES:
            for key, value in jumps:
                if key==player_pos or value==player_pos:
                    player_pos = min(key, value)
                    break
        else:
            player_pos= jumps_dict.get(player_pos, player_pos)
                
        t.append(player_pos)
    assert player_pos == num_fields
    if len(t) < 40 or len(t) >15000:
        turns.append(t)
    turns_to_win.append(turn)

def main():
    
    threads = [Thread(target=play) for i in range(NUM_ITERATIONS)]
    for t in threads:
        t.start()


    for t in threads:
        t.join()
    
    
    print("all done!")
    print(f"it took an average of {sum(turns_to_win) / len(turns_to_win)} turns to win")
    
    print(f"slowest was {max(*turns_to_win)} turns")
    print(f"fastest was {min(*turns_to_win)} turns")
    print("\nfastest turnorder was:")
    p = False
    for t in turns:
        if len(t) == min(*turns_to_win):
            print(t)
            p=True
    if not p:
        print("not recorded")

    print("\nlongest ending was:")
    p = False
    for t in turns:
        if len(t) == max(*turns_to_win):
            print(t[-20:])
            p=True
    if not p:
        print("not recorded")

    print("recorded turn lengths")
    print([len(t) for t in turns])
if __name__ == "__main__":
    main()