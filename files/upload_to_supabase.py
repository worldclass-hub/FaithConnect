import os
from .supabase_client import supabase

def upload_file_to_supabase(file_path, storage_folder="user-uploads"):
    file_name = os.path.basename(file_path)

    try:
        print(f"🎯 File selected: {file_name}")
        print(f"🎯 Uploading: {file_name}")

        # Read file from local path
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Upload to Supabase with inline preview enabled
        response = supabase.storage.from_(storage_folder).upload(
            file_name,
            file_data,
            {
                "content-type": "application/octet-stream",
                "x-upsert": "true",  # optional, avoids duplicate errors
                "content-disposition": "inline"  # ✅ allow browser preview
            }
        )

        # Get public URL
        public_url = supabase.storage.from_(storage_folder).get_public_url(file_name)
        print("✅ Supabase URL:", public_url)
        return public_url

    except Exception as e:
        print("❌ Error uploading file:", e)
        return None
