import logging
import random
import pandas as pd
import math
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
import sys
sys.path.append("../")
import constant


class Azure:
    def __init__(self, workflow_info, azure_type='azure_bench') -> None:
        self.info = workflow_info
        self.azure_type = azure_type
        self.df = self.load_df(day=self.info['azure_trace_day'])

    def load_df(self, day):
        print("Loading Azure dataset...")
        df = pd.read_csv(
            f"{constant.AZURE_TRACE_ADDR}/AzureFunctionsInvocationTraceForTwoWeeksJan2021Day{day:02d}.csv")
        df['start_timestamp'] = df['end_timestamp'] - df['duration']
        # print(df['invo_ts'])
        return df

    def load_mappers(self):
        with open(f"{constant.AZURE_BENCH_ADDR}/func_mapper.json") as load_f:
            func_map_dict = json.load(load_f)
        with open(f"{constant.AZURE_BENCH_ADDR}/app_mapper.json") as load_f:
            app_map_dict = json.load(load_f)

        return func_map_dict, app_map_dict

    def validate_input_values(self, filter_df: pd.DataFrame):
        """
        (19.999, 26.0]    66.570015
        (26.0, 28.0]       3.189493
        (28.0, 29.0]       3.667065
        (29.0, 31.0]       7.300017
        (31.0, 33.0]      10.438342
        (33.0, 35.0]       8.835067
        should be ouputed
        """
        print(filter_df["input_n"].value_counts(
            bins=[20, 26, 28, 29, 31, 33, 35], normalize=True).sort_index() * 100)

    def assign_input_values(self, filter_df: pd.DataFrame):
        num_inputs = len(filter_df)
        # Probability of each range in below, i.e., [20, 26], etc...
        prob_numrange = {
            66.56: [20, 26],
            3.19: [27, 28],
            3.66: [29, 29],
            7.3: [30, 31],
            10.45: [32, 33],
            8.85: [34, 35]
        }
        probablities = list(prob_numrange.keys())
        num_range = list(prob_numrange.values())

        # Converts each probability to a specific number according to the len(num_inputs)
        amounts = list(map(lambda x: math.ceil(
            x/100 * num_inputs), probablities))

        # Alignment
        diff = sum(amounts) - num_inputs
        if diff > 0:
            while diff:
                # Randomly select the elements and minus one, note that we have set the random seed in run.py
                random_index = random.randrange(len(amounts))
                amounts[random_index] -= 1
                diff -= 1
        else:
            num_inputs = sum(amounts)

        # print(f"{num_inputs} of inputs needed, now generating {sum(amounts)} of input values")
        distribution = {
            amounts[0]: num_range[0],
            amounts[1]: num_range[1],
            amounts[2]: num_range[2],
            amounts[3]: num_range[3],
            amounts[4]: num_range[4],
            amounts[5]: num_range[5],
        }

        input_values = []
        for amounts, num_range in distribution.items():
            # print(f"We want to generate {amounts/num_inputs * 100}% ({amounts}/{num_inputs}) of numbers from {min(num_range)} to {max(num_range)}")
            input_values.extend(
                [random.randint(min(num_range), max(num_range)) for _ in range(amounts)])
        filter_df = filter_df.reset_index().drop('index', axis=1)

        # Shuffling the input list for randomness,
        random.shuffle(input_values)
        filter_df["input_n"] = pd.Series(input_values)
        filter_df["input_n"].fillna(30, inplace=True)

        # Turn it on if you wants to check the distribution of input_values
        # self.validate_input_values(filter_df)
        return filter_df

    def plot_RPS(self, df: pd.DataFrame):
        # plt.rc('font', family='Times New Roman', weight='bold', size=10)
        plt.rc('font', weight='bold', size=10)
        os.system("mkdir -p imgs")
        time_range = constant.AZURE_SAMPLE_UNIT
        df['invo_ts'] = df['invo_ts'] + pd.to_datetime(self.info['time_line_start'], utc=True)
        df['invo_ts'] = pd.to_datetime(df['invo_ts'])
        values = df.resample(time_range, on='invo_ts').count()['func']
        values = values[values != 0]
        # fig, ax = plt.subplots(figsize=(5, 1.5))
        fig, ax = plt.subplots(figsize=(10, 3))
        x_list = values.index

        xformatter = mdates.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(xformatter)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
        # ax.set_xlabel(f"Timeline (Day{day:02d})")
        ax.set_ylabel("Concurrency", weight='bold')
        ax.set_xlabel("Timeline", weight='bold')
        ax.plot(x_list, values, lw=2)
        # plt.xticks(fontsize=8)
        fig.savefig(f"{constant.AZURE_RPS_PLOT_DIR}/benchWorkloadRPS.pdf", bbox_inches='tight')
        print(f"The rps plot is saved in {constant.AZURE_RPS_PLOT_DIR}")
        return values

    def filter_df(self, app_map_dict, num_invos):
        df = self.df
        azure_apps = self.info['workflow_names']
        start = self.info['time_line_start']
        end = self.info['time_line_end']
        if "all" not in azure_apps:
            # 筛选出指定的 app
            print(f"Filtering apps: {azure_apps}")
            df = df[pd.Series(
                list(map(lambda x: '_'.join(app_map_dict[x].split("_")[:4]), df['app']))).isin(azure_apps)]
            if df['app'].nunique() != len(azure_apps):
                raise ValueError(
                    "The number of apps before and after filtering is not equal")
        else:
            logging.info("You are using full workflow benchmark")

        # 筛选出指定的 time-line
        print(f"Filtering data from {start} to {end}")
        filter_df = df[(df['invo_ts'] >= start) &
                       (df['invo_ts'] <= end)].copy()

        # 调整invo_ts的偏移量，从0开始
        filter_df['invo_ts'] = pd.to_datetime(filter_df['invo_ts'], utc=True)
        filter_df['invo_ts'] = filter_df['invo_ts'] - \
            pd.to_datetime(start, utc=True)

        # Picks top $(num_invos) of the filter_df for benchmarking
        if num_invos:
            filter_df = filter_df[:num_invos]
        print(
            f"We have {filter_df['app'].nunique()} of unique apps, {filter_df['func'].nunique()} of unique functions, and {filter_df['invo_ts'].count()} of invocations")
        return self.assign_input_values(filter_df)
