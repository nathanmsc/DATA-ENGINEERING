```json
{
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "triggerAtHour": 7
            }
          ]
        }
      },
      "id": "f1e4d55a-fd09-4c36-981a-0ceba8f24bff",
      "name": "Scheduled Start: Check for New Posts",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [
        -1700,
        -80
      ],
      "typeVersion": 1.2
    },
    {
      "parameters": {
        "documentId": {
          "__rl": true,
          "value": "1Xnnn8magRSgVRcu3mjcHE7MVg5g0hZL2YjuCvcGCjRs",
          "mode": "list",
          "cachedResultName": "posts",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1Xnnn8magRSgVRcu3mjcHE7MVg5g0hZL2YjuCvcGCjRs/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": "gid=0",
          "mode": "list",
          "cachedResultName": "instagram",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1Xnnn8magRSgVRcu3mjcHE7MVg5g0hZL2YjuCvcGCjRs/edit#gid=0"
        },
        "options": {}
      },
      "id": "26e02555-0653-46ac-a7b2-cc4603b8dceb",
      "name": "1. Get Next Post Idea from Sheet",
      "type": "n8n-nodes-base.googleSheets",
      "position": [
        -1480,
        -80
      ],
      "typeVersion": 4.5,
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "G1A9wvnK2xYTdHdZ",
          "name": "Google Sheets account"
        }
      }
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "aa3b9a02-ac6a-4d7f-937f-a0e6e566a0c8",
              "name": "Topic",
              "type": "string",
              "value": "={{ $json.Topic }}"
            },
            {
              "id": "e48783e8-5f6b-4c54-bf4f-c004414dc510",
              "name": "TargetAudience",
              "type": "string",
              "value": "={{ $json.Audience }}"
            },
            {
              "id": "c499a954-b4c6-4702-ab86-3656aa2b1783",
              "name": "BrandVoice",
              "type": "string",
              "value": "={{ $json.Voice }}"
            },
            {
              "id": "210f7103-4d6b-42e9-9168-fd99dff94b5a",
              "name": "Platform",
              "type": "string",
              "value": "={{ $json.Platform }}"
            }
          ]
        },
        "options": {}
      },
      "id": "865969d8-438d-4f38-98ee-716ae474e87c",
      "name": "2. Prepare Input Variables (Topic, Audience, etc.)",
      "type": "n8n-nodes-base.set",
      "position": [
        -1260,
        -80
      ],
      "typeVersion": 3.4
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.replicate.com/v1/models/black-forest-labs/flux-1.1-pro-ultra/predictions",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Prefer",
              "value": "wait"
            }
          ]
        },
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"input\": {\n    \"raw\": false,\n    \"prompt\": \"{{ $('parse prompt JSON').item.json.response.prompt_options[0].prompts }}\",\n    \"aspect_ratio\": \"1:1\",\n    \"output_format\": \"jpg\",\n    \"safety_tolerance\": 6\n  }\n}",
        "options": {}
      },
      "id": "ad26b512-1439-4958-8541-a04d36d766df",
      "name": "4. Generate Image using Prompt 1 (Replicate Flux)",
      "type": "n8n-nodes-base.httpRequest",
      "position": [
        748,
        -80
      ],
      "typeVersion": 4.2,
      "credentials": {
        "httpHeaderAuth": {
          "id": "oXRpXSe3Ueh1vvc8",
          "name": "Header Auth account"
        }
      }
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "8a4260ba-3bde-4444-8f42-8a8abd51ff0c",
              "name": "ImageURL",
              "type": "string",
              "value": "={{ $json.output }}"
            },
            {
              "id": "1953ae03-6a86-4847-8686-5a928637be1d",
              "name": "Caption",
              "type": "string",
              "value": "={{ $('3c. Generate Post Caption (Ollama)').item.json.output.Caption }}"
            }
          ]
        },
        "options": {}
      },
      "id": "c5dcf712-f359-45e8-b4e7-87ab4a00b0a8",
      "name": "5. Prepare Data for Instagram API",
      "type": "n8n-nodes-base.set",
      "position": [
        968,
        -80
      ],
      "typeVersion": 3.4
    },
    {
      "parameters": {
        "httpRequestMethod": "POST",
        "graphApiVersion": "v22.0",
        "node": "17841473009917118",
        "edge": "media",
        "options": {
          "queryParameters": {
            "parameter": [
              {
                "name": "caption",
                "value": "={{ $json.Caption }}"
              },
              {
                "name": "image_url",
                "value": "={{ $json.ImageURL }}"
              }
            ]
          }
        }
      },
      "id": "78fa57f5-d3db-4f71-b9a4-7cb64ff876df",
      "name": "6a. Create Instagram Media Container",
      "type": "n8n-nodes-base.facebookGraphApi",
      "position": [
        1188,
        -80
      ],
      "typeVersion": 1
    },
    {
      "parameters": {},
      "id": "090f46cf-0509-4e13-9f6f-147247546ed3",
      "name": "6b. Wait for Container Processing",
      "type": "n8n-nodes-base.wait",
      "position": [
        1408,
        -80
      ],
      "webhookId": "1b14c8bf-151a-4054-8215-093dd5b6cbcc",
      "typeVersion": 1.1
    },
    {
      "parameters": {
        "httpRequestMethod": "POST",
        "graphApiVersion": "v22.0",
        "node": "17841473009917118",
        "edge": "media_publish",
        "options": {
          "queryParameters": {
            "parameter": [
              {
                "name": "creation_id",
                "value": "={{ $json.id }}"
              }
            ]
          }
        }
      },
      "id": "6ef316e4-0d01-49dc-8ecc-a110042723af",
      "name": "6c. Publish Post to Instagram",
      "type": "n8n-nodes-base.facebookGraphApi",
      "position": [
        1628,
        -80
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "operation": "update",
        "documentId": {
          "__rl": true,
          "mode": "list",
          "value": "1hG2NMi-4fMa7D5qGonCN8bsYVya4L2TOB_8mI4XK-9k",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1hG2NMi-4fMa7D5qGonCN8bsYVya4L2TOB_8mI4XK-9k/edit?usp=drivesdk",
          "cachedResultName": "Medium Post Automation"
        },
        "sheetName": {
          "__rl": true,
          "mode": "list",
          "value": 1510137257,
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1hG2NMi-4fMa7D5qGonCN8bsYVya4L2TOB_8mI4XK-9k/edit#gid=1510137257",
          "cachedResultName": "Postİ"
        },
        "columns": {
          "value": {
            "Topic": "={{ $('1. Get Next Post Idea from Sheet').item.json.Topic }}",
            "Status": "1"
          },
          "schema": [
            {
              "id": "Topic",
              "type": "string",
              "display": true,
              "removed": false,
              "required": false,
              "displayName": "Topic",
              "defaultMatch": false,
              "canBeUsedToMatch": true
            },
            {
              "id": "Audience",
              "type": "string",
              "display": true,
              "removed": true,
              "required": false,
              "displayName": "Audience",
              "defaultMatch": false,
              "canBeUsedToMatch": true
            },
            {
              "id": "Voice",
              "type": "string",
              "display": true,
              "removed": true,
              "required": false,
              "displayName": "Voice",
              "defaultMatch": false,
              "canBeUsedToMatch": true
            },
            {
              "id": "Platform",
              "type": "string",
              "display": true,
              "removed": true,
              "required": false,
              "displayName": "Platform",
              "defaultMatch": false,
              "canBeUsedToMatch": true
            },
            {
              "id": "Status",
              "type": "string",
              "display": true,
              "required": false,
              "displayName": "Status",
              "defaultMatch": false,
              "canBeUsedToMatch": true
            },
            {
              "id": "row_number",
              "type": "string",
              "display": true,
              "removed": true,
              "readOnly": true,
              "required": false,
              "displayName": "row_number",
              "defaultMatch": false,
              "canBeUsedToMatch": true
            }
          ],
          "mappingMode": "defineBelow",
          "matchingColumns": [
            "Topic"
          ],
          "attemptToConvertTypes": false,
          "convertFieldsToString": false
        },
        "options": {}
      },
      "id": "39281199-2f9f-4125-b495-a9d60a0bd12b",
      "name": "7. Update Post Status in Sheet",
      "type": "n8n-nodes-base.googleSheets",
      "position": [
        1848,
        -80
      ],
      "typeVersion": 4.5
    },
    {
      "parameters": {
        "content": "# 01. Content Concept Generation\n\n**Purpose:** This step uses Google Gemini to generate **one unique content concept** tailored for the specified platform (Instagram/LinkedIn), based on the input topic, audience, and brand voice. The format is fixed to \"Single Image\".\n\n**Input (from Node '2. Prepare Input Variables'):**\n*   `Topic` (string)\n*   `TargetAudience` (string)\n*   `BrandVoice` (string)\n*   `Platform` (string: 'Instagram' )\n\n**Output (JSON):**\n*   `{\"ideas\": [{\"concept\": \"Generated concept text...\", \"suggested_format\": \"Single Image\"}]}`",
        "height": 740,
        "width": 460
      },
      "id": "6a56087f-57a1-458b-936b-ea061c4765b1",
      "name": "Sticky Note",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        -1720,
        -480
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "# 03b. Image Generation\n\n**Purpose:** Generates the actual image using the **first detailed prompt** created in step 3b. It sends this prompt to the Replicate API, specifically using the 'Flux 1.1 Pro Ultra' model.\n\n**Input (from Node '3b. Generate Image Prompt Options'):**\n*   `prompt` (string: The *first* prompt string from `prompt_options[0].prompts[0]`)\n\n**Output (from Replicate API):**\n*   JSON containing the `output` URL of the generated image (e.g., `{\"output\": \"https://replicate.delivery/...\"}`)",
        "height": 740,
        "width": 380,
        "color": 4
      },
      "id": "8dc23a96-4cc2-4a58-9641-6b096c5dcf29",
      "name": "Sticky Note1",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        240,
        -520
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "# 02. Image Prompt Elaboration & Options\n\n**Purpose:** Takes the generated content concept and expands on it to create **two distinct, detailed image generation prompts**. These prompts are optimized for the target platform and suitable for AI image generators like Replicate Flux.\n\n**Input (from Nodes '2. Prepare Input Variables' & '3a. Generate Content Concept'):**\n*   `ChosenIdea` (string: Concept from step 3a)\n*   `OriginalTopic` (string)\n*   `TargetAudience` (string)\n*   `BrandVoice` (string)\n*   `Platform` (string: 'Instagram')\n\n**Output (JSON):**\n*   `{\"expanded_post_concept\": \"Elaborated concept description...\", \"prompt_options\": [{\"option_description\": \"Option 1: ...\", \"prompts\": [\"Detailed prompt 1...\"]}, {\"option_description\": \"Option 2: ...\", \"prompts\": [\"Detailed prompt 2...\"]}]}`\n",
        "height": 740,
        "width": 740,
        "color": 2
      },
      "id": "fd6194f7-a58e-4501-8d32-df7581b3d799",
      "name": "Sticky Note2",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        -1220,
        -520
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "# 03a. Caption Generation\n\n**Purpose:** Uses Google Gemini to write a short, engaging social media caption **specifically tailored for the target platform**. The caption complements the image (represented by the first generated prompt) and aligns with the overall content strategy. Includes relevant hashtags.\n\n**Input (from Nodes '1. Get Next Post Idea', '3a. Generate Content Concept', '3b. Generate Image Prompt Options'):**\n*   `ImagePrompt` (string: The *first* prompt from step 3b)\n*   `ChosenIdea` (string: Concept from step 3a)\n*   `OriginalTopic` (string)\n*   `TargetAudience` (string)\n*   `BrandVoice` (string)\n*   `Platform` (string: 'Instagram' or 'LinkedIn')\n\n**Output (JSON):**\n*   `{\"Caption\": \"Generated caption text with #hashtags...\"}`",
        "height": 740,
        "width": 620,
        "color": 3
      },
      "id": "8c6d682c-9084-4b05-82ee-689df368e483",
      "name": "Sticky Note3",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        -440,
        -500
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "# 04. Instagram Publishing\n\n**Purpose:** This block takes the final image URL and caption, prepares them for the Instagram Graph API, uploads the media to create a container, waits for Instagram to process it, and finally publishes the container as a post to the connected Instagram account.\n\n**Input (from Nodes '3c. Generate Post Caption (Gemini)' & '4. Generate Image using Prompt 1 (Replicate Flux)'):**\n*   `ImageURL` (string: URL of the generated image from Replicate)\n*   `Caption` (string: Generated post text with hashtags from Gemini)\n\n**Process:**\n1.  **Format Data (`5. Prepare Data...`):** Organizes the ImageURL and Caption into the required structure.\n2.  **Create Media Container (`6a. Create...`):** Sends the `image_url` and `caption` to the Instagram Graph API (`media` edge) to initiate the upload. Receives a container `id`.\n3.  **Wait for Processing (`6b. Wait...`):** Pauses the workflow to allow Instagram's servers time to process the uploaded media. *Note: Wait time might need adjustment depending on media size and API responsiveness.*\n4.  **Publish Media (`6c. Publish...`):** Sends the container `id` (as `creation_id`) to the Instagram Graph API (`media_publish` edge) to make the post live.\n\n**Output:** The content is published as a new post on the target Instagram profile. The final node (`6c. Publish Post...`) returns the `id` of the successfully published media object on Instagram.",
        "height": 740,
        "width": 1160,
        "color": 5
      },
      "id": "a562c581-a71d-4527-8b28-2a02ecfa4fac",
      "name": "Sticky Note4",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        680,
        -560
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "# 05. Finalize: Update Sheet Status\n\n**Purpose:** Marks the processed post idea as completed in the Google Sheet.\n\n**Action:** Finds the corresponding row in the sheet (using the 'Topic' to match) and updates its 'Status' column to '1'. This prevents the same idea from being processed again by the workflow in future runs.",
        "height": 300,
        "width": 380,
        "color": 6
      },
      "id": "ec3f6f49-eb29-4b98-92c9-34e5a5cfaeac",
      "name": "Sticky Note5",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        1840,
        -200
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "# 00. Scheduled Start & Input Preparation\n\n**Purpose:** Initiates the workflow automatically based on the user-defined schedule. Fetches the next available post idea (Status=0) from Google Sheets and prepares the necessary input variables (`Topic`, `Audience`, `Voice`, `Platform`) for the content generation steps.",
        "height": 240,
        "width": 420
      },
      "id": "c7612beb-d824-4f08-a250-57d58e96f602",
      "name": "Sticky Note7",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        -2200,
        -160
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "model": "llama3.2:1b",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmOllama",
      "typeVersion": 1,
      "position": [
        -952,
        140
      ],
      "id": "62c0b750-10c0-45e8-adb3-77008d63dc1a",
      "name": "(LLM Model for Concept)",
      "credentials": {
        "ollamaApi": {
          "id": "pEI8Q6mvoMMbpRr9",
          "name": "Ollama account 3"
        }
      }
    },
    {
      "parameters": {
        "model": "llama3.2:1b",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmOllama",
      "typeVersion": 1,
      "position": [
        -356,
        140
      ],
      "id": "362436d1-ee60-4533-9c4d-cf2b4fb7bbb9",
      "name": "(LLM Model for Prompts)",
      "credentials": {
        "ollamaApi": {
          "id": "pEI8Q6mvoMMbpRr9",
          "name": "Ollama account 3"
        }
      }
    },
    {
      "parameters": {
        "model": "llama3.2:1b",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmOllama",
      "typeVersion": 1,
      "position": [
        240,
        140
      ],
      "id": "0e93f0ac-1290-422d-b53b-77a4c4fcd005",
      "name": "(LLM Model for Caption)",
      "credentials": {
        "ollamaApi": {
          "id": "pEI8Q6mvoMMbpRr9",
          "name": "Ollama account 3"
        }
      }
    },
    {
      "parameters": {
        "promptType": "define",
        "text": "=<prompt>     <role>         You are a **highly imaginative Social Media Strategist** specializing in generating **unique, platform-aware content CONCEPTS** for **Instagram and LinkedIn**. You think beyond basic formats and consider audience engagement.     </role>      <task>         Based *only* on the `Topic`, `Target Audience`, `Brand Voice`, AND **target `Platform` ('Instagram' or 'LinkedIn')**, generate **exactly 1 creative content CONCEPT**. Focus on the **core message, angle, or hook**. The suggested format **MUST be \"Single Image\"**.         1.  **Platform Optimization:** **Explicitly tailor** the *type* and *angle* of the concept to the specified `Platform`. Consider typical user expectations and content formats:             * **Instagram:** Often more visual, storytelling, personal, community-focused, impactful single images.             * **LinkedIn:** Can utilize impactful single images to convey data points, key takeaways, or thought-provoking visuals supporting a concise message.         2.  **Originality:** Avoid common tropes (like basic quotes) unless the input strongly suggests it. Explore diverse angles: striking visual representations of data, metaphorical imagery, thought-provoking questions presented visually, behind-the-scenes moments captured in a compelling image, key message highlighted graphically.         3.  **Format Suggestion:** The format **MUST be \"Single Image\"**. The **CONCEPT is primary, the format is fixed**.      </task>      <input_context>         <param name=\"Topic\">{{ $json.Topic }}</param>         <param name=\"TargetAudience\">{{ $json.TargetAudience }}</param>         <param name=\"BrandVoice\">{{ $json.BrandVoice }}</param>         <param name=\"Platform\">{{ $json.Platform }}</param>     </input_context>      <output_instructions>         Your response MUST be a single, valid JSON object containing exactly one key: `ideas`.         The value of `ideas` MUST be an array containing exactly 1 object.         The object in the array MUST have two keys: `concept` (string: the descriptive concept text) and `suggested_format` (string: **MUST be \"Single Image\"**).         Example: `{\"ideas\": [{\"concept\": \"Concept text...\", \"suggested_format\": \"Single Image\"}]}`         Do NOT include any other text, explanations, or formatting outside the JSON structure.     </output_instructions> </prompt>"
      },
      "id": "b12547e6-3c7a-4d46-a81d-17e738a53d30",
      "name": "3a. Generate Content Concept (Ollama)",
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "position": [
        -1040,
        -80
      ],
      "typeVersion": 1.5
    },
    {
      "parameters": {
        "promptType": "define",
        "text": "=<prompt>\n    <role>\n        You are an **Expert Instagram/LinkedIn Content Strategist and AI Image Prompt Engineer**. You excel at elaborating concepts based on user feedback and crafting distinct, detailed, and visually consistent prompt options tailored for the target platform.\n    </role>\n\n    <task>\n        1.  **Analyze** the `Chosen Idea`, `User Visual Input` (if provided and relevant), and **target `Platform`** to determine the optimal post format (in this case, assumed to be Single Image based on the output) and elaborate this into a practical `expanded_post_concept`. **Justify format choice based on concept AND platform norms.**\n        2.  **Incorporate** the user's visual direction (if any) into the concept description. If no specific visual input was given, propose a clear visual direction that aligns with the concept and platform.\n        3.  Generate **TWO DISTINCT OPTIONS** for the image prompts based on the `expanded_post_concept`. **Tailor the visual style and content nuances** described in the prompts to the target `Platform`. (E.g., LinkedIn visuals might be cleaner, more data-oriented; Instagram more lifestyle or emotive).\n        4.  **Ensure Distinction:** The two options should offer meaningful variety (e.g., style, composition, focus) while remaining true to the core concept.\n        5.  **Detail:** Prompts should be highly detailed, suitable for advanced AI image generators (include subject, action, setting, style, mood, composition, lighting, color palette keywords).\n    </task>\n\n    <input_context>\n        <param name=\"ChosenIdea\"> {{ $json.ideas[0].concept }} </param>\n        <param name=\"OriginalTopic\"> {{ $('2. Prepare Input Variables (Topic, Audience, etc.)').item.json.Topic }}</param>\n        <param name=\"TargetAudience\"> {{ $('2. Prepare Input Variables (Topic, Audience, etc.)').item.json.TargetAudience }}</param>\n        <param name=\"BrandVoice\"> {{ $('2. Prepare Input Variables (Topic, Audience, etc.)').item.json.BrandVoice }}</param>\n        <param name=\"Platform\"> {{ $('2. Prepare Input Variables (Topic, Audience, etc.)').item.json.Platform }}</param>\n        </input_context>\n\n    <output_instructions>\n              The JSON object MUST contain exactly two keys expanded_post_concept and prompt_options:\n        \n        - `expanded_post_concept` (string): the elaborated visual concept text, stating the idea behind the image and its relevance (in this case, to dentistry and social well-being).\n        - `prompt_options` (array): MUST contain exactly two objects.\n          - Each object MUST have two keys:\n            - `option_description` (string): describes the distinct visual approach in Portuguese.\n            - `prompts` (string): a single detailed AI image generation prompt in English.\n        \n        Example:\n\n[\n    {\n    \"action\": \n    \"parse\",\n    \"response\": \n        {\n            \"output\": \n            {  \n            {\n              \"expanded_post_concept\": \"Transformando vidas através de Sorrisos, um tratamento dentário eficaz e sustentável. Foram estudadas as evidências científicas sobre a importância do sorriso na saúde bucal e nas relações sociais.\",\n          \"prompt_options\": [\n            {\n              \"option_description\": \"Um detalhe fotográfico que destaque o sorriso enquanto o paciente realiza o tratamento dentário, destacando sua confiança em si mesmo.\",\n              \"prompts\": \"Image of a patient smiling while receiving dental treatment, highlighting their confidence in themselves.\"\n            },\n            {\n              \"option_description\": \"Uma composição de profundidade de campos para enfatizar a anatomia do sorriso enquanto o paciente realiza o tratamento dentário. Isso pode ser feito criando diferentes ângulos fotográficos e arranjos de elementos.\",\n              \"prompts\": \"Image of a patient smiling while receiving dental treatment, with the focus on the dental anatomy and different angles/focal points.\"\n            }\n          ]\n        }\n    }\n  }\n]\n     \n        Do NOT include any other text, formatting, or explanation outside the JSON structure.\n     \n    </output_instructions>\n</prompt>"
      },
      "id": "4787b739-8471-4eba-9d4a-44920f21cd56",
      "name": "3b. Generate Image Prompt Options (Ollama)",
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "position": [
        -444,
        -80
      ],
      "typeVersion": 1.5
    },
    {
      "parameters": {
        "promptType": "define",
        "text": "=<prompt>\n    <role>\n        You are an AI Instagram/LinkedIn **Caption Writer**. You specialize in crafting concise, engaging, and contextually relevant captions based on a generated image (represented by its prompt) and the overall content strategy, specifically tailored for the target platform.\n    </role>\n\n    <task>\n        Write a short, effective social media caption **specifically tailored for the target `Platform` ('Instagram' or 'LinkedIn')**.\n        * The caption must complement the image described by `ImagePrompt` and align with all context parameters (`ChosenIdea`, `OriginalTopic`, `TargetAudience`, `BrandVoice`).\n        * **Platform Style:** Adapt tone, length, calls-to-action, and hashtag usage:\n            * **Instagram:** Can be more conversational, use more emojis, ask engaging questions, often benefits from slightly longer, more storytelling captions if relevant. Use a mix of popular and niche hashtags (3-7 recommended).\n            * **LinkedIn:** Generally more professional, concise, focused on insights or value proposition. Calls-to-action often relate to reading more, commenting with professional opinions, or business objectives. Use targeted, professional hashtags (1-3 recommended).\n        * Include 1-5 relevant, platform-appropriate hashtags adding the hastags #sorriso #odontologiacomamor❤️.\n    </task>\n\n    <input_context>\n        <param name=\"ImagePrompt\"> {{ $json.response.prompt_options[1].prompts }} </param> \n        <param name=\"ChosenIdea\"> {{ $('parse prompt JSON2').item.json.ideas[0].concept }} </param>\n        <param name=\"OriginalTopic\">{{ $('1. Get Next Post Idea from Sheet').item.json.Topic }} </param>\n        <param name=\"TargetAudience\">{{ $('1. Get Next Post Idea from Sheet').item.json.Audience }}</param>\n        <param name=\"BrandVoice\">{{ $('1. Get Next Post Idea from Sheet').item.json.Voice }} </param>\n        <param name=\"Platform\">{{ $('1. Get Next Post Idea from Sheet').item.json.Platform }} </param>\n    </input_context>\n\n    <output_instructions>\n        Your response MUST be a single, valid JSON object containing exactly one key: `Caption`.\n        The value of `Caption` MUST be a string containing the generated caption text, including hashtags.\n        Example: `{\"Caption\": \"Caption text tailored for LinkedIn goes here. #ProfessionalDevelopment #IndustryInsights\"}`\n        Do NOT include any other text, explanations, or formatting outside the JSON structure.\n    </output_instructions>\n</prompt>",
        "messages": {
          "messageValues": [
            {
              "message": "=<prompt>\n    <role>\n        You are an AI Instagram/LinkedIn **Caption Writer**. You specialize in crafting concise, engaging, and contextually relevant captions based on a generated image (represented by its prompt) and the overall content strategy, specifically tailored for the target platform.\n    </role>\n\n    <task>\n        Write a short, effective social media caption **specifically tailored for the target `Platform` ('Instagram' or 'LinkedIn')**.\n        * The caption must complement the image described by `ImagePrompt` and align with all context parameters (`ChosenIdea`, `OriginalTopic`, `TargetAudience`, `BrandVoice`).\n        * **Platform Style:** Adapt tone, length, calls-to-action, and hashtag usage:\n            * **Instagram:** Can be more conversational, use more emojis, ask engaging questions, often benefits from slightly longer, more storytelling captions if relevant. Use a mix of popular and niche hashtags (3-7 recommended).\n            * **LinkedIn:** Generally more professional, concise, focused on insights or value proposition. Calls-to-action often relate to reading more, commenting with professional opinions, or business objectives. Use targeted, professional hashtags (1-3 recommended).\n        * Include 1-5 relevant, platform-appropriate hashtags.\n    </task>\n\n    <input_context>\n        <param name=\"ImagePrompt\"> {{ $json.response.prompt_options[1].prompts }} </param>\n        <param name=\"ChosenIdea\">{{ $('3a. Generate Content Concept (Ollama)').item.json.output.ideas[0].concept }} </param>\n        <param name=\"OriginalTopic\">{{ $('1. Get Next Post Idea from Sheet').item.json.Topic }} </param>\n        <param name=\"TargetAudience\">{{ $('1. Get Next Post Idea from Sheet').item.json.Audience }}</param>\n        <param name=\"BrandVoice\">{{ $('1. Get Next Post Idea from Sheet').item.json.Voice }} </param>\n        <param name=\"Platform\">{{ $('1. Get Next Post Idea from Sheet').item.json.Platform }} </param>\n    </input_context>\n\n    <output_instructions>\n        Your response MUST be a single, valid JSON object containing exactly one key: `Caption`.\n        The value of `Caption` MUST be a string containing the generated caption text, including hashtags.\n        Example: `{\"Caption\": \"Caption text tailored for LinkedIn goes here. #ProfessionalDevelopment #IndustryInsights\"}`\n        Do NOT include any other text, explanations, or formatting outside the JSON structure.\n    </output_instructions>\n</prompt>"
            }
          ]
        }
      },
      "id": "a512ae33-9778-4b56-a71d-d249a6ac25a5",
      "name": "3c. Generate Post Caption (Ollama)",
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "position": [
        152,
        -80
      ],
      "typeVersion": 1.5
    },
    {
      "parameters": {
        "mode": "runOnceForEachItem",
        "jsCode": "const output = $input.item;\n\nlet cleanText = output.json.text\n  .replace(/```json/g, '')\n  .replace(/```/g, '')\n  .replace(/\\n/g, '');\n\nlet parsedObject = JSON.parse(cleanText);\n\n// If it's an array, take the first item\nif (Array.isArray(parsedObject)) {\n  parsedObject = parsedObject[0];\n}\n\n// Ensure the result is a single object\nif (typeof parsedObject !== 'object' || parsedObject === null || Array.isArray(parsedObject)) {\n  throw new Error('Parsed content must be a single object for `json`.');\n}\n\nconsole.log(parsedObject)\n\nreturn {\n  json: parsedObject\n};"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -68,
        -80
      ],
      "id": "d3059537-d4bc-408f-abc3-5319be5c06c6",
      "name": "parse prompt JSON"
    },
    {
      "parameters": {
        "mode": "runOnceForEachItem",
        "jsCode": "const output = $input.item;\n\nlet cleanText = output.json.text\n  .replace(/```json/g, '')\n  .replace(/```/g, '')\n  .replace(/\\n/g, '')\n  .replace(/}}$/, '}]}');\n\nlet parsedObject = JSON.parse(cleanText);\n\n// If it's an array, take the first item\nif (Array.isArray(parsedObject)) {\n  parsedObject = parsedObject[0];\n}\n\n// Ensure the result is a single object\nif (typeof parsedObject !== 'object' || parsedObject === null || Array.isArray(parsedObject)) {\n  throw new Error('Parsed content must be a single object for `json`.');\n}\n\nconsole.log(parsedObject)\n\nreturn {\n  json: parsedObject\n};"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        528,
        -80
      ],
      "id": "63869f13-cc54-4b7d-a6af-7ae2ec93c1cb",
      "name": "parse prompt JSON1"
    },
    {
      "parameters": {
        "mode": "runOnceForEachItem",
        "jsCode": "const output = $input.item;\n\nlet cleanText = output.json.text\n  .replace(/```json/g, '')\n  .replace(/```/g, '')\n  .replace(/\\n/g, '')\n  .replace(/}}$/, '}]}');\n\n\nlet parsedObject = JSON.parse(cleanText);\n\n// If it's an array, take the first item\nif (Array.isArray(parsedObject)) {\n  parsedObject = parsedObject[0];\n}\n\n// Ensure the result is a single object\nif (typeof parsedObject !== 'object' || parsedObject === null || Array.isArray(parsedObject)) {\n  throw new Error('Parsed content must be a single object for `json`.');\n}\n\nconsole.log(parsedObject)\n\nreturn {\n  json: parsedObject\n};"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -664,
        -80
      ],
      "id": "6f358292-feb7-4d58-9491-4308586cbfb6",
      "name": "parse prompt JSON2"
    }
  ],
  "connections": {
    "Scheduled Start: Check for New Posts": {
      "main": [
        [
          {
            "node": "1. Get Next Post Idea from Sheet",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "1. Get Next Post Idea from Sheet": {
      "main": [
        [
          {
            "node": "2. Prepare Input Variables (Topic, Audience, etc.)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "2. Prepare Input Variables (Topic, Audience, etc.)": {
      "main": [
        [
          {
            "node": "3a. Generate Content Concept (Ollama)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "4. Generate Image using Prompt 1 (Replicate Flux)": {
      "main": [
        [
          {
            "node": "5. Prepare Data for Instagram API",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "5. Prepare Data for Instagram API": {
      "main": [
        [
          {
            "node": "6a. Create Instagram Media Container",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "6a. Create Instagram Media Container": {
      "main": [
        [
          {
            "node": "6b. Wait for Container Processing",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "6b. Wait for Container Processing": {
      "main": [
        [
          {
            "node": "6c. Publish Post to Instagram",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "6c. Publish Post to Instagram": {
      "main": [
        [
          {
            "node": "7. Update Post Status in Sheet",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "(LLM Model for Concept)": {
      "ai_languageModel": [
        [
          {
            "node": "3a. Generate Content Concept (Ollama)",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "(LLM Model for Prompts)": {
      "ai_languageModel": [
        [
          {
            "node": "3b. Generate Image Prompt Options (Ollama)",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "(LLM Model for Caption)": {
      "ai_languageModel": [
        [
          {
            "node": "3c. Generate Post Caption (Ollama)",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "3a. Generate Content Concept (Ollama)": {
      "main": [
        [
          {
            "node": "parse prompt JSON2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "3b. Generate Image Prompt Options (Ollama)": {
      "main": [
        [
          {
            "node": "parse prompt JSON",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "3c. Generate Post Caption (Ollama)": {
      "main": [
        [
          {
            "node": "parse prompt JSON1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "parse prompt JSON": {
      "main": [
        [
          {
            "node": "3c. Generate Post Caption (Ollama)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "parse prompt JSON1": {
      "main": [
        [
          {
            "node": "4. Generate Image using Prompt 1 (Replicate Flux)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "parse prompt JSON2": {
      "main": [
        [
          {
            "node": "3b. Generate Image Prompt Options (Ollama)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "pinData": {},
  "meta": {
    "instanceId": "d0ed3acf63c845f0e88aa89e6c97fbf5093faba97c7f8f305214847efec03e6e"
  }
}
```

### REFERENCES

* [FREE AI Images Generation N8n Automation](https://www.youtube.com/watch?v=qeYgROvh1gY)
* [Python generate image](https://www.youtube.com/watch?v=-X_d2AVXVkQ)
* [Generate free images](https://www.youtube.com/watch?v=Ic5BRW_nLok)
* [Janus Multimodal](https://www.youtube.com/watch?v=8fNm6LLZ5WY)
