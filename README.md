# Shipping and Trucking Simulation

This project simulates the loading and unloading of trucks and ships. It models the process of loading trucks, storing goods in stack areas, and then loading these goods onto ships based on their destination.

## Features

- **Truck Class**: Represents a truck and its associated information like country, load quantity, etc.
- **Ship Class**: Represents a ship and its associated information like capacity, destination country, etc.
- **Loading and Unloading**: The program handles the loading of trucks into stack areas and the subsequent loading of these goods onto ships.
- **Cost Calculation**: The total cost associated with the loaded goods is calculated and displayed at the end of the simulation.

## Files

- `olaylar.csv`: Contains the event data for trucks.
- `gemiler.csv`: Contains the event data for ships.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Install the required Python packages:
    ```bash
    pip install pandas chardet
    ```

## Usage

1. Ensure you have the `olaylar.csv` and `gemiler.csv` files in the same directory.
2. Run the simulation:
    ```bash
    python simulation.py
    ```
3. The results, including the total cost and the final state of stack areas, will be printed to the console.

## Customization

- **Max Capacity**: The maximum capacity of stack areas can be adjusted by modifying the `max_capacity` variable.
- **Simulation Logic**: The logic for loading and unloading can be customized in the `simulation()` function.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
