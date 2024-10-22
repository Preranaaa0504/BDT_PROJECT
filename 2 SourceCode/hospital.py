from pymongo import MongoClient # type: ignore

# Establish a connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['PROJECT']

# Define collections for each project
collections = {
    'HeartProject': db['HeartProject'],
    'LungsProject': db['LungsProject'],
    'KidneyProject': db['KidneyProject'],
    'BrainProject': db['BrainProject'],
    'OrthoProject': db['OrthoProject'],
    'DiabetesProject': db['DiabetesProject']
}

def create_patient(collection_name, patient_data):
    """Inserts a new patient record into the specified collection."""
    collection = collections[collection_name]
    collection.insert_one(patient_data)
    print(f"Patient record inserted into {collection_name}: {patient_data}")

def update_patient(collection_name, patient_id, update_data):
    """Updates an existing patient record in the specified collection."""
    collection = collections[collection_name]
    result = collection.update_one({'_id': patient_id}, {'$set': update_data})
    if result.modified_count > 0:
        print(f"Patient with ID {patient_id} updated in {collection_name}.")
    else:
        print(f"No changes made or patient with ID {patient_id} not found in {collection_name}.")

def delete_patient(patient_id):
    """Deletes a patient record from all collections based on PatientID."""
    deleted = False
    
    for collection_name in collections:
        collection = collections[collection_name]
        result = collection.delete_one({'_id': patient_id})  # Assuming PatientID is stored in the '_id' field
        if result.deleted_count > 0:
            deleted = True
            print(f"Patient with PatientID {patient_id} deleted from {collection_name}.")
    
    if not deleted:
        print(f"Patient with PatientID {patient_id} not found in any collection.")


def search_patient(patient_id):
    """Searches for a patient record in all collections using PatientID."""
    results = []
    
    for collection_name in collections:
        collection = collections[collection_name]
        patient = collection.find_one({'PatientID': patient_id})  # Search by PatientID (string)
        if patient:
            results.append({collection_name: patient})
    
    if results:
        print(f"Patient found: {results}")
        return results
    else:
        print(f"Patient with PatientID {patient_id} not found in any collection.")
        return None

