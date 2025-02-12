# AWS Upload Tool

This Python script allows you to upload files from a local folder to an AWS S3 bucket. It supports dynamic configuration through a YAML file, making it flexible and easy to manage.

## 📦 Project Structure

```
AWS_Upload/
├── src/
│   └── aws_uploader.py
├── config/
│   └── config.yaml
├── logs/
├── requirements.txt
└── README.md
```

- ``: Main script responsible for uploading files to AWS S3.
- ``: Configuration file with AWS credentials and upload settings.
- ``: Folder where log files are automatically generated.
- ``: List of Python dependencies.
- ``: This file.

## ⚙️ Configuration

Create a `config.yaml` file inside the `config/` folder:

```yaml
aws_access_key_id: "YOUR_ACCESS_KEY_ID"
aws_secret_access_key: "YOUR_SECRET_ACCESS_KEY"
region_name: "us-west-2"
bucket_name: "your-s3-bucket-name"
local_folder: "D:\\Path\\To\\Local\\Folder"
s3_prefix: "optional/prefix/"
```

- ``: Your AWS access key.
- ``: Your AWS secret access key.
- ``: AWS region where your bucket is located.
- ``: Name of the S3 bucket.
- ``: Path to the local folder with files to upload.
- `` *(optional)*: Prefix to organize files within the S3 bucket.

## 🚀 Installation

1. **Clone or download the project.**
2. **Navigate to the project folder:**
   ```bash
   cd AWS_Upload
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📤 Usage

Run the script from the project directory:

```bash
python src/aws_uploader.py
```

## 📋 Logging

- Log files are saved in the `logs/` folder.
- Log format: `LOG_dd_mm_yyyy_hh_mm_ss.log`
- Logs include information about upload progress and any errors.

## ❗ Error Handling

- Errors during file uploads (e.g., invalid credentials, missing bucket) are logged both in the console and in the log file.
- General exceptions are also captured and logged for debugging.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## 📄 License

This project is licensed under the MIT License.

