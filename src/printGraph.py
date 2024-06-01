
from numpy import positive
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

def reformat(listA):
	
	temp_main = {}
	for i in range (5):
		items = dict(listA[i])
		
		key = items.get("country")
		positiveList = items.get("positiveWord")
		negativeList = items.get("negativeWord")
		stopList = items.get("stopWord")
		neutralList = items.get("neutralWord")
		article = []
		

		for j in range (5):
			temp_dict = {}
			article_idx = j+1
			
			temp_dict.update([("article", article_idx), ("positiveWord", positiveList[j]),
			("negativeWord", negativeList[j]), ("stopWord", stopList[j]), ("neutralWord", neutralList[j])])
			article.append(temp_dict)
			
		
		temp_main.update([(key, article)])
	return temp_main
		

def PrintSummarygraph (resultbyArticle):
	
	data_set = reformat(resultbyArticle)
	for country, value in data_set.items():
		df = pd.DataFrame(value,index=[1,2,3,4,5])
		fig = go.Figure(data=[
			go.Bar(name="positiveWords", x=[1,2,3,4,5], y=df["positiveWord"], text=df["positiveWord"], textposition="outside"),
			go.Bar(name="negativeWords", x=[1,2,3,4,5], y=df["negativeWord"], text=df["negativeWord"], textposition="outside"),
			go.Bar(name="stopWords", x=[1,2,3,4,5], y=df["stopWord"], text=df["stopWord"], textposition="outside"),
			go.Bar(name="neutralWords", x=[1,2,3,4,5], y=df["neutralWord"], text=df["neutralWord"], textposition="outside")
		])
		fig.update_layout(title=f"Word count for country {country}" )
		fig.show()  
	

def Printgraph(result):
	country_name = ["" for i in range (len(result))]
	for i in range (len(result)):
		country_name[i] = result[i].get("country")

	column_list = ["positiveWord","negativeWord", "stopWord", "neutralWord"]
	fig = make_subplots(rows=len(result), cols=1,subplot_titles=country_name, x_title= "Type of words", y_title="Number of words",)
	
	for i in range (len(result)):
		y_value = [result[i].get(j) for j in column_list ]
		
		fig.add_trace(
			go.Bar(name=result[i].get("country") ,x = column_list, y=y_value, text=y_value, textposition= "auto"),
			row=i+1, col=1
		)
	fig.update_layout(height=1000, width=600, title_text="Result by country")
	fig.show()

