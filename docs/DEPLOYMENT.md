# Azure Deployment Guide

## Prerequisites

- Azure subscription
- Azure CLI installed
- GitHub account with repository

## Setup Steps

### 1. Create Azure Resources

#### Create Resource Group
```bash
az group create --name student-ai-rg --location eastus
```

#### Create Storage Account
```bash
az storage account create \
  --resource-group student-ai-rg \
  --name studentaistorage \
  --location eastus \
  --sku Standard_LRS
```

#### Create Azure Functions App
```bash
az functionapp create \
  --resource-group student-ai-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name student-ai-functions
```

### 2. Configure Environment Variables

```bash
az functionapp config appsettings set \
  --name student-ai-functions \
  --resource-group student-ai-rg \
  --settings \
  OPENAI_API_KEY=your_api_key \
  AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string
```

### 3. Deploy to Azure

```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Login to Azure
az login

# Deploy
func azure functionapp publish student-ai-functions
```

### 4. Set Up GitHub Actions

Create `.github/workflows/deploy-azure.yml`:

```yaml
name: Deploy to Azure Functions

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Deploy to Azure
      run: |
        npm install -g azure-functions-core-tools@4
        func azure functionapp publish student-ai-functions
      env:
        AZURE_CREDENTIALS: ${{ secrets.AZURE_CREDENTIALS }}
```

## API Endpoints

Once deployed:

```
POST /api/ask                    Ask tutoring question
POST /api/ask-pdf                Ask about PDFs
POST /api/upload-pdf             Upload solution book
POST /api/add-task               Create task
POST /api/schedule               Generate schedule
GET  /api/tasks                  List tasks
GET  /api/progress               Get statistics
GET  /api/health                 Health check
```

## Monitoring

View logs in Azure Portal:
1. Go to Function App
2. Click "Monitor" in left sidebar
3. View application insights and logs

## Scaling

Azure Functions automatically scales based on demand. Configure:
1. Go to Function App settings
2. Adjust Plan type (Consumption vs Premium)
3. Set max instances if needed