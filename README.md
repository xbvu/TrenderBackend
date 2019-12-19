# TrenderBackend

TrenderBackend is the backend part of the Trender project. It features:

  - An ElasticSearch instance as search engine
  - Data input API working 24/7 and inserting data to a local database and ElasticSearch index
  - Powerful search API

## Structure of Trender

  - Frontent is available here [link](https://github.com/xbvu/Trender), it's the visible part of the project with which users interact.
  - Backend is available at this repository [link](https://github.com/xbvu/TrenderBackend), it's the invisible part of the project with which the frontend interacts.
 
*Frontend and backend in the conceptual design diagram:*
![](https://trello-attachments.s3.amazonaws.com/5dd3e8ffba67c3724351a245/661x1001/a988bcb4d1cf0be989ca0305d3504feb/backend.png) 
 
**Structure of TrenderBackend**

TrenderBackend can be divided into several most important parts:

  - Data input API. Most of the code for it is placed in [views.py](https://github.com/xbvu/TrenderBackend/blob/master/backend/trender/api/views.py)
  - ElasticSearch insertion API. Most of the code for it is placed in [elasticsearch.py](https://github.com/xbvu/TrenderBackend/blob/master/backend/trender/api/elasticsearch.py)
  - Search class. Most of the code for it is placed in [search.py](https://github.com/xbvu/TrenderBackend/blob/master/backend/trender/api/search.py)
  - Database implementation. Most of the code for it is placed in [models.py](https://github.com/xbvu/TrenderBackend/blob/master/backend/trender/api/models.py)
  
  
