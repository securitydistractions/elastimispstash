# elastimispstash - ElasticSearch enrichment via MISP
![alt text](https://www.securitydistractions.com/wp-content/uploads/2019/03/image-1024x547.png)

The original enrichment between Elastic and MISP that we created can be found documented on the following blog post:
https://www.securitydistractions.com/2019/05/17/enriching-elasticsearch-with-threat-data-part-1-misp/

However this has now been changed slightly, the original enrichment had issues:

1. Handling tags that were assigned to an attribute but also to an event. It was not possible to add the event tags into memcached.
2. There was also no logstash parsing to handle the string that memcached returned.

This new version will handle all of this, to explain how the new concept works we will use an example with the domain "bbc.com".

1. The python script retrieves all domain indicators from MISP, and places them into memcached.
2. Logstash takes the domain "bbc.com", and looks up this value against the memcached filter plugin. If it gets a hit it will move to step 3, else it will write "none" to misp.hit.
3. "bbc.com" was known via MISP in memcached, so logstash moves to the next filter. This is the ruby filter plugin, this filter does a lookup against MISP itself, dynamically substituting "bbc.com" into the lookup.
4. MISP returns the response, and the ruby filter strips out the information it needs and then writes this to the logstash event.
5. Logstash writes the event to elasticsearch.

# Yeah thats great but how the hell do I get it working?!
In order to get this enrichment running you can follow these steps:

1. Setup the python script to run every minute.
2. Copy the memcached filter plugin and ruby filter plug scripts to your logstash configuration.



