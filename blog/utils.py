import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.read()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_bar(x,y,title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(3,3))
    plt.title('The graph by '+title)
    #plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.bar(x,y,color='pink')
    plt.xlabel(title.lower())
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_pie(x,y,title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(3,3))
    plt.title('The graph by '+title)
    #plt.plot(x,y)
    plt.pie(y,labels=x)
    plt.xlabel(title.lower())
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_plot(x,y,title,x_figsize=5,y_figsize=3):
    plt.switch_backend('AGG')
    plt.figure(figsize=(x_figsize,y_figsize))
    plt.title('The graph by '+title)
    #plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.plot(x,y,color='purple')
    plt.xlabel(title.lower())
    plt.tight_layout()
    graph = get_graph()
    return graph
