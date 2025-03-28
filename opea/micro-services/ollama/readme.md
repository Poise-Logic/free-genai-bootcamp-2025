# OPEA : Ollama Service

## Quick Links
- [OPEA Project](https://opea.dev/)
- [OPEA Repository](https://github.com/opea-project)
- [OPEA Comps](https://github.com/opea-project/GenAIComps)
- [OPEA Tutorial](https://opea-project.github.io/latest/tutorial/index.html)
- [OPEA Ollama](https://github.com/opea-project/GenAIComps/tree/main/comps/third_parties/ollama)


## Deploying Ollama locally with Docker (on Windows WSL2 - Ubuntu 24.04 LTS)

### [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

Install Prerequisites:
```bash
# Update package index and install required packages
sudo apt-get update
sudo apt-get install ca-certificates curl
```

Set up Docker Repository:
```bash
# Create directory for Docker GPG key
sudo install -m 0755 -d /etc/apt/keyrings

# Download and set permissions for Docker's GPG key
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository to apt sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install Docker:
```bash
# Update package index with new repository
sudo apt-get update

# Install Docker and required plugins
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify Docker installation
sudo docker run hello-world
```

[Optional] Configure Docker to Run Without Sudo:
```bash
# Add Docker group and current user
sudo groupadd docker
sudo usermod -aG docker $USER

# Apply new group membership
newgrp docker

# Verify Docker works without sudo
docker run hello-world
```

### Determining the Host IP address
Get your local IP address:

```bash
hostname -I | awk '{print $1}'
```
-OR-

```bash 
sudo apt install net-tools

# This command gives you detailed information about all network interfaces
ifconfig
```

### Configuring and Running the Ollama Instance

#### Docker Compose Configuration
Reference the sample Docker Compose configuration:
- [docker-compose.yaml](https://github.com/opea-project/GenAIComps/blob/main/comps/third_parties/ollama/deployment/docker_compose/compose.yaml)

Key Environment variables:

- LLM_ENDPOINT_PORT=8008
- LLM_MODEL_ID="llama3.2"
- no_proxy=localhost
- host_ip=$(hostname -I | awk '{print $1}')

#### Deployment Options

1. Default Port Deployment:

Run the local Ollama instance with default settings:

```sh
host_ip=$(hostname -I | awk '{print $1}') \
no_proxy=localhost \
LLM_MODEL_ID="llama3.2" \
docker compose up -d
```

2. Custom Port Deployment

Specify the host port(LLM_ENDPOINT_PORT) for the Ollama instance:

```sh
host_ip=$(hostname -I | awk '{print $1}') \
no_proxy=localhost \
LLM_ENDPOINT_PORT=9000 \
LLM_MODEL_ID="llama3.2" \
docker compose up -d
```

#### Important Notes:

- The -d flag runs the container in detached mode, preventing terminal lockup
- Manually pulling and configuring models is required, as the container does not automatically download models on startup

### Using the Ollama API
Ollama has a REST API for running and managing models. Once ollama-server is up and running we can start to make API calls.

See the [API documentation](https://github.com/ollama/ollama/blob/main/docs/api.md) for all endpoints.

### Download/pull the model

**Note:** When you run `ollama pull llama3.2` or only specify "llama3.2" without any suffix i.e."llama3.2:1b", by default it will pull the standard release version (default/base model). In our case, It will pull the 3 billion parameter version.

```sh
curl http://localhost:8008/api/pull -d '{ "model": "llama3.2" }'
```

-OR-

```sh
docker exec -it ollama-server ollama pull llama3.2
```

### List Available Models
List models that are available locally.

#### Request

```sh
# Replace `python3` with `python` if your system uses `python` as the default Python interpreter.
curl http://localhost:8008/api/tags | python3 -m json.tool
```
#### Response

```json
{
    "models": [
        {
            "name": "llama3.2:latest",
            "model": "llama3.2:latest",
            "modified_at": "2025-03-26T20:38:37.9518954Z",
            "size": 2019393189,
            "digest": "a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72",
            "details": {
                "parent_model": "",
                "format": "gguf",
                "family": "llama",
                "families": [
                    "llama"
                ],
                "parameter_size": "3.2B",
                "quantization_level": "Q4_K_M"
            }
        }
    ]
}
```

-OR-

```sh
docker exec -it ollama-server ollama list
```

Output:
```
NAME               ID              SIZE      MODIFIED       
llama3.2:latest    a80c4f17acd5    2.0 GB    12 minutes ago
```

### Generate a response (with Streaming)

Request (Example):

```json
curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2",
  "prompt":"Why is the sky blue?"
}'
```

Response (Example):

```json
{
  "model": "llama3.2",
  "created_at": "2023-08-04T19:22:45.499127Z",
  "response": "",
  "done": true,
  "context": [1, 2, 3],
  "total_duration": 10706818083,
  "load_duration": 6338219291,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 130079000,
  "eval_count": 259,
  "eval_duration": 4232710000
}
```

### Generate a response (without Streaming)
A response can be received in one reply when streaming is off.

#### Request

```json
curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "stream": false
}' | python3 -c "import sys, json; d=json.load(sys.stdin); d['context']=[', '.join(map(str,d['context']))]; print(json.dumps(d, indent=2))"
```

#### Response

```json
{
  "model": "llama3.2",
  "created_at": "2025-03-27T09:59:18.036354972Z",
  "response": "The sky appears blue due to a phenomenon called scattering, which occurs when sunlight interacts with the tiny molecules of gases in the Earth's atmosphere.\n\nHere's what happens:\n\n1. **Sunlight enters the atmosphere**: When sunlight enters the Earth's atmosphere, it consists of a spectrum of colors, including all the colors of the visible light spectrum (red, orange, yellow, green, blue, indigo, and violet).\n2. **Molecules scatter shorter wavelengths**: The smaller molecules in the atmosphere, such as nitrogen (N2) and oxygen (O2), scatter the shorter wavelengths of light more than the longer wavelengths.\n3. **Blue light scatters most**: Since blue light has a shorter wavelength (around 450-495 nanometers), it is scattered by the atmospheric molecules more effectively than any other color. This means that when sunlight enters the atmosphere, the blue light is dispersed in all directions and reaches our eyes from every part of the sky.\n4. **Our eyes perceive the blue color**: As a result of this scattering effect, our eyes perceive the blue light as being scattered across the entire sky, making it appear blue.\n\nIt's worth noting that:\n\n* During sunrise and sunset, when the sun is lower in the sky, the shorter wavelengths (like blue) are less effective at scattering. This is why the colors of the sky often appear more red or orange during these times.\n* The color of the sky can also be affected by atmospheric conditions, such as pollution, dust, or water vapor, which can scatter light in different ways and change its appearance.\n\nSo, to summarize: the sky appears blue because of the scattering effect caused by the tiny molecules in the Earth's atmosphere, which scatter shorter wavelengths (like blue) more than longer wavelengths.",
  "done": true,
  "done_reason": "stop",
  "context": [
    "128006, 9125, 128007, 271, 38766, 1303, 33025, 2696, 25, 6790, 220, 2366, 18, 271, 128009, 128006, 882, 128007, 271, 10445, 374, 279, 13180, 6437, 30, 128009, 128006, 78191, 128007, 271, 791, 13180, 8111, 6437, 4245, 311, 264, 25885, 2663, 72916, 11, 902, 13980, 994, 40120, 84261, 449, 279, 13987, 35715, 315, 45612, 304, 279, 9420, 596, 16975, 382, 8586, 596, 1148, 8741, 1473, 16, 13, 3146, 31192, 4238, 29933, 279, 16975, 96618, 3277, 40120, 29933, 279, 9420, 596, 16975, 11, 433, 17610, 315, 264, 20326, 315, 8146, 11, 2737, 682, 279, 8146, 315, 279, 9621, 3177, 20326, 320, 1171, 11, 19087, 11, 14071, 11, 6307, 11, 6437, 11, 1280, 7992, 11, 323, 80836, 4390, 17, 13, 3146, 44, 82206, 45577, 24210, 93959, 96618, 578, 9333, 35715, 304, 279, 16975, 11, 1778, 439, 47503, 320, 45, 17, 8, 323, 24463, 320, 46, 17, 705, 45577, 279, 24210, 93959, 315, 3177, 810, 1109, 279, 5129, 93959, 627, 18, 13, 3146, 10544, 3177, 1156, 10385, 1455, 96618, 8876, 6437, 3177, 706, 264, 24210, 46406, 320, 20019, 220, 10617, 12, 21038, 20622, 33504, 705, 433, 374, 38067, 555, 279, 45475, 35715, 810, 13750, 1109, 904, 1023, 1933, 13, 1115, 3445, 430, 994, 40120, 29933, 279, 16975, 11, 279, 6437, 3177, 374, 77810, 304, 682, 18445, 323, 25501, 1057, 6548, 505, 1475, 961, 315, 279, 13180, 627, 19, 13, 3146, 8140, 6548, 45493, 279, 6437, 1933, 96618, 1666, 264, 1121, 315, 420, 72916, 2515, 11, 1057, 6548, 45493, 279, 6437, 3177, 439, 1694, 38067, 4028, 279, 4553, 13180, 11, 3339, 433, 5101, 6437, 382, 2181, 596, 5922, 27401, 430, 1473, 9, 12220, 64919, 323, 44084, 11, 994, 279, 7160, 374, 4827, 304, 279, 13180, 11, 279, 24210, 93959, 320, 4908, 6437, 8, 527, 2753, 7524, 520, 72916, 13, 1115, 374, 3249, 279, 8146, 315, 279, 13180, 3629, 5101, 810, 2579, 477, 19087, 2391, 1521, 3115, 627, 9, 578, 1933, 315, 279, 13180, 649, 1101, 387, 11754, 555, 45475, 4787, 11, 1778, 439, 25793, 11, 16174, 11, 477, 3090, 38752, 11, 902, 649, 45577, 3177, 304, 2204, 5627, 323, 2349, 1202, 11341, 382, 4516, 11, 311, 63179, 25, 279, 13180, 8111, 6437, 1606, 315, 279, 72916, 2515, 9057, 555, 279, 13987, 35715, 304, 279, 9420, 596, 16975, 11, 902, 45577, 24210, 93959, 320, 4908, 6437, 8, 810, 1109, 5129, 93959, 13"
  ],
  "total_duration": 25895991745,
  "load_duration": 413471846,
  "prompt_eval_count": 31,
  "prompt_eval_duration": 73576684,
  "eval_count": 356,
  "eval_duration": 25407589650
}
```

### Chat with a model (without streaming)

#### Request

```sh
curl http://localhost:8008/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Why is the sky blue?"}],
  "stream": false
}' | python3 -m json.tool
```

#### Response

```json
{
    "model": "llama3.2",
    "created_at": "2025-03-27T10:00:37.167674627Z",
    "message": {
        "role": "assistant",
        "content": "The sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lord Rayleigh. He discovered that when sunlight enters Earth's atmosphere, it encounters tiny molecules of gases such as nitrogen and oxygen.\n\nHere's what happens:\n\n1. **Sunlight enters the atmosphere**: When sunlight enters our atmosphere, it consists of a spectrum of colors, each with its own wavelength (measured in nanometers).\n2. **Scattering occurs**: As sunlight travels through the air, it encounters tiny molecules of gases like nitrogen and oxygen. These molecules scatter the light in all directions.\n3. **Shorter wavelengths are scattered more**: The key to understanding why the sky appears blue is that shorter wavelengths of light (like blue and violet) are scattered more than longer wavelengths (like red and orange). This is because shorter wavelengths have a smaller wavelength, making it easier for them to be deflected by the tiny molecules.\n4. **Blue light dominates the sky**: As a result of this scattering, the blue light is dispersed throughout the atmosphere, reaching our eyes from all directions. Since there are more blue light photons being scattered than any other color, our eyes perceive the sky as blue.\n\nOther colors, like red and orange, are not scattered as much because they have longer wavelengths. That's why we don't see those colors dominating the sky. The scattering of light also depends on the angle at which it enters the atmosphere, which is why the sky can appear different shades of blue during sunrise and sunset.\n\nIn summary, the sky appears blue due to the scattering of sunlight by tiny molecules in the Earth's atmosphere, with shorter wavelengths (like blue) being scattered more than longer wavelengths."
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 25959184841,
    "load_duration": 256524488,
    "prompt_eval_count": 31,
    "prompt_eval_duration": 92412779,
    "eval_count": 340,
    "eval_duration": 25607233689
}
```

## Technical Uncertainty

**Q**: What is Docker's bridge network mode, and how does it affect the accessibility of the Ollama API from both the host machine and other containers?

**A**: Docker's bridge network mode creates a private internal network where containers can communicate with each other and the host machine. The Ollama API will be accessible from:
1. The host machine via the mapped port (8008)
2. Other containers in the same network via the container name and internal port (ollama-server:11434)
3. External clients through the host's IP address and mapped port

**Q**: Which port is being mapped 8008->11434?

**A**: In this case, 8008 is the host port and it's mapped to 11434, which is the port inside the container. The host port is what we'll use to access the service from our host machine. The container port is the one the service is listening on within the Docker container.

**Q**: If we pass the LLM_MODEL_ID to the Ollama server, will it download the model when starting the Docker container?

**A**: No, it does not. The Docker Compose essentially creates a "blank" Ollama server instance that's ready to receive commands but requires manual intervention to pull and configure specific models.

**Q**: Will the model be downloaded in the container? Does that mean the LLM model will be deleted when the container is removed or stops running?

**A**: The model will be downloaded in the container and stored within the `/root/.ollama` directory. Without proper volume mounting, the model will be deleted when the container is removed as the data is not stored in a persistent Docker volume. To preserve models between container restarts, you need to mount a local drive as shown in the docker-compose configuration.

**Q**: For LLM service which can handle text generation, it suggests it will only work with TGI/vLLM and all you have to do is have it running. Do TGI and vLLM have a standardized API or is there code to detect which one is running? Do we have to really use Xeon or Gaudi processors?

**A**: vLLM, TGI (Text Generation Inference), and Ollama all offer APIs with OpenAI compatibility, so in theory they should be interchangeable.

**Q**: What are the memory requirements for different model sizes, and how does this affect container resource allocation?

**A**: Different model sizes (3B, 7B, 13B, etc.) have varying memory requirements. It's crucial to ensure your host system has sufficient RAM and that appropriate memory limits are set in the Docker container configuration.

**Q**: How does the model quantization affect the API response time and resource usage?

**A**: Quantization (Q4, Q5, Q8) impacts both the model's performance and resource usage. Understanding these tradeoffs is important for production deployments.