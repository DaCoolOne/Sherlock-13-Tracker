# Sherlock-13-Tracker
 
### An elegant way to cheat at a family card game.

[Sherlock 13](https://www.arcanewonders.com/product/sherlock-13/) is a card game similar to clue in which players must
use the process of elimination to try and figure out who the thief is. It's a really fastinating game where the process
of elimination is vital to success in a race against time (and other players). It's really good for building critical
thinking skill.

Alternatively, you can simply cheat.

## Usage

Simply run __main__.py with Python3. I used Python 3.7.9, but I think it should work with any version of Python...

`python3 __main__.py`

This command will launch a terminal where commands can be entered. Each command is listed below. Commands (and their
arguments) are case-insensitive.

`CREATE GAME` - Creates a new game.

`CREATE PLAYER [Player Name]` - Creates a new player in the game. Note that player names **must** be a single word.
*Note: You do not need to declare yourself as a player.*

`HAND [CARD1] [CARD2] ...` - Deals yourself into the game with a certain number of cards. This command must be run **after** all
players are created. Cards are identified by last name, with the exception of `SHERLOCK HOLMES` who is identified as `SHERLOCK`,
both because it avoids a name conflict, and because the name "SHERLOCK" is cool. See section "Cards"

`STAT [Optional: COMMAND]` - Prints out statistics about the game currently. Can also be run as a prefix to another command, in
which case it will print out statistics *as if* the command were the case (e.g, the command `STAT James HAS 2 BADGE` will
output a statistics screen for the hypothetical case that Adam has two Badge cards, but the game state remains unchanged).

`[Name] HAS [SOME / NO / Number] [PROPERTY]` - Used to update the statistical information about the game. This command should be
used whenever you or another player asks a question. If asking a quantity question, use a number to represent the amount that
the player states they have of a property (e.g, `Mary HAS 1 SKULL`). If asking a general question, use "SOME" or "NO" for each
individual player to represent whether or not that player has the item (e.g, `Robert HAS SOME BULB`, `Patricia HAS NO EYE`, etc for
each player). Obviously, you don't need to enter any data about the cards in your hand. The program knows...

`NOT [Cardname]` - Used to represent that you know the culprit is not a specific card. This is usually used to eliminate a card
that a player guesses the culprit is. For example, if John guesses that the card is Inspector Lestrade but is wrong, you can
enter `NOT LESTRADE` to eliminate the possibility.

`SUGGEST` - The most powerful weapon, use it wisely. Considers all possible questions and outputs the question that yeilds the
highest probability of giving a decisive result. Once you ask this question (or any question you would like) you can enter the
data collected and watch the possibilities shrink.

## Properties

Properties are named after the picture displayed on the card. These names may not be consistent with the rulebook, but do you
think I read the rulebook when writing this thing? Of course not!

| Property name |
| ------------- |
| SKULL         |
| BULB          |
| JEWEL         |
| PIPE          |
| FIST          |
| BADGE         |
| BOOK          |
| EYE           |

## Cards

Every card in this game is defined by last name, with the exception of Sherlock Holmes, who is defined as "SHERLOCK". If that's
too complicated for you, use the following table:

| Card identifier | Card Name               |
| --------------- | ----------------------- |
| ADLER           | Irene Adler             |
| GREGSON         | Inspector Gregson       |
| LESTRADE        | Inspector G. Lestrade   |
| BAYNES          | Inspector Baynes        |
| HOPKINS         | Inspector Hopkins       |
| BRADSTREET      | Inspector Bradstreet    |
| SHERLOCK        | Sherlock Holmes         |
| WATSON          | John H. Watson          |
| MORIARTY        | James Moriarty          |
| MORAN           | Sebastian Moran         |
| MORSTAN         | Mary Morstan            |
| HOLMES          | Mycroft Holmes          |
| HUDSON          | Mrs. Hudson             |

**MISC**

*All names used in examples were taken from the the Social Security Administration's list,*
*[Top 1000 names over the past 100 years](https://www.ssa.gov/oact/babynames/decades/century.html), alternating between male and female.*

