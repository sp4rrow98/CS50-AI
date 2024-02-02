from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is a Knight if he is both a knave and a knight
    Implication(AKnight, And(AKnave, AKnight)),

    # A can only be Knave or Knight, not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A can only be Knave or Knight, not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),

    # B can only be Knave or Knight, not both
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),

    # A implies they are both knaves, if he is a Knight he is right
    Implication(AKnight, And(AKnave, BKnave)),

    # If he is not, they are not both Knaves so B is a knight
    Implication(AKnave, Not(And(AKnave, BKnave)))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is either Knive/Knight, same for B.
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),
    
    # If A is Knight, they both are, if he is lying, B is a Knight
    # Consider both cases
    Biconditional(AKnight, And(AKnight, BKnight)),
    Biconditional(AKnave, And(AKnave, BKnight)),
    Biconditional(BKnight, And(BKnight, AKnave)),
    Biconditional(BKnave, And(AKnave, BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Each person can only be a Knight or a Knave
    Or(AKnave, AKnight), Not(And(AKnave, AKnight)),
    Or(BKnave, BKnight), Not(And(BKnave, BKnight)),
    Or(CKnave, CKnight), Not(And(CKnave, CKnight)),

    # A says either “I am a knight.” or “I am a knave.”, but you don’t know which.
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, And(AKnight, AKnave)),

    # B is lying about what A said so he must be a Knave, therefore he is lying about C as well
    Biconditional(BKnight, And(Implication(AKnight, AKnight), CKnave)),
    Biconditional(BKnave, And(Or(AKnight, AKnave), CKnight)),

    # C says A is a knight
    # Let's consider both cases again
    Biconditional(CKnight, AKnight),
    Biconditional(CKnave, And(AKnave, BKnight))
)



def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]

    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
