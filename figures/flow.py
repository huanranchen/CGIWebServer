import graphviz

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

flowchart = graphviz.Digraph(format='png')

flowchart.node('Start', 'Start')
flowchart.node('MainServer', 'Main Server\n(Listen on Port)')
flowchart.node('AcceptConnection', 'Accept Connection (TCP)')
flowchart.node('AssignThread', 'Assign to Worker Thread\n(From Thread Pool)')
flowchart.node('HTTPRequestHandler', 'HTTP Request Handler')
flowchart.node('StaticContent', 'Static Content')
flowchart.node('DynamicContent', 'Dynamic Content (CGI)')
flowchart.node('GenerateResponse', 'Generate HTTP Response')
flowchart.node('SendResponse', 'Send Response to Client')
flowchart.node('LogRequest', 'Log Request and Response')
flowchart.node('End', 'End')

flowchart.edge('Start', 'MainServer')
flowchart.edge('MainServer', 'AcceptConnection')
flowchart.edge('AcceptConnection', 'AssignThread')
flowchart.edge('AssignThread', 'HTTPRequestHandler')
flowchart.edge('HTTPRequestHandler', 'StaticContent')
flowchart.edge('HTTPRequestHandler', 'DynamicContent')
flowchart.edge('StaticContent', 'GenerateResponse')
flowchart.edge('DynamicContent', 'GenerateResponse')
flowchart.edge('GenerateResponse', 'SendResponse')
flowchart.edge('SendResponse', 'LogRequest')
flowchart.edge('LogRequest', 'End')

flowchart.render('/mnt/data/web_server_flowchart')

img = mpimg.imread('/mnt/data/web_server_flowchart.png')
plt.imshow(img)
plt.axis('off')
plt.show()
