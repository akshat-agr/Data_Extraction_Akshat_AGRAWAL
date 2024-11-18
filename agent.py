import time
import logging

class TaskManager:
    def __init__(self, max_retries=3, delay=5):
        self.max_retries = max_retries
        self.delay = delay
        self.logger = self.setup_logger()

    def setup_logger(self):
        """Setup logger for error handling and tracking."""
        logger = logging.getLogger("TaskManager")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def execute_task(self, task, *args, **kwargs):
        """Execute a task with retry mechanism and error handling."""
        retries = 0
        while retries < self.max_retries:
            try:
                self.logger.info(f"Executing task: {task.__name__} with arguments: {args}, {kwargs}")
                result = task(*args, **kwargs)
                self.logger.info(f"Task {task.__name__} completed successfully with result: {result}")
                return result
            except Exception as e:
                retries += 1
                self.logger.error(f"Task {task.__name__} failed on attempt {retries}. Error: {str(e)}")
                if retries < self.max_retries:
                    self.logger.info(f"Retrying task {task.__name__} in {self.delay} seconds...")
                    time.sleep(self.delay)
                else:
                    self.logger.error(f"Task {task.__name__} failed after {self.max_retries} attempts.")
                    raise e

    def handle_error(self, error_message):
        """Handle task errors globally and notify the user."""
        self.logger.error(f"An error occurred: {error_message}")
        return error_message
