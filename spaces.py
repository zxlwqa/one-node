from io import BytesIO
import random
import string
import sys
import argparse
from huggingface_hub import HfApi

parser = argparse.ArgumentParser(description="自动创建 Hugging Face Space 并注入 Secrets")
parser.add_argument("--token", type=str, required=True, help="Hugging Face的Token，需要写权限")
parser.add_argument("--uuid", type=str, default="8c8fe996-85aa-4555-84ae-d5ec03db2912", help="UUID（可选）")
parser.add_argument("--image", type=str, default="ghcr.io/zxlwqa/lwq:latest", help="Docker 镜像地址（可选）")
args = parser.parse_args()


def generate_random_string(length=8):
    """生成随机字符串，至少含一个字母"""
    chars = string.ascii_letters + string.digits
    mandatory_letter = random.choice(string.ascii_letters)
    remaining_chars = random.choices(chars, k=length - 1)
    full_chars = remaining_chars + [mandatory_letter]
    random.shuffle(full_chars)
    return "".join(full_chars)


if __name__ == "__main__":
    token = args.token
    if not token:
        print("Token 不能为空")
        sys.exit(1)

    api = HfApi(token=token)
    user_info = api.whoami()
    if not user_info.get("name"):
        print("未获取到用户名信息，程序退出。")
        sys.exit(1)
    userid = user_info["name"]

    # 镜像和 UUID，使用默认值
    image = args.image
    uuid = args.uuid

    # 随机 Space 名并创建
    space_name = generate_random_string(6)
    repoid = f"{userid}/{space_name}"
    api.create_repo(
        repo_id=repoid,
        repo_type="space",
        space_sdk="docker",
    )

    # 上传 README.md
    readme_content = f"""---
title: {space_name}
emoji: 😻
colorFrom: red
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
"""
    api.upload_file(
        repo_id=repoid,
        path_in_repo="README.md",
        path_or_fileobj=BytesIO(readme_content.encode("utf-8")),
        repo_type="space",
    )

    # 上传 Dockerfile
    dockerfile_content = f"FROM {image}"
    api.upload_file(
        repo_id=repoid,
        path_in_repo="Dockerfile",
        path_or_fileobj=BytesIO(dockerfile_content.encode("utf-8")),
        repo_type="space",
    )

    print(f"✅ Space 已创建： https://huggingface.co/spaces/{repoid}")

    # 拼接公共 URL 并自动注入 Secrets
    public_url = f"https://{space_name}.hf.space"
    api.add_space_secret(repo_id=repoid, key="UUID", value=uuid)
    api.add_space_secret(repo_id=repoid, key="DOMAIN", value=public_url)

    print(f"✅ 已注入 Secrets：UUID={uuid}, DOMAIN={public_url}")
