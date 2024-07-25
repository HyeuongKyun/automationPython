import PyPDF2
import os

def check_trailer_in_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            # Try to access the trailer
            trailer = reader.trailer
            # print(f'trailer={trailer}')
            if trailer is not None:
                return True
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
    return False

def check_trailers_in_directory(directory_path):
    results = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            has_trailer = check_trailer_in_pdf(file_path)
            results[filename] = has_trailer
    return results

# 사용 예시
# report가 있는 경로
directory_path = r'C:\Users\김형균\Downloads\report'  
results = check_trailers_in_directory(directory_path)
# print(f'results={results}')

# 결과 출력 및 카운팅
trailer_exists_count = 0
no_trailer_count = 0

for filename, has_trailer in results.items():
    if has_trailer:
        trailer_exists_count += 1
        print(f"{filename}: Trailer exists")
    else:
        no_trailer_count += 1
        print(f"{filename}: No trailer")

print(f"\nTotal PDFs with trailer: {trailer_exists_count}")
print(f"Total PDFs without trailer: {no_trailer_count}")