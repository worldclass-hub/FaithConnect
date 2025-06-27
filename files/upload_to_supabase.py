import os
from .supabase_client import supabase

def upload_file_to_supabase(file_path, storage_folder="user-uploads"):
    file_name = os.path.basename(file_path)

    try:
        # Read the file content
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Upload to Supabase Storage
        response = supabase.storage.from_(storage_folder).upload(file_name, file_data, {
            "content-type": "application/octet-stream",
            "upsert": True
        })

        # Return public URL
        public_url = supabase.storage.from_(storage_folder).get_public_url(file_name)
        return public_url

    except Exception as e:
        print("Error uploading file:", e)
        return None
