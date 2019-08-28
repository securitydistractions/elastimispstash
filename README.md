# elastiMISPstash - ElasticSearch enrichment via MISP
![alt text](https://www.securitydistractions.com/wp-content/uploads/2019/03/image-1024x547.png)

The original enrichment between Elastic and MISP that we created can be found documented on the following blog post:
https://www.securitydistractions.com/2019/05/17/enriching-elasticsearch-with-threat-data-part-1-misp/

It is highly recommended to follow these blog posts before continuing with running ElastiMISPstash!

# elastiMISPstash - ElasticSearch enrichment via MISP
We have decided to finally release this project onto github properly with a proper name and everything, as it has begun to take the shape of something which the community is screaming for.

To explain how elastiMISPstash works we will use an example with the domain "bbc.com".

**1.** The python script retrieves all domain indicators from MISP, and places them into memcached.

**2.** Logstash takes the domain "bbc.com", and looks up this value against the memcached filter plugin. If it gets a hit it will move to step 3, else it will write "none" to misp.hit.

**3.** "bbc.com" was known via MISP in memcached, so logstash moves to the next filter. This is the ruby filter plugin, this filter does a lookup against MISP itself, dynamically substituting "bbc.com" into the lookup.

**4.** MISP returns the response, and the ruby filter strips out the information it needs and then writes this to the logstash event.

**5.** Logstash writes the event to elasticsearch.

***How does this is work technically? Glad you asked.....***

**1.** The python script calls the MISP API and retrieves all IoC's of the datatypes that ElastiMISPStash will support, this is then pushed into memcached which should be running locally on your logstash nodes if possible. The IoC's are placed into memcached with a TTL of 130 seconds.

**2.** Depending on the fields you choose to enrich, logstash will make lookups against the memcached application. If it does not get a hit, it will exit the memcached filter and skip the ruby filter writing out to elasticsearch that there was no MISP hit.

**3.** Lets say that there was a match against the memcached application, logstash will write out the tags on the MISP attribute retrieved. It will then enter the next filter, the ruby filter. This filter then makes a second call to the MISP API subsituting in the attribute that resulted in the hit into the API call. 

**4.** Retrieving the entire JSON response back into the ruby filter, the script then parses the results and tears out the info we have selected to write out to elasticsearch. In the example configuration, we have taken the tags for the attribute and the events that the attribute is known in. We also take the description field from each event and parse these too.

***How does it look in the end?***

Here is a screenshot from a recent example demonstration that we gave at our local OWASP chapter meetup. This is showing MISP enrichment working against the domain "c2.0wasp.dk".

![image](https://user-images.githubusercontent.com/46198611/63843840-59733080-c987-11e9-9e4c-be90c7e0bd21.png)


# Yeah thats great, enough talk! How the hell do I get it working?!
ElastiMISPstash currrently has support for ip, domain, md5, sha1 and sha256 datatypes.

In order to get this enrichment running you can follow these steps:

**1.** Modify the python script "misppull.py" to suit your needs, enter the network address of your MISP instance and supply your MISP API key where instructed. Set this script to run every minute...

**2.** Copy the memcached filter plugin and ruby filter plugin scripts into your logstash pipeline configuration. Ensure that the order is correct, the memcached filter must come first. Substitute in the field names you want to work with, in our attached example files we are working with destination.domain. We highly recommend to use ECS (elastic common schema) this way you can limit the amount of additional configuration you will need to do this enrichment.

**Caveat, as of right now you will need to add a ruby filter for each datatype you want to work with. This is planned to be corrected in later versions of ElastiMISPstash but this is just a cosmestic thing. It's effect on performance will be minimal.**



