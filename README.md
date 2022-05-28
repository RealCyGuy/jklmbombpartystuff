# jklmbombpartystuff

[jklm.fun](https://jklm.fun) bomb party bots and scripts and stuff!

## Files

Explanation of the files in this repository!

### `.`

the root directory

- `README.md`: this file ([verified by github pilot](https://cdn.upload.systems/uploads/nPggXkRy.png))
- `utils.py`: utility functions
- `LICENSE`: MIT license!

### `humans`

lots of bots playing at once!

- `publichumans.py`: maintain 8 bots for public play
- `core/human.py`: human (bot) class
- `core/state.py`: shared state class

### `testing`

bots/scripts to test bomb party words, etc.

#### lists of things

- `correct.txt`: correct words
- `wrong.txt`: incorrect words
- `syllables.txt`: possible syllables

#### scripts to add to lists

- `roomchecker.py`: join rooms to add words to `correct.txt`
- `wordvalidator.py`: bots that validate words

### `userscripts`

browser userscripts!

- `detailed rules summary.user.js`: ([install](https://github.com/RealCyGuy/jklmbombpartystuff/raw/main/userscripts/detailed%20rules%20summary.user.js)) show a more detailed rules summary
- `precise time chat.user.js`: ([install](https://github.com/RealCyGuy/jklmbombpartystuff/raw/main/userscripts/precise%20time%20chat.user.js)) show seconds in chat

### `scripts`

some scripts that aren't bots

- `getpublicenglishbombpartygames.py`: get sorted public english bomb party games for use with `roomchecker.py`
- `roomcreator.py`: create jklm.fun rooms
- `profilepicture.py`: generate base64 data uri images for jklm profile pictures! it compresses images and allows transparency!

### `pictures`

penguin profile pictures for bots

### `lists`

several word lists from different sources
