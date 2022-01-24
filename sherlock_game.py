

from enum import Enum, auto
import math
from typing import Dict, List, Optional, Tuple

class Properties(Enum):
    SKULL=auto()
    BULB=auto()
    JEWEL=auto()
    PIPE=auto()
    FIST=auto()
    BADGE=auto()
    BOOK=auto()
    EYE=auto()

class CardName(Enum):
    ADLER="Irene Adler"
    GREGSON="Inspector Gregson"
    LESTRADE="Inspector G. Lestrade"
    BAYNES="Inspector Baynes"
    HOPKINS="Inspector Hopkins"
    BRADSTREET="Inspector Bradstreet"
    SHERLOCK="Sherlock Holmes"
    WATSON="John H. Watson"
    MORIARTY="James Moriarty"
    MORAN="Sebastian Moran"
    MORSTAN="Mary Morstan"
    HOLMES="Mycroft Holmes"
    HUDSON="Mrs. Hudson"

class Card:
    def __init__(self, name: CardName, props: List[Properties]) -> None:
        self.name = name
        self.properties = props
    def __eq__(self, __o: "Card") -> bool:
        return self.name == __o.name
    def __str__(self) -> str:
        return self.name.name # Todo: properties
    def __repr__(self) -> str:
        return self.__str__()
    def hasProp(self, prop: Properties) -> bool:
        return prop in self.properties

DEFAULT_CARDS: List[Card] = [
    Card(CardName.ADLER, [ Properties.SKULL, Properties.BULB, Properties.JEWEL ]),
    Card(CardName.GREGSON, [ Properties.BADGE, Properties.FIST, Properties.BOOK ]),
    Card(CardName.LESTRADE, [ Properties.BADGE, Properties.EYE, Properties.BOOK ]),
    Card(CardName.BAYNES, [ Properties.BADGE, Properties.BULB ]),
    Card(CardName.HOPKINS, [ Properties.BADGE, Properties.PIPE, Properties.EYE ]),
    Card(CardName.BRADSTREET, [ Properties.BADGE, Properties.FIST ]),
    Card(CardName.SHERLOCK, [ Properties.PIPE, Properties.BULB, Properties.FIST ]),
    Card(CardName.WATSON, [ Properties.PIPE, Properties.EYE, Properties.FIST ]),
    Card(CardName.MORIARTY, [ Properties.SKULL, Properties.BULB ]),
    Card(CardName.MORAN, [ Properties.SKULL, Properties.FIST ]),
    Card(CardName.MORSTAN, [ Properties.BOOK, Properties.JEWEL ]),
    Card(CardName.HOLMES, [ Properties.PIPE, Properties.BULB, Properties.BOOK ]),
    Card(CardName.HUDSON, [ Properties.PIPE, Properties.JEWEL ])
]

class Command(Enum):
    NEW_GAME = 0
    NEW_PLAYER = 1
    START_HAND = 2
    HAS_QUANTITY = 3
    HAS_SOME = 4
    HAS_NONE = 5
    NOT = 6
    STAT = 7
    ASK = 8 # May add the ability to simulate asking quesitons in the future.
    SUGGEST = 9

# How we determine which games to ask questions about.
class Query:
    def __init__(self, cmd_type: Command, player: int = 0, isStat: bool = False, cards: Optional[List[str]] = None, cardId: str = None, amount: int = 0, property: Optional[Properties] = None) -> None:
        self.cmd_type = cmd_type
        self.playerIndex = player
        self.isStat = isStat
        self.cards = [] if cards is None else cards
        self.cardId = '' if cardId is None else cardId
        self.amount = amount
        self.property = property
    @staticmethod
    def fromText(input_str: str, players: List[str]) -> "Query":
        words = input_str.strip().upper().split(" ")
        try:
            _isStat = False
            # Gets stats about game data
            if words[0] == 'STAT':
                if len(words) == 1:
                    return Query(Command.STAT)
                else:
                    _isStat = True
                    words = words[1:]
            # Create a player in the game.
            if words[0] == 'CREATE':
                if words[1] == 'PLAYER':
                    return Query(Command.NEW_PLAYER, player=words[2])
                elif words[1] == 'GAME':
                    return Query(Command.NEW_GAME)
                else:
                    raise ValueError(f'Expected "PLAYER" or "GAME", got {words[1]}')
            # Declares the player's starting hand. Uses last names of cards.
            elif words[0] == 'HAND':
                cardList = words[1:]
                for w in cardList:
                    if not w in [ c.name for c in CardName ]:
                        raise ValueError(f'Card {w} cannot be found.')
                return Query(Command.START_HAND, cards=cardList)
            # Used when someone turns over the center card.
            # Declares someone to not be the culprit.
            elif words[0] == 'NOT':
                if not words[1] in [ c.name for c in CardName ]:
                    raise ValueError(f'Card {words[1]} cannot be found')
                return Query(Command.NOT, cardId=words[1], isStat=_isStat)
            # Compute the best question to ask.
            elif words[0] == 'SUGGEST':
                return Query(Command.SUGGEST)
            # State ownership of stuff.
            elif len(words) > 1 and words[1] == 'HAS':
                try:
                    pIndex = players.index(words[0])
                except ValueError:
                    raise ValueError(f'Player {words[0]} could not be found')

                if not words[3] in [ p.name for p in Properties ]:
                    raise ValueError(f'Property {words[3]} cannot be found')
                
                if words[2].isdigit():
                    return Query(Command.HAS_QUANTITY, player=pIndex, property=Properties[words[3]], amount=int(words[2]), isStat=_isStat)
                else:
                    if words[2] == 'NO':
                        return Query(Command.HAS_NONE, player=pIndex, property=Properties[words[3]], isStat=_isStat)
                    elif words[2] == 'SOME':
                        return Query(Command.HAS_SOME, player=pIndex, property=Properties[words[3]], isStat=_isStat)
                    else:
                        raise ValueError(f'Expected "SOME" or "NO", got {words[2]}')
            else:
                raise ValueError(f'Unknown command "{words[0]}"')
        except IndexError:
            raise ValueError(f'Expected keyword, but no keyword found!')

class QuestionType(Enum):
    HAS = auto()
    QUANTITY = auto()

class Question:
    def __init__(self, question: QuestionType, prop: Properties, player: int = 0) -> None:
        self.q_type = question
        self.prop = prop
        self.player = player
    def formatAsString(self, playerNames: List[str]) -> str:
        if self.q_type == QuestionType.QUANTITY:
            return f'How many {self.prop.name} cards does {playerNames[self.player]} have?'
        else:
            return f'Which players have {self.prop.name} cards?'
    def __str__(self) -> str:
        if self.q_type == QuestionType.QUANTITY:
            return f'How many '
        else:
            return f''
    def __repr__(self) -> str:
        return self.__str__()

class GameState:
    def __init__(self, CenterCard: Card) -> None:
        self.hands: List[List[Card]] = []
        self.centerCard = CenterCard
    def numHands(self) -> int:
        return len(self.hands)
    def hand(self, index: int) -> List[Card]:
        return self.hands[index]
    def stillValid(self, q: Query) -> bool:
        if q.cmd_type == Command.NOT:
            return q.cardId != self.centerCard.name.name
        try:
            if q.cmd_type == Command.HAS_NONE:
                return not any(c.hasProp(q.property) for c in self.hands[q.playerIndex])
            elif q.cmd_type == Command.HAS_SOME:
                return any(c.hasProp(q.property) for c in self.hands[q.playerIndex])
            elif q.cmd_type == Command.HAS_QUANTITY:
                return len([c for c in self.hands[q.playerIndex] if c.hasProp(q.property)]) == q.amount
        except ValueError:
            pass
        return True
    def categorize(self, question: Question) -> str:
        if question.q_type == QuestionType.QUANTITY:
            hand: List[Card] = self.hands[question.player]
            return f'Q {sum(1 if c.hasProp(question.prop) else 0 for c in hand)}'
        else:
            has_map = [ any(c.hasProp(question.prop) for c in hand) for hand in self.hands ]
            return ' '.join([ 'H' ] + [ 'T' if h else 'F' for h in has_map ])

def fillBin(deck: List[Card], binSize: int) -> List[Tuple[List[Card], List[Card]]]:
    insIndex: List[int] = [ i for i in range(binSize) ]
    r = [ ]
    while True:
        newDeck = [ ]
        unusedDeck = [ ]
        for i in range(len(deck)):
            if i in insIndex:
                newDeck.append(deck[i])
            else:
                unusedDeck.append(deck[i])
        r.append((newDeck, unusedDeck))

        ins_i = len(insIndex) - 1

        if insIndex[ins_i] + 1 >= len(deck):
            if ins_i == 0:
                return r
            p_val = insIndex[ins_i]
            ins_i -= 1
            while insIndex[ins_i] == p_val - 1:
                p_val = insIndex[ins_i]
                if ins_i == 0:
                    return r
                ins_i -= 1
            nv = insIndex[ins_i] + 1
            for i in range(len(insIndex) - ins_i):
                insIndex[ins_i+i] = nv + i
        else:
            insIndex[ins_i] += 1

def dealHands(deck: List[Card], handSize: int, handCount: Optional[int] = None) -> List[List[List[Card]]]:
    if handCount is None:
        handCount = len(deck) // handSize
    REMS = [ deck ]
    PERMS = [ [ ] ]
    for i in range(handCount):
        _temp_perm = []
        _temp_rem = []
        for perm, rem in zip(PERMS, REMS):
            bin = fillBin(rem, handSize)
            _temp_perm += [ perm + [b[0]] for b in bin ]
            _temp_rem += [ b[1] for b in bin ]
        PERMS = _temp_perm
        REMS = _temp_rem
    return PERMS

# Compute all possible hands that could be dealt given what's already in your hand.
def ALL_PERMUTATIONS(myHand: List[Card], deck: List[Card], players: int) -> List[GameState]:
    remaining_deck = [ c for c in deck if c not in myHand ]

    assert 2 <= players, "Players must be greater than 2."
    assert (len(remaining_deck) - 1) % (players - 1) == 0, "Cards must be dealt evenly."

    # Start dealing cards...
    HAND_SIZE = (len(remaining_deck) - 1) // (players - 1)

    # Select the culprit   
    SELECT_CULPRIT = fillBin(remaining_deck, 1)

    # Create "bins" for each hand.
    games: List[GameState] = []
    for CULPRIT, REST in SELECT_CULPRIT:
        HAND_POSS = dealHands(REST, HAND_SIZE)
        for HANDS in HAND_POSS:
            g = GameState(CULPRIT[0])
            g.hands = HANDS
            games.append(g)
    
    return games

# Detemine all possible questions
def ALL_QUESTIONS(numPlayers: int, myHand: List[Card], deck: List[Card]) -> List[Question]:
    qs = []
    CARD_COUNTS = {}
    for card in deck:
        if card not in myHand:
            for prop in card.properties:
                CARD_COUNTS.setdefault(prop, 0)
                CARD_COUNTS[prop] += 1
    
    for prop in CARD_COUNTS:
        qs.append(Question(QuestionType.HAS, prop))

        for playerIndex in range(numPlayers):
            qs.append(Question(QuestionType.QUANTITY, prop, playerIndex))
    
    return qs

def SPLIT_BY_ANSWER(games: List[GameState], question: Question):
    buckets: Dict[str, List[GameState]] = {}
    for game in games:
        cat = game.categorize(question)
        buckets.setdefault(cat, [])
        buckets[cat].append(game)
    return buckets

def COMPUTE_STAT(games: List[GameState]) -> List[Tuple[CardName, int]]:
    hitMap = {}
    for game in games:
        culp = game.centerCard.name
        hitMap.setdefault(culp, 0)
        hitMap[culp] += 1
    hitList: List[Tuple[CardName, int]] = [ (k, hitMap[k]) for k in hitMap ]
    hitList.sort(key=lambda a: a[1],reverse=True)
    return hitList

def PRINT_STAT(games: List[GameState]) -> None:
    hitList = COMPUTE_STAT(games)
    if len(hitList) > 0:
        hlText = [ f'{name.value}:'.ljust(40,' ')+f'{(hits/len(games)) * 100:.2f}%' for name, hits in hitList ]
        print(f"Suspects (based on analysis of {len(games)} games):")
        print('\n'.join(hlText))
    else:
        print("No valid games found.")

# Keeps track of all current games
class GameManager:
    def __init__(self, cards: List[Card]) -> None:
        self.FULL_DECK = cards
        self.reset()
    def reset(self) -> None:
        self.myHand = []
        self.players = []
        self.games: List[GameState] = [] # All possible games that could be going on.
    def stat(self) -> str:
        PRINT_STAT(self.games)
    def run_q(self, s: str) -> None:
        try:
            query = Query.fromText(s, self.players)
        except ValueError as e:
            print(e)
            return
        
        # Run the command
        if query.cmd_type == Command.NEW_GAME:
            self.reset()
            print("Started new game. Awaiting player list.")
        elif query.cmd_type == Command.NEW_PLAYER:
            self.players.append(query.playerIndex)
            print(f"Added new player {self.players[-1]}")
        elif query.cmd_type == Command.START_HAND:
            for c in self.FULL_DECK:
                if str(c) in query.cards:
                    print(f'Added new card {c} to hand')
                    self.myHand.append(c)
            self.games = ALL_PERMUTATIONS(self.myHand, self.FULL_DECK, len(self.players) + 1)
        elif query.cmd_type == Command.STAT:
            self.stat()
        elif query.cmd_type == Command.SUGGEST:
            if len(self.games) == 0:
                print("No data to pull suggestions from!")
                return
            
            # If we already know who it is, suggest we accuse.
            if all(culp.centerCard == self.games[0].centerCard for culp in self.games):
                print(f"Accuse {self.games[0].centerCard}!")

            bestQuestion = None
            bestConf = []
            bestScore = -1
            oneHundoPercent = 0
            questions = ALL_QUESTIONS(len(self.players), self.myHand, self.FULL_DECK)
            if len(questions) == 0:
                raise ValueError(f'Could not generate any questions!')
            for question in questions:
                grouping = SPLIT_BY_ANSWER(self.games, question)
                conf = []
                _onehundo = 0
                score = 0
                for groupName in grouping:
                    group = grouping[groupName]
                    probability = len(group) / len(self.games)
                    stats = COMPUTE_STAT(group)
                    confidence = max(s[1] for s in stats) / sum(s[1] for s in stats)
                    if math.isclose(confidence, 1):
                        _onehundo += probability
                    score += confidence * probability
                if score > bestScore:
                    bestQuestion = question
                    oneHundoPercent = _onehundo * 100
                    bestScore = score
            print(f'You should ask, "{bestQuestion.formatAsString(self.players)}"')
            print(f'Average certainty:    {bestScore * 100:.2f}%')
            print(f'Solve probability:    {oneHundoPercent:.2f}%')
        else:
            # Let the fun begin. Cull all games that don't match >:)
            _new_games = [ g for g in self.games if g.stillValid(query) ]
            if query.isStat:
                PRINT_STAT(_new_games)
            else:
                self.games = _new_games
