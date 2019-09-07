# gramhopper
[![image](https://img.shields.io/pypi/v/gramhopper.svg)](https://pypi.org/project/gramhopper/)
[![image](https://img.shields.io/pypi/l/gramhopper.svg)](https://pypi.org/project/gramhopper/)
[![image](https://img.shields.io/pypi/pyversions/gramhopper.svg)](https://pypi.org/project/gramhopper/)

A bot platform for automatic responses based on various triggers.

![](https://raw.githubusercontent.com/OrBin/gramhopper/master/demo.gif "Conversation example")
<details>
 <summary>Click to view this demo's configuration</summary>

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
  # Identifies a cat (a global "cat" trigger) and sends "Hello cat!" (an inline response).
  - trigger: cat
    response:
      type: preset.message
      preset_response: Hello cat!
  # Identifies a dog (an inline trigger) and replies "Hey, here's a dog!"
  # (a global "found_dog" response).
  - trigger:
      type: text.has_substring
      substring:
        - Woof
        - woof
        - Ruff
        - ruff
    response: found_dog
  # Identifies an animal sound (an inline trigger) and replies 
  # 'I hear "(the animal sound)"' (an inline response), with a 30% probability.
  - trigger:
      type: text.regexp
      pattern: ^(Quack|Meow|Woof|Moo)$
    response:
      type: match.message
      template: I hear "{0}"
    probability: 0.3
  # Identifies 5 occurrences in 60 seconds of a duck sound (an inline event_streak
  # trigger that uses a global "duck" trigger") and replies "Shut up duck!".
  - trigger:
      type: event_streak
      counting_event_trigger: duck
      streak_timeout_sec: 60
      event_count: 5
    response:
      type: preset.message
      preset_response: Shut up duck!
```
</details>

## Setup and Configuration
Follow [this tutorial](SETUP_AND_CONFIGURE.md) to setup a bot and configure gramhopper.

## Install and Run
To run gramhopper, just run:
#### From installed package

```bash
pip install gramhopper
gramhopper
```

##### Specify configuration file
```bash
gramhopper --config=/path/to/rules_file.yml
```

#### From docker image
```bash
docker pull orbin/gramhopper:latest
docker run -it -v /your/configuration/dir:/root/.gramhopper orbin/gramhopper:latest
```

## Documentation
Read more about the various triggers and responses in [our documentation](https://gramhopper.readthedocs.io/en/latest/).

## Contributing
You are welcome to contribute to gramhopper - read the [contribution guidelines](CONTRIBUTING.md) to get started.
