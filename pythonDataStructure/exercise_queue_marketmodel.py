"""
File: exercise_queue_marketmodel.py
Author: Chen Zhang
Requirement: Program to predict customer queue state of a market in different case.
"""
import random
from queue_linked import LinkedQueue


class MarketModel(object):
    def __init__(self, probability_of_single_customer, total_running_time, average_serving_time):
        self._prob_of_customer = probability_of_single_customer
        self._total_time = total_running_time
        self._average_time = average_serving_time
        self._cashier = Cashier()

    def run_simulation(self):
        """Run the clock for n ticks."""
        for current_time in range(self._total_time):
            # Attempt to generate a new customer
            customer = Customer.generate_customer(self._prob_of_customer, current_time, self._average_time)

            # Send customer to cashier if successfully
            # generated
            if customer is not None:
                self._cashier.add_customer(customer)

            # Tell cashier to provide another unit of service
            self._cashier.serve_customers(current_time)

    def __str__(self):
        return str(self._cashier)


class Cashier(object):
    def __init__(self):
        self._total_customer_wait_time = 0
        self._customer_served = 0
        self._current_customer = None
        self._queue = LinkedQueue()

    def add_customer(self, c):
        self._queue.add(c)

    def serve_customers(self, current_time):
        if self._current_customer is None:
            # No customers yet
            if self._queue.isEmpty():
                return
            else:
                # Pop first waiting customer and tally results
                self._current_customer = self._queue.pop()
                self._total_customer_wait_time += current_time - self._current_customer.arrival_time()
                self._customer_served += 1

        # Give a unit of service
        self._current_customer.serve()

        # If current customer is finished, send it away
        if self._current_customer.amount_of_service_needed() == 0:
            self._current_customer = None

    def __str__(self):
        result = 'Totals for the cashier \n' + 'Number of customers served:' + str(self._customer_served) + '\n'
        if self._customer_served != 0:
            ave_wait_time = self._total_customer_wait_time / self._customer_served
            result += 'Number of customers left in queue:' + str(len(self._queue)) + '\n' + \
                      'Average time customers spend waiting to be served:' + '%5.2f' % ave_wait_time
        return result


class Customer(object):

    @classmethod
    def generate_customer(cls, probability_of_new_arrival, arrival_time, ave_time_per_customer):
        """
        Returns a Customer object if the probability of arrival is greater than or equal to a random number.
        Otherwise, return None, indicating no new customer
        """
        if random.random() <= probability_of_new_arrival:
            return Customer(arrival_time, ave_time_per_customer)
        else:
            return None

    def __init__(self, arrival_time, service_needed):
        self._arrival_time = arrival_time
        self._amount_of_service_needed = service_needed

    def arrival_time(self):
        return self._arrival_time

    def serve(self):
        """Accept a unit of service from the cashier."""
        self._amount_of_service_needed -= 1

    def amount_of_service_needed(self):
        return self._amount_of_service_needed


def main():
    # Set
    print('Welcome the Market Simulator \n')
    total_running_time = int(input('Enter the total running time: '))
    average_time_per_customer = int(input('Enter the average time per customer: '))
    probability_of_new_arrival = float(input('Enter the probability of a new arrival: '))

    model = MarketModel(probability_of_new_arrival, total_running_time, average_time_per_customer)
    model.run_simulation()

    print(str(model))


if __name__ == '__main__':
    main()
