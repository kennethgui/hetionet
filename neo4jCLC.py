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

graph = Graph("bolt://localhost:7690", auth=("neo4j", "password")) 

def get_existing_treatment_info(disease_id):
    query = f"""
    MATCH (d:Disease {{id: '{disease_id}'}})
    MATCH (d)-[:DaG]->(g:Gene)  // Disease associates with Gene
    MATCH (a:Anatomy)<-[:DlA]-(d)  // Anatomy localizes Disease
    MATCH (c:Compound)-[:CtD|CpD]->(d)  //treat or palliate this disease
    RETURN d.name AS disease_name, 
           COLLECT(DISTINCT c.name) AS drugs, 
           COLLECT(DISTINCT g.name) AS gene_names, 
           COLLECT(DISTINCT a.name) AS locations
    """

    result = graph.run(query)
    return result.data()

def get_new_treatment_compounds(disease_id):
    query = f"""
    MATCH (d:Disease {{id: '{disease_id}'}})
    MATCH (d)-[:DlA]->(a:Anatomy)  // Disease is localized in anatomy
    MATCH (a)-[:AuG]->(g:Gene)  // Anatomy up-regulates a gene
    MATCH (c:Compound)-[:CdG]->(g)  // Compound down-regulates/up-regulates the gene
    WHERE NOT (c)-[:CtD]->(d) AND NOT (c)-[:CpD]->(d)  // Compound doesn't already treat/palliate the disease
    RETURN COLLECT(DISTINCT c.name) AS new_treatment_compounds
    """
    
    result = graph.run(query)
    return result.data()

def main():
    print("Welcome to the Hetionet, a heterogeneous information network (HETNET) for biomedical information.")
    
    while True:
        disease_id = input("Enter Disease ID (or type 'exit' to quit): ")
        if disease_id.lower() == 'exit':
            break
        
        queryOption = input("(1) Get existing disease info \n (2) Get new treatment compounds \n\n Please selection an option: ")
        # Query 1: Gets existing treatment info
        if queryOption == "1":
            existing_info = get_existing_treatment_info(disease_id)
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
        
        # Query 2: Gets new treatment compounds
        if queryOption == "2":
            new_treatments = get_new_treatment_compounds(disease_id)
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
