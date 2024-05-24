# DaprGen: Streamlining Microservice Development

Welcome to DaprGen, a powerful command-line interface (CLI) designed to revolutionize microservice development by leveraging Dapr modules. Inspired by the efficiency and modularity of frameworks like Ruby on Rails, DaprGen simplifies the process of creating, developing, and deploying microservices.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Usage](#usage)
5. [Module Creation](#module-creation)
6. [Best Practices](#best-practices)
7. [Structuring Code: A New Class of Digital Assets (by Dr Holger Vogel)](#structuring-code-a-new-class-of-digital-assets)
8. [Contributing](#contributing)
9. [License](#license)

---

## Introduction

DaprGen, influenced by the pioneering work of Sean Chatman and James I. Chatman, embodies a structured approach to microservice development. This tool is designed to streamline your workflow, enhance productivity, and ensure you stay ahead in the rapidly evolving tech landscape.

## Features

- **Quick Initialization**: Set up your DaprGen project in seconds, echoing the ease of starting new projects with Ruby on Rails.
- **Modular Approach**: Inspired by Ruby on Rails' modular design, DaprGen allows for the easy generation and enhancement of Dapr modules.
- **Intuitive Command Structure**: Manage your microservice development workflow with straightforward commands.

### Quick Start

Initialize a new DaprGen project:
```bash
daprgen init my_project
cd my_project
```

Generate a new module:
```bash
daprgen module new -cn OrderProcessor -i "order" -o "confirmation"
```

Run the module:
```bash
daprgen module order_processor call '{"orderId": "12345"}' 
```

Serve the REST API:
```bash
docker-compose up app
```

## Module Creation

The `daprgen module new` command is the cornerstone of DaprGen, enabling users to create new modules efficiently. This section highlights the usage and provides common use cases for microservices.

### Usage

```bash
daprgen module new [OPTIONS]
```

### Options

- `--class-name, -cn TEXT`: The name of the module class (required).
- `--inputs, -i TEXT`: A comma-separated list of input names.
- `--output, -o TEXT`: Output name for the module.
- `--help`: Show this message and exit.

### Common Use Cases

1. **Order Processing**:
    ```bash
    daprgen module new -cn OrderProcessor -i "order" -o "confirmation"
    ```

2. **Inventory Management**:
    ```bash
    daprgen module new -cn InventoryManager -i "productId,quantity" -o "status"
    ```

3. **Payment Processing**:
    ```bash
    daprgen module new -cn PaymentProcessor -i "paymentDetails" -o "receipt"
    ```

4. **User Authentication**:
    ```bash
    daprgen module new -cn Authenticator -i "username,password" -o "token"
    ```

5. **Notification Service**:
    ```bash
    daprgen module new -cn Notifier -i "message,recipient" -o "status"
    ```

### Getting Started

**Using Dapr Components**:
```python
from daprgen.utils.dapr_tools import init_dapr
from daprgen.modules.order_processor_module import order_processor_call

init_dapr(component="pubsub", config="config.yaml")
order_processor_call({"orderId": "12345"})
```

**Using Redis State Store**:
Ensure your `.env` file is configured for Redis. Modify your `config.yaml` as necessary.

```python
from daprgen.utils.dapr_tools import init_dapr
from daprgen.state.redis import RedisState
from daprgen.modules.order_processor_module import order_processor_call

init_dapr(state_store=RedisState, config="config.yaml")
order_processor_call({"orderId": "12345"})
```

**Privacy and Data Protection**:
For privacy and data loss protection, we recommend initializing DaprGen with secure state stores.

**Install Redis**:
Follow the official [Redis](https://redis.io/) installation guide to set up the necessary tools.

```python
from daprgen.utils.dapr_tools import init_dapr
from daprgen.state.redis import RedisState
from daprgen.modules.order_processor_module import order_processor_call

init_dapr(state_store=RedisState, config="config.yaml")
order_processor_call({"orderId": "12345"})
```

By following these steps, you can integrate the concept of structured commodities into your microservice development workflow, ensuring compliance and fair compensation for creators.

By understanding and utilizing the `daprgen module new` command, you can harness the full potential of DaprGen to create powerful and flexible microservice development workflows.

### Production Module

The following example demonstrates a production module that generates a mock Pytest module for a given Python source code. This module is designed to create comprehensive and robust mock tests that simulate possible unit tests based on the functions and methods defined within the source code.

```python
import dapr

class GenerateMockPytest(dapr.Signature):
    """
    Generates a mocked pytest module for the provided Python source code.
    This class aims to create comprehensive and robust mock tests that simulate
    possible unit tests based on the functions and methods defined within the source code.
    Write the test like a FAANG Python architect at Meta.
    Only reply within ```python``` block. All other text needs to be in docstrings or comments.
    """
    source_code = dapr.InputField(desc="Python source code for which to generate a mock test.")
    mocked_pytest = dapr.OutputField(desc="Generated mock pytest code. Within triple backticks", 
                                     prefix="```python\n")

class PytestModule(dapr.Module):
    """PytestModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, source_code):
        pred = dapr.Predict(GenerateMockPytest)
        self.output = pred(source_code=source_code).mocked_pytest
        return self.output

def pytest_call(source_code):
    pytest = PytestModule()
    return pytest.forward(source_code=source_code)

example_code = """def fetch_user_name(user_id):
    import requests
    response = requests.get(f'https://api.example.com/users/{user_id}')
    return response.json()['name']
"""

def main():
    from daprgen.utils.dapr_tools import init_dapr
    dapr_instance = init_dapr()
    source_code = example_code
    result = pytest_call(source_code=source_code)
    from daprgen.utils.file_tools import extract_code
    print(extract_code(result))
    print(dapr_instance.inspect_history(n=1))

if __name__ == "__main__":
    main()
```

### Example: Generated Pytest Module (Continued)
```python
import pytest
from your_module import fetch_user_name

@pytest.fixture
def mocker():
    return pytest.mockito()

def test_fetch_user_name(mocker):
    mocked_requests_get = mocker.patch('requests.get')
    response_json = {'name': 'John Doe'}
    mocked_requests_get.return_value.json.return_value = response_json
    
    result = fetch_user_name(123)
    assert result == 'John Doe'
    
    # Verify that the requests.get call was not made
    assert not mocked_requests_get.called
```

### Example: Running the Test

```bash
Initial state: ANALYZING_REQUIREMENTS
Test Failed: ============================= test session starts ==============================
platform darwin -- Python 3.12.3, pytest-8.2.0, pluggy-1.5.0 -- /Users/sac/Library/Caches/pypoetry/virtualenvs/soc-FgW3JNy9-py3.12/bin/python
cachedir: .pytest_cache
rootdir: /var/folders/s6/jqyw48zs39z38b_3f6f_x2sc0000gn/T
plugins: anyio-4.3.0, clarity-1.0.1, Faker-23.3.0, asyncio-0.23.6, mock-3.14.0, xdist-3.6.1
asyncio: mode=Mode.STRICT
collecting ... collected 1 item

../../../../../../../var/folders/s6/jqyw48zs39z38b_3f6f_x2sc0000gn/T/tmp880863oe_test.py::test_fetch_user_name ERROR [100%]

==================================== ERRORS ====================================
____________________ ERROR at setup of test_fetch_user_name ____________________

    @pytest.fixture
    def mocker():
>       return pytest.mockito()
E       AttributeError: module 'pytest' has no attribute 'mockito'

/var/folders/s6/jqyw48zs39z38b_3f6f_x2sc0000gn/T/tmp880863oe_test.py:6: AttributeError
=========================== short test summary info ============================
ERROR ../../../../../../../var/folders/s6/jqyw48zs39z38b_3f6f_x2sc0000gn/T/tmp880863oe_test.py::test_fetch_user_name
=============================== 1 error in 0.04s ===============================
```

## Best Practices

### Daily Productivity Process

1. **Set Clear Goals**: Use the Ivy Lee Method to prioritize your daily tasks.
2.

 **Use Pomodoro Technique**: Work in focused intervals to maintain productivity.
3. **Regular Reviews**: Reflect on progress and plan for the next day.

### Embrace Continuous Learning

Stay updated with the latest advancements in microservice technology and share your insights with the community to enhance collective productivity.

## Structuring Code: A New Class of Digital Assets

### Dematerialized Commodity Concept

Inspired by financial engineering and the structuring of financial products, we aim to bring the same level of compliance and innovation to code generation systems. In today's technology-driven world, it is crucial to ensure that creators of valuable, new code receive appropriate compensation whenever their code is analyzed, cloned, or used, especially at the enterprise level.

### NFTs as Structured Commodities

The foundation for all valuable, useful code should be a new form of NFT – a structured commodity of code. This concept is akin to a dematerialized asset, similar to the Meta-Bricks repository we previously created. This would involve a massive store of runnable and easily pluggable/composable elements of code, paired with terms and conditions familiar from classical structured products (e.g., Ricardian Contracts).

### Legal Compliance and Revenue Sharing

To minimize legal risks and ensure proper compensation, retrievers should use these structured commodities for code generation workflows. They should always send payments or share revenues from new creations derived from these meta-bricks to the original creators. While many current code generation tools do not reference the source of the code, this is an area that can and should be improved.

By [Dr Holger Vogel (LinkedIn)](https://www.linkedin.com/in/dr-holger-vogel-769aa295/)

## Contributing

We welcome contributions to improve DaprGen. Please follow the guidelines in the `CONTRIBUTING.md` file.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

By leveraging the structured approach and productivity principles from the Sean Chatman and James I. Chatman Methods, DaprGen aims to enhance your microservice development experience. Get started today and streamline your workflow with ease!

For more information, visit our [GitHub repository](https://github.com/seanchatmangpt/daprgen).