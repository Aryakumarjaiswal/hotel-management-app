import pandas as pd
import json
import chromadb
df = pd.read_csv(r'Hotel_Management_App\units_info.csv')  
def parse_notes(note):
    try:
        parsed = json.loads(note)  # Parse JSON safely
        return parsed
    except json.JSONDecodeError:
        return {}
df['parsed_notes'] = df['notes'].apply(parse_notes)


expanded_columns = pd.json_normalize(df['parsed_notes'])


df = pd.concat([df, expanded_columns], axis=1)


df = df.drop(columns=['parsed_notes'])
df.drop(['task_room_image', 'task_image', 'pms_id', 'updated_at', 'created_at', 'status', 'images', 'main_image', 'images_same_as_unittype', 'address_same_as_property', 'owner_id', 'organization_id', 'property_id', 'unit_type_id' ,'unit_code', 'description'], axis=1, inplace=True)
df['full_address'] = df['unit_name'] + ', ' + df['address'] + ', Country code: ' + df['country_code'].astype(str) + ', Province: ' + df['province'] + ', City: ' + df['city'] + ', Zip Code: ' + df['zip_code'].astype(str) + ', Latitude: ' + df['latitude'].astype(str) + ', Longitude: ' + df['longitude'].astype(str) + ', Unit Condition: ' + df['unit_condition']
df.drop(['unit_name', 'address', 'country_code', 'province', 'city', 'zip_code', 'latitude', 'longitude'], axis=1, inplace=True)
df.drop(['unit_group_sequence', 'notes', 'unit_condition', 'dateRanges'], axis=1, inplace=True)
concatenated_strings = df.astype(str).agg('\n\n'.join, axis=1)
lengths = concatenated_strings.str.len()
average_length = lengths.mean()
min_length = lengths.min()
max_length = lengths.max()
df['combined_info'] = df.apply(lambda row: '\n'.join([f"{col}: {row[col]}" for col in df.columns]), axis=1)
df['id'] = df['id'].astype(str)

client = chromadb.PersistentClient(path='UNITS_INFO_CHUNCK')

# Function to chunk text
def chunk_text(text, chunk_size=100):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


# Process and store in ChromaDB
for idx, row in df.iterrows():
    doc_id = str(row['id'])
    combined_info = row['combined_info']
    
    # Create a collection for each ID
    collection = client.get_or_create_collection(
        name=f"collection_{doc_id}",
        metadata={"id": doc_id},
    )
    
    # Chunk the text and store in ChromaDB
    chunks = chunk_text(combined_info)
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[{"chunk_index": i}],
            ids=[f"{doc_id}_{i}"]
        )

print("Data successfully stored in ChromaDB.")
