import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor

import requests
import sentry_sdk

class StellarMapAsyncHelpers:

    def execute_async(self, *args, **kwargs):
        """
        Executes a task asynchronously using a thread pool executor.

        :param args: Arguments to pass to the task function.
        :param kwargs: Keyword arguments to pass to the task function.
        :return: None
        """

        # Get the event loop
        loop = asyncio.get_event_loop()

        # Schedule the task function to be executed asynchronously and get the future object
        future = asyncio.ensure_future(self.add_task_to_threadpool(*args, **kwargs))
        
        # Run the event loop until the task is complete
        loop.run_until_complete(future)

    async def add_task_to_threadpool(self, task_list, custom_function, *args, **kwargs):
        """
        This function runs a list of tasks asynchronously using a custom function.

        :param self: The object instance of the class method.
        :param task_list: The list of objects to be used as tasks.
        :param custom_function: The custom function to execute on each task.
        :param args: The non-keyword arguments for the custom function.
        :param kwargs: The keyword arguments for the custom function.

        The function initializes an empty list called tasks. It then creates a ThreadPoolExecutor 
        with a maximum of 17 workers and a requests session.

        Next, it initializes an event loop, and for each row or task in the task_list, it executes
        the custom_function using the session, obj, args, and kwargs as parameters. This is done
        using loop.run_in_executor() and functools.partial().

        The tasks list is updated with the resulting tasks from each execution. Finally, the tasks
        are initiated to run, and their results are awaited. If an error occurs during the execution,
        it is caught, and an error message is raised with the corresponding exception captured by Sentry SDK.
        """

        try:
            tasks = []

            # Create thread pool and requests session
            with ThreadPoolExecutor(max_workers=17) as executor:
                with requests.Session() as session:

                    # Initialize event loop
                    loop = asyncio.get_event_loop()

                    # Create tasks for each object in task_list
                    tasks = [
                        loop.run_in_executor(
                            executor,
                            functools.partial(custom_function, session, obj, *args, **kwargs)
                        )
                        for obj in task_list
                    ]

                    # Run and await tasks
                    for response in await asyncio.gather(*tasks):
                        print('Success')
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'StellarMapAsyncHelpers.add_task_to_threadpool Error: {e}')
