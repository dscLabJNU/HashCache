
from locust import LoadTestShape
from azure_load import analyze


class AzureLoadShape(LoadTestShape):
    """
    A step load shape that waits until the target user count has
    been reached before waiting on a per-step timer.
    The purpose here is to ensure that a target number of users is always reached,
    regardless of how slow the user spawn rate is. The dwell time is there to
    observe the steady state at that number of users.
    Keyword arguments:
        targets_with_times -- iterable of 2-tuples, with the desired user count first,
            and the dwell (hold) time with that user count second
    """

    targets_with_times = analyze.generate_targets_with_times_azure()

    def __init__(self, *args, **kwargs):
        self.step = 0
        self.time_active = False
        super().__init__(*args, **kwargs)

    def tick(self):
        """
        This function executed per second
        """
        if self.step >= len(self.targets_with_times):
            return None

        target = self.targets_with_times[self.step]
        users = self.get_current_user_count()

        if target.users == users:
            # run_time = self.get_run_time()
            # if run_time > target.dwell:
            self.step += 1
            print(f"step: {self.step}/{len(self.targets_with_times)}, num of users: {users}")

        # Spawn rate is the second value here. It is not relevant because we are
        # rate-limited by the User init rate.  We set it arbitrarily high, which
        # means "spawn as fast as you can"
        return (target.users, 100)
