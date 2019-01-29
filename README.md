# gramhopper
A bot platform for automatic responses based on various triggers.

## Install
Install the latest version:

```bash
$ pip install gramhopper
```

## Configure

### Create a bot
1. [Create a bot using BotFather](https://core.telegram.org/bots#6-botfather).
2. Save the received token in `~/.gramphopper/token.txt`.
3. Enable receiving messages from groups for the bot by sending `/setprivacy` to BotFather,
 then select the new bot and click `Disable`. 

### Enable nicknames for user-based rules
To use user nicknames, `~/.gramphopper/users.json` should contain an object in which the keys 
are nicknames and the values are user IDs, for example:
```json
{
  "nickname1": 123456789,
  "nickname2": 987654321
}
``` 

### Rules configuration
The configuration file is located at `~/.gramphopper/rules.yml`.
 
Basically, the configuration file has three parts:
* **Global triggers**: triggers that can be used in rules without redefining.
* **Global responses**: responses that can be used in rules without redefining.
* **Rules**: Pairs of triggers and responses, which define together what triggers the bot and how it responds.

#### `rules.yml` example
The following configuration file:
```yaml
triggers:
  - name: cat
    type: text.has_exact_word
    word:
      - Meow
      - meow

  - name: duck
    type: text.has_exact_word
    word: Quack

responses:
  - name: found_dog
    type: preset.reply
    preset_response:
      - Hey, here's a dog!

rules:
  - trigger: cat
    response:
      type: preset.message
      preset_response: Hello cat!

  - trigger:
      type: text.has_substring
      substring:
        - Woof
        - woof
        - Ruff
        - ruff
    response: found_dog

  - trigger:
      type: text.regexp
      pattern: ^(Quack|Meow|Woof|Moo)$
    response:
      type: match.message
      template: I hear "{0}"
    probability: 0.3

  - trigger:
      type: event_streak
      counting_event_trigger: duck
      streak_timeout_sec: 60
      event_count: 5
    response:
      type: preset.message
      preset_response: Shut up duck!
```
will yield the following conversation:

![](./demo.gif "Conversation example")


## Run
To run gramhopper, just run:
```bash
$ gramhopper
```
