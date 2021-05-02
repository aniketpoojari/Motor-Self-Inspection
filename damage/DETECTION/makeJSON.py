import json
import os

def jsonmaker(c,centroid,dimen,label,score, claim):
        address = "static/JSON/data_" + str(claim) + ".txt"
        # address = os.getcwd() + "\\" + str(claim) + ".txt"
        file = open(address,'a')
        if os.stat(address).st_size == 0:
                data = {}
                data["damage"] = "1"
                data["details"] = []
                data["details"].append({
                        "front":[],
                        "left":[],
                        "back":[],
                        "right":[]
                })
                json.dump(data,file)
        file.close()
        if c == 0:
                if(centroid[1] <= (0.35*dimen[1])):
                        location = "windsheild"
                else:
                        location = "bonet"
                with open(address) as f:
                        config = json.loads(f.read())
                        config["details"][0]["front"].append({
                                "label":label,
                                "score":str(score),
                                "location":location
                        })
                        f.close()
                with open(address, "w") as f:
                        json.dump(config,f)
                        f.close()
        elif c == 1:
                if (centroid[0]<=(0.25*dimen[0]) and centroid[1]>=(0.35*dimen[1])):
                        location = "bonet"
                elif (centroid[0]>(0.25*dimen[0]) and centroid[0]<=(0.5*dimen[0])) and (centroid[1]<=(0.35*dimen[1])):
                        location = "front door glass"
                elif (centroid[0]>(0.25*dimen[0]) and centroid[0]<=(0.5*dimen[0])) and (centroid[1]>(0.35*dimen[1])):
                        location = "front door"
                elif (centroid[0]>(0.5*dimen[0]) and centroid[0]<=(0.75*dimen[0])) and (centroid[1]<=(0.35*dimen[1])):
                        location = "back door glass"
                elif (centroid[0]>(0.5*dimen[0]) and centroid[0]<=(0.75*dimen[0])) and (centroid[1]>(0.35*dimen[1])):
                        location = "back door"
                elif (centroid[0]>(0.75*dimen[0]) and centroid[1]>(0.30*dimen[1])):
                        location = "backside"
                else:
                        location = "none"
                with open(address) as f:
                        config = json.loads(f.read())
                        config["details"][0]["left"].append({
                                "label":label,
                                "score":str(score),
                                "location":location
                        })
                        f.close()
                with open(address, "w") as f:
                        json.dump(config,f)
                        f.close()
                #print(config["details"][0]['front']);
        elif c == 2:
                if(centroid[1] <= (0.35*dimen[1])):
                        location = "backside glass"
                else:
                        location = "backside dicky/bumper"
                with open(address) as f:
                        config = json.loads(f.read())
                        config["details"][0]["back"].append({
                                "label":label,
                                "score":str(score),
                                "location":location
                        })
                        f.close()
                with open(address, "w") as f:
                        json.dump(config,f)
                        f.close()
        elif c == 3:
                if (centroid[0]<=(0.25*dimen[0]) and centroid[1]>=(0.35*dimen[1])):
                        location = "backside"
                elif (centroid[0]>(0.25*dimen[0]) and centroid[0]<=(0.5*dimen[0])) and (centroid[1]<=(0.35*dimen[1])):
                        location = "back door"
                elif (centroid[0]>(0.25*dimen[0]) and centroid[0]<=(0.5*dimen[0])) and (centroid[1]>(0.35*dimen[1])):
                        location = "back door glass"
                elif (centroid[0]>(0.5*dimen[0]) and centroid[0]<=(0.75*dimen[0])) and (centroid[1]<=(0.35*dimen[1])):
                        location = "front door"
                elif (centroid[0]>(0.5*dimen[0]) and centroid[0]<=(0.75*dimen[0])) and (centroid[1]>(0.35*dimen[1])):
                        location = "front door glass"
                elif (centroid[0]>(0.75*dimen[0]) and centroid[1]>(0.30*dimen[1])):
                        location = "bonet"
                else:
                        location = "none"
                with open(address) as f:
                        config = json.loads(f.read())
                        config["details"][0]["right"].append({
                                "label":label,
                                "score":str(score),
                                "location":location
                        })
                        f.close()
                with open(address, "w") as f:
                        json.dump(config,f)
                        f.close()

