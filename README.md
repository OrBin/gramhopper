# gramhopper
A bot platform for automatic responses based on various triggers.

## Installation
Install the latest version:

```bash
pip install gramhopper
```

## Usage
To run gramhopper, just run:
```bash
$ gramhopper
```

## Configuration
The configuration file is located at `~/.gramphopper/rules.yml`.
 
Basically, the configuration file has three parts:
* **Global triggers**: triggers that can be used in rules without redefining them.
* **Global responses**: responses that can be used in rules without redefining them.
* **Rules**: Pairs of triggers and responses, which define together what triggers the bot and how it responds.

