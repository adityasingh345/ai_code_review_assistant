import zipfile
import io

ALLOWED_EXTENSIONS = (".py", ".js", ".ts", ".java")

def extract_code_files(zip_bytes):
    extracted_files = {}

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        for file_name in z.namelist():
            if file_name.endswith(ALLOWED_EXTENSIONS):
                with z.open(file_name) as f:
                    extracted_files[file_name] = f.read().decode("utf-8")

    return extracted_files
