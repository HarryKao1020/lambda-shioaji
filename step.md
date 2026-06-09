步驟 1：安裝 AWS CLI（在你的 Terminal 執行）

  curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
  sudo installer -pkg AWSCLIV2.pkg -target /

  安裝完後確認：
  aws --version

  ---
  步驟 2：設定 AWS 憑證

  aws configure

  會要求輸入：
  - AWS Access Key ID — 從 AWS Console > IAM > 你的帳號 > Security credentials 取得
  - AWS Secret Access Key
  - Default region name — 輸入 ap-northeast-1
  - Default output format — 輸入 json

  ---
  步驟 3：執行部署（你的專案已有現成腳本）

  cd /Users/1quanttradingtachan.com.tw/Desktop/lambda-shioaji
  ./deploy-to-ecr.sh

  這個腳本會自動依序做：
  1. 登入 ECR (aws ecr get-login-password ...)
  2. docker build -t shioaji-image-repo .
  ---
  步驟 2：設定 AWS 憑證

  aws configure

  會要求輸入：
  - AWS Access Key ID — 從 AWS Console > IAM > 你的帳號 > Security credentials 取得
  - AWS Secret Access Key
  - Default region name — 輸入 ap-northeast-1
  - Default output format — 輸入 json

  ---
  步驟 3：執行部署（你的專案已有現成腳本）

  cd /Users/1quanttradingtachan.com.tw/Desktop/lambda-shioaji
  ./deploy-to-ecr.sh

  這個腳本會自動依序做：
  1. 登入 ECR (aws ecr get-login-password ...)
  2. docker build -t shioaji-image-repo .
  3. docker tag shioaji-image-repo:latest 590992438228.dkr.ecr.ap-northeast-1.amazonaws.com/shioaji-image-repo:latest
  4. docker push 590992438228.dkr.ecr.ap-northeast-1.amazonaws.com/shioaji-image-repo:latest

  ---
  步驟 4：更新 Lambda 函數使用新 Image

  Push 完後，還要更新 Lambda 函數本身：
  aws lambda update-function-code \
    --function-name <你的Lambda函數名稱> \
    --image-uri 590992438228.dkr.ecr.ap-northeast-1.amazonaws.com/shioaji-image-repo:latest \
    --region ap-northeast-1

  ---
  先安裝 AWS CLI，設定好憑證後，用 ! ./deploy-to-ecr.sh 直接在這裡執行部署腳本，我可以幫你看輸出結果。