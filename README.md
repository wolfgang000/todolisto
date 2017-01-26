todolisto
===
Todolisto is a simple todolist app to experiment with various technologies, design patterns and frameworks 
such as clean architecture, google app engine, vue.js, for this reason this simple app is probably
very over-engineered and more complicate that your average todolist app.

Deployment
===

Google App Engine(GAE)
---
1. You need accound in GAE(if not go [here](https://appengine.google.com/)) and the GAE SDK installed(if not go [here](https://cloud.google.com/appengine/docs/python/download)).

2. Open a terminal in the repository folder 
```
sh setup_gae.sh
gcloud  app deploy app.yaml
```
You don't need to configure the Database since Todolisto use the [GAE Datastore](https://cloud.google.com/datastore/).

Nginx/Gunicorn
---
Coming soon
