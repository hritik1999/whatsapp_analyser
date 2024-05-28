# WhatsApp Analyzer

## Introduction

WhatsApp Analyzer is a project designed to analyze WhatsApp chat data and provide insightful metrics and visualizations. This tool can help you understand patterns and trends in your WhatsApp conversations.

## Prerequisites

- Git
- Python 3.x
- Necessary Python libraries (details provided below)

## Installation

### Step 1: Clone the Repository

To get started with the WhatsApp Analyzer, you need to clone the repository from GitHub to your local system. Open the command prompt in the directory where you want to store the repository and run the following command:

```sh
git clone https://github.com/hritik1999/whatsapp_analyser.git
```

### Step 2: Navigate to the Project Directory

Change your working directory to the newly cloned repository:

```sh
cd whatsapp_analyser
```

### Step 3: Set Up a Virtual Environment
Use a virtual environment to manage dependencies. You can create and activate a virtual environment using the following commands:

```sh
python -m venv .venv
```
### Step 4: Run the files
After that in a new terminal<br>

For windows:

```sh
.\.venv\Scripts\activate
```

For macOS and Linux:
```sh
source .venv/bin/activate
```
### Step 4: Install Dependencies
Install the required Python libraries using pip:
```sh
pip install -r requirements.txt
```
### Step 5: Create a dotenv file
a dotenv file is required with the api key to run this app locally. Create a file named .env in whatsapp_analyser folder with the following content
```sh
API_KEY=sk-proj-OKc4LTCr8FbedqwBO7cvT3BlbkFJvpZH2AmYoECDNvTlg7bJ
```

Then in a new terminal 
```sh
cd .\whatsapp_analyser\
```
```sh
python main.py
```
Likewise repeat the Step 4 each time in a new terminal and run the files 
- analyser.py
- chunker.py
- plotter.py
### Step 5: Navigate to frontend folder
Make sure you have NodeJs and Vue.js installed in your machine. Navigate to the frontend folder and then run the command:
```sh
npm run dev
```
Click on the local host link and run the application locally

### Introduction
WhatsApp Text Analyzer is a tool designed to analyze WhatsApp chat data and provide insightful metrics and visualizations. With this tool, you can understand patterns, trends, and even personality traits of users within your WhatsApp conversations.
### Features
- Analyze WhatsApp chat data to generate insights.
- Identify personality traits of users based on chat messages.
- Visualize chat data with various charts and graphs.
## Usage

1. **Export Chat Data**: Export your WhatsApp chat data in text format and save it on your computer.

2. **Run the Analyzer**: Use the provided script to analyze the chat data and generate insights. Upload the chat here:
   ![WhatsApp Image 2024-05-28 at 13 36 30_36b7132d](https://github.com/hritik1999/whatsapp_analyser/assets/144601619/bbcfad92-3bd3-4679-977f-ca424b93c774)


3. **View Results**: Explore the generated analysis report to gain insights into the chat data, including personality traits of users.

# Example Screenshot
Below is an example screenshot showing personality traits analysis for each user.

## Analysis of each user
![image](https://github.com/hritik1999/whatsapp_analyser/assets/144601619/92bfeab8-8809-4035-b65b-f728fc5347f8)
<br>
![WhatsApp Image 2024-05-28 at 13 57 47_5e127f83](https://github.com/hritik1999/whatsapp_analyser/assets/144601619/e58473b7-d838-4376-854f-61f63c08849f)
## Statistical summary of the chat 
![image](https://github.com/hritik1999/whatsapp_analyser/assets/144601619/eb11a4cc-56db-42ef-9831-a29e020f6d84)<br>
![image](https://github.com/hritik1999/whatsapp_analyser/assets/144601619/2e216a39-002c-41ad-9346-97c6da072a29)<br>
![image](https://github.com/hritik1999/whatsapp_analyser/assets/144601619/b36818d5-5c1c-45b6-b5a2-d9267111d08e)<br>
![image](https://github.com/hritik1999/whatsapp_analyser/assets/144601619/9ae9c1b2-8f60-4b8d-8f66-cecce48cf93a)
# Conclusion
In summary, the WhatsApp Text Analyzer is a transformative tool, providing users with unparalleled insights into their WhatsApp conversations. Through sophisticated analysis of chat data, it unveils communication patterns, user behaviors, and even personality traits, offering invaluable understanding and awareness. With its user-friendly interface, comprehensive features, and exportable reports, it empowers individuals, researchers, and organizations to derive meaningful insights from their chat history effortlessly. Whether for personal introspection, group dynamics examination, or data-driven decision-making, this tool proves indispensable. Continuously evolving with community contributions, it remains at the forefront of communication analysis, offering new features and enhancements to enrich the analysis experience. As users delve into their WhatsApp conversations, they gain newfound understanding and appreciation for their interactions. The WhatsApp Text Analyzer stands as a testament to the power of technology in facilitating deeper connections and insights. With gratitude to its users, developers, and contributors, it looks forward to further enhancing communication analysis for the benefit of all.













