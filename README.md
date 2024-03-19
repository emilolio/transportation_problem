# Airline Fuel Optimization Solver

## Overview

This project introduces a solver designed to tackle a distinct optimization challenge faced by an airline company aiming to minimize its fuel purchasing expenses. The company is required to source gasoline from three suppliers to satisfy the demands of four different locations, with each location having specific fuel requirements. The problem's complexity is increased by the varying fuel prices, limited supply capacities, and unique requirements for certain locations, including one supplier's inability to deliver to a specific location and a discount offer for large purchases from another.

## Problem Description

- **Suppliers**: Three suppliers with finite fuel supplies (100K, 120K, and 60K liters).
- **Locations**: Four locations with individual fuel demands (50K, 40K, 90K, and 70K liters).
- **Pricing**: Different prices per liter for each supplier-location combination, coupled with a discount mechanism for bulk purchases from one supplier to a specific location.
- **Constraints**: Restrictions include the non-delivery capability of one supplier to a certain location and the overall supply limitations of each supplier.

## Solver

The solver in this project employs Vogel's Initialization Method, adept at addressing transportation problems by initiating with a viable solution and refining iteratively. The solver particularly accounts for:
- The incapability of one supplier to service a specific location.
- A discount pricing scheme for orders exceeding a specified volume from one supplier to one location.

To effectively manage the discount scenario, the solver is executed twice: initially with the standard price, followed by a run with the discounted price. This approach ensures that the optimal purchasing strategy is identified, taking into account the real costs after applying the discount for bulk purchases.
