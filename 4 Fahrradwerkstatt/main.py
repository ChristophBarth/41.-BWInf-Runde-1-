import pandas as pd
import matplotlib.pyplot as plt

MINUTES_PER_DAY = 1440
OPENING_TIME = 540
CLOSING_TIME = 1020
OPENING_HOURS = range(OPENING_TIME, CLOSING_TIME)

def get_df(n):
    df = pd.read_csv(f'res/fahrradwerkstatt{n}.txt', header=None, sep=" ")
    df.columns = ["recieved", "duration"]
    df['begin'] = df['recieved']
    df['completed'] = 0
    df['delay'] = 0
    df['relative_delay'] = 0

    return df

def get_closing_time_of_day(t):
    return ((t//MINUTES_PER_DAY)*MINUTES_PER_DAY)+CLOSING_TIME

def get_opening_time_of_next_day(t):
    return (((t//MINUTES_PER_DAY)+1)*MINUTES_PER_DAY)+OPENING_TIME

def get_valid_begin(t):
    task_time = t%MINUTES_PER_DAY
    if(task_time in OPENING_HOURS):return t
    else:
        if(task_time < OPENING_TIME):return t + (OPENING_TIME - task_time)
        elif(task_time >= CLOSING_TIME):return get_opening_time_of_next_day(t)

def get_time_til_closing(t):
    return get_closing_time_of_day(t)-t

def get_completion_time(begin, time_remaining):
    projected_completion = begin + time_remaining
    if(not projected_completion > get_closing_time_of_day(begin)):
        return projected_completion
    else:
        time_remaining = time_remaining-get_time_til_closing(begin)
        begin = get_opening_time_of_next_day(begin)
        return get_completion_time(begin, time_remaining)

def evaluate_df(df):
    metric = 'relative_delay'
    print(df[metric].describe())

def plot_hist(df1, df2):
    fig, axes = plt.subplots(1, 2)
    df1['relative_delay'].hist(bins=100, ax=axes[0])
    df2['relative_delay'].hist(bins=100, ax=axes[1])
    plt.show()

def simulate_method1(df):

    for i in range(len(df)):
        df['begin'][i] = get_valid_begin(df['begin'][i])
        df['completed'][i] = get_completion_time(df['begin'][i], df['duration'][i])

        if(i < len(df)-1):
            if(df['completed'][i] > df['recieved'][i+1]):
                df['begin'][i+1] = df['completed'][i]

    df['delay'] = df['completed']-df['recieved']
    df['relative_delay'] = df['delay']/df['duration']
    evaluate_df(df)
    return df

def simulate_method2(df):
    for i in range(len(df)):

        df['begin'][i] = get_valid_begin(df['begin'][i])
        df['completed'][i] = get_completion_time(df['begin'][i], df['duration'][i])

        counter = 1
        while(i+counter < len(df) and (df['completed'][i] > df['recieved'][i+counter])):
            df['begin'][i+counter] = df['completed'][i]
            counter+=1

        df[i+1: i + counter] = df[i+1: i + counter].sort_values(by='duration')

    df['delay'] = df['completed']-df['recieved']
    df['relative_delay'] = df['delay']/df['duration']
    evaluate_df(df)
    return df

df = get_df(4)
df1 = simulate_method1(df.copy())
df2 = simulate_method2(df.copy())

plot_hist(df1, df2)