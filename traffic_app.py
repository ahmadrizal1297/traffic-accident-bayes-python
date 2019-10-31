from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
import json

# DATASET
light = []
status = []
stname  = []
surface = []
weather = []

# read file training traffic
with open('resources/data_training.json', 'r') as myfile:
    bigData=myfile.read()
# parse file
obj = json.loads(bigData)
# Assign dataset
for rawData in obj:
    light.append(int(rawData["light"]))
    status.append(int(rawData["status"]))
    stname.append(rawData["stname"])
    surface.append(int(rawData["surface"]))
    weather.append(int(rawData["weather"]))


# creating labelEncoder
le = preprocessing.LabelEncoder()

# Converting string labels into numbers.
stname_encoded = le.fit_transform(stname)
le_stname_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

weather_encoded = le.fit_transform(weather)
le_weather_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

status_encoded = le.fit_transform(status)
le_status_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

light_encoded = le.fit_transform(light)
le_light_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

surface_encoded = le.fit_transform(surface)
le_surface_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

#print ("Street:",stname_encoded)
#print ("Weather:",weather_encoded)
#print ("Light:",light_encoded)
#print ("Surface:",surface_encoded)
#print ("Status:",status_encoded)


# RESULT
i=0
for data in obj:
	#print i+1,".", data["stname"] ,"\t",  data["weather"] ,"\t",  data["light"] ,"\t",  data["status"]

	i+=1
	if i >= 5 : break


features=zip(weather_encoded,surface_encoded)

# Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets
model.fit(features, status_encoded)

#WEATHER {0 = CLEAR, 1 = CLOUDY, 2 = RAIN}
#STATUS  {0 = HIT, 1 = INJURY, 2 = FATAL}
#LIGHT  {0 = DAY, 1 = UNKNOWN, 2 = DARK}

with open('resources/data_traffic_baton.json', 'r') as myfile2:
    bigData2=myfile2.read()
# parse file
obj2 = json.loads(bigData2)

# Sort JSON file as object
obj2sorted = sorted(obj2, key = lambda i: i['CRASH'], reverse=True)

# TABLE TITLE 
print "\n\t\t\t5 TOP STREET TRAFFIC CRASH BATON"
print "\n================================================================================================="
print "STREET NAME" ,"\t", "CRASH" ,"\t", "HIT" ,"\t","PRIOH" ,"\t\t", "FATAL" ,"\t","PRIOF" ,"\t\t","REASON","\t\t","PRIOR" 
print "=================================================================================================\n"
# RESULT

i=0
for so in obj2sorted:


	totalrow=0
	reason=""
	prior=0.0
	# WEATHER PRIO
	wclear=0
	wcloud=0
	wrainy=0

	# LIGHT PRIO
	lday=0
	lunk=0
	ldark=0

	# SURFACE PRIO
	sdry=0
	swet=0

	obj = json.loads(bigData)
	# Assign dataset
	for rawData in obj:

		if rawData["stname"] == so["STNAME"] :
			
			# ROW COUNT
			totalrow+=1

			cweather 	= int(rawData["weather"])
			clight		= int(rawData["light"])
			csurface	= int(rawData["surface"])

			# WEATHER PRIO COUNT
			if cweather==0 : wclear+=1
			elif cweather==1 : wcloud+=1
			elif cweather==2 : wrainy+=1
			
			# LIGHT PRIO COUNT
			if clight==0 : lday+=1
			elif clight==1 : lunk+=1
			elif clight==2 : ldark+=1

			# SURFACE PRIO COUNT
			if csurface==0 : sdry+=1
			elif csurface==1 : swet+=1

	# STATUS
	rweather 	= 0
	rlight		= 0
	rsurface	= 0

	# PRIO CALCULATION
	pwclear = float(wclear) / float(totalrow)
	pwcloud = float(wcloud) / float(totalrow)
	pwrainy = float(wrainy) / float(totalrow)

	#print pwclear, pwcloud, pwrainy
	if pwrainy > pwcloud and pwrainy > pwclear : rweather = 1
	
	plday 	= float(lday) / float(totalrow)
	plunk	= float(lunk) / float(totalrow)
	pldark	= float(ldark) / float(totalrow)
	if pldark > plday and pldark > plunk : rlight = 1

	
	psdry	= float(sdry) / float(totalrow)
	pswet	= float(swet) / float(totalrow)
	if pswet > psdry : rsurface = 1
	
	if rweather == 1 and rlight == 1 and rsurface == 1 : 
		reason = "Slippery and Dark road" 
		prior = pldark+pswet+pwrainy
	elif rweather == 1 and rlight == 0 and rsurface == 1 : 
		reason = "Slippery road" 
		prior = pwrainy+pswet
	elif rweather == 0 and rlight == 0 and rsurface == 1 : 
		reason = "Slippery road" 
		prior = pswet
	elif rweather == 1 and rlight == 0 and rsurface == 0 : 
		reason = "Slippery road" 
		prior = pwrainy
	elif rweather == 0 and rlight == 1 and rsurface == 0 : 
		reason = "Dark road" 
		prior = pldark
	elif rweather == 0 and rlight == 0 and rsurface == 0 : 
		reason = "Accident" 
		prior = so["OVERCAST"]
	
	
	#print "\n", totalrow, wclear, wcloud, wrainy, "\t", lday, lunk, ldark, "\t", sdry, swet, "\t", rweather, rlight, rsurface

	print i+1, so["STNAME"] ,"\t",  so["CRASH"] ,"\t",  so["HIT"] ,"\t",  so["PRIOHIT"] ,"%\t",  so["FATAL"] ,"\t",  so["PRIOFATAL"] , "%" , "\t", reason, "\t", round(float(prior),3),"%\n"

	i+=1
	if i >= 5 : break

"""
	REASON			WEATHER		LIGHT		SURFACE
	bad weather		1			0			0
	dark road		0			1			0
	slippery road	0			0			1
	accident		0			0			0
"""