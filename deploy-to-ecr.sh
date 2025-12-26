#!/bin/bash

# AWS ECR 部署腳本
# 用法: ./deploy-to-ecr.sh [region] [repository-name]

# 設定參數（可自行修改或透過命令列參數傳入）
AWS_REGION=${1:-ap-northeast-1}
REPOSITORY_NAME=${2:-shioaji-image-repo}
IMAGE_TAG=${3:-latest}

echo "========================================="
echo "開始部署 Docker Image 到 AWS ECR"
echo "========================================="
echo "Region: ${AWS_REGION}"
echo "Repository: ${REPOSITORY_NAME}"
echo "Tag: ${IMAGE_TAG}"
echo "========================================="

# 檢查 AWS CLI 是否安裝
if ! command -v aws &> /dev/null; then
    echo "錯誤: AWS CLI 未安裝。請先安裝 AWS CLI。"
    exit 1
fi

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo "錯誤: Docker 未安裝。請先安裝 Docker。"
    exit 1
fi

# 取得 AWS Account ID
echo "正在取得 AWS Account ID..."
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "錯誤: 無法取得 AWS Account ID。請檢查 AWS 憑證設定。"
    exit 1
fi
echo "AWS Account ID: ${AWS_ACCOUNT_ID}"

# 建立 ECR URI
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}"
echo "ECR URI: ${ECR_URI}"

# 檢查 ECR repository 是否存在，不存在則建立
echo "正在檢查 ECR Repository..."
REPO_CHECK=$(aws ecr describe-repositories --repository-names ${REPOSITORY_NAME} --region ${AWS_REGION} 2>&1)
if [ $? -ne 0 ]; then
    if echo "$REPO_CHECK" | grep -q "RepositoryNotFoundException"; then
        echo "Repository 不存在，正在建立..."
        aws ecr create-repository \
            --repository-name ${REPOSITORY_NAME} \
            --region ${AWS_REGION} \
            --image-scanning-configuration scanOnPush=true
        if [ $? -ne 0 ]; then
            echo "錯誤: Repository 建立失敗。"
            exit 1
        fi
        echo "Repository 建立完成！"
    else
        echo "錯誤: 無法檢查 Repository 狀態。"
        echo "$REPO_CHECK"
        exit 1
    fi
else
    echo "Repository 已存在。"
fi

# 建立 Docker Image
echo "正在建立 Docker Image..."
docker build -t ${REPOSITORY_NAME}:${IMAGE_TAG} .
if [ $? -ne 0 ]; then
    echo "錯誤: Docker Image 建立失敗。"
    exit 1
fi
echo "Docker Image 建立完成！"

# 登入 ECR
echo "正在登入 ECR..."
aws ecr get-login-password --region ${AWS_REGION} | \
    docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
if [ $? -ne 0 ]; then
    echo "錯誤: ECR 登入失敗。"
    exit 1
fi
echo "ECR 登入成功！"

# 為 Image 加上 ECR 標籤
echo "正在為 Image 加上標籤..."
docker tag ${REPOSITORY_NAME}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
echo "標籤加上完成！"

# 推送 Image 到 ECR
echo "正在推送 Image 到 ECR..."
docker push ${ECR_URI}:${IMAGE_TAG}
if [ $? -ne 0 ]; then
    echo "錯誤: Image 推送失敗。"
    exit 1
fi

echo "========================================="
echo "部署完成！"
echo "========================================="
echo "Image URI: ${ECR_URI}:${IMAGE_TAG}"
echo ""
echo "你可以使用以下 URI 來部署 Lambda 函數："
echo "${ECR_URI}:${IMAGE_TAG}"
echo "========================================="
