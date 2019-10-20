<img src="https://github.com/BetWave/BetWaves/blob/master/Wave_inputs/wave_ico.ico" width="50" height="50"> 

# BetWaves

BetWaves is a tool to navigate Betfair Exchange markets using live data, and therefore minimise the advantage Betmakers have over general users. This is achieved primarily by providing a platform to define and execute betting strategies automatically, and secondly by presenting live data regarding market trends with which the user can make an informed decision whether to enter/leave the market.

## Installation

Basic usage:

The branch should be cloned/downloaded locally and the .exe file started.

Development usage:

The tool should be cloned to a local directory, and executed in a Python environment.

## Code Structure

The code is structured into modules, which contain abbreviations to make it easier to understand their role.

| Abbreviation  | Description                                            | Limit  |
| ------------- | ------------------------------------------------------ | ------------- |
| main | The module "main_BetWaves" forms the core of the Betwaves tool. Its role is to open the GUI, form a que and execute betting strategies | 1 file |
| open | The module type shall open driver windows, new files etc | Unlimited |
| reader | The module type shall read information from an open module, and present it in a class | Unlimited |
| strategy | The module type shall apply logic to a reader module data, and output class variables | Unlimited |
| launch | The module type shall execute a given bet by clicking on the appropriate GUI buttons | Unlimited |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Social Media
[Twitter](https://twitter.com/betwaves)
