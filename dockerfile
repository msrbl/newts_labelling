FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Замените значения на свои или передавайте через docker run -e
# ENV DRIVE_RAW_FOLDER_ID="your_drive_raw_folder_id"
# ENV DRIVE_PROCESSED_FOLDER_ID="your_drive_processed_folder_id"

CMD ["python", "-m", "src.main"]