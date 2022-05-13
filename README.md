# GLOBAL-LOGIC-ENTRY-CHALLENGE

*python 3.10.1*

## Example usage

```bash
$ cd src/cmd
$ python cli.py (-h) (-help) (--help)           # with or without the switch it will display the below 
                                                # shown instructions

$ python cli.py shop status                     # the status of every item in the shop
$ python cli.py shop status apple               # the status of apple in the shop
$ python cli.py shop estimate apple 12          # estimate the cost of 12 apples in the shop

$ python cli.py warehouse status                # the status of every item in the warehouse
$ python cli.py warehouse status apple          # the status of apple in the warehouse
$ python cli.py warehouse estimate apple 12     # the status of apple in the warehouse

# The above commands do not require the REST servers to be run, it will operate directly
# on the warehouse.json file.


# On the other hand the below command sends requests and to the rest servers
# It takes config from cli_config.json
$ python cli.py -rest ...     # run any from the above commands by using REST


# This command does NOT work with REST  
$ python cli.py warehouse add -product apple -quantity 12 -price 0.5
        # add product to the warehouse with the specified code, in the quantity, and with the price


$ python cli.py config  # configure the project with this CLI tool 
                       <shop/warehouse> --listen-addr 127.0.0.1:8080
                       # address on which <shop/warehouse> REST server will be listening


```



### Files

```yaml

src/
    cmd/
        - cli.py
                # the command line interface
    config/
    shop/
    warehouse/
        - warehouse.py
                # warehouse logic, it will get its configuration from src/config/warehouse_config(_test).json

        - warehouse.json
                # This file will have the contents of the warehouse persisted

        - warehouse_test.json
                # This file will be used for testing the project, and its contents will be constantly reset every test

```


Two REST API servers, for the shop, and for the warehouse, each one with an REST API.
The warehouse


<br>
<br>
<br>

##  &nbsp; The task:

### Description
 
As a customer, I would like to buy a product from the shop
Given I’m a customer
Given the current state of `<product>` in shop is `<initial_amount>`
When I buy `<buy_amount>` `<product>`
Then the number of products in the warehouse is updated to `<final_state>`

 
#### Examples:
 - /`product`/`initial_amount`/`buy_amount`/`final_state`/
 - /`orange`/`13`/`10`/`3`/
 - /`apple`/`55`/`15`/`40`/
 - /`apple`/`55`/`15`/`40`/

 
#### Acceptance Criteria:
 - Implement an API for **buying products**,
 - Implement an API for **checking the status** in the shop.

#### Mandatory requirements
 - Publishing the code on GitHub on a public repository,
 - History of git commits with **incremental changes** that prove individual effort,
 - **Object-Oriented Programming** style,
 - Python style convention - PEP8, https://peps.python.org/pep-0008/,
 - Correctly designing the interface of classes or methods and python modules,
 - **Unit tests**,
 - **Command-line interface**,

The state of the shop can be persisted in a **JSON file**, whenever a user wants to check the state of the shop, the shop is reading the file and extracting proper values, when a user buys something the shop modifies the file,

README.md file with instructions about how to run the project.

#### It will be an asset if you:

 - Add another complexity with a warehouse that is selling products to the shop. The shop is calculating the price with 30% commission. A product in a warehouse can have various prices from which the shop is buying a given amount of the product. When a customer wants to buy some amount of product, the shop needs to calculate what would be the price of that product based on prices in the warehouse. The order of product packages in the warehouse is fixed, eg. if we have 10 apples at price \$5, 15 at price \$2, and 5 at price \$5 then we’re not optimizing the prices but selling it in the fixed order,
 - Using flask and implementing **REST API**,
 - Designing **tests for flask** application,
 - Packaging the project (**setup.py** script) with instructions on how to do that,
 - Docker image and instruction on how to run the application using docker image,
 - Using GitHub Actions - https://docs.github.com/en/actions/quickstart.