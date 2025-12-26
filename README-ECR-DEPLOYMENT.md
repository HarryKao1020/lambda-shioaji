# Docker Image 部署到 AWS ECR 指南

本專案提供了將 Lambda 函數的 Docker Image 部署到 AWS ECR 的完整流程。

## 前置需求

1. **安裝 Docker**
   - macOS: 下載 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
   - 確認安裝: `docker --version`

2. **安裝 AWS CLI**
   ```bash
   # macOS
   brew install awscli

   # 確認安裝
   aws --version
   ```

3. **設定 AWS 憑證**
   ```bash
   aws configure
   ```
   需要輸入:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name (例如: ap-northeast-1)
   - Default output format (建議: json)

## 使用方法

### 方法一：使用自動化腳本（推薦）

1. **給予腳本執行權限**
   ```bash
   chmod +x deploy-to-ecr.sh
   ```

2. **執行部署腳本**
   ```bash
   # 使用預設設定 (region: ap-northeast-1, repository: lambda-shioaji)
   ./deploy-to-ecr.sh

   # 或指定 region 和 repository 名稱
   ./deploy-to-ecr.sh us-east-1 my-lambda-function

   # 指定特定的 tag
   ./deploy-to-ecr.sh ap-northeast-1 lambda-shioaji v1.0.0
   ```

3. **完成後，腳本會顯示 Image URI**，例如：
   ```
   123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/lambda-shioaji:latest
   ```

### 方法二：手動執行步驟

#### 1. 建立 Docker Image
```bash
docker build -t lambda-shioaji .
```

#### 2. 設定環境變數
```bash
export AWS_REGION=ap-northeast-1  # 修改為你的 region
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export REPOSITORY_NAME=lambda-shioaji
export ECR_URI=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}
```

#### 3. 建立 ECR Repository（如果還沒有）
```bash
aws ecr create-repository \
    --repository-name ${REPOSITORY_NAME} \
    --region ${AWS_REGION} \
    --image-scanning-configuration scanOnPush=true
```

#### 4. 登入 ECR
```bash
aws ecr get-login-password --region ${AWS_REGION} | \
    docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
```

#### 5. 為 Image 加上標籤
```bash
docker tag lambda-shioaji:latest ${ECR_URI}:latest
```

#### 6. 推送 Image 到 ECR
```bash
docker push ${ECR_URI}:latest
```

## 更新 Lambda 函數使用新的 Image

### 透過 AWS Console

1. 前往 AWS Lambda Console
2. 選擇你的 Lambda 函數
3. 在 "Code" 頁籤，點選 "Deploy new image"
4. 輸入 Image URI: `${ECR_URI}:latest`
5. 點選 "Save"

### 透過 AWS CLI

```bash
aws lambda update-function-code \
    --function-name your-lambda-function-name \
    --image-uri ${ECR_URI}:latest \
    --region ${AWS_REGION}
```

## 實用指令

### 查看 ECR 中的所有 Images
```bash
aws ecr list-images \
    --repository-name lambda-shioaji \
    --region ${AWS_REGION}
```

### 查看特定 Image 的詳細資訊
```bash
aws ecr describe-images \
    --repository-name lambda-shioaji \
    --region ${AWS_REGION}
```

### 刪除舊的 Image（清理空間）
```bash
# 刪除特定 tag 的 image
aws ecr batch-delete-image \
    --repository-name lambda-shioaji \
    --image-ids imageTag=old-tag \
    --region ${AWS_REGION}
```

### 設定 Lifecycle Policy（自動清理舊 Images）
```bash
# 建立 policy 檔案
cat > lifecycle-policy.json << 'EOF'
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "保留最新的 5 個 images",
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF

# 套用 policy
aws ecr put-lifecycle-policy \
    --repository-name lambda-shioaji \
    --lifecycle-policy-text file://lifecycle-policy.json \
    --region ${AWS_REGION}
```

## 測試本地 Docker Image

在推送到 ECR 之前，你可以在本地測試 Docker Image：

```bash
# 建立 Image
docker build -t lambda-shioaji .

# 執行容器
docker run -p 9000:8080 lambda-shioaji

# 在另一個終端機測試
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
  "apiKey": "your-api-key",
  "secretKey": "your-secret-key",
  "action": "get_account_id"
}'
```

## 常見問題

### 1. AWS CLI 認證失敗
確認你的 AWS 憑證設定正確：
```bash
aws sts get-caller-identity
```

### 2. Docker 建立失敗
檢查 Dockerfile 語法和依賴項是否正確：
```bash
docker build --no-cache -t lambda-shioaji .
```

### 3. ECR 登入失敗
確認你有正確的 ECR 權限：
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:PutImage`

### 4. Image 推送緩慢
ECR 位於不同 region 可能會較慢，建議使用離你較近的 region。

## 版本管理建議

為不同版本的 Image 加上有意義的標籤：

```bash
# 使用版本號
docker tag lambda-shioaji:latest ${ECR_URI}:v1.0.0

# 使用 git commit hash
GIT_HASH=$(git rev-parse --short HEAD)
docker tag lambda-shioaji:latest ${ECR_URI}:${GIT_HASH}

# 同時推送 latest 和版本標籤
docker push ${ECR_URI}:latest
docker push ${ECR_URI}:v1.0.0
```

## 安全性建議

1. **啟用 Image 掃描**: 已在腳本中啟用 `scanOnPush=true`
2. **使用私有 Repository**: ECR repositories 預設為私有
3. **定期更新 base image**: 更新 `public.ecr.aws/lambda/python:3.11` 到最新版本
4. **不要在 Image 中包含敏感資訊**: 使用 Lambda 環境變數或 AWS Secrets Manager
