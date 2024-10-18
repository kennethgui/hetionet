from py2neo import Graph

def PrintAcsiiArt():
    acsiiArt = r"""
  ___ ___          __  .__                      __   
 /   |   \   _____/  |_|__| ____   ____   _____/  |_ 
/    ~    \_/ __ \   __\  |/  _ \ /    \_/ __ \   __\
\    Y    /\  ___/|  | |  (  <_> )   |  \  ___/|  |  
 \___|_  /  \___  >__| |__|\____/|___|  /\___  >__|  
       \/       \/                    \/     \/      
    """
    print(acsiiArt)

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7690", auth=("neo4j", "password"))

def format_disease_id(user_input_):
    print("\nEntered:", user_input_)
    
    if (user_input_[14:].isnumeric() and 
        user_input_[0:7].isalpha() and  
        user_input_[9:13].isalpha()):
        
        formatted_input = (user_input_[0].upper() +  
                           user_input_[1:7].lower() + "::" + 
                           user_input_[9:13].upper() + ":" + 
                           user_input_[14:])
        print("Formatted:", formatted_input)
        return formatted_input
    else:
        retry_input = input("\nEnter a valid disease ID in the format 'Disease::[A-Za-z]:[0-9]': ")
        return format_disease_id(retry_input)

def getExistingTreatmentInfo(disease_id):
    query = f"""
    MATCH (d:Disease {{id: '{disease_id}'}})
    MATCH (d)-[:DaG]->(g:Gene)
    MATCH (a:Anatomy)<-[:DlA]-(d)
    MATCH (c:Compound)-[:CtD|CpD]->(d)
    RETURN d.name AS disease_name, 
           COLLECT(DISTINCT c.name) AS drugs, 
           COLLECT(DISTINCT g.name) AS gene_names, 
           COLLECT(DISTINCT a.name) AS locations
    """

    result = graph.run(query)
    return result.data()

def getNewTreatmentCompounds(disease_id):
    query = f"""
    MATCH (d:Disease {{id: '{disease_id}'}})
    MATCH (d)-[:DlA]->(a:Anatomy)
    MATCH (a)-[:AuG]->(g:Gene)
    MATCH (c:Compound)-[:CdG]->(g)
    WHERE NOT (c)-[:CtD]->(d) AND NOT (c)-[:CpD]->(d)
    RETURN COLLECT(DISTINCT c.name) AS new_treatment_compounds
    """
    
    result = graph.run(query)
    return result.data()

def main():
    print("Welcome to the Hetionet, a heterogeneous information network (HETNET) for biomedical information.")
    
    while True:
        user_input = input("\nEnter Disease ID (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        disease_id = format_disease_id(user_input)
        
        queryOption = input("\n\n(1) Get existing disease info \n (2) Get new treatment compounds \n\n Please select an option: ")
        
        if queryOption == "1":
            existing_info = getExistingTreatmentInfo(disease_id)
            if existing_info:
                info = existing_info[0]
                print("\nDisease Name:", info['disease_name'])
                print("\nCompound count:", len(info['drugs']))
                print("Compound:\n", info['drugs'])
                print("\nGene count", len(info['gene_names']))
                print("Gene Names:\n", info['gene_names'])
                print("\nLocations known:", len(info['locations']))
                print("Locations:\n", info['locations'])
            else:
                print("No existing treatments found for the disease ID.")
        
        if queryOption == "2":
            new_treatments = getNewTreatmentCompounds(disease_id)
            if new_treatments and new_treatments[0]['new_treatment_compounds']:
                new_drugs = new_treatments[0]['new_treatment_compounds']
                print("\nNew Compound count:", len(new_drugs))
                print("\nNew Treatment Compounds:\n", new_drugs)
            else:
                print("No new treatment compounds found for the disease ID.")
            
        print() 

if __name__ == "__main__":
    PrintAcsiiArt()
    main()
