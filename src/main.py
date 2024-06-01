from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import geodesic
from itertools import permutations
import plotly.graph_objects as go
import trie, textManager as text
from itertools import product
from statistics import mean
import printGraph as graph
import csvReader as csv
import numpy as np
import folium

#Functions for Problem 1

country = ["KR","MX","TR", "TH", "PH"]
positiveWordFile = "All articles_n_References\Positive_words.txt"
negativeWordFile = "All articles_n_References\\Negative_words.txt"
stopWordFile = "All articles_n_References\Stop_words.txt"

treePositive = trie.Trie()
treeNegative = trie.Trie()

result = [{"country": "null","positiveWord": 0, "negativeWord":0, "stopWord": 0, "neutralWord":0} for i  in range(len(country))]
resultbyArticle = []
sumOfPositive = [0 for i in range(len(country))]
sumOfNegative = [0 for i in range(len(country))]

def defineReference():
    positiveWord = text.readFile(positiveWordFile).lower().split(", ")
    negativeWord = text.readFile(negativeWordFile).lower().split(", ")
    global stopWord
    stopWord = text.readFile(stopWordFile).lower().split(", ")

    for word in positiveWord:
        treePositive.add(word)
    
    for word in negativeWord:
        treeNegative.add(word)

def printGraph():
    graph.Printgraph(result)
    graph.PrintSummarygraph(resultbyArticle)

######################################################################################
######################################################################################

#Functions for Problem 2

# Get shop name by using coordinate
def get_shop_name(state_arr, coord):

    for i in state_arr:
        if [i[15],i[16]] == [str(i) for i in coord]:
            return i[0]

#find the distribution center
def get_lowest_sum(lat_long_arr):

    list_of_distances = [geodesic(a, b).km for a, b in permutations(lat_long_arr, 2)]
    chunked_list = list()
    chunk_size = len(lat_long_arr) -1
    
    for i in range(0,len(list_of_distances),chunk_size):
        
        chunked_list.append(list_of_distances[i:i+chunk_size])

    sums =[]
    
    for i in chunked_list:
        
        sum = 0.0
        
        for j in i:
            
            sum = sum + j
        
        sums.append(sum)
    
    coordsindex = sums.index(min(sums))
    
    return lat_long_arr[coordsindex]

def create_data_model(lat_long_arr, lowest_sum):
    
    data = {}

    #calculate distance between stores
    list_of_distances = np.array([int(geodesic(a, b).km) for a, b in product(lat_long_arr, repeat = 2)])
    distance_matrix = list_of_distances.reshape(int(list_of_distances.size**0.5), int(list_of_distances.size**0.5))

    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 1
    data['starts'] = [lat_long_arr.index(lowest_sum)]
    data['ends'] = [lat_long_arr.index(lowest_sum)]
    
    return data

def distance_callback(from_index, to_index):
    
    #returns the distance between two locations
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)

    return data["distance_matrix"][from_node][to_node]

def print_solution(manager, routing, solution):

    #print total cost
    print("\nTotal distance travelled: {} km".format(solution.ObjectiveValue()))

    #print route taken
    index = routing.Start(0)
    plan_output = "Route taken: "

    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += " {} ->".format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    
    plan_output += " {}\n".format(manager.IndexToNode(index))
    print(plan_output)

def get_route(solution, routing, manager):

    #get vehicle route and store it in a one dimensional array 
    #how 'route' looks like: [0, 7, 2, 3, 4, 6, 8, 1, 5, 9, 0] 

    index = routing.Start(0)
    route = [manager.IndexToNode(index)]

    while not routing.IsEnd(index):
        
        index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))  
        
    return route

######################################################################################
######################################################################################

if __name__ =="__main__":

    #Problem 1

    print('\n##### PROBLEM 1 #####')

    defineReference()
    TotalWord = 0 # total of words
    TotalStopword = 0 #total of stop words
    sentiment_score_arr = [[0 for i in range(5)] for j in range(len(country))]

    for i in range (len(country)):
        print('*'*50)
        print("Calculating word count for country", country[i], "\n")
        temp = {
                "country": country[i],
                "article": [1,2,3,4,5],
                "positiveWord": [0,0,0,0,0],
                "negativeWord": [0,0,0,0,0],
                "stopWord":[0,0,0,0,0],
                "neutralWord":[0,0,0,0,0]
            }
        
        negativeCountList = []
        positiveCountList = []
        stopCountList = []
        neutralCountList = []

        for j in range (5):

            filePath = "All articles_n_References\\" + country[i] + "_Article_" + str(j+1) + ".txt"

            article = text.readFile(filePath).replace('\n', " ")      
            wordList = article.lower().split(" ")
            n = len(wordList) #total number of words
            cleanwordList = text.removeStopwords(wordList, stopWord)
            n_stopword = n - len(cleanwordList)

            positiveWordCount = 0
            negativeWordCount = 0
            
            print('Article', j+1)
            print('\nBefore cleaning -', len(wordList), 'words')
            print('After cleaning -', len(cleanwordList), 'words\n')
            
            for x in cleanwordList:
                if treePositive.searchIn(x):
                    positiveWordCount+=1
                elif treeNegative.searchIn(x):
                    negativeWordCount+=1
            
            print("Positive word count in article", j+1,":", positiveWordCount)
            print("Negative word count in article", j+1,":", negativeWordCount)
 
            sentiment_score = round((positiveWordCount-negativeWordCount)/(positiveWordCount+negativeWordCount), 3)
            sentiment_score_arr[i][j] = sentiment_score

            print("\nSentiment score:", sentiment_score)
            print(f'This article is giving {"positive" if positiveWordCount > negativeWordCount else "negative" if positiveWordCount < negativeWordCount else "neutral"} sentiment.')

            negativeCountList.append(negativeWordCount)
            positiveCountList.append(positiveWordCount)
            stopCountList.append(n_stopword)
            
            neutralCountList.append(n-negativeWordCount-positiveWordCount-n_stopword)

            sumOfPositive[i] += positiveWordCount
            sumOfNegative[i] += negativeWordCount

            TotalWord += n
            TotalStopword += n_stopword
            print()
            print('-'*50)

        temp.update([
            ("positiveWord",positiveCountList),
            ("negativeWord", negativeCountList),
            ("stopWord",stopCountList),
            ("neutralWord",neutralCountList)
        ])

        resultbyArticle.append(temp)
        TotalneutralWord = TotalWord - TotalStopword - sumOfNegative[i] - sumOfPositive[i]
        result[i].update({"country": country[i],"positiveWord": sumOfPositive[i], "negativeWord": sumOfNegative[i],"stopWord": TotalStopword, "neutralWord": TotalneutralWord})
        
        print("\nAverage sentiment score for",country[i] ,":", round(mean(sentiment_score_arr[i]), 2),"\n")
    
    printGraph()

    average_sentiment = [round(mean(i), 2) for i in sentiment_score_arr]
    
    sentiment_an = [[i, j] for i, j in zip(country, average_sentiment)]
    sentiment_an = sorted(sentiment_an, key=lambda x: x[1], reverse=True)

    print('Ranking from the most recommended countries to the least recommended countries to have an expansion (Sentiment Analysis): ')
    for i in range(len(sentiment_an)):
        print(i+1,'-',sentiment_an[i][0],'-',sentiment_an[i][1])

    fig = go.Figure(
            data=[go.Bar(x=country, y=[average_sentiment[0],
            average_sentiment[1],average_sentiment[2],
            average_sentiment[3],average_sentiment[4]])],
            layout=go.Layout(
                title=go.layout.Title(text="Average Sentiment of Countries")
            )
        )

    fig.show()
    
######################################################################################
######################################################################################

    #Problem 2

    print('\n##### PROBLEM 2 #####')

    country_distance = np.array([
        ["KR", 0],
        ["MX", 0],
        ["TR", 0],
        ["TH", 0],
        ["PH", 0]
    ])

    #setup map
    m = folium.Map(location=[0, 0], zoom_start=5)

    for x in country_distance:
        
        #print country
        print('\nCurrent country: ', x[0], '\n')

        #get coordinates of all stores in the country
        state_arr = csv.get_state_info(x[0])
        lat_long_arr = csv.get_lat_long(state_arr, m)

        #find the distribution center
        lowest_sum = get_lowest_sum(lat_long_arr)
        shop_name = get_shop_name(state_arr, lowest_sum)

        #display the distribution center
        print('Shop name \'', shop_name, '\' should be the distribution centre.', sep = "")
        print(shop_name, '\'s coordinates = ', lowest_sum, sep = "")

        #tag distribution centre on the map w/ red marking
        folium.Marker(location=lowest_sum, popup="{}. {}".format(lat_long_arr.index(lowest_sum), shop_name), icon=folium.Icon(color='red', icon='cloud')).add_to(m)

        #create the data model, the index manager and the routing model
        data = create_data_model(lat_long_arr, lowest_sum)
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['starts'], data['ends'])
        routing = pywrapcp.RoutingModel(manager)

        #returns distance between two points and registers it with the solver 
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        #define the cost of travel as the distance between two locations
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        #define default search parameters and the solution heuristic
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        #solve the problem
        solution = routing.SolveWithParameters(search_parameters)

        #print the solution
        if solution:
            print_solution(manager, routing, solution)
            x[1] = solution.ObjectiveValue()

        #add lines to the map to show path taken
        route = get_route(solution, routing, manager)
        for index in range(1, len(route)):
            folium.PolyLine(locations=[lat_long_arr[route[index]], lat_long_arr[route[index-1]]]).add_to(m)

    m.save("map.html")

######################################################################################
######################################################################################

    #Problem 3

    print('\n##### PROBLEM 3 #####')

    total_sentiment = sum(average_sentiment)
    total_distance = sum([int(x[1]) for x in country_distance])
    
    i = 0
    prob_country = []
    for x in country_distance:
        prob_score = round((average_sentiment[i]/total_sentiment), 2)
        prob_distance = round((int(x[1])/total_distance), 2)
        prob_country.append(round((prob_score*(1-prob_distance)), 2))
        i = i + 1

    result = [[i, j] for i, j in zip(country, prob_country)]
    result = sorted(result, key=lambda x: x[1], reverse=True)

    print('Ranking from the most recommended countries to the least recommended countries to have an expansion (Overall): ')
    for i in range(len(country)):
        print(i+1,'-',result[i][0],'-',result[i][1])
    
    fig_pro_three = go.Figure(
            data=[go.Bar(x=country, y=[prob_country[0],
            prob_country[1],prob_country[2],
            prob_country[3],prob_country[4]])],
            layout=go.Layout(
                title=go.layout.Title(text="The Probability of Countries to Have an Expansion")
            )
        )

    fig_pro_three.show()