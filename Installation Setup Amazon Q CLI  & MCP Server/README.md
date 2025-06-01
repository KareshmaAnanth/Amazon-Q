# Quick Start: Deploying Amazon Q CLI & Extension Locally💻

Unlock the power of Amazon Q for your coding workflow! This guide provides step-by-step instructions to install and use Amazon Q CLI locally—both in terminal and as a VS Code extension—on macOS, Linux, and Windows (WSL-Ubuntu). Instructions for MCP Server setup are included at the end.

---

## 🚀 What is Amazon Q?

Amazon Q is an AI-powered coding assistant that helps you write, debug, and understand code faster. It integrates seamlessly into your terminal and VS Code, enhancing your productivity with powerful AI features.

![image alt])(https://www.google.com/imgres?q=amazon%20q%20login%20terminal&imgurl=https%3A%2F%2Fd2908q01vomqb2.cloudfront.net%2F7719a1c782a1ba91c031a682a0a2f8658209adbf%2F2025%2F05%2F20%2Fcli-persistence.png&imgrefurl=https%3A%2F%2Fnoise.getoto.net%2Ftag%2Fdevelopment%2F&docid=P-O1ZvIA4rCbNM&tbnid=NAikx6kzH4wncM&vet=12ahUKEwjqkJifkNGNAxUmyDgGHY6qAcMQM3oECBwQAA..i&w=1138&h=640&hcb=2&itg=1&ved=2ahUKEwjqkJifkNGNAxUmyDgGHY6qAcMQM3oECBwQAA)

---

## 🛠️ Installation Steps

### 1. Prerequisites

- **Amazon AWS Account:** Make sure you have an AWS account with permissions to use Amazon Q.
- **Python 3.8+** (for CLI)
- **Node.js & npm** (for some environments/VS Code extension, if required)
- **VS Code** (for the extension)
- **Git** (recommended)

---

### 2. Install Amazon Q CLI

#### macOS

```bash
brew update
brew install amazon-q/amazon-q/amazon-q
```


#### Windows (WSL-Ubuntu)

#Ubuntu install - [click here](https://documentation.ubuntu.com/wsl/latest/howto/install-ubuntu-wsl2/)

```bash 
sudo apt-get update
```

```bash 
sudo apt install libfuse2
```

```bash 
curl -O https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip
unzip q-x86_64-linux.zip
```

- Unzip the installer: unzip q.zip
- Run the install program:./q/install.shBy default, the files are installed to ~/.local/bin

or

```bash
curl -fsSL https://amazon-q-cli-releases.s3.amazonaws.com/install.sh | bash
```

#### Linux (Debian/Ubuntu)

```bash 
sudo apt-get update
```

```bash 
sudo apt install libfuse2
```

- Install Amazon Q debian file
```bash
sudo apt install -y ./amazon-q.deb
```


```bash
curl --proto '=https' --tlsv1.2 -sSf https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.deb -o amazon-q.deb
```

or 

```bash
curl -fsSL https://amazon-q-cli-releases.s3.amazonaws.com/install.sh | bash
```

---

### 3. Configure Amazon Q CLI

After installation, **Run**:

```bash
amazon-q configure
```
or 

```bash
q login
```

- Follow the prompts to:

 Before that Create Builder ID [Builder ID](https://community.aws/builderid) and Claim alias name for yourself (unchangeable)

- It will asked for **login method**. 
- Select **Free with Builder ID** 
- Open URL and Click Logic approved!✅

---

### 4. Using Amazon Q CLI in Terminal

Once configured, you can use Amazon Q directly from your terminal:

```bash
amazon-q help
amazon-q ask "How do I use boto3 to upload a file to S3?"
amazon-q explain path/to/file.py
```

---

### 5. Install Amazon Q as a VS Code Extension

1. Open VS Code.
2. Go to the Extensions Marketplace (Ctrl+Shift+X or Cmd+Shift+X).
3. Search for **Amazon Q**.
4. Click **Install**.
5. After installation, open the **Amazon Q** side panel and sign in with your AWS credentials as prompted.

**Tip:** Make sure the CLI is installed and configured for best integration.

---

### 6. (Optional) MCP Server Installation

**MCP (Model Coordination Platform) Server** is required for advanced on-prem/enterprise features.

#### Install MCP Server

-Now let's power up your Amazon Q CLI with MCP Servers.
-MCP Servers can be setup locally with npx , uvx, docker
-In this blog we have used uvx
-If you want to install simply use the commands

**MacOS**
```bash
brew install uv
```
---

**Linux / WSL**

```bash
sudo snap install astral-uv --classic
```
---

Now create a file called mcp.json in ~/.aws/amazon

```bash
vim mcp.json
```
- Paste the below code Press i to code

```bash
{

	"mcpServers" : {
    
 "awslabs.cdk-mcp-server": {
        "command": "uvx",
        "args": ["awslabs.cdk-mcp-server@latest"],
        "env": {
           "FASTMCP_LOG_LEVEL": "ERROR"
        }
   },
 "awslabs.aws-diagram-mcp-server": {
 		"command": "uvx",
 		"args": ["awslabs.aws-diagram-mcp-server"],
 		"env": {
 			"FASTMCP_LOG_LEVEL": "ERROR"
 		},
 		"autoApprove": [],
 		"disabled": false
 	}
}

}
```

Save & Exit - esc :wq enter

```bash
cat mcp.json
```

---

or 

1. Clone the MCP server repository:
    ```bash
    git clone https://github.com/aws/amazon-q-mcp-server.git
    cd amazon-q-mcp-server
    ```

2. Build and start the server (example using Docker Compose):

    ```bash
    docker-compose up -d
    ```

3. Configure your Amazon Q CLI or extension to point to your MCP server instance as described in the server documentation.

4. For detailed configuration, refer to the [official MCP Server documentation](https://github.com/aws/amazon-q-mcp-server).

---

Login again using **q login** and check for **uvx** command

---

##TIP 

If you want to switch your windows terminal to Ubuntu 

```bash
wsl -d Ubuntu-22.04
```
Before that check the list distros by:

```bash
wsl -l -v (or) wsl --list --verbose
```

Ask Amazon q cli to copy your directory to windows if you want because all files created will be in root directory of Ubuntu (Windows users)

---

## Start prompting

- Architecture diagram creation
- Building game using Pygame in Amazon Q cli

## 📚 Resources

- [Amazon Q Documentation](https://docs.aws.amazon.com/amazon-q/latest/userguide/)
- [Amazon Q CLI GitHub](https://github.com/aws/amazon-q-cli)
- [Amazon Q VS Code Extension](https://marketplace.visualstudio.com/items?itemName=amazon-q.amazon-q)

---

## ❤️ Need Help?

- Visit the [Amazon Q Community](https://github.com/aws/amazon-q-cli/discussions)
- Open an issue on the relevant GitHub repository

---

Happy coding with Amazon Q! 🚀