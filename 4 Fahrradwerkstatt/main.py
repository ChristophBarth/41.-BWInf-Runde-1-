import pandas as pd
import matplotlib.pyplot as plt


#Parameter

MINUTES_PER_DAY = 1440
OPENING_TIME = 540 #in Minuten
CLOSING_TIME = 1020 #in Minuten
OPENING_HOURS = range(OPENING_TIME, CLOSING_TIME)

METRIC = "delay" #auszuwertende Spalte des Dataframes (anderer geeigneter Wert: "relative_delay")

#Statistisch asuwertende Methoden

def plot_hist(df1, df2, df3):

    plt.hist(df1[METRIC], bins=50, color='c', edgecolor='k', range=[0, max([df1[METRIC].max(), df2[METRIC].max(), df3[METRIC].max()])])
    plt.axvline(df1[METRIC].mean(), color = 'k', linestyle='dashed')

    plt.show()

def evaluate_df(df):
    print(df[METRIC].describe())
    #print(df['delay'].mean(), df['relative_delay'].mean())

#Hilfsmethoden

#Erzeugung der Daten
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

def get_priority(begin, recieved, duration):
    p = (begin-recieved)/duration
    return round(p*100000, 0)

#Simulationen

#FIFO
def simulate_method1(df):

    for i in range(len(df)): #für jeden Auftrag

        df['begin'][i] = get_valid_begin(df['begin'][i]) #Beginn innerhalb der Arbeitszeiten verschieben
        df['completed'][i] = get_completion_time(df['begin'][i], df['duration'][i]) #Zeitpunkt der Fertigstellung berechnen

        if(i < len(df)-1): #Wenn auf diesen Auftrag noch Auträge folgen
            if(df['completed'][i] > df['recieved'][i+1]): #Wenn während der Bearbeitung des aktuellen Auftrags bereits der nächste eintrifft
                df['begin'][i+1] = df['completed'][i] #Verschieben des Arbeitsbeginns am nächsten Auftrag auf das Ende des aktuellen Auftrages

    df['delay'] = df['completed']-df['recieved'] #Wartezeit berechnen
    df['relative_delay'] = df['delay']/df['duration'] #relative Wartezeit berechnen

    evaluate_df(df) #statistische Auswertung der Ergebnisse
    return df

#Priorisierung von kurzen Aufträgen
def simulate_method2(df):
    for i in range(len(df)): #für jeden Auftrag

        df['begin'][i] = get_valid_begin(df['begin'][i]) #Beginn innerhalb der Arbeitszeiten verschieben
        df['completed'][i] = get_completion_time(df['begin'][i], df['duration'][i]) #Zeitpunkt der Fertigstellung berechnen

        counter = 1 #Zählvariable, wie viele neue Aufträge währen der Bearbeitung des aktuellen Auftrags eingehen
        while(i+counter < len(df) and (df['completed'][i] > df['recieved'][i+counter])):
            df['begin'][i+counter] = df['completed'][i]
            counter+=1

        df[i+1: i + counter] = df[i+1: i + counter].sort_values(by='duration') #Sortierung der neu eingegangenen Aufträge nach ihrer Dauer

    df['delay'] = df['completed']-df['recieved'] #Wartezeit berechnen
    df['relative_delay'] = df['delay']/df['duration'] #reöative Wartezeit berechnen

    evaluate_df(df) #statistische Auswertung
    return df

#neuer Algorithmus
def simulate_method3(df):
    df['priority'] = 0

    for i in range(len(df)): #für jeden Auftrag

        df['begin'][i] = get_valid_begin(df['begin'][i]) #Beginn innheralb der Arbeitszeiten verschieben
        df['completed'][i] = get_completion_time(df['begin'][i], df['duration'][i]) #Zeitpunkt der Fertigstellung berechnen

        counter = 1 #Zählvariable für die, währen der Bearbeitung des aktuellen Auftrags eingegangenen Aufträge
        while(i+counter < len(df) and (df['completed'][i] > df['recieved'][i+counter])):
            df['begin'][i+counter] = df['completed'][i]
            df['priority'][i+counter] = get_priority(df['begin'][i+counter], df['recieved'][i+counter], df['duration'][i+counter]) #Berechnung der Priorität der neuen Aufträge
            counter+=1

        df[i+1: i + counter] = df[i+1: i + counter].sort_values(by='priority', ascending=False) #Sortieren der neuen Aufträge nach Priorität

    df['delay'] = df['completed']-df['recieved'] #Berechnung Wartezeit
    df['relative_delay'] = df['delay']/df['duration'] #Berechnung relative Wartezeit

    evaluate_df(df) #statistische Auswertung
    return df


def run():
    df = get_df('0')

    #Erzeugen der Datensätze

    df1 = simulate_method1(df.copy()) #FIFO
    df2 = simulate_method2(df.copy()) #Priorisierung von kurzen Aufträgen
    df3 = simulate_method3(df.copy()) #neuer Algorithmus

    plot_hist(df1, df2, df3) #Histogramm mit Durchscnitt plotten, standardmäßig Verfahren 1 -> muss in plot_hist() Methode angepasst werden

if(__name__ == "__main__"):
        run()